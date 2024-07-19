import random
import tkinter as tk
import ttkbootstrap as ttk
import matplotlib.pyplot as plt
import numpy as np

#defines question variable
class Question:
    def __init__(self, phrase, colors, answer):
        self.phrase = phrase
        self.colors = colors
        self.answer = answer
    
    def __str__(self):
        return f'Do you value {self.phrase}? Associated with: {self.colors}. User answer: {self.answer}'
    
    #returns randomized list of question vairables
    def add_questions():
        #empty list for question objects
        questions = []

        #mono one
        questions.append(Question("Peace", ["white"], 0))
        questions.append(Question("Perfection", ["blue"], 0))
        questions.append(Question("Satisfaction", ["black"], 0))
        questions.append(Question("Freedom", ["red"], 0))
        questions.append(Question("Harmony", ["green"], 0))

        #mono two
        questions.append(Question("Order", ["white"], 0))
        questions.append(Question("Knowledge", ["blue"], 0))
        questions.append(Question("Ruthlessness", ["black"], 0))
        questions.append(Question("Action", ["red"], 0))
        questions.append(Question("Acceptance", ["green"], 0))

        #allied pairs
        questions.append(Question("Structure", ["white", "blue"], 0))
        questions.append(Question("Growth Mindset", ["blue", "black"], 0))
        questions.append(Question("Independence", ["black", "red"], 0))
        questions.append(Question("Authenticity", ["red", "green"], 0))
        questions.append(Question("Community", ["green", "white"], 0))

        #enemy pairs
        questions.append(Question("Tribalism", ["white", "black"], 0))
        questions.append(Question("Creativity", ["blue", "red"], 0))
        questions.append(Question("Profanity", ["black", "green"], 0))
        questions.append(Question("Heroism", ["red", "white"], 0))
        questions.append(Question("Truth-Seeking", ["green", "blue"], 0))

        #mono three
        questions.append(Question("Trust", ["white"], 0))
        questions.append(Question("Group", ["white"], 0))
        questions.append(Question("Nurture", ["blue"], 0))
        questions.append(Question("Reason", ["blue"], 0))
        questions.append(Question("Individual", ["black"], 0))
        questions.append(Question("Exploitation", ["black"], 0))
        questions.append(Question("Emotion", ["red"], 0))
        questions.append(Question("Chaos", ["red"], 0))
        questions.append(Question("Preservation", ["green"], 0))
        questions.append(Question("Nature", ["green"], 0))

        #randomizes questions
        random.shuffle(questions)

        return questions

font_size = 42

#weights score based on probability
#calls dice_prob function
def weight(score):
    result = 0
    for i in range(score + 1):
        result += dice_prob(3, 8, i)
    return round(result * 100 * score / 16)

#probability of getting target_num score with random answers
#called by weight function
def dice_prob(dice_sides, dice_num, target_num):
    combinations = 0
    total_events = dice_sides**dice_num

    for i in range(total_events):
        x = i
        event = []
        for j in range(dice_num):
            event.append(x % (dice_sides))
            x = int(x/(dice_sides))
        if sum(event) == target_num:
            combinations += 1

    return(combinations/total_events)

#runs when user gives answer
def answer(user_response):
    if current_question_int.get() < len(questions)-1:
        questions[current_question_int.get()].answer = user_response #records user answer in list

        #print(f'{questions[current_question_int.get()].phrase}: {questions[current_question_int.get()].answer}')

        current_question_int.set(current_question_int.get() + 1) #itterates question
        question_label['text']=(f'{questions[current_question_int.get()].phrase}?') #updates label

    #runs when all questions are answered
    elif current_question_int.get() == len(questions)-1:
        questions[current_question_int.get()].answer = user_response #records user answer in list
        current_question_int.set(current_question_int.get() + 1) #itterates question to freeze program with result displayed

        #calculates final result
        final_calc()
        
#calculates final result
#called by answer func
def final_calc():
    #declaring scores for each color
    white = 0
    blue = 0
    black = 0
    red = 0
    green = 0

    #calculates scores
    for i in questions:
        for j in i.colors:
            if j == 'white':
                white += i.answer
            if j == 'blue':
                blue += i.answer
            if j == 'black':
                black += i.answer
            if j == 'red':
                red += i.answer
            if j == 'green': 
                green += i.answer

    #calculates weighted scores
    weighted_white = weight(white)
    weighted_blue  = weight(blue)
    weighted_black = weight(black)
    weighted_red   = weight(red)
    weighted_green = weight(green)

    #calculates weighted percents
    score_sum = weighted_white + weighted_blue + weighted_black + weighted_red + weighted_green
    if score_sum > 0:
        white_percent = round(weighted_white * 100 / score_sum)
        blue_percent  = round(weighted_blue  * 100 / score_sum)
        black_percent = round(weighted_black * 100 / score_sum)
        red_percent   = round(weighted_red   * 100 / score_sum)
        green_percent = round(weighted_green * 100 / score_sum)
    else:
        white_percent = 0
        blue_percent  = 0
        black_percent = 0
        red_percent   = 0
        green_percent = 0

    sensitivity = 20 #sensitivity of the identiy calculation
    identity = ''

    if white_percent >= sensitivity and white > 6:
        identity += "white "
    if blue_percent  >= sensitivity and blue  > 6:
        identity += "blue "
    if black_percent >= sensitivity and black > 6:
        identity += "black "
    if red_percent   >= sensitivity and red   > 6:
        identity += "red "
    if green_percent >= sensitivity and green > 6:
        identity += "green "

    if identity == "":
        identity = "colorless "

    result_label = ttk.Label(quiz_window, text=f'You are a {identity}planeswalker.', font=('Arail', font_size))
    result_label.place(relx=0.5, y=400, anchor='center')

    #creates array of results
    results = np.array([green_percent, red_percent , black_percent, blue_percent, white_percent])

    # pie chart of results
    plt.pie(
        results, 
        colors=['green', 'red', 'black', 'blue' , 'white'], 
        labels=[str(green_percent), str(red_percent), str(black_percent), str(blue_percent), str(white_percent)], 
        startangle=90, 
        wedgeprops={'edgecolor' : 'black', 'linewidth' : 2})
    plt.show()



#calls add questions 
questions = Question.add_questions()

#create window
quiz_window = ttk.Window(themename="darkly")
quiz_window.geometry(f'{quiz_window.winfo_screenwidth()}x{quiz_window.winfo_screenheight()}')
quiz_window.title('MTG Color Quiz')

#number of current question in list
current_question_int = tk.IntVar(value=0)

#"Do you value" part of prompt
prompt_label = tk.Label(quiz_window, text='Do you value:', font=('Arail', font_size))
prompt_label.pack(pady=10)

#prompt from question
question_label = tk.Label(quiz_window, text=f'{questions[current_question_int.get()].phrase}?', font=('Arial', font_size))
question_label.pack(pady=10)

#frame to hold answers in line
answers_frame = ttk.Frame(quiz_window)

# style buttons
# ttk.Style().configure('TButton', font=('Arial', font_size))

#answer buttons
no_button = ttk.Button(answers_frame, text='No', command=lambda:answer(0), width= 50)
no_button.place(relx=0.25, rely=0.5, height=50, anchor='center')
sometimes_button = ttk.Button(answers_frame, text='Sometimes', command=lambda:answer(1), width= 50)
sometimes_button.place(relx=0.5, rely=0.5, height=50, anchor='center')
yes_button = ttk.Button(answers_frame, text='Yes', command=lambda:answer(2), width= 50)
yes_button.place(relx=0.75, rely=0.5, height=50, anchor='center')

answers_frame.place(relx=0.5, y=250, relwidth=1, height=50, anchor='center')

if __name__=='__main__':
    #runs quiz windowwindow
    quiz_window.mainloop()