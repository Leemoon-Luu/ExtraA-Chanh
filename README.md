# Student Gradebook CLI

## Overview

This project is a Python-based command-line application for managing a student gradebook.
It supports adding, updating, deleting, and viewing courses, as well as computing
overall and semester-based weighted GPA. Data is persisted in a JSON file between sessions.

## Features

- Add a course (code, name, credits, semester, score)
- Update an existing course by code
- Delete a course
- View all courses in a tabular format
- Compute overall weighted GPA (0–10 scale)
- Compute GPA by semester
- Persistent storage in `gradebook.json`
- Input validation to prevent invalid scores, credits, and duplicate course codes

## Project Structure

```text
gradebook_project/
├─ gradebook/
│  ├─ __init__.py
│  ├─ data.py
│  ├─ operations.py
│  └─ cli.py
├─ gradebook.json
└─ README.md
```


## How to Run the Project

### 1. Navigate to the project folder

```bash
cd gradebook_project
```

### 2. Run the CLI application

```bash
python -m gradebook.cli
```

### 3. Use the menu to interact with the program

```text
===== Student Gradebook Menu =====
1. Add a course
2. Update a course
3. Delete a course
4. View gradebook
5. Calculate overall GPA
6. Calculate GPA by semester
0. Exit
==================================
Select an option:
```

