FROM python:3.11.15-trixie
WORKDIR /app
COPY ./scripts /app/
RUN pip install python-dotenv streamlit groq
CMD streamlit run app.py --server.port=8501 --server.address=0.0.0.0
EXPOSE 8501