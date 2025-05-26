import re
import openai

class MillionaireGame:
    def __init__(self, deployment, system_prompt, player_name=None):
        self.deployment = deployment
        self.system_prompt = system_prompt
        self.initial_prompt = system_prompt
        self.player_name = player_name
        self.asked_questions = []
        self.messages = [{"role": "system", "content": system_prompt}]

    def process_reply(self, reply):
        self.messages.append({"role": "assistant", "content": reply})
        lower = reply.lower()

        if "question" in lower:
            self.asked_questions.append(reply.strip())

        if "your name" in lower and not self.player_name:
            return "ask_name"

        if "would you like to play again" in lower:
            return "ask_restart"

        if any(phrase in lower for phrase in ["say yes", "are you ready"]):
            if not re.search(r"\b[a-d][).]", lower):
                return "ask_start"

        if re.search(r"\b[a-dA-D][).]?", lower):
            return "ask_answer"

        return "generic_input"

    def submit_user_input(self, user_input):
        self.messages.append({"role": "user", "content": user_input})
        if not self.player_name:
            self.player_name = user_input

    def ask_gpt(self):
        response = openai.ChatCompletion.create(
            engine=self.deployment,
            messages=self.messages
        )
        return response["choices"][0]["message"]["content"]

    def reset_game(self):
        excluded_qs = "\n".join(self.asked_questions)
        new_prompt = (
            self.initial_prompt +
            f"\nThe player's name is {self.player_name}. Continue using it." +
            f"\nDo not reuse any of the following previously asked questions:\n{excluded_qs}"
        )
        self.messages = [{"role": "system", "content": new_prompt}]
