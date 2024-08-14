import os
import random
import pandas as pd
import streamlit as st

# Constants
FILENAME = "random.csv"  # Name of the CSV file to store the random numbers


# Functions
def read_unique_numbers(filename):
    """
    Read the list of unique random numbers from a CSV file.

    :param filename: Name of the file to read from
    :return: List of unique random numbers
    """
    try:
        unique_numbers_df = pd.read_csv(filename)
        return list(unique_numbers_df["Random Number"])
    except FileNotFoundError:
        return []  # Return an empty list if the file does not exist


def generate_unique_random_number(start, end, unique_numbers_list):
    """
    Generate a unique random number within a specified range.

    :param start: Start of the range (inclusive)
    :param end: End of the range (inclusive)
    :param unique_numbers_list: List of already generated unique numbers
    :return: A unique random number not in the unique_numbers_list
    """
    num = random.randint(start, end)
    while num in unique_numbers_list:
        num = random.randint(start, end)  # Regenerate if number is not unique
    return num


def write_unique_numbers(unique_numbers_list, filename):
    """
    Write the list of unique random numbers to a CSV file.

    :param unique_numbers_list: List of unique random numbers
    :param filename: Name of the file to write to
    """
    df = pd.DataFrame({"Random Number": unique_numbers_list})
    df.to_csv(filename, index=False)  # Save to CSV without the index column


def reset_csv_file(filename):
    """
    Reset the CSV file by clearing its contents and adding the header.

    :param filename: Name of the file to reset
    """
    with open(filename, "w") as f:
        f.write("Random Number\n")  # Write header to the file


# Main function
# Create two tabs in the Streamlit app: one for generating numbers and one for displaying them
tab1, tab2 = st.tabs(["Generate", "Numbers"])

# Initialize the CSV file if it doesn't exist
if not os.path.exists(FILENAME):
    reset_csv_file(FILENAME)

# Get the start and end range for random number generation from the user
start_range = tab1.number_input("Start Range", min_value=0, max_value=100, value=20)
end_range = tab1.number_input("End Range", min_value=0, max_value=100, value=50)

# Reset the CSV file if the "Reset" button is pressed
if tab1.button("Reset"):
    reset_csv_file(FILENAME)

# Read the list of unique numbers from the CSV file
unique_numbers_list = read_unique_numbers(FILENAME)

# Calculate the total numbers to be generated in the given range
total_numbers = end_range - start_range + 1
# Get the count of numbers already generated
total_numbers_generated = len(unique_numbers_list)

# Generate a new unique number if not all numbers have been generated
if total_numbers != total_numbers_generated:
    num = generate_unique_random_number(start_range, end_range, unique_numbers_list)
    unique_numbers_list.append(num)
    unique_numbers_list = sorted(unique_numbers_list)  # Sort the list for display
    write_unique_numbers(
        unique_numbers_list, FILENAME
    )  # Save the updated list to the CSV file

    # Display the newly generated number
    tab1.info(f"# {num}")
    tab1.button("Generate")  # Button to trigger another generation (if needed)

# Recalculate the progress after potential generation
total_numbers_generated = len(unique_numbers_list)
progress_percentage = total_numbers_generated / total_numbers

# Display the progress
tab1.success(f"Progress: {total_numbers_generated}/{total_numbers}")

# Show a progress bar based on the current progress percentage
tab1.progress(progress_percentage)

# Display the list of generated numbers in the second tab
tab2.write(unique_numbers_list)
