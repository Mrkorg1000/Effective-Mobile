FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTONUNBUFFERED=1
WORKDIR /app
COPY . ./
RUN pip install -r requirements.txt
CMD uvicorn main:app --host 0.0.0.0 --port 8000