import requests,json,html,random,time
import pygame as pg
pg.init()

def display_difficulty_selection():
    display.fill(background_clr)
    blit_wrapped(display, "Select Difficulty:", displaysize[0] - 2 * scale, font, text_clr, scale, scale)
    difficulties = ["easy", "medium", "hard", None]
    for i, difficulty in enumerate(difficulties, 1):
        if difficulty is not None:
            text = f"{i} - {difficulty.capitalize()}"
        else:
            text = f"{i} - Random"
        blit_wrapped(display, text, displaysize[0] - 2 * scale, font, text_clr, scale, (i + 1) * scale)

    pg.display.flip()
    selected_difficulty = "MMMM"
    while selected_difficulty == "MMMM":
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.unicode.isdigit() and 1 <= int(event.unicode) <= len(difficulties):
                    selected_difficulty = difficulties[int(event.unicode) - 1]
                    break
    return selected_difficulty


def display_topic_selection():
    display.fill(background_clr)
    blit_wrapped(display, "Select a Topic:", displaysize[0] - 2 * scale, font, text_clr, scale, scale)

    topics_list = list(topics.values())
    topics_per_page = 9
    visible_topics = topics_list[:topics_per_page]
    start_index = 0
    font2 = pg.font.SysFont(None,round(1.20*scale))

    while True:
        display.fill(background_clr)
        blit_wrapped(display, "Select a Topic:", displaysize[0] - 1.20*2 * scale, font2, text_clr, 1.20*scale, 1.20*scale)
        for i, topic_name in enumerate(visible_topics, 1):
            blit_wrapped(display, f"{i} - {topic_name}", displaysize[0] - 1.20*2 * scale, font2, text_clr, 1.20*scale, (i + 1) *1.20* scale)

        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_DOWN and start_index + topics_per_page < len(topics_list):
                    start_index += 1
                    visible_topics = topics_list[start_index:start_index + topics_per_page]
                elif event.key == pg.K_UP and start_index > 0:
                    start_index -= 1
                    visible_topics = topics_list[start_index:start_index + topics_per_page]
                elif event.unicode.isdigit() and 1 <= int(event.unicode) <= len(visible_topics):
                    selected_topic = visible_topics[int(event.unicode) - 1]
                    return selected_topic





def display_question_count_selection():
    display.fill(background_clr)
    blit_wrapped(display, "Enter Number of Questions:", displaysize[0] - 2 * scale, font, text_clr, scale, scale)
    pg.display.flip()

    count_input = ""
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.unicode.isdigit():
                    count_input += event.unicode
                    
                elif event.key == pg.K_BACKSPACE:
                    count_input = count_input[:len(count_input)-1]

                elif event.key == pg.K_RETURN:
                    return int(count_input)

        display.fill(background_clr)
        blit_wrapped(display, "Enter Number of Questions:", displaysize[0] - 2 * scale, font, text_clr, scale, scale)
        blit_wrapped(display, count_input, displaysize[0] - 2 * scale, font, text_clr, scale, 3 * scale)
        pg.display.flip()



def save_scores(score):
    display.fill(background_clr)
    blit_wrapped(display, "Do you want to save your score? (y/n)", displaysize[0] - 2 * scale, font, text_clr, scale, scale)
    pg.display.flip()

    save_option_selected = False
    while not save_option_selected:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.unicode.lower() == "y" or event.unicode == "1":
                    save_option_selected = True
                    break
                elif event.unicode.lower() == "n" or event.unicode == "2":
                    return

    display.fill(background_clr)
    blit_wrapped(display, "Enter your username:", displaysize[0] - 2 * scale, font, text_clr, scale, scale)
    pg.display.flip()

    username = ""
    gong = False
    while not gong:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    print("enter!")
                    if len(username) > 3:
                        save_option_selected = True
                        gong = True
                elif event.unicode.isalnum():
                    username += event.unicode

                elif event.key == pg.K_BACKSPACE:
                    username = username[:len(username)-1]
                    
                elif event.key == pg.K_ESCAPE:
                    return

        display.fill(background_clr)
        blit_wrapped(display, "Enter your username:", displaysize[0] - 2 * scale, font, text_clr, scale, scale)
        blit_wrapped(display, username, displaysize[0] - 2 * scale, font, text_clr, scale, 3 * scale)
        pg.display.flip()


    user_data = {"username": username, "score": score}
    print(user_data)
    try:
        with open("USERS.json", "r") as file:
            users = json.load(file)
    except FileNotFoundError:
        users = []

    users.append(user_data)

    with open("USERS.json", "w") as file:
        json.dump(users, file)

    display.fill(background_clr)
    blit_wrapped(display, f"Score saved for {username}!", displaysize[0] - 2 * scale, font, text_clr, scale, scale)
    pg.display.flip()
    time.sleep(2)


def show_score(score, max_score):
    display.fill(background_clr)

    if score == max_score:
        message = f"Amazing! Perfect Score: {score}/{max_score}"
    elif score == 0:
        message = f"Oops! Better luck next time. Score: {score}/{max_score}"
    else:
        message = f"Test Completed! Score: {score}/{max_score}"

    # Calculate the position to center the message
    text_width, text_height = font.size(message)
    x = (displaysize[0] - text_width) // 2
    y = (displaysize[1] - text_height) // 2

    blit_wrapped(display, message, displaysize[0] - 2 * scale, font, text_clr, x, y)
    pg.display.flip()
    time.sleep(3)

def blit_wrapped(screen, text, max_width, font, color, x, y):
    words = text.split(" ")
    wrapped_lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            wrapped_lines.append(current_line)
            current_line = word + " "

    wrapped_lines.append(current_line)

    total_height = 0
    for line in wrapped_lines:
        rendered_text = font.render(line, True, color)
        screen.blit(rendered_text, (x, y + total_height))
        total_height += font.size(line)[1]
    return total_height



def display_question(n,q):
    global score
    category = html.unescape(q["category"])
    difficulty = html.unescape(q["difficulty"])
    question = html.unescape(q["question"])
    qtype = html.unescape(q["type"])

    if qtype == "multiple":
        correct_answer = html.unescape(q["correct_answer"])
        incorrect_answers = [html.unescape(q["incorrect_answers"][i]) for i in range(len(q["incorrect_answers"]))]

        incorrect_answers.append(correct_answer)
        answers = incorrect_answers
        random.shuffle(answers)

        display.fill(background_clr)
        try:
            h = blit_wrapped(display, chr(n + 65)+" - "+question, displaysize[0]-2*scale, font, text_clr, scale, scale)
        except:
            h = blit_wrapped(display, "?"+" - "+question, displaysize[0]-2*scale, font, text_clr, scale, scale)
        for num,a in enumerate(answers):
            blit_wrapped(display, "        "+str(num+1)+" - "+a, displaysize[0]-2*scale, font, text_clr, scale, h + 2*scale+num*scale)
        blit_wrapped(display, f"Score: {score}", displaysize[0] - 2 * scale, font, text_clr, scale, displaysize[1] - 3 * scale)




        pg.display.flip()
        answered = False
        while not answered:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return "ex"
                if event.type == pg.KEYDOWN:
                    if event.unicode in ["1","2","3","4"]:
                        answered = True
                        ans = int(event.unicode)
                        break
                    if event.key == pg.K_g:
                        answered = True
                        ans = answers.index(correct_answer)+1


        if answers[ans-1] == correct_answer:
            print("correct!")
            score += 1
            for num,a in enumerate(answers):
                if a == correct_answer:
                    blit_wrapped(display, "        "+str(num+1)+" - "+a, displaysize[0]-2*scale, font, correct_clr, scale, h + 2*scale+num*scale)
                    break
        else:
            print("wrong!")
            for num,a in enumerate(answers):
                if a == correct_answer:
                    blit_wrapped(display, "        "+str(num+1)+" - "+a, displaysize[0]-2*scale, font, correct_clr, scale, h + 2*scale+num*scale)
                if a == answers[ans-1]:
                    blit_wrapped(display, "        "+str(num+1)+" - "+a, displaysize[0]-2*scale, font, wrong_clr, scale, h + 2*scale+num*scale)

        print("correct answer:",correct_answer)
        pg.display.flip()
        time.sleep(2)


    elif qtype == "boolean":
        correct_answer = q["correct_answer"]
        if correct_answer == "True":
            correct_answer = True
        else:
            correct_answer = False
        display.fill(background_clr)
        try:
            h = blit_wrapped(display, chr(n + 65)+" - "+question, displaysize[0]-2*scale, font, text_clr, scale, scale)
        except:
            h = blit_wrapped(display, "?"+" - "+question, displaysize[0]-2*scale, font, text_clr, scale, scale)
        for num,a in enumerate(["True","False"]):
            blit_wrapped(display, "        "+str(num+1)+" - "+a, displaysize[0]-2*scale, font, text_clr, scale, h + 2*scale+num*scale)
        blit_wrapped(display, f"Score: {score}", displaysize[0] - 2 * scale, font, text_clr, scale, displaysize[1] - 3 * scale)

        pg.display.flip()
        answered = False
        while not answered:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return
                if event.type == pg.KEYDOWN:
                    if event.unicode.lower() in ["1","2","t","f","y","n"]:
                        answered = True
                        ans = event.unicode.lower()
                        break
                    if event.key == pg.K_g:
                        answered = True
                        if correct_answer:
                            ans = "1"
                        else:
                            ans = "2"


        if ans in ["1","t","y"] and correct_answer:
            print("correct!")
            score += 1
            blit_wrapped(display, "        1 - True", displaysize[0]-2*scale, font, correct_clr, scale, h + 2*scale+0*scale)
        elif ans in ["2","f","n"] and not correct_answer:
            print("correct!")
            score += 1
            blit_wrapped(display, "        2 - False", displaysize[0]-2*scale, font, correct_clr, scale, h + 2*scale+1*scale)

        elif ans in ["1","t","y"] and not correct_answer:
            print("wrong!")
            blit_wrapped(display, "        1 - True", displaysize[0]-2*scale, font, wrong_clr, scale, h + 2*scale+0*scale)
            blit_wrapped(display, "        2 - False", displaysize[0]-2*scale, font, correct_clr, scale, h + 2*scale+1*scale)
        else:
            print("wrong!")
            blit_wrapped(display, "        1 - True", displaysize[0]-2*scale, font, correct_clr, scale, h + 2*scale+0*scale)
            blit_wrapped(display, "        2 - False", displaysize[0]-2*scale, font, wrong_clr, scale, h + 2*scale+1*scale)


        pg.display.flip()
        print("correct answer:",correct_answer)
        time.sleep(2)









cheating = False
scale = int(pg.display.Info().current_w / 40)
score = 0
text_clr = (255,255,255)
correct_clr = (0,255,0)
wrong_clr = (255,0,0)
background_clr = (0,0,0)


font = pg.font.SysFont(None,scale)
displaysize = (scale*30,scale*15)
display = pg.display.set_mode(displaysize)

topics = {
    "any": "Any Category",
    "9": "General Knowledge",
    "10": "Entertainment: Books",
    "11": "Entertainment: Film",
    "12": "Entertainment: Music",
    "13": "Entertainment: Musicals & Theatres",
    "14": "Entertainment: Television",
    "15": "Entertainment: Video Games",
    "16": "Entertainment: Board Games",
    "17": "Science & Nature",
    "18": "Science: Computers",
    "19": "Science: Mathematics",
    "20": "Mythology",
    "21": "Sports",
    "22": "Geography",
    "23": "History",
    "24": "Politics",
    "25": "Art",
    "26": "Celebrities",
    "27": "Animals",
    "28": "Vehicles",
    "29": "Entertainment: Comics",
    "30": "Science: Gadgets",
    "31": "Entertainment: Japanese Anime & Manga",
    "32": "Entertainment: Cartoon & Animations"
}


questioncount = display_question_count_selection()
diff = display_difficulty_selection()
topic = display_topic_selection()
print("selected category:",topic)

for key,value in topics.items():
    if value == topic:
        topic = key
        break





timeG = time.time()
print("requesting questions...")
link = "https://opentdb.com/api.php?amount="+str(questioncount)




if topic != "any":
    link += "&category="+topic


if diff:
    link+="&difficulty="+diff

R = requests.get(link)
questions = R.json()["results"]
print("questions recived in "+str(round(time.time()-timeG,2))+" seconds!")





for n,q in enumerate(questions):
    R = display_question(n,q)
    if R == "ex":
        break
print("test over! your score:",score)



show_score(score,questioncount)
save_scores(score)

pg.quit()
quit()
