import subprocess
import re
from pwn import *

def parse_question(question):
    # Extract levels and categories using regex
    match = re.match(r"Q ([0-9]+). Can a Subject with level ([A-Za-z]+) and categories \{([A-Z, ]*)\} (read|write) an Object with level ([A-Za-z]+) and categories \{([A-Z, ]*)\}\?\n", question)
    if match:
        question = int(match.group(1))
        subject_security_level = match.group(2)
        if match.group(3) == "":
            subject_categories = ""
        else:
            subject_categories = match.group(3).split(', ')
        action = match.group(4)
        object_security_level = match.group(5)
        if match.group(6) == "":
            object_categories = ""
        else:
            object_categories = match.group(6).split(', ')

        return question, subject_security_level, subject_categories, action, object_security_level, object_categories

    return None

def can_access(security_levels, subject_security_level, subject_categories, action, object_security_level, object_categories):
    
    if action == 'write':
        # Check if subject has a lower level than object.
        if security_levels.index(subject_security_level) > security_levels.index(object_security_level):
            return False
        
        # Check if object has all subject's categories.
        for subject_category in subject_categories:
            if subject_category not in object_categories:
                return False

    elif action == 'read':
        # Check if object has a higher level than subject.
        if security_levels.index(subject_security_level) < security_levels.index(object_security_level):
            return False

        # Check if subject has all object's categories.
        for object_category in object_categories:
            if object_category not in subject_categories:
                return False
    
    return True

def main():
    # ANSI escape code for green text.
    GREEN = '\033[92m'
    RESET = '\033[0m'

    # ANSI escape code for red text.
    RED = '\033[91m'
    RESET = '\033[0m'

    # Start the challenge process.
    print("\nStarting challenge process ...")

    try:
        # Open the challenge program.
        process = subprocess.Popen(
            ['/challenge/run'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            encoding="utf-8",
        )

    except Exception as error:
        print(f"{RED}[-] Failed to start the challenge process: {error}{RESET}")
        print(f"{RED}[-] Aborting ...{RESET}\n")
        exit(1)

    # Continue with the rest of the code
    print(f"{GREEN}[+] Challenge process started successfully.{RESET}\n")
    counter = 1

    print("Getting levels name ...")
    level_counter = 1
    security_levels = []
    
    while True:
        line = process.stdout.readline()

        if line.endswith("sensitive):\n"):
            while level_counter <= 40:
                security_levels.append(process.stdout.readline().strip())
                level_counter = level_counter + 1 

            break
    
    if not security_levels:
        print(f"{RED}[-] Failed to get the security levels{RESET}")
        print(f"{RED}[-] Aborting ...{RESET}\n")
        exit(1)

    print(f"{GREEN}[+] Levels name stored successfully.{RESET}\n")

    # Define the level hierarchy.
    # I corrected the bug of reversing.
    security_levels.reverse()

    question_counter = 1

    print("Getting questions ...")
    while question_counter <= 129:
        
        if question_counter == 129:
            flag = process.stdout.read()
            break
        
        question = process.stdout.readline()

        if not question.startswith("Q "):
            continue
        
        print(question.strip())
        parsed_question = parse_question(question)

        if not parsed_question:
            print(f"Failed to parse the question")
            print("Aborting ...\n")
            exit(1)
        
        question_number, subject_security_level, subject_categories, action, object_security_level, object_categories = parsed_question

        if can_access(security_levels, subject_security_level, subject_categories, action, object_security_level, object_categories):
            print(f"{GREEN}{repr('Yes')}{RESET}")
            process.stdin.write("Yes\n")
            process.stdin.flush()

        else:
            print(f"{GREEN}{repr('No')}{RESET}")
            process.stdin.write("No\n")
            process.stdin.flush()

        question_counter = question_counter + 1
    
    print(f"{flag}")

if __name__ == "__main__":
    main()
