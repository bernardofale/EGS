from fastapi import APIRouter, Query, UploadFile, File, HTTPException, \
                                                BackgroundTasks, Depends
from fastapi.responses import FileResponse
from app.resp_models.models import Document, DocumentResponse, DocumentSign
from app.db.database import engine
from sqlmodel import Session, select
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from tempfile import NamedTemporaryFile
from dropbox_sign import ApiClient, ApiException, Configuration, apis, models
from app.dependencies import get_hello_sign_key
import os


app = APIRouter()


@app.post("/upload", status_code=201)
async def upload_document(user_id: str,
                          file: UploadFile = File(...)):
    # Mock function to upload document to the database
    new_doc = Document(name=file.filename,
                       content_type=file.content_type,
                       content=bytes(file.file.read()),
                       signed=False,
                       uploaded_by=user_id)
    with Session(engine) as session:
        session.add(new_doc)
        session.commit()
        session.refresh(new_doc)
    return DocumentResponse(id=new_doc.id,
                            name=new_doc.name,
                            content_type=new_doc.content_type,
                            signed=False,
                            uploaded_by=new_doc.uploaded_by)


@app.get("/", status_code=200)
async def get_all_documents(user_id: str = Query(None)):
    # Function to retrieve all documents of given user from the database
    with Session(engine) as session:
        results = session.exec(select(Document).where(Document.uploaded_by ==
                                                      user_id)).all()
        if len(results) == 0:
            raise HTTPException(status_code=404,
                                detail="ERROR: No documents found for this \
                                user")
        docs = [DocumentResponse(id=doc.id,
                                 name=doc.name,
                                 content_type=doc.content_type,
                                 signed=doc.signed,
                                 uploaded_by=doc.uploaded_by)
                for doc in results]
        return docs


def delete_tempfile(file_path: str):
    os.unlink(file_path)


@app.get("/{document_id}", status_code=200)
async def get_document(background_tasks: BackgroundTasks,
                       document_id: str,
                       user_id: str = Query(None)):
    # Function to retrieve a document from the database
    with Session(engine) as session:
        try:
            results = session.exec(select(Document).where(Document.id ==
                                                          document_id)).one()
        except NoResultFound:
            raise HTTPException(status_code=404,
                                detail="ERROR: No document found")
        except MultipleResultsFound:
            raise HTTPException(status_code=500,
                                detail="ERROR: Multiple documents found")

        with NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(results.content)
            background_tasks.add_task(delete_tempfile, temp_file.name)
            return FileResponse(temp_file.name,
                                media_type=results.content_type,
                                filename=results.name)


@app.delete("/{document_id}", status_code=204)
async def delete_document(document_id: str):
    # Check if document exists
    with Session(engine) as session:
        results = session.exec(select(Document).where(Document.id ==
                                                      document_id))
        if results is None:
            raise HTTPException(status_code=404, detail="No document found")
        session.delete(results.one())
        session.commit()


@app.post("/{document_id}/sign/", status_code=200)
async def sign_document(background_tasks: BackgroundTasks,
                        document_id: str,
                        doc_sign: DocumentSign,
                        api_key: str = Depends(get_hello_sign_key)):
    config = Configuration(
        username=api_key
    )

    with Session(engine) as session:
        # Fetch document from the database
        try:
            results = session.exec(select(Document).where(Document.id ==
                                                          document_id)).one()
        except NoResultFound:
            raise HTTPException(status_code=404,
                                detail="ERROR: No document found")
        except MultipleResultsFound:
            raise HTTPException(status_code=500,
                                detail="ERROR: Multiple documents found")
        # Write document to a temporary file
        with NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(results.content)
            background_tasks.add_task(delete_tempfile, temp_file.name)
            # Send document for signing
            with ApiClient(config) as api_client:
                signature_request_api = apis.SignatureRequestApi(api_client)

                signer_1 = models.SubSignatureRequestSigner(
                    email_address=doc_sign.user_email,
                    name=doc_sign.user_name,
                    order=0,
                )
                signing_options = models.SubSigningOptions(
                    draw=True,
                    type=True,
                    upload=True,
                    phone=True,
                    default_type="draw",
                )

                field_options = models.SubFieldOptions(
                    date_format="DD - MM - YYYY",
                )

                data = models.SignatureRequestSendRequest(
                    title=results.name,
                    subject=doc_sign.subject,
                    message=doc_sign.message,
                    signers=[signer_1],
                    cc_email_addresses=[],
                    files=[open(temp_file.name, "rb")],
                    metadata={},
                    signing_options=signing_options,
                    field_options=field_options,
                    test_mode=True,
                )

                try:
                    response = signature_request_api.signature_request_send(
                                                                        data
                                                                        )
                    results.signature_request_id = response.signature_request\
                        .signature_request_id
                    session.add(results)
                    session.commit()
                except ApiException as e:
                    print("Exception when calling Dropbox Sign API: %s\n" % e)
                    print("Exception when calling Dropbox Sign API: %s\n" % e)
        return {"message": "Document sent for signing"}


@app.post("/{document_id}/sign/verify", status_code=200)
async def verify_document(document_id: str,
                          api_key: str = Depends(get_hello_sign_key)):
    config = Configuration(
        username=api_key
    )

    with Session(engine) as session:
        # Fetch document from the database
        try:
            results = session.exec(select(Document).where(Document.id ==
                                                          document_id)).one()
        except NoResultFound:
            raise HTTPException(status_code=404,
                                detail="ERROR: No document found")
        except MultipleResultsFound:
            raise HTTPException(status_code=500,
                                detail="ERROR: Multiple documents found")
        # Check if document is signed
        if results.signed:
            return {"message": "Document available for download"}
        with ApiClient(config) as api_client:
            signature_request_api = apis.SignatureRequestApi(api_client)
            signature_request_id = results.signature_request_id
            try:
                response = signature_request_api.signature_request_get(
                                                        signature_request_id
                                                        )
                if response.signature_request.is_complete:
                    results.signed = True
                    response = signature_request_api.signature_request_files(
                                                        signature_request_id
                                                        )
                    results.content = response.read()
                    session.add(results)
                    session.commit()
                    return {"message": "Document available for download"}
                return {"message": "Document not signed yet"}
            except ApiException as e:
                print("Exception when calling Dropbox Sign API: %s\n" % e)


@app.get("/{document_id}/download", status_code=200)
async def download_document(background_tasks: BackgroundTasks,
                            document_id: str):
    with Session(engine) as session:
        try:
            results = session.exec(select(Document).where(
                                            Document.id == document_id)).one()
        except NoResultFound:
            raise HTTPException(status_code=404,
                                detail="ERROR: No document found")
        except MultipleResultsFound:
            raise HTTPException(status_code=500,
                                detail="ERROR: Multiple documents found")
    if results.signed is False:
        raise HTTPException(status_code=404,
                            detail="ERROR: Document not signed yet")
    with NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(results.content)
        background_tasks.add_task(delete_tempfile,
                                  temp_file.name)
        return FileResponse(temp_file.name,
                            media_type=results.content_type,
                            filename=results.name)
