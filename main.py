from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import pandas as pd
import os

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

def add_student():
    add_window = Toplevel()
    add_window.title("학생 성적 추가")
    add_window.resizable(False, False)

    name_label = Label(add_window, text="이름", font=("맑은 고딕", 15))
    name_label.grid(row=0, column=0)
    name_entry = Entry(add_window)
    name_entry.grid(row=0, column=1)

    korean_label = Label(add_window, text="국어", font=("맑은 고딕", 15))
    korean_label.grid(row=1, column=0)
    korean_entry = Entry(add_window)
    korean_entry.grid(row=1, column=1)

    math_label = Label(add_window, text="수학", font=("맑은 고딕", 15))
    math_label.grid(row=2, column=0)
    math_entry = Entry(add_window)
    math_entry.grid(row=2, column=1)

    english_label = Label(add_window, text="영어", font=("맑은 고딕", 15))
    english_label.grid(row=3, column=0)
    english_entry = Entry(add_window)
    english_entry.grid(row=3, column=1)

    def save_student():
        name = name_entry.get()
        korean = korean_entry.get()
        math = math_entry.get()
        english = english_entry.get()

        if any(value == '' for value in [name, korean, math, english]):
            messagebox.showwarning("경고", "학생 성적을 모두 입력해주세요.")
            return
        elif not korean.isdigit() or not math.isdigit() or not english.isdigit():
            messagebox.showwarning("경고", "성적은 숫자로만 입력해주세요.")
            return
        elif not (0 <= int(korean) <= 100) or not (0 <= int(math) <= 100) or not (0 <= int(english) <= 100):
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
            else:
                df.to_csv('students.csv', mode='a', header=False, index=False)

        messagebox.showinfo("성적 추가", "학생 성적이 추가되었습니다.")
        name_entry.delete(0, END)
        korean_entry.delete(0, END)
        math_entry.delete(0, END)
        english_entry.delete(0, END)

    save_button = create_button(add_window, "저장", ("맑은 고딕", 10), save_student, 4, 0, 0, 0)

    def back():
        add_window.destroy()
        enter_window.deiconify()

    back_button = create_button(add_window, "뒤로가기", ("맑은 고딕", 10), back, 4, 1, 0, 0)
    add_window.mainloop()

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
        grades_window = Tk()
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

        grades_window.mainloop()

    display_grades(student_grades)

def enter():
    global enter_window
    main_window.withdraw()

    enter_window = Tk()
    enter_window.title("학생 성적 관리 프로그램")
    enter_window.resizable(False, False)

    add_button = create_button(enter_window, "학생 성적 추가", ("맑은 고딕", 15), add_student, 0, 0, 10, 10)
    print_button = create_button(enter_window, "학생 성적 출력", ("맑은 고딕", 15), print_grades, 1, 0, 10, 10)

    def back():
        enter_window.destroy()
        main_window.deiconify()

    back_button = create_button(enter_window, "뒤로가기", ("맑은 고딕", 15), back, 2, 0, 10, 10)

    enter_window.mainloop()

title = Label(main_window, text="학생 성적 관리 프로그램", font=("맑은 고딕", 20))
title.grid()

Enter = Button(main_window, text="접속하기", font=("맑은 고딕", 15), command=enter)
Enter.grid()

Exit = Button(main_window, text="종료하기", font=("맑은 고딕", 15), command=main_window.quit)
Exit.grid()

main_window.mainloop()
