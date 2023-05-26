from django import template
from news.templatetags.censored_words import BLACKLIST

register = template.Library()


@register.filter()
def censor(value):
    if not isinstance(value, str):
        raise ValueError("Filter *censor* only operates with str type, not", type(value))

    # Censores words taken from BLACKLIST changing letters to '*', leaving the first letter
    # Also unsesitive to register
    # Examples: rump = r***, Rump = R***, rUmP = r***
    text = value.lower() # using extra variable to keep original register... original
    for word in BLACKLIST:
        i = 0
        while i < 100:
            i += 1
            cursor = text.find(word) # if none found, returns -1, else - returns the position of first character
            if cursor != -1:
                censored_word = "*" * (len(word) - 1) # asterisks without first letter
                # a way to change part of a string by using position
                value = censored_word.join([value[:cursor + 1], value[cursor + len(word):]])
                text = value.lower()
            else:
                break
    return value