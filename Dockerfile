#Step1 Django Project Copy
FROM python:3.9.0
COPY ./ /django_sample
WORKDIR /django_sample

#Step2 pip Install
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt

#Step3 DB Migrate & django project run 
EXPOSE 8000 
CMD ["bash", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]