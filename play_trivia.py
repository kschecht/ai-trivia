import re
import openai
import random

GRADE_NAMES = {
    -1: "preschool",
    0: "kindergarten",
    1: "1st grade",
    2: "2nd grade",
    3: "3rd grade",
    4: "4th grade",
    5: "5th grade",
    6: "6th grade",
    7: "7th grade",
    8: "8th grade",
    9: "9th grade",
    10: "10th grade",
    11: "11th grade",
    12: "12th grade",
    13: "college freshman",
    14: "college sophomore",
    15: "college junior",
    16: "college senior",
    17: "master's degree"
}

with open("ai_secrets/ai_organization.txt", 'r') as org_file:
    openai.organization = org_file.read()
with open("ai_secrets/ai_secret_key.txt", 'r') as secret_file:
    openai.api_key = secret_file.read()

def get_players():
    print()
    confirm = "n"
    players = []
    while confirm != "y":
        players = input("Enter all player names separated by spaces (ex: Alice Bob   Carl): ").split()
        print("Your players are:")
        for player in players:
            print(player)
        confirm = input("Is this correct? (y/n) ")
    return players

def is_int(int_str):
    return re.match('-?\d+', int_str)

def get_number_of_grades():
    print()
    num_grades = input("Enter the number of grades you'd like to complete. The winner will be the first player to answer one question correctly in each grade! If you choose not to enter a number, we'll select the default of 6 grades. ")
    if is_int(num_grades):
        return int(num_grades)
    else:
        return 6

def get_grades(num_grades):
    print()
    print("Now you'll choose which grade levels your questions will be in! For example, if you type '6', your question will be at a 6th grade level.")
    print("<0 = preschool")
    print("0 = kindergarten")
    print("1-12 = grades 1-12")
    print("13-16 = undergraduate freshman through senior")
    print(">16 = master's degree")
    print("Your grade number selections should ideally be in ascending order so that your questions will get more difficult as the game goes on!")
    print("If you don't respond with a number, we'll pick one of the default grades (7, 8, 9, 10, 11, 12)")
    print()
    grades = []
    for grade_num in range(1, num_grades+1):
        grade = input(f"What grade level should Question {grade_num} be? ")
        if is_int(grade):
            grades.append(int(grade))
        else:
            grades.append(grade_num + 6)
    return grades

def get_ai_response(content):
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": content}]
    ).choices[0].message.content

def get_random_player_index():
    return random.randrange(0,len(REMAINING_PLAYERS))

def did_someone_win(num_grades):
    found_winner = False
    score_strs = []
    for player in PLAYERS_SCORES:
        score = PLAYERS_SCORES[player]
        score_strs.append(f"{player}:{score}")
        if not found_winner and score >= num_grades:
            print()
            print(f"Congrats {player}! You've won this game of TrivAI Pursuit!!!")
            print(get_ai_response(f"{player} just won a trivia competition! Please give them a compliment about how much smarter they are than everybody else. Also bestow upon them a made-up title awarded to them for this honor."))
            found_winner = True
    if found_winner:
        print()
        print(f"Here are the final scores!")
        print(score_strs)
    return found_winner

def get_category_player(turn_index):
    global REMAINING_PLAYERS
    global ALL_PLAYERS
    if len(REMAINING_PLAYERS) == 1 and REMAINING_PLAYERS[0] == ALL_PLAYERS[turn_index]:
        REMAINING_PLAYERS = []
    if len(REMAINING_PLAYERS) <= 0:
        for player in ALL_PLAYERS:
            REMAINING_PLAYERS.append(player)
    category_player_index = get_random_player_index()
    while REMAINING_PLAYERS[category_player_index] == ALL_PLAYERS[turn_index]:
        category_player_index = get_random_player_index()
    category_player = REMAINING_PLAYERS[category_player_index]
    REMAINING_PLAYERS.remove(category_player)
    return category_player

def get_grade_for_player(player):
    grade_index = PLAYERS_SCORES[player]
    grade = GRADES[grade_index]
    if grade < -1:
        grade = -1
    if grade > 17:
        grade = 17
    return GRADE_NAMES[grade]

def turns(num_grades):
    turn_index = 0
    while not did_someone_win(num_grades):
        print()
        answering_player = ALL_PLAYERS[turn_index]
        print(f"It's now {answering_player}'s turn!")
        grade_name = get_grade_for_player(answering_player)
        topic = input(f"{get_category_player(turn_index)}: Pick a topic for a {grade_name} level question for {answering_player}! ")
        print()
        question = get_ai_response(f"Write a {grade_name} level question about {topic}. Please write a question with an answer that is not longer than one sentence. Do not write down the answer in your response. Do not make the answer the topic that was chosen.")
        print()
        user_answer = input(f"{answering_player}, please answer the following question: {question} ")
        print()
        ai_answer = get_ai_response(f'The question is: "{question}". Is the correct answer {user_answer}? Please make the first word of your response "Yes" if this is the correct answer, or "No" if this is not the correct answer, and make sure to explain what the correct answer was if the provided answer was incorrect. If the question was subjective, count any answer as correct.')
        print(ai_answer)
        print()
        if ai_answer[0] == "Y":
            PLAYERS_SCORES[answering_player] = PLAYERS_SCORES[answering_player] + 1
            print(f"{answering_player} gets a point! Your score is now {PLAYERS_SCORES[answering_player]}!")
        else:
            print(f"{answering_player} gets no points this round!")
        print("Remember, for this game, the AI's answer is always the right answer! (Even if it's actually the wrong answer)")
        turn_index = turn_index + 1
        if turn_index >= len(ALL_PLAYERS):
            turn_index = 0


def main():
    print("Welcome to TrivAI Pursuit! Where you decide the category, and AI comes up with the questions!")
    global ALL_PLAYERS
    ALL_PLAYERS = get_players()
    global REMAINING_PLAYERS
    REMAINING_PLAYERS = []
    for player in ALL_PLAYERS:
        REMAINING_PLAYERS.append(player)
    num_grades = get_number_of_grades()
    global GRADES
    GRADES = get_grades(num_grades)
    initial_score = 0
    global PLAYERS_SCORES
    PLAYERS_SCORES = {player:initial_score for player in ALL_PLAYERS}
    print()
    print("All right! We're ready to play!")
    print(get_ai_response("Tell me a random fun motivational catchphrase for a trivia competition!"))
    print()
    turns(num_grades)

    
if __name__ == "__main__":
    main()