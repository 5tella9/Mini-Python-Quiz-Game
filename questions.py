EASY_QUESTIONS = [
    {
        "question": "What is the output of this code?\n\nprint(2 + 3)",
        "options": ["4", "5", "6", "Error"],
        "answer": "5"
    },
    {
        "question": "Which symbol is used for multiplication in Python?",
        "options": ["x", "*", "#", "%"],
        "answer": "*"
    },
    {
        "question": "Which function is used to show output in Python?",
        "options": ["input()", "print()", "show()", "display()"],
        "answer": "print()"
    }
]


MEDIUM_QUESTIONS = [
    {
        "question": "What is the output?\n\nnumbers = [1, 2, 3]\nprint(len(numbers))",
        "options": ["2", "3", "4", "Error"],
        "answer": "3"
    },
    {
        "question": "Which data type stores key-value pairs?",
        "options": ["List", "Tuple", "Dictionary", "Set"],
        "answer": "Dictionary"
    },
    {
        "question": "What does `range(3)` produce in a loop?",
        "options": ["1, 2, 3", "0, 1, 2", "0, 1, 2, 3", "3 only"],
        "answer": "0, 1, 2"
    }
]


HARD_QUESTIONS = [
    {
        "question": "What is the output?\n\ntry:\n    print(10 / 0)\nexcept ZeroDivisionError:\n    print('Error')",
        "options": ["10", "0", "Error", "ZeroDivisionError"],
        "answer": "Error"
    },
    {
        "question": "What does `finally` do in exception handling?",
        "options": [
            "Runs only if there is an error",
            "Runs only if there is no error",
            "Runs no matter what",
            "Stops the program"
        ],
        "answer": "Runs no matter what"
    },
    {
        "question": "What does a decorator usually do?",
        "options": [
            "Deletes a function",
            "Modifies or extends a function",
            "Creates a list",
            "Stops recursion"
        ],
        "answer": "Modifies or extends a function"
    }
]


def get_questions(level):
    if level == "Easy":
        return EASY_QUESTIONS
    elif level == "Medium":
        return MEDIUM_QUESTIONS
    elif level == "Hard":
        return HARD_QUESTIONS
    else:
        return EASY_QUESTIONS