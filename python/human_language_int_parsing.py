NUMBERS_MAP = {
    'zero': 0,
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    'ten': 10,
    'eleven': 11,
    'twelve': 12,
    'thirteen': 13,
    'fourteen': 14,
    'fifteen': 15,
    'sixteen': 16,
    'seventeen': 17,
    'eighteen': 18,
    'nineteen': 19,
    'twenty': 20,
    'thirty': 30,
    'forty': 40,
    'fifty': 50,
    'sixty': 60,
    'seventy': 70,
    'eighty': 80,
    'ninety': 90,
    'hundred': 100,
    'thousand': 1000,
    'million': 1000000,
}
MULTIPLIERS = {
    1000000,
    1000,
    100,
}

# Find highest "order" and solve the problem recursively
def convert_to_int(parsed_input: list[int]):
    if len(parsed_input) == 0:
        return 0
    if len(MULTIPLIERS.intersection(set(parsed_input))) == 0:
        return sum(parsed_input)
    position, multiplier = 0, 1
    for index, number in enumerate(parsed_input):
        if number in MULTIPLIERS and multiplier < number:
            position, multiplier = index, number
    result = convert_to_int(parsed_input[:position]) * multiplier + convert_to_int(
        parsed_input[position + 1 :]
    )
    return result


# This function parses numbers written in human language into machine representation
def parse_int(input: str):
    parsed_input = [NUMBERS_MAP.get(item, 0) for item_raw in input.split(' ') for item in item_raw.split('-')]
    return convert_to_int(parsed_input)


if __name__ == '__main__':
    assert parse_int('one') == 1
    assert parse_int('twenty') == 20
    assert parse_int('two hundred and forty-six') == 246
    assert parse_int('three thousand two hundred forty-six') == 3246
    assert parse_int('forty-seven thousand nine hundred seventy-six') == 47976
    assert parse_int('three hundred thousand five') == 300005
    assert parse_int('twelve thousand six') == 12006
    assert parse_int('five hundred thirty-one thousand six hundred eighty-six') == 531686
