# validation.py

def get_int(prompt, nullable=False, default=None):
    """
    Prompt user for an integer input, optionally allowing null.
    """
    value = input(f"{prompt}: ").strip()

    if nullable and value == "":
        return None

    try:
        int_val = int(value)
        return int_val
    except ValueError:
        if default is not None:
            return default
        raise ValueError("Input must be a valid integer.")

def get_str(prompt, nullable=False):
    """
    Prompt user for a string input, optionally allowing null.
    """
    value = input(f"{prompt}: ").strip()

    if nullable and value == "":
        return None

    if not nullable and not value:
        raise ValueError("Input cannot be empty.")
    
    return value


def get_state(prompt, nullable=False):
    """
    Prompt user for a valid 2-letter state abbreviation.
    """
    states = [
        'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
        'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
        'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
        'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
        'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
        ]
    value = input(f"{prompt}: ").strip().upper()
    if nullable and value == "":
        return None
    if value not in states:
        raise ValueError("Input must be a valid 2-letter state abbreviation.")
    
    return value


def get_yes_no(prompt):
    """
    Prompt user for a yes/no confirmation.
    """
    value = input(f"{prompt}: ").strip().lower()

    if value not in ['y', 'n']:
        raise ValueError("Input must be 'y' or 'n'.")
    
    return value == 'y'


def get_positive_float(prompt, nullable=False):
    """
    Prompt user for a positive float, optionally allowing null.
    """
    value = input(f"{prompt}: ").strip()

    if nullable and value == "":
        return None

    return validate_positive_float(value)


def get_float_in_range(prompt, min_val, max_val, default=None):
    """
    Prompt user for a float within a specified range.
    """
    value = input(f"{prompt}: ").strip()

    try:
        f_val = float(value)
        if not (min_val <= f_val <= max_val):
            raise ValueError(f"Value must be between {min_val} and {max_val}.")
        return f_val
    except ValueError:
        if default is not None:
            return default
        raise ValueError("Input must be a valid number.")


def get_choice(prompt, valid_choices):
    """
    Prompt user to select one valid choice from a list.
    """
    value = input(f"{prompt}: ").strip()

    try:
        int_val = int(value)
        if int_val not in valid_choices:
            raise ValueError(f"Value must be one of {valid_choices}.")
        return int_val
    except ValueError:
        raise ValueError("Input must be a valid choice.")


def validate_positive_float(value):
    """
    Validate that a given value is a positive float.
    """
    try:
        f_val = float(value)
        if f_val < 0:
            raise ValueError("Value must be a positive number.")
        return f_val
    except ValueError:
        raise ValueError("Input must be a valid number.")