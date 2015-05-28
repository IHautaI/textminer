import re


def binary(text):
    if re.match(r'^[01]+$', text):
        return True
    return False


def binary_even(text):
    return int(text[-1]) == 0

def hex(text):
    if re.match(r'^[0-9A-F]+$', text):
        return True
    return False

def word(text):
    return re.match(r'.+[A-Za-z]+.+', text) and not re.match(r'.+[^A-Za-z0-9-].+', text)

def words(text, count=0):

    if text:

        text = re.findall(r'\b\w*[A-Za-z-_]+\w*\b', text)

        if not text:
            return False

        notwords = [item for item in text if not word(item)]

        if notwords:
            return False

        if (count != 0 and count == len(text)) or count == 0:
            return True

    return False


def phone_number(text):
    result = re.match(r'\(?([0-9]{3})\)?[\s\.-]?([0-9]{3})[\.-]?([0-9]{4})', text)
    if result:
        return True
    return False

def money(text):
    result = re.match(r"""
                       ^(\${1})(\d{1,3},)((?:\d{3},)*)(\d{3})(\.\d{2})?$|
                       ^(\${1})([0-9]+)(\.\d{2})?$
                       """, text, flags=re.X)

    if result:
        return True
    return False

def zipcode(text):
    result = re.match(r'([0-9]{5})-([0-9]{4})$|([0-9]{5})$', text)

    if result:
        return True
    return False

def email(text):
    result = re.findall(r'([A-Za-z0-9]+\.?[A-Za-z0-9]+)@([\w]+\.[A-Za-z]+)', text)

    if result:
        return True
    return False

def address(text):
    result = re.match(r"""(?P<address>[0-9]+(?:\s\w+\.?)*)[,\s]+
                       (?P<city>\w+\s?(?:\w+)?)[,\s]+(?P<state>[A-Z]{2})[,\s]+
                       (?P<zip>[0-9]+-?(?:[0-9]+)?)""" , text, re.X)

    if result:
        return True
    return False
