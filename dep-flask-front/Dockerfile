FROM docker.io/python

WORKDIR /app
COPY . ./
RUN pip install -r requirements.txt 

EXPOSE 8888 
CMD ["gunicorn", "-b", "0.0.0.0:8888", "dep:app"]
