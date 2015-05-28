import re
import textminer.validator as v

months = {
          'January':1,
          'Jan':1,
          'February':2,
          'Feb':2,
          'March':3,
          'April':4,
          'May':5,
          'June':6,
          'July':7,
          'August':8,
          'Aug':8,
          'September':9,
          'Sept':9,
          'October':10,
          'Oct':10,
          'November':11,
          'Nov':11,
          'December':12,
          'Dec':12
}
days_month= {
    1:31,
    2:28,
    3:31,
    4:30,
    5:31,
    6:30,
    7:31,
    8:31,
    9:30,
    10:31,
    11:30,
    12:31
}

def words(text):
    wrds = re.findall(r'\b\w*[A-Za-z-_]+\w*\b', text)
    if wrds:
        return wrds
    return None


def phone_number(text):
    result = re.match(r'\(?([0-9]{3})\)?[\s\.-]?([0-9]{3})[\.-]?([0-9]{4})', text)
    if result:
        result = result.groups()
        return {'area_code': result[0], 'number': result[1] + '-' + result[2]}
    return None


def money(text):

    result = re.match(r"""
                       ^(\${1})(\d{1,3},)((?:\d{3},)*)(\d{3})(\.\d{2})?$|
                       ^(\${1})([0-9]+)(\.\d{2})?$
                       """, text, flags=re.X)

    if result:
        result = "".join(item for item in result.groups() if item)
        result = re.sub(",", "", result)

        return {'amount': float(result[1:]), 'currency': result[0]}
    return None


def zipcode(text):
    result = re.match(r'([0-9]{5})-([0-9]+)|([0-9]{5})\b', text)

    if result:
        result = result.groups()

        if result[0]:
            if result[1] and len(result[1]) == 4:
                return {'zip': result[0], 'plus4': result[1]}

            return None
        else:
            return {'zip': result[2], 'plus4': None}

    return None


def date(text):
    regs = ['^(?P<month>[0-9]{1,2})[/-](?P<day>[0-9]{1,2})[/-](?P<year>[0-9]{4})$',
            '^(?P<year>[0-9]{4})[/-](?P<month>[0-9]{1,2})[/-](?P<day>[0-9]{1,2})$',
            '^(?P<year>[0-9]{4})\s+(?P<month>[A-Za-z]+)\.?\s+(?P<day>[0-9]{2})$',
            '^(?P<month>[A-Za-z]+)\.?\s+(?P<day>[0-9]{1,2}),\s+(?P<year>[0-9]{4})$',
            ]

    result = [re.match(r'{}'.format(item), text) for item in regs]
    result = [item for item in result if item]

    if result:
        result = result[0].groupdict()

        if result['month'] in months.keys():
            result['month'] = months[result['month']]

        result = {item: int(value) for item, value in result.items() if value}

        if result['day'] > days_month[result['month']]:
            return None

        return result

    return None


def email(text):
    result = re.match(r'([A-Za-z0-9]+\.?[A-Za-z0-9]+)@([\w]+\.[A-Za-z]+)', text)

    if result:
        result = result.groups()
        return {'local': result[0], 'domain': result[1]}
    return None


def address(text):
    result = re.match(r"""(?P<address>[0-9]+(?:\s\w+\.?)*)[,\s]+
                       (?P<city>\w+\s?(?:\w+)?)[,\s]+(?P<state>[A-Z]{2})[,\s]+
                       (?P<zip>[0-9]+-?(?:[0-9]+)?)""" , text, re.X)

    if result:

        result = result.groupdict()

        if not [item for item, value in result.items() if value == None]:
            if v.zipcode(result['zip']):
                if v.words(result['city']):
                    zip_parts = zipcode(result['zip'])
                    for item, value in zip_parts.items():
                        result[item] = value

                    return result

    return None
