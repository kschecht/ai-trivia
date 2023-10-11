import re
import openai
import random

ALL_PLAYERS = []
REMAINING_PLAYERS = []
TURN_INDEX = 0

def get_players_input():
    return 

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
    return re.match('\d+', int_str)

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

with open("ai_secrets/ai_organization.txt", 'r') as org_file:
    openai.organization = org_file.read()
with open("ai_secrets/ai_secret_key.txt", 'r') as secret_file:
    openai.api_key = secret_file.read()

def get_ai_response(content):
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": content}]
    ).choices[0].message.content

def get_category_player():
    category_player_index = random.randrange(0,len(REMAINING_PLAYERS))
    while REMAINING_PLAYERS[category_player_index] == ALL_PLAYERS[TURN_INDEX]:
        category_player_index = random.randrange(0,len(REMAINING_PLAYERS))
    category_player = REMAINING_PLAYERS[category_player_index]
    REMAINING_PLAYERS.remove(category_player)
    return category_player

def turn():
    answering_player = ALL_PLAYERS[TURN_INDEX]
    print(f"It's now {answering_player}'s turn!")
    print(f"{get_category_player()}: Pick a topic for ")

def main():
    print("Welcome to AI trivia! Where you decide the category, and AI comes up with the questions!")
    ALL_PLAYERS = get_players()
    REMAINING_PLAYERS = ALL_PLAYERS
    num_grades = get_number_of_grades()
    grades = get_grades(num_grades)
    print()
    print("All right! We're ready to play!")
    print(get_ai_response("Tell me a random fun motivational catchphrase for a trivia competition!"))
    print()

    
if __name__ == "__main__":
    main()