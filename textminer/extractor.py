import re

phones = ['(\([0-9]{3}\))?[\s-]?([0-9]{3})[\s-]?([0-9])']

def phone_numbers(text):
    return re.findall(r'\([0-9]{3}\)\s[0-9]{3}-[0-9]{4}', text)

def emails(text):
    return re.findall(r'[-_A-Za-z\.]+@[-A-Za-z\.]+', text)
