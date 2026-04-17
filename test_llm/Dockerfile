FROM python:3.12-slim

WORKDIR /code

RUN pip install fastapi uvicorn

COPY llm_test.py /code/llm_test.py

CMD [ "uvicorn", "llm_test:app", "--host", "0.0.0.0", "--port", "8000" ]