"""
gui_main.py - Tkinter GUI for Resume Screening System
====================================================
A graphical interface for the Resume Screening System.


"""

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
from utils import (
    clean_text, tokenize, load_roles, load_resume_from_file, match_skills,
    calculate_score, get_grade, generate_suggestions, save_analysis,
    load_analysis_history
)

class ResumeScreeningApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📄 Resume Screening System (AI)")
        self.root.geometry("900x700")
        self.root.configure(bg="#f4f6fb")
        self.resume_text = ""
        self.selected_role = ""
        self.roles = load_roles()
        self._build_gui()

    def _build_gui(self):
        # Header with color and emoji
        header_frame = tk.Frame(self.root, bg="#3a7ca5", pady=18)
        header_frame.pack(fill="x")
        header = tk.Label(
            header_frame,
            text="  📄 Resume Screening System  ",
            font=("Segoe UI", 26, "bold"),
            fg="#fff",
            bg="#3a7ca5"
        )
        header.pack()

        # Frame for actions with modern button style
        action_frame = tk.Frame(self.root, bg="#f4f6fb")
        action_frame.pack(pady=18)

        btn_style = {
            "font": ("Segoe UI", 12, "bold"),
            "bg": "#e3eafc",
            "fg": "#1a2639",
            "activebackground": "#b6ccfe",
            "activeforeground": "#1a2639",
            "relief": tk.RAISED,
            "bd": 2,
            "width": 14,
            "cursor": "hand2",
            "highlightthickness": 0,
            "padx": 2,
            "pady": 2
        }
        buttons = [
            ("Paste Resume", self.paste_resume),
            ("Load Resume File", self.load_resume_file),
            ("Select Role", self.select_role),
            ("Analyze", self.analyze_resume),
            ("History", self.show_history),
            ("Roles", self.show_roles),
            ("Help", self.show_help)
        ]
        for i, (label, cmd) in enumerate(buttons):
            btn = tk.Button(action_frame, text=label, command=cmd, **btn_style)
            btn.grid(row=0, column=i, padx=6)

        # Resume text area with border and background
        resume_frame = tk.LabelFrame(self.root, text="Paste or Load Resume", font=("Segoe UI", 12, "bold"), fg="#3a7ca5", bg="#f4f6fb", bd=2, relief=tk.GROOVE, padx=8, pady=8)
        resume_frame.pack(pady=8, padx=18, fill="x")
        self.resume_textbox = scrolledtext.ScrolledText(resume_frame, height=8, width=110, font=("Consolas", 11), bg="#fafdff", bd=1, relief=tk.SUNKEN)
        self.resume_textbox.pack()

        # Status label
        self.status_label = tk.Label(self.root, text="Resume: Not loaded | Role: Not selected", fg="#3a7ca5", bg="#f4f6fb", font=("Segoe UI", 11, "bold"), pady=6)
        self.status_label.pack()

        # Output area with border and background
        output_frame = tk.LabelFrame(self.root, text="Analysis & Output", font=("Segoe UI", 12, "bold"), fg="#3a7ca5", bg="#f4f6fb", bd=2, relief=tk.GROOVE, padx=8, pady=8)
        output_frame.pack(pady=8, padx=18, fill="both", expand=True)
        self.output_box = scrolledtext.ScrolledText(output_frame, height=18, width=110, state='disabled', font=("Consolas", 11), bg="#fafdff", bd=1, relief=tk.SUNKEN)
        self.output_box.pack(fill="both", expand=True)

    def update_status(self):
        resume_status = "Loaded" if self.resume_text else "Not loaded"
        role_status = self.selected_role if self.selected_role else "Not selected"
        self.status_label.config(text=f"Resume: {resume_status} | Role: {role_status}")

    def paste_resume(self):
        self.resume_text = self.resume_textbox.get("1.0", tk.END).strip()
        if self.resume_text:
            word_count = len(tokenize(clean_text(self.resume_text)))
            messagebox.showinfo("Resume Loaded", f"Resume loaded successfully!\nWord count: {word_count}")
        else:
            messagebox.showwarning("No Text", "Please paste your resume text.")
        self.update_status()

    def load_resume_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            content = load_resume_from_file(file_path)
            if content:
                self.resume_text = content
                self.resume_textbox.delete("1.0", tk.END)
                self.resume_textbox.insert(tk.END, content)
                word_count = len(tokenize(clean_text(content)))
                messagebox.showinfo("Resume Loaded", f"Loaded from: {file_path}\nWord count: {word_count}")
            else:
                messagebox.showerror("Error", "Failed to load resume. Check the file.")
        self.update_status()

    def select_role(self):
        if not self.roles:
            messagebox.showerror("No Roles", "No roles available. Check roles.json.")
            return
        role_names = list(self.roles.keys())
        win = tk.Toplevel(self.root)
        win.title("Select Job Role")
        tk.Label(win, text="Select a job role:").pack(pady=5)
        lb = tk.Listbox(win, width=50, height=10)
        for r in role_names:
            lb.insert(tk.END, r)
        lb.pack(pady=5)
        def on_select():
            sel = lb.curselection()
            if sel:
                self.selected_role = role_names[sel[0]]
                messagebox.showinfo("Role Selected", f"Selected: {self.selected_role}")
                win.destroy()
                self.update_status()
        tk.Button(win, text="Select", command=on_select).pack(pady=5)

    def analyze_resume(self):
        if not self.resume_text:
            messagebox.showwarning("No Resume", "Please paste or load a resume first.")
            return
        if not self.selected_role:
            messagebox.showwarning("No Role", "Please select a job role first.")
            return
        if self.selected_role not in self.roles:
            messagebox.showerror("Role Error", f"Role '{self.selected_role}' not found.")
            return
        role_data = self.roles[self.selected_role]
        required_skills = role_data.get("required_skills", [])
        experience_keywords = role_data.get("experience_keywords", [])
        matched_skills, missing_skills = match_skills(self.resume_text, required_skills)
        matched_exp, _ = match_skills(self.resume_text, experience_keywords)
        skill_score = calculate_score(len(matched_skills), len(required_skills))
        exp_bonus = calculate_score(len(matched_exp), len(experience_keywords)) * 0.1 if experience_keywords else 0
        final_score = min(round(skill_score + exp_bonus, 2), 100.0)
        grade, rating = get_grade(final_score)
        suggestions = generate_suggestions(missing_skills, self.selected_role)
        if matched_exp:
            suggestions.append(f"Good: Your resume mentions relevant experience terms like: {', '.join(matched_exp[:3])}")
        # Save to history
        save_analysis(self.selected_role, final_score, grade, matched_skills, missing_skills)
        # Display report
        self.output_box.config(state='normal')
        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, f"\n=== Resume Analysis Report ===\n")
        self.output_box.insert(tk.END, f"Target Role: {self.selected_role}\nScore: {final_score}%\nGrade: {grade}\nRating: {rating}\n")
        self.output_box.insert(tk.END, f"\nMatched Skills ({len(matched_skills)}): {', '.join(matched_skills)}\n")
        self.output_box.insert(tk.END, f"Missing Skills ({len(missing_skills)}): {', '.join(missing_skills)}\n")
        self.output_box.insert(tk.END, f"\nSuggestions:\n")
        for i, s in enumerate(suggestions, 1):
            self.output_box.insert(tk.END, f"  {i}. {s}\n")
        self.output_box.config(state='disabled')
        self.update_status()

    def show_history(self):
        history = load_analysis_history()
        self.output_box.config(state='normal')
        self.output_box.delete("1.0", tk.END)
        if not history:
            self.output_box.insert(tk.END, "No analysis history found.\n")
        else:
            self.output_box.insert(tk.END, f"Analysis History ({len(history)} records):\n")
            for i, rec in enumerate(history, 1):
                self.output_box.insert(tk.END, f"{i}. {rec['timestamp']} | {rec['role']} | Score: {rec['score']} | Grade: {rec['grade']}\n")
        self.output_box.config(state='disabled')

    def show_roles(self):
        if not self.roles:
            messagebox.showerror("No Roles", "No roles available.")
            return
        self.output_box.config(state='normal')
        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, "Available Job Roles:\n")
        for name, data in self.roles.items():
            desc = data.get("description", "No description")
            skills = data.get("required_skills", [])
            exp = data.get("experience_keywords", [])
            self.output_box.insert(tk.END, f"\n{name}: {desc}\n  Required Skills: {', '.join(skills)}\n  Experience Keywords: {', '.join(exp)}\n")
        self.output_box.config(state='disabled')

    def show_help(self):
        help_text = (
            "How to use this tool:\n"
            "1. Paste or load your resume.\n"
            "2. Select a job role.\n"
            "3. Click Analyze to see your score, matched/missing skills, and suggestions.\n"
            "Other options: View history, browse roles, or see this help.\n"
        )
        self.output_box.config(state='normal')
        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, help_text)
        self.output_box.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = ResumeScreeningApp(root)
    root.mainloop()
