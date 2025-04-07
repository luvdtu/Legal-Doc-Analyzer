import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS legal_documents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    document TEXT,
    analysis TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

def save_document(document, analysis):
    query = "INSERT INTO legal_documents (document, analysis) VALUES (%s, %s)"
    cursor.execute(query, (document, analysis))
    conn.commit()

def fetch_all_documents():
    cursor.execute("SELECT id, document, analysis, created_at FROM legal_documents")
    return cursor.fetchall()

def search_documents_by_keyword(keyword):
    query = "SELECT id, document, analysis, created_at FROM legal_documents WHERE document LIKE %s OR analysis LIKE %s"
    cursor.execute(query, (f"%{keyword}%", f"%{keyword}%"))
    return cursor.fetchall()
