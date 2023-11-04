from tkinter import *
import csv

my_font = ("Helvetica", 12)
big_font = ("Helvetica", 18)


cat_question = "Kennst du Die brasilianische Katze von Sir Arthur Conan Doyle?"
thomas_question = "Kennst du die Geschichte \"Thomas\" von Vanessa Krypczyk?"
auftrag_question = "Kennst du die Geschichte \"Ein geheimer Auftrag\" von Wolfgang Koeppen?"


def chose_text_question(text):
    if text == "cat":
        text_question = cat_question
    elif text == "thomas":
        text_question = thomas_question
    else:
        text_question = auftrag_question
    return text_question


def radio_button(r, text, this_row, parent, text_1="ja", text_2="nein"):
    Message(parent, anchor='w', text=text, width=1000, borderwidth=5, font=my_font).grid(sticky="W", row=this_row, column=0)
    r_1 = Radiobutton(parent, text=text_1, variable=r, value=1)
    r_1.grid(row=this_row, column=2)
    r_2 = Radiobutton(parent, text=text_2, variable=r, value=2)
    r_2.grid(row=this_row, column=3)
    return r


def lickert_question(text, this_row, parent):
    Message(parent, anchor='w', text=text, width=1000, borderwidth=5, font=my_font).grid(sticky="W", row=this_row, column=0)
    l_1 = Label(parent, text="Ich stimme gar nicht zu", borderwidth=4, font=my_font)
    l_1.grid(row=this_row, column=1)
    s = Scale(parent, from_=-10, to=10, showvalue=0, orient=HORIZONTAL, length=200)
    s.grid(row=this_row, column=2, columnspan=2)
    l_2 = Label(parent, text="Ich stimme sehr zu", borderwidth=4, font=my_font)
    l_2.grid(row=this_row, column=4)
    return s


def user_input(text, this_row, parent, lines=1):
    Message(parent, anchor='w', text=text, width=1000, borderwidth=5, font=my_font).grid(sticky="W", row=this_row, column=0)
    if lines == 1:
        e = Entry(parent, width=100)
    else:
        e = Text(parent, width=100, height=3)
    e.grid(row=this_row, column=1, columnspan=4)
    return e


class QuestionWindow:
    def __init__(self, title, question_list):
        self.window = Tk()
        self.window.title(title)
        self.w_height = 768
        self.w_width = 1366
        self.center_screen()
        self.window.attributes("-topmost", True)
        self.question_list = question_list
        self.frame = Frame(self.window)
        self.frame.place(in_=self.window, anchor="c", relx=.5, rely=.5)
        self.s_button = Button(self.frame, text="Speichern", command=self.submit, font=my_font)
        self.s_button.grid(row=len(self.question_list), column=0, columnspan=5)

    def center_screen(self):
        # gets the coordinates of the center of the screen
        global screen_height, screen_width, x_coordinate, y_coordinate
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x_coordinate = int(screen_width/2) - (self.w_width/2)
        y_coordinate = int(screen_height/2) - (self.w_height/2)
        self.window.geometry(f"{self.w_width}x{self.w_width}+{int(x_coordinate)}+{int(y_coordinate)}")

    def display_questions(self, multiline=False):
        for i in range(len(self.question_list)):
            self.question_list[i]["intvar"] = IntVar()
            if self.question_list[i]["user_input"] == "1":
                if not multiline:
                    r = user_input(self.question_list[i]["text"], i, self.frame)
                else:
                    r = user_input(self.question_list[i]["text"], i, self.frame, 4)
            elif self.question_list[i]["lickert"] == "1":
                r = lickert_question(self.question_list[i]["text"], i, self.frame)
            elif "rechts" in self.question_list[i]["text"]:
                r = radio_button(self.question_list[i]["intvar"], self.question_list[i]["text"], i, self.frame, "rechts", "links")
            else:
                r = radio_button(self.question_list[i]["intvar"], self.question_list[i]["text"], i, self.frame)
            self.question_list[i]["value"] = r

    def submit(self):
        for q in self.question_list:
            try:
                q["result"] = q["value"].get()
            except TypeError:  # if it was a text input question, the result is a different type,
                # and it needs 2 additional arguments, a starting point and an end point for saving the string
                q["result"] = q["value"].get("1.0", 'end-1c')
            # now restructure items for super simple statistics
            q.pop("qu_number")
            q.pop("value")
            for x in ["user_input", "yes_no", "lickert"]:
                if q[x] == "1":
                    q["mode"] = x
                q.pop(x)
        for q in self.question_list:
            if "result" not in q:
                q["result"] = "not_answered"
        self.window.iconify()
        self.window.quit()
        self.window.destroy()


def read_in_questions(question_file):
    questions = []
    with open(question_file +".csv", newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, dialect='excel', delimiter=";")
        for row in reader:
            questions.append(dict(row))
    questions_part_1 = [x for x in questions if x["second_window"] == "0"]
    questions_part_2 = [x for x in questions if x["second_window"] == "1"]
    return [questions_part_1, questions_part_2]


def meta_data_to_dict(read_text, count_round):
    text_qu = chose_text_question(read_text)
    data_list = [{'qu_number': 0, 'text': 'Teilnahme-ID', 'user_input': '1', 'lickert': '0', 'yes_no': '0'},
                 {'qu_number': 1, 'text': 'Alter', 'user_input': '1', 'lickert': '0', 'yes_no': '0'},
                 {'qu_number': 2, 'text': 'Höchster Abschluss', 'user_input': '1', 'lickert': '0', 'yes_no': '0'},
                 {'qu_number': 3, 'text': 'Wie viel liest du? (z.B. "sehr wenig", "wenig", "durchschnittlich", "viel", "sehr viel")', 'user_input': '1', 'lickert': '0', 'yes_no': '0'},
                 {'qu_number': 4, 'text': 'Welche Buchgenres liest du?', 'user_input': '1', 'lickert': '0', 'yes_no': '0'},
                 {'qu_number': 5, 'text': 'Bist du rechtshändig oder linkshändig?', 'user_input': '0', 'lickert': '0', 'yes_no': '1'},
                 {'qu_number': 6, 'text': 'Hast du eine Farbfehlsichtigkeit? (Rot-/Grünschwäche o.ä.)', 'user_input': '0', 'lickert': '0', 'yes_no': '1'},
                 {'qu_number': 7, 'text': 'Bist du dyslexisch (Lese- und Rechtschreibschwäche)?', 'user_input': '0', 'lickert': '0', 'yes_no': '1'},
                 {'qu_number': 8, 'text': 'Hast du bereits einmal einen Text in diesem Experimentsetting gelesen?', 'user_input': '0', 'lickert': '0', 'yes_no': '1'},
                 {'qu_number': 9, 'text': text_qu, 'user_input': '0', 'lickert': '0', 'yes_no': '1'}]
    if count_round == 2:
        data_list = [x for x in data_list if x["qu_number"] in [0, 9]]
    return data_list


def callback(event, window):
    window.destroy()


def init_thanks():
    thank_you = Tk()
    thank_you.geometry("1920x1080")
    thank_you.attributes("-fullscreen", True)
    thank_you.attributes("-topmost", True)
    lab = Label(thank_you, text="Vielen Dank. Diese Runde ist beendet. Hole bitte die Experimentleitung.", font=big_font)
    lab.place(relx=.5, rely=.5, anchor="center")
    lab.bind("<Button-1>", lambda x: callback("<Button-1>", thank_you))
    lab.pack()
    thank_you.mainloop()


