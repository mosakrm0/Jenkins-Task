FROM python:3.12-alpine

WORKDIR /SimpleApp

COPY req.txt .
RUN pip install --no-cache-dir -r req.txt

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]

