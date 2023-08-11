#!/usr/bin/env python
# coding: utf-8

# In[1]:


def replace_chars_with_colon(input_string):
    # Define the characters to replace with a colon
    chars_to_replace = [' ', ',', '.']
    replacement = ':'

    # Replace characters in the input string
    for char in chars_to_replace:
        input_string = input_string.replace(char, replacement)

    return input_string

# Test the function
if __name__ == "__main__":
    input_string = input("Enter a string: ")
    result = replace_chars_with_colon(input_string)
    print("Result:", result)


# In[2]:


import re

def find_words_starting_with_a_or_e(input_string):
    # Define the regular expression pattern to find words starting with 'a' or 'e'
    pattern = r'\b[aeAE]\w*\b'
    
    # Find all matches using the pattern
    matches = re.findall(pattern, input_string)
    
    return matches

# Test the function
if __name__ == "__main__":
    input_string = input("Enter a string: ")
    result = find_words_starting_with_a_or_e(input_string)
    print("Words starting with 'a' or 'e':", result)


# In[3]:


import re

def find_long_words(input_string):
    # Compile the regular expression pattern to match words at least 4 characters long
    pattern = re.compile(r'\b\w{4,}\b')
    
    # Find all matches using the compiled pattern
    matches = pattern.findall(input_string)
    
    return matches

# Test the function
if __name__ == "__main__":
    input_string = input("Enter a string: ")
    result = find_long_words(input_string)
    print("Words at least 4 characters long:", result)


# In[4]:


import re

def find_words_with_length(input_string, min_length, max_length):
    # Compile the regular expression pattern to match words of specified length range
    pattern = re.compile(r'\b\w{' + str(min_length) + ',' + str(max_length) + r'}\b')
    
    # Find all matches using the compiled pattern
    matches = pattern.findall(input_string)
    
    return matches

# Test the function
if __name__ == "__main__":
    input_string = input("Enter a string: ")
    min_length = 3
    max_length = 5
    result = find_words_with_length(input_string, min_length, max_length)
    print(f"Words with {min_length}-{max_length} characters:", result)


# In[11]:


import re

def remove_parentheses(strings_list):
    # Question 5- Create a function in Python to remove the parenthesis in a list of strings.The use of the re.compile() method is mandatory.
    pattern = re.compile(r'\(|\)')

    # Remove parentheses from each string in the list
    sanitized_list = [pattern.sub('', string) for string in strings_list]

    return sanitized_list

# Test the function
if __name__ == "__main__":
    input_list = ["example (.com)", "hr@fliprobo (.com)", "github (.com)", "Hello (Data Science World)", "Data (Scientist)"]
    result = remove_parentheses(input_list)
    print("List with parentheses removed:", result)


# In[15]:


import re

def split_uppercase(string):
    pattern = r'(?=[A-Z])'
    uppercase_parts = re.split(pattern, string)
    uppercase_parts = [part for part in uppercase_parts if part != '']
    return uppercase_parts

if __name__ == "__main__":
    input_string = "ImportanceOfRegularExpressionsInPython"
    result = split_uppercase(input_string)
    print("Uppercase parts:", result)


# In[17]:


import re

def insert_spaces_between_numbers_and_words(input_string):
    pattern = r'(\d)([A-Za-z]+)'
    modified_string = re.sub(pattern, r'\1 \2', input_string)
    return modified_string

# Test the function
if __name__ == "__main__":
    input_string = "RegularExpression1IsAn2ImportantTopic3InPython"
    result = insert_spaces_between_numbers_and_words(input_string)
    print("Modified string:", result)



# In[19]:


import re

def insert_spaces_between_caps_and_numbers(input_string):
    pattern = r'([A-Z\d])([a-z]+)'
    modified_string = re.sub(pattern, r'\1 \2', input_string)
    return modified_string

# Test the function
if __name__ == "__main__":
    input_string = "RegularExpression1IsAn2ImportantTopic3InPython"
    result = insert_spaces_between_caps_and_numbers(input_string)
    print("Modified string:", result)

    


# In[21]:


import os


# In[22]:


os.getcwd


# In[23]:


'c:\\users\\text'


# In[30]:


os.chdir('C:\\Users\\text\\Desktop')


# In[20]:


import re

def extract_email_addresses(text):
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    email_addresses = re.findall(pattern, text, re.IGNORECASE)
    return email_addresses

def process_file(input_file):
    with open(input_file, 'r') as file:
        content = file.read()
        
    extracted_emails = extract_email_addresses(content)
    
    if extracted_emails:
        print("Extracted email addresses:")
        for email in extracted_emails:
            print(email)
    else:
        print("No email addresses found in the text.")

if __name__ == "__main__":
    input_file_name = "text.txt"   # Replace with your input file name
    
    process_file(input_file_name)


# In[31]:


import re

def is_valid_string(input_string):
    pattern = r'^[A-Za-z0-9_]+$'
    return re.match(pattern, input_string) is not None

if __name__ == "__main__":
    input_string = input("Enter a string: ")
    if is_valid_string(input_string):
        print("The string is valid.")
    else:
        print("The string is not valid.")


# In[32]:


def starts_with_number(input_string, number):
    return input_string.startswith(str(number))

if __name__ == "__main__":
    input_string = input("Enter a string: ")
    specific_number = 42  # Replace with the specific number you want to check
    
    if starts_with_number(input_string, specific_number):
        print("The string starts with the specific number.")
    else:
        print("The string does not start with the specific number.")


# In[33]:


def remove_leading_zeros(ip_address):
    components = ip_address.split('.')
    normalized_components = [str(int(component)) for component in components]
    normalized_ip = '.'.join(normalized_components)
    return normalized_ip

if __name__ == "__main__":
    ip_address = input("Enter an IP address: ")
    normalized_ip = remove_leading_zeros(ip_address)
    print("IP address without leading zeros:", normalized_ip)


# In[34]:


import re

def extract_dates_from_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    pattern = r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}\b'
    dates = re.findall(pattern, content, re.IGNORECASE)
    return dates

if __name__ == "__main__":
    file_path = "dates.txt"  # Replace with your file path
    
    extracted_dates = extract_dates_from_file(file_path)
    if extracted_dates:
        print("Extracted dates:")
        for date in extracted_dates:
            print(date)
    else:
        print("No valid dates found in the text file.")


# In[36]:


import re

def search_strings_with_regex(text, literals):
    pattern = '|'.join(re.escape(literal) for literal in literals)
    matches = re.findall(pattern, text, re.IGNORECASE)
    return matches

if __name__ == "__main__":
    main_string = "The quick brown fox jumps over the lazy dog."
    search_literals = ["sample", "literals", "search"]
    
    found_strings = search_strings_with_regex(main_string, search_literals)
    
    if found_strings:
        print("Found strings:")
        for found_string in found_strings:
            print(found_string)
    else:
        print("No matches found.")


# In[38]:


import re

def search_strings_with_positions_and_regex(text, literals):
    pattern = '|'.join(re.escape(literal) for literal in literals)
    matches = re.finditer(pattern, text, re.IGNORECASE)
    found_strings = [(match.group(), match.start()) for match in matches]
    return found_strings

if __name__ == "__main__":
    main_string = "The quick brown fox jumps over the lazy dog."
    search_literals = ["dog", "fox"]
    
    found_strings = search_strings_with_positions_and_regex(main_string, search_literals)
    
    if found_strings:
        print("Found strings and their positions:")
        for found_string, position in found_strings:
            print(f"'{found_string}' found at position {position}")
    else:
        print("No matches found.")

        


# In[39]:


def find_substrings(input_string):
    substrings = [input_string[i:j] for i in range(len(input_string)) for j in range(i + 1, len(input_string) + 1)]
    return substrings

if __name__ == "__main__":
    input_string = input("Enter a string: ")
    substrings = find_substrings(input_string)
    
    print("Found substrings:")
    for substring in substrings:
        print(substring)


# In[40]:


def find_substring_occurrences(input_string, substring):
    occurrences = []
    start = 0
    while start < len(input_string):
        position = input_string.find(substring, start)
        if position == -1:
            break
        occurrences.append((substring, position))
        start = position + 1
    return occurrences

if __name__ == "__main__":
    input_string = input("Enter a string: ")
    target_substring = input("Enter the substring to find: ")
    
    occurrences = find_substring_occurrences(input_string, target_substring)
    
    if occurrences:
        print(f"Occurrences of '{target_substring}':")
        for substring, position in occurrences:
            print(f"'{substring}' found at position {position}")
    else:
        print(f"No occurrences of '{target_substring}' found.")


# In[41]:


from datetime import datetime

def convert_date_format(input_date):
    # Parse the input date in yyyy-mm-dd format
    date_object = datetime.strptime(input_date, '%Y-%m-%d')
    
    # Convert the date to dd-mm-yyyy format
    formatted_date = date_object.strftime('%d-%m-%Y')
    
    return formatted_date

if __name__ == "__main__":
    input_date = input("Enter a date in yyyy-mm-dd format: ")
    
    try:
        converted_date = convert_date_format(input_date)
        print("Converted date:", converted_date)
    except ValueError:
        print("Invalid date format. Please use yyyy-mm-dd format.")


# In[42]:


import re

def find_decimal_numbers(input_string):
    pattern = re.compile(r'\b\d+\.\d{1,2}\b')
    decimal_numbers = pattern.findall(input_string)
    return decimal_numbers

if __name__ == "__main__":
    input_string = input("Enter a string: ")
    decimal_numbers = find_decimal_numbers(input_string)
    
    if decimal_numbers:
        print("Decimal numbers with precision of 1 or 2:")
        for number in decimal_numbers:
            print(number)
    else:
        print("No decimal numbers with precision of 1 or 2 found.")


# In[43]:


def separate_numbers_and_positions(input_string):
    numbers = []
    positions = []
    
    for idx, char in enumerate(input_string):
        if char.isdigit():
            numbers.append(char)
            positions.append(idx)
    
    return numbers, positions

if __name__ == "__main__":
    input_string = input("Enter a string: ")
    numbers, positions = separate_numbers_and_positions(input_string)
    
    if numbers:
        print("Numbers and their positions:")
        for num, pos in zip(numbers, positions):
            print(f"Number: {num}, Position: {pos}")
    else:
        print("No numbers found in the string.")


# In[61]:


import re

def extract_max_numeric_value(input_string):
    numeric_values = re.findall(r'\d+(\.\d+)?', input_string)
    
    if numeric_values:
        max_value = max(map(float, numeric_values))
        return max_value
    else:
        return None

if __name__ == "__main__":
    input_string = input("Enter a string: ")
    max_numeric_value = extract_max_numeric_value(input_string)
    
    if max_numeric_value is not None:
        print("Maximum numeric value:", max_numeric_value)
    else:
        print("No numeric values found in the string.")


# In[62]:


import re

def insert_spaces_between_capital_words(input_string):
    pattern = r'([A-Z][a-z]*)'
    modified_string = re.sub(pattern, r' \1', input_string)
    return modified_string.strip()

if __name__ == "__main__":
    input_string = input("Enter a string: ")
    modified_string = insert_spaces_between_capital_words(input_string)
    print("Modified string:", modified_string)


# In[63]:


import re

def find_uppercase_followed_by_lowercase(input_string):
    pattern = r'[A-Z][a-z]+'
    matches = re.findall(pattern, input_string)
    return matches

if __name__ == "__main__":
    input_string = input("Enter a string: ")
    result = find_uppercase_followed_by_lowercase(input_string)
    
    if result:
        print("Sequences of one uppercase letter followed by lowercase letters:")
        for match in result:
            print(match)
    else:
        print("No matches found.")


# In[65]:


import re

def remove_continuous_duplicates(sentence):
    pattern = r'\b(\w+)(\s+\1)+\b'
    modified_sentence = re.sub(pattern, r'\1', sentence)
    return modified_sentence

if __name__ == "__main__":
    input_sentence = input("Enter a sentence: ")
    modified_sentence = remove_continuous_duplicates(input_sentence)
    print("Modified sentence:", modified_sentence)


# In[66]:


import re

def is_valid_string(input_string):
    pattern = r'^.*[A-Za-z0-9]$'
    return re.match(pattern, input_string) is not None

if __name__ == "__main__":
    input_string = input("Enter a string: ")
    
    if is_valid_string(input_string):
        print("The string is valid.")
    else:
        print("The string is not valid.")


# In[67]:


import re

def extract_hashtags(input_string):
    pattern = r'#\w+'
    hashtags = re.findall(pattern, input_string)
    return hashtags

if __name__ == "__main__":
    input_string = input("Enter a string: ")
    hashtags = extract_hashtags(input_string)
    
    if hashtags:
        print("Extracted hashtags:")
        for tag in hashtags:
            print(tag)
    else:
        print("No hashtags found in the string.")


# In[71]:


get_ipython().run_line_magic('cd', 'C:\\Users\\HP\\Desktop')
    


# In[75]:


get_ipython().run_line_magic('pwd', '')


# In[77]:


import re

def extract_dates_from_file(C:\Users\HP\Desktop\text.txt):
    with open(C:\Users\HP\Desktop\text.txt, 'r') as file:
        content = file.read()

    pattern = r'\b\d{1,2}/\d{1,2}/\d{4}\b'  # Assuming date format: dd/mm/yyyy
    dates = re.findall(pattern, content)
    return dates

if __name__ == "__main__":
    file_path = "C:\Users\HP\Desktop\text.txt"  # Replace with your file path
    
    extracted_dates = extract_dates_from_file(C:\Users\HP\Desktop\text.txt)
    if extracted_dates:
        print("Extracted dates:")
        for date in extracted_dates:
            print(date)
    else:
        print("No dates found in the text file.")


# In[78]:


import re

def remove_words_by_length(input_string):
    pattern = re.compile(r'\b\w{2,4}\b')
    modified_string = pattern.sub('', input_string)
    return modified_string

if __name__ == "__main__":
    input_string = input("Enter a string: ")
    modified_string = remove_words_by_length(input_string)
    print("Modified string:", modified_string)


# In[ ]:




