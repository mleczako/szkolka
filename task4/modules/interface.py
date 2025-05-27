import re

def display(text):
    print(f"\nGPT-4o says:\n{text}\n")

def get_input(prompt):
    return input(prompt).strip()

def ask_name():
    return get_input("Your name: ")

def ask_answer():
    raw = input("Your answer (A/B/C/D): ").strip().upper()
    match = re.match(r"([A-D])", raw)
    if match:
        return match.group(1) 
    else:
        print("Invalid answer. Please enter A, B, C or D.")
        return ask_answer()  

def ask_start():
    return get_input("Say 'yes' to begin: ").lower()

def ask_restart():
    return get_input("Play again? (yes/no): ").lower()

def ask_generic():
    return get_input("Your input: ")
