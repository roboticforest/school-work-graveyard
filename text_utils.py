#!/usr/bin/env python3

def ordinal_str(num: int) -> str:
    """
    Converts a given integer to a string with an ordinal suffix applied, preserving the sign.

    :param num: Any integer, be it positive, negative, or zero.
    :return: The number as a string with the correct ordinal suffix applied. 0 becomes "0th",
      1 becomes "1st", 10 becomes "10th", -2 becomes "-2nd", etc.
    """

    def single_digit_ordinal(num: str) -> str:
        """
        Helper function to append ordinal suffixes to single digit number strings.

        :param num: A single character string containing one digit of a positive integer.
        :return: The number string with the correct ordinal suffix appended.
        """
        if num == "1":
            return num + "st"
        elif num == "2":
            return num + "nd"
        elif num == "3":
            return num + "rd"
        else:
            return num + "th"

    def two_digit_ordinal(num: str) -> str:
        """
        Helper function to append ordinal suffixes to two-digit number strings.

        :param num: A string representing a positive integer.
        :return: The number string with the correct ordinal suffix appended.
        """
        if num[0] != "1":
            return num[0] + single_digit_ordinal(num[1])
        else:
            return num + "th"

    # Convert the int to a str and extract the sign.
    raw_num = str(num)
    if raw_num[0] == "-":
        sign = raw_num[0]
        base_num = raw_num[1:]
    else:
        sign = ""
        base_num = raw_num[:]

    # Reassemble the sign and number, appending the appropriate ordinal suffix.
    if len(base_num) == 1:
        return sign + single_digit_ordinal(base_num)
    else:
        return sign + base_num[:-2] + two_digit_ordinal(base_num[-2:])


def remove_line_comment(line: str) -> str:
    """Finds and erases Python style line comments, stripping any leading/trailing whitespace."""
    split_pos = line.find("#")
    if split_pos != -1:
        clean_line = line[:split_pos]
    else:
        clean_line = line
    return clean_line.strip()

# Main program.
if __name__ == "__main__":
    print("Testing utilities...")

    for number in range(-100, 201):
        print(ordinal_str(number))
