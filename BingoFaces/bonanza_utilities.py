class BonanzaUtilities:
    numeral_string = "0123456789ABCDEFGHIJKLMNPQRSTUVWXYZ"

    @staticmethod
    def translate_integer_to_bptid(regular_number):
        """
        Translate an integer into the Bonanza numbering system (bptid/bpt_id)
        :type regular_number: int
        :rtype str
        :param regular_number: integer to be translated
        :return: string representation in the new system
        """
        # Set the number system's base using the length of the string
        # containing of all the characters in the system (*in the order
        # of value*).
        base_size = len(BonanzaUtilities.numeral_string)
        number_string = ""
        while regular_number:
            number_string += BonanzaUtilities.numeral_string[regular_number % base_size]
            regular_number //= base_size
        return number_string[::-1] or "0"

    @staticmethod
    def translate_bptid_to_integer(bpt_id):
        """
        Translates a Bonanza number into its decimal equivalent
        :type bpt_id: str
        :rtype int
        :param bpt_id: Bonanza alphanumeric string
        :return: integer equivalent of Bonanza value
        """
        base_size = len(BonanzaUtilities.numeral_string)
        total = 0
        power = 1
        for letter in bpt_id[::-1]:
            index = BonanzaUtilities.numeral_string.find(letter)
            total += index * power
            power *= base_size
        return total
