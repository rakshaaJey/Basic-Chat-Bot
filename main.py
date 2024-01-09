import json
from difflib import get_close_matches

KNOWLEDGE_BASE_FILE = 'Basic-Chat-Bot\knowledge_base.json'
CUT_OFF = 0.8

def load_knowledge_base(file_path: str) -> dict:
    ''' load_knowledge_base(file_path) opens the json file containing all past interactions the user had with the bot

    @param file_path is a string representing the path to the json file
    '''
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

def save_knowledge_base(file_path: str, data: dict):
    ''' save_knowledge_base(file_path, data) saves the learned data to the json file

    @param file_path is a string representing the path to the json file
    @param data a dictionary containing the new data
    '''
    with open(file_path, 'w') as file:
        json.dump(data, file, indent = 2)

def find_best_match(user_question: str, questions: list[str]) -> str | None:
    ''' find_best_match(user_question, questions) returns the closest looking question to the question the user gave
    
    @param user_question is the question the user asked
    @param questions is the list of questions the chat bot already knows how to answer
    '''
    matches: list = get_close_matches(user_question, questions, n = 1, cutoff = CUT_OFF)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    ''' get_answer_for_question(question, knowledge_base) returns the answer to the question by looking through a dictionary that contains
    questions and answers
    
    @param question is the question that is being searched for
    @param knowledge_base is a dictionary containing questions and answers
    '''
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]

def chat_bot():
    ''' chat_bot() Allows the user to get answers to their question based on past collected data
    '''
    knowledge_base: dict = load_knowledge_base(KNOWLEDGE_BASE_FILE)

    while True:
        user_input: str = input('You: ')

        if user_input.lower() == 'quit':
            break
        
        best_match: str | None = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])
        if best_match:
            answer: str = get_answer_for_question(best_match, knowledge_base)
            print(f'Bot: {answer}')

            answer_satisfaction: str = input('Are you satisfied with the answer (Y/N): ')
            if(answer_satisfaction.lower() == 'n'):
                new_answer: str = input('What answer are you looking for: ')
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})

        else:
            print('I don\'t know the answer. Can you teach me?')
            new_answer: str = input('Type the answer or "skip" to skip\n')

            if new_answer.lower() != 'skip':
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base(KNOWLEDGE_BASE_FILE, knowledge_base)
                print('Bot: Thank you! I learned a new response.')

if __name__ == '__main__':
    chat_bot()