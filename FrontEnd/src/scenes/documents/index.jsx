import DescriptionOutlinedIcon from "@mui/icons-material/DescriptionOutlined";
import { Box, Button, Typography, useTheme } from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import axios from "axios";
import Cookies from "js-cookie";
import React, { useEffect, useState } from "react";
import DocumentModal from "../../components/DocumentModal"; // Certifica-te que este é o caminho correto
import Header from "../../components/Header";
import { tokens } from "../../theme";

const Documents = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const [open, setOpen] = useState(false);
  const [selectedDocument, setSelectedDocument] = useState(null);
  const [documents, setDocuments] = useState([]);

  const fetchDocuments = async () => {
    const token = Cookies.get('access_token');
    try {
      const response = await axios.get('/documents', {
        params: { token }
      });
      setDocuments(response.data);
    } catch (error) {
      console.error("Error fetching documents", error);
    }
  };

  useEffect(() => {
    fetchDocuments();
    const interval = setInterval(fetchDocuments, 5000);
    return () => clearInterval(interval);
  }, []);

  const uploadDocument = async (file) => {
    const token = Cookies.get('access_token');
    const formData = new FormData();
    formData.append("file", file);

    try {
      await axios.post("/documents/upload", formData, {
        params: { token },
        headers: { "Content-Type": "multipart/form-data" },
      });
      fetchDocuments();
    } catch (error) {
      console.error("Error uploading document", error);
    }
  };

  const deleteDocument = async (documentId) => {
    const token = Cookies.get('access_token');
    try {
      await axios.delete(`/documents/${documentId}`, {
        params: { token },
      });
      fetchDocuments();
    } catch (error) {
      console.error("Error deleting document", error);
    }
  };

  const signDocument = async (documentId, userEmail, userName, subject, message) => {
    const token = Cookies.get('access_token');
    try {
      await axios.post(`/documents/${documentId}/sign`, {
        user_email: userEmail,
        user_name: userName,
        subject,
        message,
      }, {
        params: { token },
      });
      fetchDocuments();
    } catch (error) {
      console.error("Error signing document", error);
    }
  };

  const verifyDocument = async (documentId) => {
    const token = Cookies.get('access_token');
    try {
      await axios.post(`/documents/${documentId}/sign/verify`, null, {
        params: { token },
      });
      fetchDocuments();
    } catch (error) {
      console.error("Error verifying document", error);
    }
  };

  const downloadDocument = async (documentId) => {
    const token = Cookies.get('access_token');
    try {
      const response = await axios.get(`/documents/download/${documentId}`, {
        params: { token },
        responseType: 'blob',
      });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `document_${documentId}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error("Error downloading document", error);
    }
  };

  const handleRowClick = (params) => {
    setSelectedDocument(params.row);
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    setSelectedDocument(null);
  };

  const columns = [
    {
      field: "name",
      headerName: "Name",
      flex: 1,
      cellClassName: "name-column--cell",
      renderCell: ({ row }) => (
        <Box display="flex" alignItems="center">
          <DescriptionOutlinedIcon color="primary" />
          <Typography ml={1}>{row.name}</Typography>
        </Box>
      ),
    },
    {
      field: "size",
      headerName: "Size",
      flex: 1,
    },
    {
      field: "type",
      headerName: "Type",
      flex: 1,
    },
    {
      field: "date",
      headerName: "Date",
      flex: 1,
    },
    {
      field: "description",
      headerName: "Description",
      flex: 1,
    },
    {
      field: "actions",
      headerName: "Actions",
      flex: 1,
      renderCell: ({ row }) => (
        <Box display="flex" justifyContent="space-between" width="100%">
          <Button
            variant="contained"
            color="primary"
            onClick={() => downloadDocument(row.id)}
          >
            Download
          </Button>
          <Button
            variant="contained"
            color="secondary"
            onClick={() => deleteDocument(row.id)}
          >
            Delete
          </Button>
          <Button
            variant="contained"
            color="default"
            onClick={() => signDocument(row.id, 'ricardocruzmachado@gmail.com', 'User Name', 'Sign Subject', 'Sign Message')}
          >
            Sign
          </Button>
          <Button
            variant="contained"
            color="default"
            onClick={() => verifyDocument(row.id)}
          >
            Verify
          </Button>
        </Box>
      ),
    },
  ];

  return (
    <Box m="10px">
      <Header title="Documents" subtitle="Browse and manage company documents" />
      <Box m="10px 0" display="flex" justifyContent="space-between">
        <Button
          variant="contained"
          color="primary"
          component="label"
        >
          Upload Document
          <input
            type="file"
            hidden
            onChange={(e) => uploadDocument(e.target.files[0])}
          />
        </Button>
      </Box>
      <Box
        m="10px 0 0 0"
        height="75vh"
        sx={{
          "& .MuiDataGrid-root": {
            border: "none",
          },
          "& .MuiDataGrid-cell": {
            borderBottom: "none",
          },
          "& .name-column--cell": {
            color: colors.greenAccent[300],
          },
          "& .MuiDataGrid-columnHeaders": {
            backgroundColor: colors.blueAccent[700],
            borderBottom: "none",
          },
          "& .MuiDataGrid-virtualScroller": {
            backgroundColor: colors.primary[400],
          },
          "& .MuiDataGrid-footerContainer": {
            borderTop: "none",
            backgroundColor: colors.blueAccent[700],
          },
          "& .MuiCheckbox-root": {
            color: `${colors.greenAccent[200]} !important`,
          },
        }}
      >
        <DataGrid
          rows={documents}
          columns={columns}
          onRowClick={handleRowClick}
        />
      </Box>
      {selectedDocument && (
        <DocumentModal
          open={open}
          onClose={handleClose}
          document={selectedDocument}
        />
      )}
    </Box>
  );
};

export default Documents;
