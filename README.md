# ⚖️ Legal Doc Analyzer

Legal Doc Analyzer is an AI-powered web application built with **Streamlit**, **Together.ai**, and **MySQL** that helps users **analyze legal documents clause-by-clause**, **chat with uploaded contracts**, and **store/search past documents**. It’s perfect for legal professionals, students, and anyone dealing with complex legal text.

---

## 🚀 Features

- ✂️ **Clause Extraction** – Automatically identifies and extracts legal sections and clauses.
- 🤖 **AI-Powered Analysis** – Uses Together.ai (Mistral model) to summarize documents and detect missing or risky clauses.
- 💬 **Chat with Document** – Ask natural questions about your legal document.
- 🔍 **Search Past Uploads** – Find previously analyzed documents by keyword.
- 🗃 **Persistent Storage** – All documents and their AI insights are saved in a MySQL database.

---

## 🛠 Tech Stack

- **Frontend**: Streamlit
- **AI/NLP**: Together.ai API (Mistral-7B-Instruct)
- **Database**: MySQL (via `mysql-connector-python`)
- **PDF Parsing**: PyPDF2 & PyMuPDF
- **Environment Management**: python-dotenv

---

## 📂 Project Structure

```
📁 Legal-Doc-Analyzer
│
├── app.py               # Streamlit app with complete tabbed interface
├── extract.py           # PDF text extraction
├── database.py          # Save & fetch from MySQL
├── requirements.txt     # Python dependencies
├── .env.example         # Example for environment variables
├── LICENSE              # MIT License
└── README.md            # Project documentation
```

---

## 🔧 Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/legal-doc-analyzer.git
cd legal-doc-analyzer
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment**
- Rename `.env.example` to `.env`
- Fill in your API key and MySQL credentials
```env
TOGETHER_API_KEY=your_together_ai_key
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=legal_documents_db
```

4. **Run the application**
```bash
streamlit run app.py
```

---

## 📌 How It Works

- Upload a `.pdf` legal document
- AI extracts text and summarizes key clauses
- AI flags missing clauses (e.g., confidentiality, indemnity)
- Save and search all documents in the database
- Chat with uploaded documents for fast queries

---

## 🔐 Security

- API keys and credentials are managed securely via `.env`
- User uploads and analysis remain local unless explicitly exported

---

## 🤖 AI Model

The analysis is powered by:
- **Model**: `mistralai/Mistral-7B-Instruct-v0.2`
- **Provider**: [Together.ai](https://www.together.ai/)
- **Interface**: OpenAI-compatible API

---

## 👨‍💻 Author

**Luv Kanodia**   
🌐 [LinkedIn](https://www.linkedin.com/in/luv-kanodia)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 💡 Future Enhancements

- Multi-user login system
- More AI model options
- Export analysis as PDF
- OCR support for scanned documents

