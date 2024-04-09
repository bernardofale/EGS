# 
FROM python:3.10

# 
WORKDIR /Notifications

# 
COPY ./requirements.txt /Notifications/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /Notifications/requirements.txt

# 
#COPY ./db /Notifications/db
#COPY ./routers /Notifications/routers
#COPY ./templates /Notifications/templates
#COPY ./app.py /Notifications/app.py
#COPY ./.env /Notifications/.env
COPY . .
#

CMD ["uvicorn", "app:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
