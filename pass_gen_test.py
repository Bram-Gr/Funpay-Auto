import random
import string


def pass_gen(length=12):
    # Define the character sets for password generation
    letters = string.ascii_letters  # a-z, A-Z
    digits = string.digits          # 0-9
    special_chars = string.punctuation  # Special characters like !, @, #

    # Ensure the password contains at least one character from each category
    all_characters = letters + digits + special_chars
    
    # Generate a random password
    password = [
        random.choice(letters),
        random.choice(digits),
        random.choice(special_chars)
    ]
    
    # Fill the rest of the password with random characters from all categories
    password += random.choices(all_characters, k=length - len(password))
    
    # Shuffle the result to prevent predictable patterns
    random.shuffle(password)
    
    return ''.join(password)

pass_holder = pass_gen(12)
pass2_holder = pass_holder
print(pass_holder,pass2_holder)