# Court-Data Fetcher & Mini-Dashboard

## 🏛 Court Selected
**Faridabad District Court** (https://districts.ecourts.gov.in/faridabad)

## 🚀 Stack Used
- Frontend: HTML, CSS
- Backend: Python (Flask)
- Scraping: Playwright
- Database: PostgreSQL

## ⚙️ Setup Instructions
1. Clone repo
2. Create `.env` file:
DB_NAME=your_db
DB_USER=your_user
DB_PASS=your_password
DB_HOST=localhost
DB_PORT=5432

go
Copy
Edit
3. Install dependencies:
```bash
pip install -r requirements.txt
playwright install
Run the app:

bash
Copy
Edit
python run.py
🧠 CAPTCHA Strategy
Manual CAPTCHA entry is prompted using saved screenshot captcha.png.

💾 Data Stored
Each query and raw HTML are logged to PostgreSQL (queries table).

✅ Features
Fetch court case metadata

Show latest PDF orders/judgments

Log queries for audit

Friendly error messages