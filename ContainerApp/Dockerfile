FROM python:3.7.9
COPY . /webapp
WORKDIR /webapp
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["run.py"]