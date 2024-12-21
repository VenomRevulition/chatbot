from flask import Flask, request, jsonify
import tkinter as tk
from tkinter import messagebox, ttk
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    # Simulate a response from the chatbot
    bot_response = f"You said: {user_message}"
    return jsonify({'response': bot_response})

class ChatGPTUsageSurvey:
    def __init__(self, master):
        self.master = master
        master.title("Survei Penggunaan ChatGPT dalam Pembelajaran")
        master.geometry("800x600")
        master.configure(bg='#2C3E50')

        # Survey questions with multiple choice options
        self.questions = [
            {
                "text": "Seberapa sering Anda menggunakan ChatGPT untuk membantu belajar?",
                "options": [
                    "Hampir setiap hari",
                    "Beberapa kali seminggu",
                    "Sekali sebulan",
                    "Jarang sekali"
                ]
            },
            {
                "text": "Dalam mata pelajaran apa Anda paling sering menggunakan ChatGPT?",
                "options": [
                    "Matematika",
                    "Bahasa",
                    "Sains",
                    "Sejarah",
                    "Lainnya"
                ]
            },
            {
                "text": "Bagaimana ChatGPT membantu proses belajar Anda?",
                "options": [
                    "Menjelaskan konsep sulit",
                    "Membantu mengerjakan tugas",
                    "Membuat ringkasan materi",
                    "Persiapan ujian",
                    "Lainnya"
                ]
            },
            {
                "text": "Apakah Anda merasa ChatGPT memudahkan atau mempersulit proses belajar?",
                "options": [
                    "Sangat memudahkan",
                    "Sedikit memudahkan",
                    "Netral",
                    "Sedikit mempersulit",
                    "Sangat mempersulit"
                ]
            }
        ]

        self.current_question = 0
        self.answers = []

        # Judul dan deskripsi
        self.title_label = tk.Label(
            master, 
            text="Survei Penggunaan ChatGPT dalam Pembelajaran", 
            font=("Arial", 16, "bold"), 
            bg='#2C3E50', 
            fg='white'
        )
        self.title_label.pack(pady=20)

        # Frame untuk pertanyaan dan pilihan
        self.survey_frame = tk.Frame(master, bg='#34495E', padx=20, pady=20)
        self.survey_frame.pack(expand=True, fill=tk.BOTH, padx=50, pady=20)

        # Label pertanyaan
        self.question_label = tk.Label(
            self.survey_frame, 
            text="", 
            wraplength=700, 
            font=("Arial", 14), 
            bg='#34495E', 
            fg='white'
        )
        self.question_label.pack(pady=20)

        # Variabel untuk pilihan radio
        self.selected_option = tk.StringVar()

        # Frame untuk opsi pilihan
        self.options_frame = tk.Frame(self.survey_frame, bg='#34495E')
        self.options_frame.pack(expand=True, fill=tk.BOTH)

        # Tombol navigasi
        self.button_frame = tk.Frame(master, bg='#2C3E50')
        self.button_frame.pack(pady=20)

        self.next_button = tk.Button(
            self.button_frame, 
            text="Selanjutnya", 
            command=self.next_question, 
            bg='#3498DB', 
            fg='white', 
            font=("Arial", 12)
        )
        self.next_button.pack(side=tk.RIGHT, padx=10)

        # Mulai survei
        self.load_question()

    def load_question(self):
        # Reset pilihan
        self.selected_option.set("")

        # Hapus opsi sebelumnya
        for widget in self.options_frame.winfo_children():
            widget.destroy()

        # Tampilkan pertanyaan saat ini
        question = self.questions[self.current_question]
        self.question_label.config(text=question["text"])

        # Buat opsi radio
        for option in question["options"]:
            radio = tk.Radiobutton(
                self.options_frame, 
                text=option, 
                variable=self.selected_option, 
                value=option, 
                font=("Arial", 12), 
                bg='#34495E', 
                fg='white', 
                selectcolor='#2980B9'
            )
            radio.pack(anchor=tk.W, padx=20, pady=10)

    def next_question(self):
        # Validasi pilihan
        if not self.selected_option.get():
            messagebox.showwarning("Peringatan", "Silakan pilih salah satu opsi!")
            return

        # Simpan jawaban
        self.answers.append({
            "pertanyaan": self.questions[self.current_question]["text"],
            "jawaban": self.selected_option.get()
        })

        # Pindah ke pertanyaan berikutnya
        self.current_question += 1

        if self.current_question < len(self.questions):
            self.load_question()
        else:
            self.send_survey_results()

    def send_survey_results(self):
        try:
            # Konfigurasi email
            sender_email = "surveiemailku@gmail.com"  # Ganti dengan email Anda
            sender_password = "password_email_anda"  # Ganti dengan password email Anda

            # Buat koneksi email
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = "muhammadsubhan2701@gmail.com"
            msg['Subject'] = "Hasil Survei Penggunaan ChatGPT"

            # Buat body email
            body = "Hasil Survei Penggunaan ChatGPT:\n\n"
            for answer in self.answers:
                body += f"Pertanyaan: {answer['pertanyaan']}\n"
                body += f"Jawaban: {answer['jawaban']}\n\n"

            msg.attach(MIMEText(body, 'plain'))

            # Kirim email
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            server.quit()

            messagebox.showinfo("Sukses", "Survei berhasil dikirim!")
            self.master.quit()

        except Exception as e:
            messagebox.showerror("Kesalahan", f"Gagal mengirim survei: {str(e)}")

def main():
    root = tk.Tk()
    app = ChatGPTUsageSurvey(root)
    root.mainloop()

if __name__ == "__main__":
    main()