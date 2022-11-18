# String containing every character used in the numbering
# system in their relative value positions.
numeral_string = "0123456789ABCDEFGHIJKLMNPQRSTUVWXYZ"


def translate_integer_to_bptid(number):
    """
    Translate an integer into the Bonanza numbering system (bptid/bpt_id)
    :type number: int
    :rtype str
    :param number: integer to be translated
    :return: string representation in the new system
    """
    # Set the number system's base using the length of the string
    # containing of all the characters in the system (*in the order
    # of value*).
    base_size = len(numeral_string)
    number_string = ""
    while number:
        # Add to the string the character at the index of the modulo of dividing the
        # passed number by the base, reset the number to the floor division value,
        # and repeat until there are no modulos left to conquer.
        number_string += numeral_string[number % base_size]
        number //= base_size
    # Reverse the resulting string to get the bptid or
    # '0' if there's nothing in the string.
    return number_string[::-1] or "0"


def translate_bptid_to_integer(bpt_id):
    """
    Translates a Bonanza number into its integer equivalent
    :type bpt_id: str
    :rtype int
    :param bpt_id: Bonanza alphanumeric string
    :return: integer equivalent of Bonanza value
    """
    # Base size = total number of characters in the string
    base_size = len(numeral_string)
    total = 0
    power = 1
    for letter in bpt_id[::-1]:
        # Cycle through the passed string in reverse to assure
        # the correct power is used while multiplying. Find the
        # letter's index value, multiply it by the base power
        # associated with the current slot, and add the result to
        # the total. Raise the base power to the next order of
        # magnitude.
        index = numeral_string.find(letter)
        total += index * power
        power *= base_size
    return total
