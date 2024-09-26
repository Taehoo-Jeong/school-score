from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import pandas as pd
import os
import shutil
import datetime

main_window = Tk()
main_window.title("학생 성적 관리 프로그램")
main_window.resizable(False, False)

def create_button(window, text, font, command, row, column, padx, pady):
    button = Button(window, text=text, font=font, command=command)
    button.grid(row=row, column=column, padx=padx, pady=pady)
    return button

def calculate_grade(score, all_scores):
    sorted_scores = sorted(all_scores, reverse=True)
    rank = sorted_scores.index(score) + 1
    percentile = rank / len(all_scores)

    if percentile <= 0.1:
        return 'A+'
    elif percentile <= 0.2:
        return 'A0'
    elif percentile <= 0.3:
        return 'B+'
    elif percentile <= 0.5:
        return 'B0'
    elif percentile <= 0.6:
        return 'C+'
    elif percentile <= 0.7:
        return 'C0'
    else:
        return 'D0'

def create_input_field(window, label_text, row):
    label = Label(window, text=label_text, font=("맑은 고딕", 15))
    label.grid(row=row, column=0)
    entry = Entry(window)
    entry.grid(row=row, column=1)
    return entry

def validate_score(score):
    if not score.isdigit():
        return False
    score_int = int(score)
    return 0 <= score_int <= 100

def backup_csv():
    if os.path.exists('students.csv'):
        backup_file = f'students_backup_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        shutil.copy('students.csv', backup_file)

def add_student():
    add_window = Toplevel()
    add_window.title("학생 성적 추가")
    add_window.resizable(False, False)

    name_entry = create_input_field(add_window, "이름", 0)
    korean_entry = create_input_field(add_window, "국어", 1)
    math_entry = create_input_field(add_window, "수학", 2)
    english_entry = create_input_field(add_window, "영어", 3)

    def save_student():
        name = name_entry.get()
        korean = korean_entry.get()
        math = math_entry.get()
        english = english_entry.get()

        if any(value == '' for value in [name, korean, math, english]):
            messagebox.showwarning("경고", "학생 성적을 모두 입력해주세요.")
            return
        if not all(validate_score(value) for value in [korean, math, english]):
            messagebox.showwarning("경고", "성적은 0과 100 사이의 숫자로 입력해주세요.")
            return

        student_data = {'이름': [name], '국어': [korean], '수학': [math], '영어': [english]}
        df = pd.DataFrame(student_data)

        if not os.path.exists('students.csv'):
            df.to_csv('students.csv', index=False)
        else:
            existing_df = pd.read_csv('students.csv')
            if name in existing_df['이름'].values:
                messagebox.showwarning("경고", "해당 학생이 이미 존재합니다.")
                return
            df.to_csv('students.csv', mode='a', header=False, index=False)

        backup_csv()  # 백업 기능 호출
        messagebox.showinfo("성적 추가", "학생 성적이 추가되었습니다.")
        for entry in [name_entry, korean_entry, math_entry, english_entry]:
            entry.delete(0, END)

    create_button(add_window, "저장", ("맑은 고딕", 10), save_student, 4, 0, 0, 0)
    create_button(add_window, "뒤로가기", ("맑은 고딕", 10), add_window.destroy, 4, 1, 0, 0)
    add_window.mainloop()

def update_student():
    update_window = Toplevel()
    update_window.title("학생 성적 수정")
    update_window.resizable(False, False)

    name_entry = create_input_field(update_window, "이름", 0)
    korean_entry = create_input_field(update_window, "국어", 1)
    math_entry = create_input_field(update_window, "수학", 2)
    english_entry = create_input_field(update_window, "영어", 3)

    def save_updated_student():
        name = name_entry.get()
        korean = korean_entry.get()
        math = math_entry.get()
        english = english_entry.get()

        if any(value == '' for value in [name, korean, math, english]):
            messagebox.showwarning("경고", "학생 성적을 모두 입력해주세요.")
            return
        if not all(validate_score(value) for value in [korean, math, english]):
            messagebox.showwarning("경고", "성적은 0과 100 사이의 숫자로 입력해주세요.")
            return

        df = pd.read_csv('students.csv')
        if name not in df['이름'].values:
            messagebox.showwarning("경고", "해당 학생이 존재하지 않습니다.")
            return

        # 백업 후 수정
        backup_csv()
        df.loc[df['이름'] == name, ['국어', '수학', '영어']] = [korean, math, english]
        df.to_csv('students.csv', index=False)

        messagebox.showinfo("성적 수정", "학생 성적이 수정되었습니다.")
        for entry in [name_entry, korean_entry, math_entry, english_entry]:
            entry.delete(0, END)

    create_button(update_window, "수정", ("맑은 고딕", 10), save_updated_student, 4, 0, 0, 0)
    create_button(update_window, "뒤로가기", ("맑은 고딕", 10), update_window.destroy, 4, 1, 0, 0)
    update_window.mainloop()

def print_grades():
    if not os.path.exists('students.csv'):
        messagebox.showwarning("경고", "학생 데이터가 없습니다.")
        return

    df = pd.read_csv('students.csv')
    
    korean_scores = df['국어'].astype(int).tolist()
    math_scores = df['수학'].astype(int).tolist()
    english_scores = df['영어'].astype(int).tolist()

    df['국어'] = df['국어'].astype(int).apply(lambda score: calculate_grade(score, korean_scores))
    df['수학'] = df['수학'].astype(int).apply(lambda score: calculate_grade(score, math_scores))
    df['영어'] = df['영어'].astype(int).apply(lambda score: calculate_grade(score, english_scores))

    student_grades = df.to_dict(orient='records')

    def display_grades(student_grades):
        grades_window = Toplevel()
        grades_window.title("성적 등급 출력")
        grades_window.resizable(False, False)

        tree = ttk.Treeview(grades_window, columns=('이름', '국어', '수학', '영어'), show='headings')
        tree.heading('이름', text='이름')
        tree.heading('국어', text='국어')
        tree.heading('수학', text='수학')
        tree.heading('영어', text='영어')

        for grades in student_grades:
            tree.insert('', 'end', values=(grades['이름'], grades['국어'], grades['수학'], grades['영어']))
        tree.grid()

    display_grades(student_grades)

def enter():
    global enter_window
    main_window.withdraw()

    enter_window = Toplevel()
    enter_window.title("학생 성적 관리 프로그램")
    enter_window.resizable(False, False)

    create_button(enter_window, "학생 성적 추가", ("맑은 고딕", 15), add_student, 0, 0, 10, 10)
    create_button(enter_window, "학생 성적 수정", ("맑은 고딕", 15), update_student, 1, 0, 10, 10)
    create_button(enter_window, "학생 성적 출력", ("맑은 고딕", 15), print_grades, 2, 0, 10, 10)
    create_button(enter_window, "뒤로가기", ("맑은 고딕", 15), lambda: [enter_window.destroy(), main_window.deiconify()], 3, 0, 10, 10)

    enter_window.mainloop()

title = Label(main_window, text="학생 성적 관리 프로그램", font=("맑은 고딕", 20))
title.grid()

create_button(main_window, "접속하기", ("맑은 고딕", 15), enter, 1, 0, 10, 10)
create_button(main_window, "종료하기", ("맑은 고딕", 15), main_window.quit, 2, 0, 10, 10)

main_window.mainloop()