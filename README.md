
---

# 🧾 Sales Quotation Generator (Offline AI-Powered)

An offline, intelligent sales quotation generator that creates tailored PDF quotes across multiple product lines, powered by a **local LLM** (e.g., Mistral-7B) via **LM Studio**.

---

## 🚀 Features

* 🧠 AI-generated professional sales quotes
* 📄 Automatically generates downloadable PDFs
* 🗃️ Saves quotes to a local **MySQL** database
* 🧾 View quote history from the Streamlit sidebar
* ✅ Fully offline – no cloud dependencies
* 🧱 Supports brand-specific:

  * Contacts (name, email, phone)
  * Product catalogs (model, category, price, description)

---

## 🧰 Tech Stack

| Layer       | Tech                     |
| ----------- | ------------------------ |
| UI          | Streamlit                |
| LLM         | Mistral-7B via LM Studio |
| PDF Engine  | ReportLab (Platypus)     |
| DB Storage  | MySQL                    |
| Environment | Conda / Python 3.11+     |
| Data        | `brand_models.json`      |

---

## 📁 Folder Structure

```
sales_quotation_tool/
│
├── app.py                 # Main Streamlit UI
├── db.py                  # MySQL connector and quote fetch/save
├── generate_pdf.py        # Generates flowing multi-page PDFs
├── llm_client.py          # Connects to LM Studio API
├── brand_models.json      # Product catalog with contacts
├── quotes/                # Auto-created folder to store PDFs
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

---

## ⚙️ Setup Instructions

### 1. ✅ Clone the Project

```bash
git clone <repo-url>
cd sales_quotation_tool
```

### 2. ✅ Set Up Python Environment

Using Conda:

```bash
conda create -p sales_agent python=3.11 -y
conda activate ./sales_agent
pip install -r requirements.txt
```

Or use `venv`:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. ✅ MySQL Setup

Create a database and table:

```sql
CREATE DATABASE sales_quotes;
USE sales_quotes;

CREATE TABLE quotes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(255),
    brand VARCHAR(100),
    model VARCHAR(100),
    price DECIMAL(10,2),
    quote_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

Update credentials in `db.py`:

```python
mysql.connector.connect(
    host="localhost",
    user="your_user",
    password="your_password",
    database="sales_quotes"
)
```

---

## 🧠 LM Studio Configuration

1. Download **LM Studio**: [https://lmstudio.ai](https://lmstudio.ai)
2. Load a quantized model (e.g., `mistral-7b-instruct` or `openchat`)
3. Enable: `⚙️ Settings > Allow Local API Access`
4. Note your API endpoint (e.g., `http://localhost:1234/v1/completions`)
5. Update `llm_client.py` with your IP/port if needed

---

## ▶️ Run the App

```bash
streamlit run app.py
```

Visit: [http://localhost:8501](http://localhost:8501)

---

## ✨ Usage Flow

1. Enter customer name
2. Select brand and model
3. Click **Generate Quote**
4. Review the generated text
5. Click **Save & Generate PDF**
6. Download your PDF — also saved to `/quotes/`
7. Use the sidebar to browse previous quotes

---

## ❓ Troubleshooting

| Problem                        | Fix                                            |
| ------------------------------ | ---------------------------------------------- |
| Quote text disappears          | Ensure `st.session_state` is used correctly    |
| PDF text gets cut off          | Use `generate_pdf.py` with `Platypus`          |
| LM Studio returns blank output | Use `mistral-instruct` or `chat`-style models  |
| Database not saving            | Check MySQL running and credentials in `db.py` |
| Port 1234 not reachable        | Recheck LM Studio's “Allow Local API” setting  |

---

## 🔒 Offline Capability

✅ 100% Offline

* No internet required after initial setup
* All AI runs locally via LM Studio
* PDF and DB storage is local

---

## 🤝 Contributors

* Designed and developed for internal enterprise use
* Powered by open-source AI and Python tools

---

## 📃 License

MIT License — Use and modify freely for internal enterprise AI integration.

---
