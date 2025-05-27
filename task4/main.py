import os
import openai
from dotenv import load_dotenv
from modules.quiz_game import MillionaireGame
from modules import interface


load_dotenv()

openai.api_type = "azure"
openai.api_key = os.getenv("AZURE_OPENAI_KEY")
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_version = "2024-02-15-preview"
deployment = os.getenv("AZURE_DEPLOYMENT_NAME")

def load_prompt():
    with open("prompts/best.txt", "r", encoding="utf-8") as f:
        return f.read()

def run():
    print("Welcome to the Millionaire Quiz Game!\nLet's play!\n")

    game = MillionaireGame(deployment, load_prompt())

    while True:
        reply = game.ask_gpt()
        interface.display(reply)

        action = game.process_reply(reply)

        if action == "ask_name":
            user_input = interface.ask_name()
        elif action == "ask_answer":
            user_input = interface.ask_answer()
        elif action == "ask_start":
            user_input = interface.ask_start()
        elif action == "ask_restart":
            user_input = interface.ask_restart()
            if user_input == "no":
                print("Exiting the game. Thanks for playing!")
                break
            elif user_input == "yes":
                game.reset_game()
                continue
            else:
                print("Please answer 'yes' or 'no'.")
                continue
        else:
            user_input = interface.ask_generic()

        game.submit_user_input(user_input)

if __name__ == "__main__":
    run()
