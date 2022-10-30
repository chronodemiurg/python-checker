FROM python:latest
ADD urlsync.py .
ADD testfiles/test-urls.csv ./testfiles/
RUN pip install requests
CMD ["python3", "./urlsync.py"] 
