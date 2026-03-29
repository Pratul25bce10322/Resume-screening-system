# 📄 Resume Screening System (with GUI)

> An AI-powered resume screening tool with both **CLI** and **GUI (Tkinter)** interfaces. Evaluate resumes against predefined job role requirements using NLP techniques and simple scoring logic.

---

## 📋 Table of Contents
- [About the Project](#about-the-project)
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [How to Set Up & Run](#how-to-set-up--run)
- [How to Use the GUI](#how-to-use-the-gui)
- [How to Use the CLI](#how-to-use-the-cli)
- [Sample Input / Output](#sample-input--output)
- [Scoring Logic](#scoring-logic)
- [Available Job Roles](#available-job-roles)
- [Contributing](#contributing)

---

## 🧠 About the Project

### Problem Statement
Job seekers often struggle to assess how well their resume matches a target job role. Manually comparing skills against job descriptions is tedious and error-prone.

### Solution
This **Resume Screening System** provides an automated tool that:
- Accepts resume text (paste or file upload)
- Compares it against predefined skill sets for popular job roles
- Uses **NLP preprocessing** (tokenization, text cleaning) and **keyword matching**
- Produces a **match score (0–100%)**, lists matched/missing skills, and provides **actionable suggestions**
- **Now features a GUI built with Tkinter for an easy, interactive experience!**

### AI/NLP Concepts Used
| Concept | Application |
|---------|------------|
| **Text Preprocessing** | Lowercasing, punctuation removal, whitespace normalization |
| **Tokenization** | Splitting text into individual word tokens |
| **N-gram Generation** | Creating bigrams/trigrams for multi-word skill matching |
| **Keyword Matching** | Comparing tokens against predefined skill dictionaries |
| **Scoring Algorithm** | Calculating percentage match based on skill overlap |

---

## ✨ Features

- ✅ **GUI Interface (Tkinter)** — User-friendly window for loading resumes, selecting roles, and viewing results
- ✅ **CLI Option** — Terminal-based interaction for advanced users
- ✅ **Paste or Upload Resume** — Enter text directly or load from `.txt` file
- ✅ **8 Job Roles** — Web Developer, Data Analyst, Software Engineer, ML Engineer, Cybersecurity Analyst, Mobile App Developer, DevOps Engineer, UI/UX Designer
- ✅ **Smart Matching** — Handles multi-word skills (e.g., "machine learning", "power bi")
- ✅ **Detailed Reports** — Score, grade, progress bar, matched/missing skills
- ✅ **Actionable Suggestions** — Personalized tips to improve your resume
- ✅ **Analysis History** — All past analyses saved automatically
- ✅ **Experience Bonus** — Extra points for relevant experience keywords
- ✅ **Beautiful CLI** — Color-coded output with Unicode formatting

---

## 📂 Project Structure

```
resume-screening-system/
├── gui_main.py           # GUI application (Tkinter interface)
├── main.py               # Main CLI application (entry point)
├── utils.py              # Helper functions (text processing, scoring, display)
├── roles.json            # Job roles database (skills & keywords)
├── README.md             # Project documentation (CLI)
├── README_GUI.md         # Project documentation (GUI)
├── data/
│   ├── sample_resume.txt      # Sample resume for testing
│   └── analysis_history.json  # Auto-generated analysis history
└── report/
    └── project_report.md      # Project report document
```

---

## 🔧 Prerequisites

- **Python 3.7 or higher**
- **Tkinter** (comes pre-installed with most Python distributions)
- A terminal / command prompt (for CLI)

Verify Python is installed:
```bash
python --version
```

> **Note:** This project uses only Python standard library modules (`json`, `os`, `string`, `datetime`, `sys`, `tkinter`). No `pip install` needed!

---

## 🚀 How to Set Up & Run

### Step 1: Clone the Repository
```bash
git clone https://github.com/sam-2811/Resume-Screening-System
cd Resume-Screening-System
```

### Step 2: Run the GUI Application
```bash
python gui_main.py
```

### (Optional) Run the CLI Application
```bash
python main.py
```

---

## 🖼️ How to Use the GUI


### GUI Screenshots

**Starting Page:**
![alt text](<WhatsApp Image 2026-03-29 at 5.09.39 PM.jpeg>)

**Result Page (After Analysis):**
![alt text](<WhatsApp Image 2026-03-29 at 5.10.20 PM.jpeg>)

1. **Launch the GUI**: Run `python gui_main.py`.
2. **Load your resume**: Paste text or select a `.txt` file using the interface.
3. **Select a job role**: Choose from the dropdown menu.
4. **Analyze**: Click the analyze button to view your match score, grade, matched/missing skills, and suggestions.
5. **View history**: Access past analyses from the GUI.
6. **Exit**: Close the window when done.

---

## 📖 How to Use the CLI

1. **Load your resume** (Option `1` or `2`)
   - Option `1`: Paste resume text directly into the terminal
   - Option `2`: Load from a `.txt` file (e.g., `data/sample_resume.txt`)
2. **Select a job role** (Option `3`)
   - Choose from 8 available roles by entering the role number
3. **Analyze** (Option `4`)
   - The system will process your resume and display the results in the terminal
4. **View history** (Option `5`)
5. **Exit** (Option `0`)

---

## 📊 Sample Input / Output (GUI)

- **Input**: Load a resume and select a role in the GUI, then click Analyze.
- **Output**: A window displays your match score, grade, matched/missing skills, and suggestions in a clear, user-friendly format.

---

## 🧮 Scoring Logic

### Formula
```
Skill Score = (Matched Skills / Total Required Skills) × 100
Experience Bonus = (Matched Exp Keywords / Total Exp Keywords) × 10
Final Score = min(Skill Score + Experience Bonus, 100)
```

### Grading Scale

| Score Range | Grade | Rating |
|:-----------:|:-----:|:------:|
| 80–100% | Excellent Match | ★★★★★ |
| 60–79% | Good Match | ★★★★☆ |
| 40–59% | Average Match | ★★★☆☆ |
| 0–39% | Needs Improvement | ★★☆☆☆ |

---

## 🎯 Available Job Roles

| # | Role | Skills Count |
|---|------|:------------:|
| 1 | Web Developer | 28 |
| 2 | Data Analyst | 28 |
| 3 | Software Engineer | 29 |
| 4 | Machine Learning Engineer | 27 |
| 5 | Cybersecurity Analyst | 28 |
| 6 | Mobile App Developer | 27 |
| 7 | DevOps Engineer | 26 |
| 8 | UI/UX Designer | 26 |

---

## 🛠️ Technical Details

### NLP Techniques Used
- **Text Cleaning**: Lowercasing, punctuation removal
- **Tokenization**: Whitespace-based word splitting
- **N-gram Generation**: Bigrams and trigrams for multi-word skill detection
- **Keyword Matching**: Set-based intersection for O(1) lookup performance

### Key Design Decisions
- **No external dependencies**: Runs with Python standard library only
- **Modular architecture**: Separate `utils.py` for reusability
- **JSON-based roles**: Easy to add/modify job roles without code changes
- **Persistent history**: Analysis results saved for future reference
- **GUI with Tkinter**: Simple, cross-platform, and easy to use

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-role`)
3. Add your changes
4. Commit (`git commit -m 'Add new job role'`)
5. Push (`git push origin feature/new-role`)
6. Open a Pull Request

### Adding a New Job Role
Simply add an entry to `roles.json`:
```json
{
    "New Role Name": {
        "description": "Role description here",
        "required_skills": ["skill1", "skill2", "skill3"],
        "experience_keywords": ["keyword1", "keyword2"]
    }
}
```

---

## 👤 Author

- **Name**: Pratul Kashyap
- **Registration No**: 25BCE10322
- **Course**: CSA2001 — Artificial Intelligence
- **University**: VIT Bhopal University

---

> Now with a modern GUI for a better user experience!
