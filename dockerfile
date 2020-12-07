#docker run --name ai_lab_2_ai --rm ai_lab_2_ai

FROM python:3
ENV PYTHONUNBUFFERED = 1
RUN pip install --no-cache-dir pandas scikit-learn pymysql cryptography joblib
COPY run.py /
COPY rf-classifier.pkl /
CMD ["python", "run.py"]
