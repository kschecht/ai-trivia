# TrivAI Pursuit

## Overview
Welcome to TrivAI Pursuit! This is a trivia game combining everyone's favorite parts of Trivial Pursuit and Are You Smarter Than a 5th Grader, where you choose the topics and AI generates the questions!

## Setup
The following setup is required on your own personal machine to run this game.

### Python
This version has been tested to run stably on Python version [3.9.2](https://www.python.org/downloads/release/python-392/).

### Requirements
Run `pip install -r requirements.txt` to install required modules.

### OpenAI Secret Key
1. Follow [OpenAI's instructions](https://platform.openai.com/docs/quickstart/account-setup) to create an account if you do not already have one and subsequently create an API secret key.
2. Create a folder in your local clone of this repo called `ai_secrets`.
3. Inside that folder, create a file called `ai_secret_key.txt`.
4. Paste your secret key you created in Step 1 into the file you created in Step 3.
    * As a reminder, **never share your secret key with anyone else**. This is your own private key and can be used to access paid content in your OpenAI account.
    * By default, the `ai_secrets` folder and all of its contents are included in a `.gitignore` file, meaning git will ignore these contents if you push to a branch of your own.

Using OpenAI's API does cost money, though not very much for personal usage. For reference, when I was running many tests on this game, I made 565 API requests, which cost me $0.62. You can view your own usage and costs at https://platform.openai.com/usage.

## How to Start
To start this game, run the `play_trivia.py` script. You will be guided by command prompts through the game.

## How to Play
Are you someone who can't remember how to play a game after reading/being read instructions? Same here! Therefore, the following instructions are **not** necessary to read before playing this game, as the command prompt will guide you through every step as you play. For everyone else who likes to know how a game works before playing, keep reading!

### Setup
Before playing, you'll be asked to set up your game with the following information:

1. **Players:** The names of everyone who will be playing. Players will take turns answering questions in the order they are entered during this setup. Random players will choose topics for each other.
2. **Number of Grades:** This essentially means the number of questions a player has to answer correctly in order to win the game. The default is **3** grades.
3. **Grade Numbers:** Each question will be asked at a grade level specified during this setup. Each player will continue to answer questions in each specified grade level until they answer one correctly, at which point they move on to answering questions in the next specified grade level. To win the game, a player must answer one question correctly from each specified grade level. Available grade levels to choose from include:
    * Preschool
    * Kindergarten
    * 1st - 12th Grade
    * College Freshman
    * College Sophomore
    * College Junior
    * College Senior
    * Master's Degree
4. **AI Host Traits:** Pick a personality for your AI host! To get the personality to come through more, try to choose fewer traits, though there is no limit on what traits you can specify. Examples include:
    * `sleepy`
    * `secretly a cat`
    * `speaks in rhyme`
    * `scared of trivia`

### Turns
Each player's turn will follow these steps:

1. A random player will be selected to pick a topic for a question for the player whose turn it is to answer.
    * These question topics can be anything you want! From general academic subjects like `geometry` to specific niches like `season 6 of Riverdale`, anything goes!
2. The AI will generate a question in this topic appropriate for the preset grade level.
3. The player whose turn it is will type their answer to the generated question. 
4. The AI will evaluate whether the player's answer accurately answered the question and, if so, gives them a point.
    * The AI may not always evaluate player's answers completely correctly, but the AI has the final say on points!

### How to Win
The first player to answer one question in each grade level correctly wins!

## Sources
* `openai_chat.py` was largely adapted from DougDougGithub's [Babagaboosh/openai_chat.py](https://github.com/DougDougGithub/Babagaboosh/blob/main/openai_chat.py).