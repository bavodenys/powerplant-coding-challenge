FROM python:3.8-alpine
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["api.py"]