import streamlit as st
import base64
import csv
import os
import time
import threading
from datetime import datetime

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# ================= CONFIG =================
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
HISTORY_FILE = "email_history.csv"


# ================= LOGIN =================
def gmail_login():
    flow = InstalledAppFlow.from_client_secrets_file(
        "credentials.json",
        SCOPES
    )
    creds = flow.run_local_server(port=0)
    return build("gmail", "v1", credentials=creds)


# ================= SEND EMAIL (WITH ATTACHMENT) =================
def send_email(service, to, subject, message, file):

    try:
        msg = MIMEMultipart()
        msg["to"] = to
        msg["subject"] = subject

        # text
        msg.attach(MIMEText(message, "plain"))

        # attachment (photo/file)
        if file is not None:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(file.read())
            encoders.encode_base64(part)

            part.add_header(
                "Content-Disposition",
                f"attachment; filename={file.name}"
            )

            msg.attach(part)

        raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()

        service.users().messages().send(
            userId="me",
            body={"raw": raw}
        ).execute()

        return True

    except Exception as e:
        st.error(e)
        return False


# ================= HISTORY =================
def save_history(to, subject, status, schedule_time):
    file_exists = os.path.isfile(HISTORY_FILE)

    with open(HISTORY_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["Time", "Scheduled Time", "Receiver", "Subject", "Status"])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            schedule_time,
            to,
            subject,
            status
        ])


# ================= SCHEDULER =================
def schedule_email(service, send_time, to, subject, message, file):

    def job():
        while True:
            if datetime.now() >= send_time:

                status = "Sent" if send_email(service, to, subject, message, file) else "Failed"

                save_history(
                    to,
                    subject,
                    status,
                    send_time.strftime("%Y-%m-%d %H:%M:%S")
                )
                break

            time.sleep(1)

    threading.Thread(target=job, daemon=True).start()


# ================= UI =================
st.title("📧 Gmail Dashboard (Email + Files + Photos + Scheduler)")

if "service" not in st.session_state:
    st.session_state.service = None


# ---------------- LOGIN ----------------
if st.session_state.service is None:
    if st.button("🔐 Login with Google"):
        st.session_state.service = gmail_login()
        st.success("Gmail Connected ✔")
        st.rerun()


# ---------------- DASHBOARD ----------------
else:

    menu = st.sidebar.selectbox(
        "Menu",
        ["Send Email", "Schedule Email", "History"]
    )

    # ---------------- SEND EMAIL ----------------
    if menu == "Send Email":

        to = st.text_input("Receiver Email")
        subject = st.text_input("Subject")
        message = st.text_area("Message")

        file = st.file_uploader(
            "Upload Photo / File",
            type=["png", "jpg", "jpeg", "pdf", "docx", "txt"]
        )

        if st.button("Send Email"):

            status = "Sent" if send_email(
                st.session_state.service,
                to,
                subject,
                message,
                file
            ) else "Failed"

            save_history(to, subject, status, "Immediate")

            if status == "Sent":
                st.success("Email Sent ✔")


    # ---------------- SCHEDULE EMAIL ----------------
    elif menu == "Schedule Email":

        to = st.text_input("Receiver Email")
        subject = st.text_input("Subject")
        message = st.text_area("Message")

        file = st.file_uploader(
            "Upload File / Photo",
            type=["png", "jpg", "jpeg", "pdf", "docx", "txt"],
            key="file2"
        )

        date = st.date_input("Select Date")
        time_input = st.time_input("Select Time")

        if st.button("Schedule Email"):

            send_time = datetime.combine(date, time_input)

            schedule_email(
                st.session_state.service,
                send_time,
                to,
                subject,
                message,
                file
            )

            st.success(f"Email Scheduled for {send_time}")


    # ---------------- HISTORY ----------------
    elif menu == "History":

        st.subheader("📜 Email History")

        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                st.table(list(csv.reader(f)))
        else:
            st.info("No history found")