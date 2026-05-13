import streamlit as st
import smtplib
import csv
import os
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading
import time

HISTORY_FILE = "email_history.csv"


# ---------------- SEND EMAIL ----------------
def send_email(sender, password, receiver, subject, message):
    try:
        msg = MIMEMultipart()
        msg["From"] = sender
        msg["To"] = receiver
        msg["Subject"] = subject

        msg.attach(MIMEText(message, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())
        server.quit()

        return True
    except Exception as e:
        st.error(f"Email Error: {e}")
        return False


# ---------------- SAVE HISTORY ----------------
def save_history(receiver, subject, message, status, schedule_time):
    file_exists = os.path.isfile(HISTORY_FILE)

    with open(HISTORY_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow([
                "Sent Time",
                "Scheduled Time",
                "Receiver",
                "Subject",
                "Message",
                "Status"
            ])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            schedule_time,
            receiver,
            subject,
            message,
            status
        ])


# ---------------- SCHEDULE EMAIL ----------------
def schedule_email(send_time, sender, password, receiver, subject, message):

    def job():
        while True:
            if datetime.now() >= send_time:

                status = "Sent" if send_email(sender, password, receiver, subject, message) else "Failed"

                save_history(
                    receiver,
                    subject,
                    message,
                    status,
                    send_time.strftime("%Y-%m-%d %H:%M:%S")
                )
                break

            time.sleep(1)

    threading.Thread(target=job, daemon=True).start()


# ---------------- STREAMLIT UI ----------------
st.set_page_config(page_title="Email Automation Bot", layout="centered")

st.title("📧 Email Automation Bot")

menu = st.sidebar.selectbox(
    "Menu",
    ["Send Email Now", "Schedule Email", "Email History"]
)


# ---------------- SEND EMAIL ----------------
if menu == "Send Email Now":

    st.subheader("📨 Send Email Instantly")

    sender = st.text_input("Your Gmail")
    password = st.text_input("App Password", type="password")
    receiver = st.text_input("Receiver Email")
    subject = st.text_input("Subject")
    message = st.text_area("Message")

    if st.button("Send Email"):

        status = "Sent" if send_email(sender, password, receiver, subject, message) else "Failed"

        save_history(receiver, subject, message, status, "Immediate")

        if status == "Sent":
            st.success("Email Sent Successfully!")


# ---------------- SCHEDULE EMAIL ----------------
elif menu == "Schedule Email":

    st.subheader("⏰ Schedule Email")

    sender = st.text_input("Your Gmail", key="s1")
    password = st.text_input("App Password", type="password", key="s2")
    receiver = st.text_input("Receiver Email", key="s3")
    subject = st.text_input("Subject", key="s4")
    message = st.text_area("Message", key="s5")

    date = st.date_input("Select Date")
    time_input = st.time_input("Select Time")

    if st.button("Schedule Email"):

        send_time = datetime.combine(date, time_input)

        schedule_email(send_time, sender, password, receiver, subject, message)

        st.success(f"Email scheduled for: {send_time}")


# ---------------- EMAIL HISTORY ----------------
elif menu == "Email History":

    st.subheader("📜 Email History")

    if os.path.exists(HISTORY_FILE):

        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            data = list(reader)

        if len(data) > 1:
            st.table(data)
        else:
            st.info("No history yet.")

    else:
        st.info("History file not found.")