import subprocess
import re

def parse_question(question):
    # Extract levels and categories using regex
    match = re.match(r"Q ([0-9]+). Can a Subject with level ([A-Z]+) and categories \{([A-Z, ]*)\} (read|write) an Object with level ([A-Z]+) and categories \{([A-Z, ]*)\}\?\n", question)
    if match:
        question = int(match.group(1))
        subject_security_level = match.group(2)
        if match.group(3) == "":
            print("Satisfied_1")
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

def can_access(subject_security_level, subject_categories, action, object_security_level, object_categories):
    
    # Define the level hierarchy.
    security_levels = ["UC", 'C', 'S', "TS"]
    
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
        print(f"Failed to start the challenge process: {error}")
        print("Aborting ...\n")
        exit(1)

    # Continue with the rest of the code.
    print("Challenge process started successfully.\n")
    counter = 1

    while counter <= 65:
        if counter == 65:
            line = process.stdout.read()
            break

        line = process.stdout.readline()

        if not line.startswith("Q "):
            continue
        
        print(line.strip())
        parsed_question = parse_question(line)

        if not parsed_question:
            print(f"Failed to parse the question")
            print("Aborting ...\n")
            exit(1)

        question_number, subject_security_level, subject_categories, action, object_security_level, object_categories = parsed_question

        if can_access(subject_security_level, subject_categories, action, object_security_level, object_categories):
            print("Yes\n")
            process.stdin.write("Yes\n")
        else:
            print("No\n")
            process.stdin.write("No\n")

        process.stdin.flush()
        result = process.stdout.readline()

        counter = counter + 1
    
    print(f"{line}")

if __name__ == "__main__":
    main()
