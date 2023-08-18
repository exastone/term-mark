from InquirerPy import prompt

questions = [
    {
        "type": "list",
        "message": "What's your favourite programming language:",
        "choices": ["Go", "Python", "Rust", "JavaScript"],
    },
]
result = prompt(questions)
fav_lang = result[0]