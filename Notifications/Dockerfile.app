# 
FROM python:3.10

# 
WORKDIR /notifications

# 
COPY ./requirements.txt /notifications/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /notifications/requirements.txt

# 
#COPY ./db /notifications/db
#COPY ./routers /notifications/routers
#COPY ./templates /notifications/templates
#COPY ./app.py /notifications/app.py
#COPY ./.env /notifications/.env
COPY . .
#

CMD ["uvicorn", "app:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
