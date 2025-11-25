import streamlit as st
import time
import os

# Import Modul Buatan Kita Sendiri
from modules import database, mailer

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Uji Akses Modular",
                   page_icon="📦", layout="wide")
st.title("📦 Sistem Uji Akses (Modular Version)")

# --- SIDEBAR ---
with st.sidebar:
    st.header("🔐 Konfigurasi")
    email_user = st.text_input("Email Gmail")
    email_pass = st.text_input("App Password", type="password")
    st.divider()
    nama_pengirim = st.text_input("Nama Pengirim", "Nama Kamu")
    tujuan_req = st.text_input("Tujuan Request", "Tugas Akhir")

# --- FILE PATHS ---
FILE_DATA = 'data.xlsx'
FILE_KTP = 'ktp.pdf'

# --- LOAD DATA ---
df = database.load_data(FILE_DATA)

if df is None:
    st.error("❌ File 'data.xlsx' tidak ditemukan!")
    st.stop()

# --- UI TABS ---
tab1, tab2 = st.tabs(["🚀 KIRIM BATCH", "📩 CEK BALASAN"])

# === TAB 1: PENGIRIMAN ===
with tab1:
    # Hitung Statistik
    total = len(df)
    terkirim_count = df['Status'].apply(lambda x: 'Terkirim' in str(x)).sum()

    m1, m2 = st.columns(2)
    m1.metric("Total Data", total)
    m2.metric("Sudah Terkirim", int(terkirim_count))
    st.progress(terkirim_count/total if total > 0 else 0)

    st.dataframe(df, height=200, use_container_width=True)

    c1, c2 = st.columns([3, 1])
    limit = c1.slider("Limit Harian", 1, 50, 10)
    tombol_kirim = c2.button(
        "MULAI KIRIM", type="primary", use_container_width=True)

    if tombol_kirim:
        if not email_user or not email_pass:
            st.error("Login dulu di Sidebar!")
        elif not os.path.exists(FILE_KTP):
            st.error("File KTP tidak ditemukan!")
        else:
            # Filter Antrian (Status Kosong atau NaN)
            antrian = df[df['Status'].isna() | (
                df['Status'] == '')].head(limit)

            if antrian.empty:
                st.success("Semua antrian selesai!")
            else:
                progress_bar = st.progress(0)
                log_text = st.empty()
                sukses = 0

                for i, row in antrian.iterrows():
                    log_text.text(
                        f"Mengirim ke: {row['Nama Badan Publik']}...")

                    # Panggil Fungsi dari Modul mailer
                    is_sent, message = mailer.send_single_email(
                        (email_user, email_pass),
                        row,
                        FILE_KTP,
                        nama_pengirim,
                        tujuan_req
                    )

                    if is_sent:
                        df.at[i, 'Status'] = message
                        sukses += 1
                    else:
                        df.at[i, 'Status'] = f"Gagal: {message}"

                    # Save setiap kali kirim (biar aman)
                    database.save_data(df, FILE_DATA)

                    # Update UI
                    progress_bar.progress((sukses + 1) / len(antrian))
                    time.sleep(3)  # Jeda

                st.success(f"Batch selesai! {sukses} terkirim.")
                time.sleep(1)
                st.rerun()

# === TAB 2: CEK INBOX ===
with tab2:
    st.caption("Tips: Pastikan IMAP sudah ENABLE di settingan Gmail Web.")
    btn_cek = st.button("🔄 Cek Inbox Sekarang")

    if btn_cek:
        if not email_user or not email_pass:
            st.error("Login dulu!")
        else:
            with st.spinner("Mengambil data dari Gmail..."):
                # Panggil Fungsi dari Modul mailer
                hasil = mailer.check_inbox((email_user, email_pass))

                if not hasil:
                    st.info("Tidak ada email ditemukan.")
                elif "error" in hasil[0]:
                    st.error(
                        f"Error IMAP: {hasil[0]['error']}. \n\nSOLUSI: Cek Setting Gmail -> Forwarding and POP/IMAP -> Enable IMAP.")
                else:
                    for msg in hasil:
                        with st.expander(f"📩 {msg['subject']}"):
                            st.write(f"**Dari:** {msg['sender']}")
                            st.text_area("Isi Pesan:", msg['body'], height=150)
