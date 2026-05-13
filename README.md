# 📧 Email Automation Bot (Gmail Dashboard)

A Python + Streamlit project that allows users to send emails using Gmail API with a simple dashboard interface.

---

## 🚀 Features

- 🔐 Google Login (OAuth 2.0)
- 📧 Send Emails from dashboard
- 📎 Attach Photos & Files (PDF, JPG, PNG, DOCX, TXT)
- ⏰ Schedule Emails (Date + Time)
- 📜 Email History Tracking
- 🎛️ Streamlit Web Dashboard

---

## 🛠️ Tech Stack

- Python 🐍
- Streamlit 🎯
- Gmail API 📧
- Google OAuth 2.0 🔐

---

## 📁 Project Structure

Email Automation Bot/
│
├── app.py
├── credentials.json   (DO NOT UPLOAD)
├── token.json         (DO NOT UPLOAD)
├── email_history.csv  (auto-generated)
├── .gitignore
├── README.md

---

## ⚙️ Installation & Setup

### 1. Install Required Libraries

Install dependencies using pip:

pip install streamlit google-auth-oauthlib google-api-python-client

---

### 2. Setup Gmail API (Important)

To use Gmail sending feature:

- Go to Google Cloud Console
- Create a new project
- Enable Gmail API
- Configure OAuth Consent Screen
- Create OAuth Client ID
- Download credentials file
- Rename it to:

credentials.json

Place it inside the project folder.

---

### 3. Run the Project

Start the Streamlit app:

python -m streamlit run app.py

---

## 📧 How It Works

1. Click "Login with Google"
2. Authorize Gmail account
3. Enter receiver email
4. Write subject and message
5. (Optional) Attach files or photos
6. Choose schedule time (optional)
7. Send email

---

## 📎 File Upload Support

You can attach:

- 🖼 Images (JPG, PNG)
- 📄 Documents (PDF, DOCX)
- 📃 Text files (TXT)

---

## ⏰ Scheduling Feature

- Select date
- Select time
- Email will be sent automatically at scheduled time

---

## 📜 Email History

Stores:
- Sent time
- Receiver email
- Subject
- Status (Sent/Failed)

---

## ⚠️ Important Security Note

Do NOT upload these files to GitHub:

- credentials.json
- token.json

These contain sensitive Google OAuth data.

---

## 👨‍💻 Author

Developed by https://github.com/Kami2628

---

## ⭐ Project Goal

To automate email sending with:

- Secure Gmail integration
- File attachments
- Scheduling system
- Simple dashboard interface
