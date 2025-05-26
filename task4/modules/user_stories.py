import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_type = "azure"
openai.api_key = os.getenv("AZURE_OPENAI_KEY")
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_version = "2024-02-15-preview"
deployment = os.getenv("AZURE_DEPLOYMENT_NAME")

def make_story():

    os.makedirs("backlog", exist_ok=True)

    with open("prompts/story_prompt.txt", "r", encoding="utf-8") as f:
        base = f.read()

    with open("prompts/best.txt", "r", encoding="utf-8") as f:
        game_description = f.read()

    full_prompt = base + "\n\n" + game_description

    response = openai.ChatCompletion.create(
        engine=deployment,
        messages=[{"role": "user", "content": full_prompt}],
    )

    with open("backlog/sprint1.md", "w", encoding="utf-8") as f:
        content = response["choices"][0]["message"]["content"]
        f.write(content)


if __name__ == "__main__":
    make_story()
