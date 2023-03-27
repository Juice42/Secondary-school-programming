from tkinter import *
from functools import partial  # To prevent unwanted windows
import random
import re
import csv
from random import shuffle



class Start:
    def __init__(self, parent):
        # GUI for Quiz
        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        # Quiz Heading
        self.Quiz_box_label = Label(self.start_frame, text="Country and Capital Quiz",
                                    font="Arial 19 bold")
        self.Quiz_box_label.grid(row=0, column=0)

        # Quiz text
        self.start_text = Label(self.start_frame, text="Welcome to my Country and Capitals Quiz "
                                                       "i have got a large variety of "
                                                       " questions and i hope you enjoy the quiz, "
                                                       "as it is my first ever peice of code that i have done "
                                                       "majority of by myself.\n\n"
                                                       "press start when ready!",
                                justify=LEFT, width=40, wrap=250, font="Arial 12")
        self.start_text.grid(row=1)

        # Help and Play button (row 3)
        self.help_export_frame = Frame(self.start_frame)
        self.help_export_frame.grid(row=2, pady=15, padx=15)

        self.start_button = Button(self.help_export_frame, text="Start",
                                   bg="midnight blue", fg="white", font="Arial 15 bold", width=10,
                                   command=self.mode)
        self.start_button.grid(row=0, column=0, padx=10, pady=10)

        self.help_button = Button(self.help_export_frame, text="Help",
                                  font="Arial 15 bold", width=10,
                                  bg="maroon", fg="white", command=self.help)
        self.help_button.grid(row=0, column=1, padx=2)

    def mode(self):
        print("Choose a mode!")
        choose_mode = Quiz(self)
        # to_do = Quiz(self)

        # hide start up window
        self.start_frame.destroy()

    def help(self):
        print("you asked for help")
        get_help = Help(self)
        get_help.help_text.config

class Help:
    def __init__(self, partner):
        button_font = "Arial 12 bold"

        # disable help button
        partner.help_button.config(state=DISABLED)

        # sets up child window (ie: help box)
        self.help_box = Toplevel()

        # If user press cross at top, closes help and 'releases' help button
        self.help_box.protocol('WM_DELETE_WINDOW', partial(self.close_help, partner))

        # Set up GUI Frame
        self.help_frame = Frame(self.help_box, width=300, )
        self.help_frame.grid()

        # Set up Help Heading (row 0)
        self.how_heading = Label(self.help_frame, text="Help / Instructions",
                                 font=button_font)
        self.how_heading.grid(row=0)

        help_text = "1. Pressing start will take you straight to the quiz.\n\n" \
                    "2. When ready press next and it will display a question, write your answer in the entry box.\n\n" \
                    "3. it is good to note that there is only 10 questions.\n\n" \
                    "4. While in the quiz you can quit at anytime.\n\n" \
                    "5. At the end of the quiz it will disable both buttons and it will tell you your score" \
                    " then you can press quit and the quiz will end.\n\n"

        # if have a blank answer that is a feature but will be marked wrong***

        # Help text (label, row 1)
        self.help_text = Label(self.help_frame, text=help_text,
                               justify=LEFT, wrap=400, padx=10, pady=10)
        self.help_text.grid(row=1)

        # Dismiss button (row 2)
        self.dismiss_btn = Button(self.help_frame, text="Dismiss",
                                  width=10,
                                  command=partial(self.close_help, partner))
        self.dismiss_btn.grid(row=2, padx=10, pady=10)

    def close_help(self, partner):
        # Put help button back to normal...
        partner.help_button.config(state=NORMAL)
        self.help_box.destroy()


class Quiz:
    def __init__(self, parent):

        self.var_countries = StringVar()
        self.my_score = IntVar()
        self.my_score.set(0)
        self.questions_done = IntVar()
        self.questions_done.set(0)

        # set up variable to hold question

        # GUI for Quiz
        self.quiz_frame = Frame(padx=15, pady=15)
        self.quiz_frame.grid()

        # Quiz Heading
        self.country_capitals_label = Label(self.quiz_frame, text="Capitals and Countries",
                                            font="Arial 19")
        self.country_capitals_label.grid(row=0)

        # Initial Instructions (row 1)
        self.quiz_instructions = Label(self.quiz_frame, font="Arial 11 italic",
                                          text="Please press the <next> button",
                                          wrap=275, justify=LEFT, padx=10, pady=10)
        self.quiz_instructions.grid(row=1)

        # Entry box (row 2)
        self.entry_frame = Frame(self.quiz_frame, width=200)
        self.entry_frame.grid(row=2)

        # Entry Box (row 3)
        self.entry_box = Entry(self.quiz_frame, width=20,
                                font="Arial 14 bold", justify=CENTER)
        self.entry_box.grid(row=3, pady=10)

        # amount_error label (set to blank at start)
        self.answer_label = Label(self.quiz_frame, font="Arial 10 italic",
                                  text="Answer goes here",
                                  wrap=275, justify=LEFT, padx=10, pady=10)
        self.answer_label.grid(row=4)

        # Check and Next button (row 5)
        self.quiz_export_frame = Frame(self.quiz_frame)
        self.quiz_export_frame.grid(row=5, pady=15, padx=15)

        # Check Button
        self.check_button = Button(self.quiz_export_frame, width = 15, text="Check",
                                   font="Arial 12 bold", bg = "Dark green", fg="white", command=self.check_answer)
        self.check_button.grid(row=5,column=0, padx=15, pady=15)

        self.check_button.config(state=DISABLED)

        # Next Button
        self.next_button = Button(self.quiz_export_frame, width=15, text="Next",
                                   font="Arial 12 bold", bg="black", fg="white", command=self.next_question)
        self.next_button.grid(row=5,column=1, padx=15, pady=15)

        # Quit Button
        self.quit_quiz_button = Button(self.quiz_export_frame,width=15, text="Quit",
                                      font="Arial 12 bold", bg="Grey", fg="white", command=self.to_quit)
        self.quit_quiz_button.grid(row=6, padx=15,columnspan=3, pady=15)

    def to_quit(self):
        root.destroy()

    def next_question(self):
        with open("country_capitals_csv.csv", "r") as country_capitals_csv_file:
            csv_reader = csv.reader(country_capitals_csv_file)

            questions_done = self.questions_done.get()

            country_list = list(csv_reader)[1:]

            # choose random item from a list
            random_q_a = random.choice(country_list)

            self.check_button.config(state = NORMAL)
            self.next_button.config(state = DISABLED)

            question = random_q_a[1]
            print(question)
            answer = random_q_a[0]
            # print(answer)

            self.var_countries.set(answer)

            print("Type in the text box what country you think it is...")

            # clear entry box??
            self.entry_box.config(bg="white")
            self.entry_box.delete(0, END)

            self.quiz_instructions.config(text=question, font = "Arial 15 bold ")

            # pressing next will + 1 question
            questions_done += 1
            self.questions_done.set(questions_done)

            # self.next_button(questions_done)

            # Capital Question
            # self.capital_question = Label(self.start_frame, text=(random_q_a [1]), font = "Arial 15 bold ")
            # self.capital_question.grid(row=2)


            # # Country Answer
            # self.country_answer1 = Label(self.start_frame, text =(random_q_a [0]), font = "Arial 15 bold ")
            # self.country_answer1.grid(row=5)


    def check_answer(self):
        # Check answer - if what the user wrote is the same as what is in position 0 then it is correct but if it is,
        # not the same as position 0 it is incorrect.

        country_answer = self.var_countries.get()
        user_answer = self.entry_box.get()
        score = self.my_score.get()
        questions_done = self.questions_done.get()

        self.check_button.config(state=DISABLED)
        self.next_button.config(state=NORMAL)

        # print(user_answer)
        print(country_answer)

        error_back = "#ffafaf"
        correct_back = "Pale Green"

        if user_answer.lower() == country_answer.lower():
            has_errors = "no"
            # Each time i get something right it adds + 1 to my score
            score += 1
            self.my_score.set(score)

            error_feedback =" That is correct!  Score: {}/10, press next to continue".format(score)

        else:
            has_errors = "yes"
            error_feedback ="That is incorrect, the answer is {}.  Score: {}/10".format(country_answer, score)

        if has_errors == "yes":
            self.entry_box.config(bg=error_back)
            self.answer_label.config(text=error_feedback, font="Arial 10 italic")

        if has_errors == "no":
            self.entry_box.config(bg=correct_back)
            self.answer_label.config(text=error_feedback, font="Arial 10 italic")

        if questions_done == 10:
            self.next_button.config(state=DISABLED)
            self.check_button.config(state=DISABLED)
            self.quiz_frame.focus()
            self.answer_label.config(text="Game Over, Your final score was {}/10".format(score))


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Capitals and Countries quiz")
    Start(root)
    root.mainloop()

