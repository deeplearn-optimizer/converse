FROM ubuntu:latest
LABEL "Author"="Deepak"
LABEL "Project"="Converse"
RUN apt update && apt install git -y
RUN apt install python3 -y
RUN apt install python3-pip -y
RUN pip install django
RUN pip install pillow
RUN pip install djangorestframework
RUN pip install django-filter
RUN pip install markdown
RUN pip install tzdata
RUN pip install whitenoise
RUN pip install django-cors-headers
RUN pip install djangorestframework-simplejwt
WORKDIR /home
EXPOSE 8000
RUN git init
RUN git pull https://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@github.com/deeplearn-optimizer/converse.git
CMD ["python3", "./manage.py", "runserver", "0.0.0.0:8000"]
