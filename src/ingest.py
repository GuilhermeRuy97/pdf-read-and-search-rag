import os
from dotenv import load_dotenv

load_dotenv()

PDF_PATH = os.getenv("PDF_PATH")

def ingest_pdf():
    pass


if __name__ == "__main__":
    ingest_pdf()