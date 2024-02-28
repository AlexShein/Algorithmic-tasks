import re
from string import ascii_lowercase as symbols

OFFSET = 97  # Decimal code of 'a'
ALPHABET_SIZE = len(symbols)


def encode(character: str, key_number: int) -> str:
    return chr((((ord(character) - OFFSET) * key_number) % ALPHABET_SIZE) + OFFSET)


def decode(to_be_decoded: str) -> str:
    key_number, string = re.findall("\d+|[a-z]+", to_be_decoded)
    decode_table = {
        encode(character, int(key_number)): character for character in symbols
    }
    if len(decode_table) != ALPHABET_SIZE:
        return "Impossible to decode"

    return "".join([decode_table[character] for character in string])


def testing_decode(string, expected):
    actual = decode(string)
    print(f"{expected=} {actual=}")
    assert actual == expected


if __name__ == "__main__":
    print(symbols)
    testing_decode(
        "1273409kuqhkoynvvknsdwljantzkpnmfgf", "uogbucwnddunktsjfanzlurnyxmx"
    )
    testing_decode("761328qockcouoqmoayqwmkkic", "Impossible to decode")
    testing_decode("1544749cdcizljymhdmvvypyjamowl", "mfmwhbpoudfujjozopaugcb")
    testing_decode(
        "1122305vvkhrrcsyfkvejxjfvafzwpsdqgp", "rrsxppowmjsrclfljrajtybwviqb"
    )
