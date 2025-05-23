import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_type = "azure"
openai.api_key = os.getenv("AZURE_OPENAI_KEY")
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_version = "2024-02-15-preview"
deployment = os.getenv("AZURE_DEPLOYMENT_NAME")


def run():
    print("Welcome to the Millionaire Quiz Game!")
    print("Let's play!\n")

    with open("prompts/best.txt", "r", encoding="utf-8") as f:
        system_prompt = f.read()

    player_name = None 
    asked_questions = [] 
    initial_system_prompt = system_prompt
    messages = [{"role": "system", "content": system_prompt}]

    while True:
        response = openai.ChatCompletion.create(
            engine=deployment,
            messages=messages
        )

        reply = response["choices"][0]["message"]["content"]

        if "question" in reply.lower():
            asked_questions.append(reply.strip())

        print(f"\nGPT-4o says:\n{reply}\n")

        messages.append({"role": "assistant", "content": reply})

        lower_reply = reply.lower()


        if "your name" in lower_reply and not player_name:
            user_input = input("Your name: ").strip()
            player_name = user_input
            messages.append({"role": "user", "content": user_input})
            continue

        elif "would you like to play again" in lower_reply:
            user_input = input("Play again? (yes/no): ").strip().lower()
            if user_input == "no":
                print("\nExiting the game. Thanks for playing!")
                exit(0)
            elif user_input == "yes":
                excluded_qs = "\n".join(asked_questions)
                system_prompt_with_name = (
                    initial_system_prompt
                    + f"\nThe player's name is {player_name}. Continue using it."
                    + f"\nDo not reuse any of the following previously asked questions:\n{excluded_qs}"
                )
                messages = [{"role": "system", "content": system_prompt_with_name}]
                continue
            else:
                print("Please answer 'yes' or 'no'.")
                continue

        elif ("say yes" in lower_reply or "are you ready" in lower_reply) and not any(
            opt in lower_reply for opt in ["a)", "a.", "b)", "b.", "c)", "c.", "d)", "d."]
        ):
            user_input = input("Say 'yes' to begin: ").strip().lower()
            messages.append({"role": "user", "content": user_input})
            continue

        elif any(opt in lower_reply for opt in ["a)", "a.", "b)", "b.", "c)", "c.", "d)", "d."]):
            user_input = input("Your answer (A/B/C/D): ").strip().upper()
            messages.append({"role": "user", "content": user_input})
            continue

        else:
            user_input = input("📝 Your input: ").strip()
            messages.append({"role": "user", "content": user_input})


if __name__ == "__main__":
    run()
