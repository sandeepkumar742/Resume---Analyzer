import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfReader
import json
import os

# Skills load from JSON
with open("skills.json", "r") as file:
    skill_domains = json.load(file)

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text.lower()

def analyze_resume(text):
    found_skills = set()
    suggested_domains = {}

    for domain, skills in skill_domains.items():
        match_count = sum(1 for skill in skills if skill in text)
        if match_count > 0:
            suggested_domains[domain] = match_count
            found_skills.update(skill for skill in skills if skill in text)

    return found_skills, suggested_domains

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if not file_path:
        return

    text = extract_text_from_pdf(file_path)
    skills_found, domain_scores = analyze_resume(text)

    result_text.delete("1.0", tk.END)

    if not domain_scores:
        result_text.insert(tk.END, "❌ No matching job domain found.\nTry adding more technical skills in your resume.\n")
        return

    result_text.insert(tk.END, "✅ Skills Found:\n" + ", ".join(skills_found) + "\n\n")
    result_text.insert(tk.END, "💼 Suggested Domains:\n")
    for domain, score in sorted(domain_scores.items(), key=lambda x: x[1], reverse=True):
        result_text.insert(tk.END, f"🔹 {domain} - Skill Match: {score}\n")

def toggle_dark_mode():
    if root["bg"] == "black":
        root.config(bg="white")
        result_text.config(bg="white", fg="black")
        dark_btn.config(text="Enable Dark Mode", bg="lightgray")
    else:
        root.config(bg="black")
        result_text.config(bg="black", fg="white")
        dark_btn.config(text="Disable Dark Mode", bg="gray")

# GUI
root = tk.Tk()
root.title(" Resume Analyzer")
root.geometry("600x500")
root.config(bg="white")

title = tk.Label(root, text="Resume Analyzer", font=("Helvetica", 18, "bold"), bg="white", fg="blue")
title.pack(pady=10)

browse_btn = tk.Button(root, text="📂 Browse Resume (PDF)", command=browse_file, bg="green", fg="white", padx=10, pady=5)
browse_btn.pack(pady=10)

dark_btn = tk.Button(root, text="Enable Dark Mode", command=toggle_dark_mode, bg="lightgray", padx=10, pady=5)
dark_btn.pack(pady=5)

result_text = tk.Text(root, height=20, wrap="word", bg="white", fg="black")
result_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

root.mainloop()