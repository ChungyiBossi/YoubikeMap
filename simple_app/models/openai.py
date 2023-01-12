from flask import current_app
import openai


def question_and_answer(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"I am a highly intelligent question answering bot. If you ask me a question that is rooted in truth, I will give you the answer in Chinese. If you ask me a question that is nonsense, trickery, or has no clear answer, I will respond with \"Unknown\".\n\nQ: What is human life expectancy in the United States?\nA: Human life expectancy in the United States is 78 years.\n\nQ: Who was president of the United States in 1955?\nA: Dwight D. Eisenhower was president of the United States in 1955.\n\n{prompt}\nA:",
        temperature=0,
        max_tokens=300,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["\n"]
    )

    return response['choices'][0]['text']
