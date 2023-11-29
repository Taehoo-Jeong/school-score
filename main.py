from tkinter import *
from tkinter import messagebox
import pandas as pd
import os

main_window = Tk()
main_window.title("학생 성적 관리 프로그램")
main_window.resizable(False, False)
def add_student():
    # Create a new window for adding students
    add_window = Toplevel()
    add_window.title("학생 성적 추가")
    add_window.resizable(False, False)

    # Create entry fields for the student's name and grades
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

    # Function to save the student's grades to the CSV file
    def save_student():
        name = name_entry.get()
        korean = korean_entry.get()
        math = math_entry.get()
        english = english_entry.get()

        if any(value == '' for value in [name, korean, math, english]):
            messagebox.showwarning("경고", "학생 성적을 모두 입력해주세요.")
            return

        student_data = {'이름': [name], '국어': [korean], '수학': [math], '영어': [english]}
        df = pd.DataFrame(student_data)
        df.to_csv('students.csv', mode='a', header=False, index=False)

        messagebox.showinfo("성적 추가", "학생 성적이 추가되었습니다.")

    # Create a button to save the student's grades
    save_button = Button(add_window, text="저장", command=save_student)
    save_button.grid(row=4, column=0, columnspan=2)

    def back():
        add_window.destroy()
        enter_window.deiconify()

    back_button = Button(add_window, text="뒤로가기", command=back)
    back_button.grid(row=5, column=0, columnspan=2)

    add_window.mainloop()

def delete_student():
    def delete():
        name = name_entry.get()

        if name == '':
            messagebox.showwarning("경고", "학생 이름을 입력해주세요.")
            return

        if not os.path.exists('students.csv'):
            messagebox.showwarning("경고", "학생 데이터가 없습니다.")
            return

        df = pd.read_csv('students.csv')

        if name not in df['이름'].values:
            messagebox.showwarning("경고", "해당 학생이 존재하지 않습니다.")
            return

        df = df[df['이름'] != name]
        df.to_csv('students.csv', index=False)

        messagebox.showinfo("성적 삭제", "학생 성적이 삭제되었습니다.")
        delete_window.destroy()  # Close the delete_window

    enter_window.withdraw()
    delete_window = Toplevel()
    delete_window.title("학생 성적 삭제")
    delete_window.resizable(False, False)

    name_label = Label(delete_window, text="이름:", font=("맑은 고딕", 15))
    name_label.grid(row=0, column=0, padx=10, pady=10)
    name_entry = Entry(delete_window, font=("맑은 고딕", 15))
    name_entry.grid(row=0, column=1, padx=10, pady=10)

    delete_button = Button(delete_window, text="삭제", font=("맑은 고딕", 15), command=delete)
    delete_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

def search_student():
    def search():
        name = name_entry.get()

        if name == '':
            messagebox.showwarning("경고", "학생 이름을 입력해주세요.")
            return

        if not os.path.exists('students.csv'):
            messagebox.showwarning("경고", "학생 데이터가 없습니다.")
            return

        df = pd.read_csv('students.csv')

        if name not in df['이름'].values:
            messagebox.showwarning("경고", "해당 학생이 존재하지 않습니다.")
            return

        student = df[df['이름'] == name]
        messagebox.showinfo("학생 성적", f"이름: {name}\n국어: {student['국어'].values[0]}\n수학: {student['수학'].values[0]}\n영어: {student['영어'].values[0]}")

    def back():
        search_window.destroy()
        enter_window.deiconify()

    # Close the search_window
    enter_window.withdraw()
    search_window = Toplevel()
    search_window.title("학생 검색")
    search_window.resizable(False, False)

    # Create entry field for the student's name
    name_label = Label(search_window, text="이름")
    name_label.grid(row=0, column=0)
    name_entry = Entry(search_window)
    name_entry.grid(row=0, column=1)

    # Create a button to search for the student
    search_button = Button(search_window, text="검색", command=search)
    search_button.grid(row=1, column=0, columnspan=2)
    
    back_button = Button(search_window, text="뒤로가기", command=back)
    back_button.grid(row=2, column=0, columnspan=2)
    
def update_student():
    # Create a new window
    update_window = Tk()
    update_window.title("학생 성적 수정")
    update_window.resizable(False, False)

    # Create entry fields for the student's name and new grades
    name_label = Label(update_window, text="이름")
    name_label.grid(row=0, column=0)
    name_entry = Entry(update_window)
    name_entry.grid(row=0, column=1)

    korean_label = Label(update_window, text="국어")
    korean_label.grid(row=1, column=0)
    korean_entry = Entry(update_window)
    korean_entry.grid(row=1, column=1)

    math_label = Label(update_window, text="수학")
    math_label.grid(row=2, column=0)
    math_entry = Entry(update_window)
    math_entry.grid(row=2, column=1)

    english_label = Label(update_window, text="영어")
    english_label.grid(row=3, column=0)
    english_entry = Entry(update_window)
    english_entry.grid(row=3, column=1)

    # Function to update the student's grades in the CSV file
    def save_updated_student():
        name = name_entry.get()
        korean = korean_entry.get()
        math = math_entry.get()
        english = english_entry.get()

        df = pd.read_csv('students.csv')
        df.loc[df['이름'] == name, '국어'] = korean
        df.loc[df['이름'] == name, '수학'] = math
        df.loc[df['이름'] == name, '영어'] = english
        df.to_csv('students.csv', index=False)

        messagebox.showinfo("성적 수정", "학생 성적이 수정되었습니다.")
        update_window.destroy()

    # Create a button to save the updated grades
    save_button = Button(update_window, text="저장", command=save_updated_student)
    save_button.grid(row=4, column=0, columnspan=2)

    update_window.mainloop()

def print_grades():
    if not os.path.exists('students.csv'):
        messagebox.showwarning("경고", "학생 데이터가 없습니다.")
        return

    df = pd.read_csv('students.csv')

    # Calculate the average grades for each student
    df['평균성적'] = df[['국어', '수학', '영어']].mean(axis=1)

    median_grades = df[['국어', '수학', '영어']].median()
    standard_deviation = df[['국어', '수학', '영어']].std().mean()

    messagebox.showinfo("성적 출력", f"각 과목의 중간값: {median_grades.to_dict()}\n"
                                    f"전체 학생의 표준편차: {standard_deviation}\n"
                                    f"각 학생의 평균 성적: {df['평균성적'].to_dict()}")

def create_button(window, text, font, command, row, column):
    button = Button(window, text=text, font=font, command=command)
    button.grid(row=row, column=column, padx=10, pady=10)
    return button

def enter():
    global enter_window
    main_window.withdraw()

def print_grades():
    if not os.path.exists('students.csv'):
        messagebox.showwarning("경고", "학생 데이터가 없습니다.")
        return

    df = pd.read_csv('students.csv')

    max_grades = df[['국어', '수학', '영어']].max()
    student_averages = df[['국어', '수학', '영어']].mean(axis=1).round(3)
    standard_deviation = df[['국어', '수학', '영어']].std().mean().round(2)

    student_names = df['이름'].tolist()
    student_grades = dict(zip(student_names, student_averages))

    messagebox.showinfo("성적 출력", f"각 과목의 최고점: {max_grades.to_dict()}\n"
                                    f"각 학생의 평균: {student_grades}\n"
                                    f"전체 학생의 표준편차: {standard_deviation}")


def create_button(window, text, font, command, row, column):
    button = Button(window, text=text, font=font, command=command)
    button.grid(row=row, column=column, padx=10, pady=10)
    return button

def enter():
    global enter_window
    main_window.withdraw()

    enter_window = Tk()
    enter_window.title("학생 성적 관리 프로그램")
    enter_window.resizable(False, False)

    # 학생 성적 추가 버튼
    add_button = create_button(enter_window, "학생 성적 추가", ("맑은 고딕", 15), add_student, 0, 0)

    # 학생 성적 검색 버튼
    search_button = create_button(enter_window, "학생 성적 검색", ("맑은 고딕", 15), search_student, 1, 0)

    # 학생 성적 삭제 버튼
    delete_button = create_button(enter_window, "학생 성적 삭제", ("맑은 고딕", 15), delete_student, 2, 0)

    # 학생 성적 출력 버튼
    print_button = create_button(enter_window, "학생 성적 출력", ("맑은 고딕", 15), print_grades, 3, 0)

    # 학생 성적 수정 버튼
    update_button = create_button(enter_window, "학생 성적 수정", ("맑은 고딕", 15), update_student, 4, 0)

    def back():
        enter_window.destroy()
        main_window.deiconify()
    # 뒤로가기 버튼
    back_button = create_button(enter_window, "뒤로가기", ("맑은 고딕", 15), lambda: enter_window.destroy(), 5, 0)

    enter_window.mainloop()

title = Label(main_window, text="학생 성적 관리 프로그램", font=("맑은 고딕", 20))
title.grid()

Enter = Button(main_window, text="접속하기", font=("맑은 고딕", 15), command=enter)
Enter.grid()

Exit = Button(main_window, text="종료하기", font=("맑은 고딕", 15), command=main_window.quit)
Exit.grid()

main_window.mainloop()