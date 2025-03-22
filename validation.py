def get_int(prompt, nullable=False, default=None):
    """
    Prompt user for an integer input UNTIL valid.j
    """
    while True:
        try:
            value = input(f"{prompt}: ").strip()
            if nullable and value == "":
                return None
            return int(value)
        except ValueError:
            if default is not None:
                return default
            print("Invalid input. Please enter a valid integer.")

def get_str(prompt, nullable=False):
    """
    Prompt user for a string input UNTIL valid.
    """
    while True:
        value = input(f"{prompt}: ").strip()
        if nullable and value == "":
            return None
        if not nullable and not value:
            print("Input cannot be empty.")
        else:
            return value

def get_state(prompt, nullable=False):
    """
    Prompt user for a valid 2-letter state abbreviation,
    had to hardcode states
    """
    states = [
        'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
        'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
        'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
        'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
        'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
    ]
    while True:
        value = input(f"{prompt}: ").strip().upper()
        if nullable and value == "":
            return None
        if value not in states:
            print("Invalid input. Please enter a valid 2-letter state abbreviation.")
        else:
            return value

def get_yes_no(prompt):
    """
    Prompt user for a yes/no until one is given.
    """
    while True:
        value = input(f"{prompt}: ").strip().lower()
        if value not in ['y', 'n']:
            print("Invalid input. Please enter 'y' or 'n'.")
        else:
            return value == 'y'

def get_positive_float(prompt, nullable=False):
    """
    prompt for float >= 0, retrying until valid
    """
    while True:
        try:
            value = input(f"{prompt}: ").strip()
            if nullable and value == "":
                return None
            return validate_positive_float(value)
        except ValueError as e:
            print(e)

def get_float_in_range(prompt, min_val, max_val, default=None):
    """
    get float in range [min_val, max_val], retrying until valid
    """
    while True:
        try:
            value = input(f"{prompt}: ").strip()
            if value == "" and default is not None:
                return default
            f_val = float(value)
            if not (min_val <= f_val <= max_val):
                raise ValueError(f"Value must be between {min_val} and {max_val}.")
            return f_val
        except ValueError as e:
            print(e)

def get_choice(prompt, valid_choices):
    """
    Prompt user for a choice from a list of valid choices.
    """
    while True:
        try:
            value = input(f"{prompt}: ").strip()
            int_val = int(value)
            if int_val not in valid_choices:
                raise ValueError(f"Value must be one of {valid_choices}.")
            return int_val
        except ValueError as e:
            print(e)

def validate_positive_float(value):
    """
    Validate that the input is a positive float.
    """
    try:
        f_val = float(value)
        if f_val < 0:
            raise ValueError("Value must be a positive number.")
        return f_val
    except ValueError:
        raise ValueError("Input must be a valid number.")