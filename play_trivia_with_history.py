import openai_chat as chat
import random
import re
#import getpass


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


def setup_game():
    print("Welcome to TrivAI Pursuit! Where you decide the category, and AI comes up with the questions!")
    global ALL_PLAYERS
    ALL_PLAYERS = get_players()
    global REMAINING_PLAYERS
    REMAINING_PLAYERS = []
    for player in ALL_PLAYERS:
        REMAINING_PLAYERS.append(player)
    global NUM_GRADES
    NUM_GRADES = get_number_of_grades()
    global GRADES
    GRADES = get_grades()
    initial_score = 0
    global PLAYERS_SCORES
    PLAYERS_SCORES = {player:initial_score for player in ALL_PLAYERS}
    global AI_PERSONALITY
    AI_PERSONALITY = get_ai_personality()
    print()
    print("All right! We're ready to play!")


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


def get_number_of_grades():
    print()
    num_grades = input("Enter the number of grades you'd like to complete. The winner will be the first player to answer one question correctly in each grade! If you choose not to enter a number, we'll select the default of 6 grades. ")
    if is_int(num_grades):
        return int(num_grades)
    else:
        return 6


def get_grades():
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
    for grade_num in range(1, NUM_GRADES+1):
        grade = input(f"What grade level should Question {grade_num} be? ")
        if is_int(grade):
            grades.append(int(grade))
        else:
            grades.append(grade_num + 6)
    return grades


def is_int(int_str):
    return re.match('-?[0-9]+', int_str)


def get_ai_personality():
    print()
    personality = input(f"What traits do you want your AI host to have? ")
    print()
    return personality


def ai_init(openai_manager):
    FIRST_SYSTEM_MESSAGE = {"role": "system", "content": f'''
    We are playing a trivia game, and you are the host. Please adopt the following personality traits: {AI_PERSONALITY} 
    When you receive a command that begins with "Question: ", you will write a trivia question. Your rules for writing these questions are:
    1) Do not write down the answer in your response. 
    2) Do not make the question subjective.
    When you receive a command that begins with "Answer: ", you will then be given an answer from the user that you will evaluate as correct or incorrect. Please follow these rules for evaluating user answers:
    1) The first word of your response should be "Yes" or "No".
    2) Explain the reasoning why the answer was correct or incorrect, including the correct answer. 
    3) Explain your answer in character with the following traits: {AI_PERSONALITY}
    4) If the question was subjective, count any answer as correct.
    '''}
    openai_manager.chat_history.append(FIRST_SYSTEM_MESSAGE)
    intro = openai_manager.chat_with_history("Hi! Please introduce this trivia game with a random fun motivational catchphrase for a trivia competition!")
    print(intro)


def did_someone_win(openai_manager):
    found_winner = False
    score_strs = []
    for player in PLAYERS_SCORES:
        score = PLAYERS_SCORES[player]
        score_strs.append(f"{player}:{score}")
        if not found_winner and score >= NUM_GRADES:
            print()
            print(f"Congrats {player}! You've won this game of TrivAI Pursuit!!!")
            ai_congrats = openai_manager.chat_with_history(f"{player} just won a trivia competition! Please give them a compliment about how much smarter they are than everybody else. Also bestow upon them a made-up title awarded to them for this honor. Answer in character with these traits: {AI_PERSONALITY}")
            print(ai_congrats)
            found_winner = True
    if found_winner:
        print()
        print(f"Here are the final scores!")
    print(score_strs)
    print()
    return found_winner


def get_grade_for_player(player):
    grade_index = PLAYERS_SCORES[player]
    grade = GRADES[grade_index]
    if grade < -1:
        grade = -1
    if grade > 17:
        grade = 17
    return GRADE_NAMES[grade]


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


def get_random_player_index():
    return random.randrange(0,len(REMAINING_PLAYERS))


def get_valid_question(grade_name, topic):
    invalid = True
    question = openai_manager.chat_with_history(f"Question: Write a {grade_name} level question about {topic}.")
    count = 0
    #print(question)
    while invalid and count < 13:
        answer_match = openai_manager.chat_with_history(f"The question is {question}. Please answer Yes or No: Is the following answer correct? {topic}")
        #print(answer_match)
        if answer_match[0] == "N":
            invalid = False
        else:
            question = openai_manager.chat_with_history(f"Question: Please write a different {grade_name} level question about {topic} that has a different answer than your previous question.")
            #print(question)
        count += 1
    return question


def turns(openai_manager):
    turn_index = 0
    while not did_someone_win(openai_manager):
        print()
        answering_player = ALL_PLAYERS[turn_index]
        print(f"It's now {answering_player}'s turn!")
        grade_name = get_grade_for_player(answering_player)
        topic = input(f"{get_category_player(turn_index)}: Pick a topic for a {grade_name} level question for {answering_player}! ") #getpass.getpass(prompt=f"{get_category_player(turn_index)}: Pick a topic for a {grade_name} level question for {answering_player}! ")
        print()
        question = get_valid_question(grade_name, topic)
        print(question)
        print()
        user_answer = input(f"{answering_player}, please answer the above question. ")
        print()
        ai_answer = openai_manager.chat_with_history(f'Answer: The question is: "{question}". Is the correct answer {user_answer}?')
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


if __name__ == '__main__':
    setup_game()
    openai_manager = chat.OpenAiManager()
    ai_init(openai_manager)
    turns(openai_manager)
        