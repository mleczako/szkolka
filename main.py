import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_type = "azure"
openai.api_key = os.getenv("AZURE_OPENAI_KEY")
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_version = "2024-02-15-preview"
deployment = os.getenv("AZURE_DEPLOYMENT_NAME")

prompts = [
    "Wytłumacz teorię względności w prostych słowach.",
    "Podaj 3 pomysły na obiad z makaronem.",
    "Jak działa algorytm wyszukiwania binarnego?"
]

os.makedirs("logs", exist_ok=True)

usage_data = []

for prompt in prompts:
    response = openai.ChatCompletion.create(
        engine=deployment,
        messages=[{"role": "user", "content": prompt}],
    )
    reply = response["choices"][0]["message"]["content"]
    tokens_in = response["usage"]["prompt_tokens"]
    tokens_out = response["usage"]["completion_tokens"]
    total = response["usage"]["total_tokens"]

    input_cost = tokens_in * 0.000005
    output_cost = tokens_out * 0.000015
    cost = input_cost + output_cost

    usage_data.append({
        "prompt": prompt,
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "cost": cost,
    })

    print(f"\nPrompt: {prompt}")
    print(f"GPT-4o Response:\n{reply}")


with open("logs/usage.md", "w", encoding="utf-8") as f:
    f.write("# GPT-4o Usage Report\n\n")
    f.write("| Prompt | Tokens In | Tokens Out | Cost ($) |\n")
    f.write("|--------|------------|-------------|----------|\n")
    for row in usage_data:
        f.write(f"| {row['prompt']} | {row['tokens_in']} | {row['tokens_out']} | {row['cost']:.6f} |\n")

    most_efficient = min(usage_data, key=lambda x: x["cost"])
    f.write("\n**Most cost-efficient prompt:**\n")
    f.write(f"\n> {most_efficient['prompt']}\n")
    f.write(f"\nIt only cost **${most_efficient['cost']:.6f}**\n")
