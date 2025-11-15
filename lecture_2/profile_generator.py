class ProfileGenerator:
    """
    Class for storing user information:
    - name
    - year of birth
    - age
    - life stage
    - list of hobbies
    """

    def __init__(self):
        # Initialization of class attributes
        self.user_name: str = ""  # Username
        self.birth_year_str: str = ""  # Year of birth
        self.current_age: int = 0  # User age
        self.life_stage: str = ""  # Life stage: Child, Teenager, Adult
        self.hobbies: "list[str]" = []  # User's hobby list
        self.user_profile: "dict[str, object]" = {}  # Dictionary for storing complete user information

    def input_name(self) -> None:
        """Requests username with validation."""
        while True:
            # Query the name and remove spaces at the beginning and end
            self.user_name = input("Enter your full name: ").strip().title()
            # Check for an empty string and that the name consists of letters and spaces
            if not self.user_name or not all(char.isalpha() or char.isspace() for char in self.user_name):
                print("Name cannot be empty and must contain only letters and spaces.")
                continue
            break

    def input_birth_year(self) -> None:
        """Requests the user's year of birth with validation."""
        while True:
            self.birth_year_str = input("Enter your birth year: ").strip()
            # Checks that only numbers and a year are entered in the range from 1900 to 2025
            if self.birth_year_str.isdigit() and 1900 <= int(self.birth_year_str) <= 2025:
                self.current_age = 2025 - int(self.birth_year_str)  # Calculate current age
                break
            else:
                print("Please enter numbers only.")

    def generate_profile(self, age: int) -> str:
        """Determines life stage based on age."""
        if 0 <= age <= 12:
            return "Child"
        elif 13 <= age <= 19:
            return "Teenager"
        else:
            return "Adult"

    def input_hobbies(self) -> None:
        """Requests the user's hobbies and saves them to a list."""
        while True:
            hobby = input("Enter a favourite hobby or type 'stop' to finish: ").strip().capitalize()
            if hobby.lower() == "stop":
                break
            if hobby:  # Check that the entered string is not empty
                self.hobbies.append(hobby)
            else:
                print("Hobby cannot be empty. Try again.")

    def build_user_profile(self) -> None:
        """Creates a dictionary with complete information about the user."""
        self.life_stage = self.generate_profile(self.current_age)
        self.user_profile = {
            'name': self.user_name,
            'age': self.current_age,
            'stage': self.life_stage,
            'hobbies': self.hobbies
        }

    def print_profile(self) -> None:
        """Prints all user information in a readable format."""
        print(f"---\nProfile Summary:\nName: {self.user_profile['name']}\nAge: {self.user_profile['age']}\n"
              f"Life Stage: {self.user_profile['stage']}")
        if self.user_profile['hobbies']:  # Checking for a hobby
            print(f"Favourite Hobbies ({len(self.user_profile['hobbies'])})")
            for hobby in self.user_profile['hobbies']:
                print(f"- {hobby}")
            print("---")
        else:
            print("You didn't mention any hobbies.\n---")


def main():
    user = ProfileGenerator()
    user.input_name()
    user.input_birth_year()
    user.input_hobbies()
    user.build_user_profile()
    user.print_profile()


if __name__ == "__main__":
    main()
