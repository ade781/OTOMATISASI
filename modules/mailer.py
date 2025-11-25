import smtplib
import imaplib
import email
from email.header import decode_header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import time
from datetime import datetime

# --- FUNGSI KIRIM EMAIL (SMTP) ---


def send_single_email(credentials, data_row, ktp_path, sender_name, purpose):
    """Mengirim 1 email. Return: (Sukses/Gagal, Pesan Error/Status)"""
    sender_email, app_password = credentials

    try:
        # Setup Server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, app_password)

        # Siapkan Pesan
        target_email = data_row['Email']
        instansi = data_row['Nama Badan Publik']
        pertanyaan = data_row['Pertanyaan']

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = target_email
        msg['Subject'] = f"Permohonan Informasi Publik - {instansi}"

        body = f"""Kepada Yth. Pejabat Pengelola Data dan Informasi (PPID)
{instansi}

Dengan hormat,
Saya {sender_name}, bermaksud mengajukan permohonan informasi:
{pertanyaan}

Tujuan: {purpose}.
Identitas KTP terlampir.

Hormat saya,
{sender_name}"""

        msg.attach(MIMEText(body, 'plain'))

        # Attach KTP
        with open(ktp_path, "rb") as f:
            part = MIMEApplication(f.read(), Name="KTP.pdf")
            part['Content-Disposition'] = 'attachment; filename="KTP_Pemohon.pdf"'
            msg.attach(part)

        # Kirim
        server.send_message(msg)
        server.quit()

        timestamp = datetime.now().strftime('%d/%m %H:%M')
        return True, f"Terkirim ({timestamp})"

    except Exception as e:
        return False, str(e)

# --- FUNGSI BACA INBOX (IMAP) ---


def check_inbox(credentials, keyword="Permohonan", limit=10):
    sender_email, app_password = credentials
    results = []

    try:
        # Koneksi IMAP
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(sender_email, app_password)
        mail.select("inbox")

        # Cari email berdasarkan Subject
        status, messages = mail.search(None, f'(SUBJECT "{keyword}")')

        if not messages[0]:
            return []

        mail_ids = messages[0].split()
        latest_ids = mail_ids[-limit:]  # Ambil X terakhir

        for i in reversed(latest_ids):
            res, msg_data = mail.fetch(i, "(RFC822)")
            for response in msg_data:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])

                    # Decode Subject
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(
                            encoding if encoding else "utf-8")

                    # Decode Sender
                    sender = msg.get("From")

                    # Get Body
                    body = "Tidak ada teks (Mungkin gambar/HTML)"
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                try:
                                    body = part.get_payload(
                                        decode=True).decode()
                                except:
                                    pass
                                break
                    else:
                        try:
                            body = msg.get_payload(decode=True).decode()
                        except:
                            pass

                    results.append({
                        "sender": sender,
                        "subject": subject,
                        "body": body
                    })
        mail.logout()
        return results

    except Exception as e:
        return [{"error": str(e)}]
