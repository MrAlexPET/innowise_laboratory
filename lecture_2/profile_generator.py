def generate_profile(age: int) -> str:
    """Determines life stage based on age."""
    if 0 <= age <= 12:
        return "Child"
    elif 13 <= age <= 19:
        return "Teenager"
    else:
        return "Adult"


# Request the username and make it look nice
user_name: str = input("Enter your full name: ").strip().title()

# Request the user's year of birth and remove extra spaces
birth_year_str: str = input("Enter your birth year: ").strip()

# Converting the year of birth from str to int
birth_year: int = int(birth_year_str)

# Calculate the current age
current_age: int = 2025 - birth_year

# Create an empty list for hobbies
hobbies: list = []

# Request the user's hobbies and saves them to a list
while True:
    hobby = input("Enter a favourite hobby or type 'stop' to finish: ").strip().capitalize()
    if hobby.lower() == "stop":  # If the user typed 'stop', we exit the loop
        break
    if hobby:  # Check that the entered string is not empty
        hobbies.append(hobby)
    else:
        print("Hobby cannot be empty. Try again.")

# Determining the life stage
life_stage: str = generate_profile(current_age)

# Create a dictionary to store all user data
user_profile = {
    'name': user_name,
    'age': current_age,
    'stage': life_stage,
    'hobbies': hobbies
}

# Print the user's name, age, and life stage in a beautiful format
print(f"---\nProfile Summary:\nName: {user_profile['name']}\nAge: {user_profile['age']}\n"
      f"Life Stage: {user_profile['stage']}")

# Print the user's hobbies in order on a new line
if user_profile['hobbies']:  # Checking for a hobby
    print(f"Favourite Hobbies ({len(user_profile['hobbies'])})")
    for hobby in user_profile['hobbies']:
        print(f"- {hobby}")
    print("---")
else:  # If there is no hobby, print information about it.
    print("You didn't mention any hobbies.\n---")
