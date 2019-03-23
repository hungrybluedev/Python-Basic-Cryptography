"""
This module houses 3 classes: The Cipher base class and the two subclasses: KeyedCipher
and ShiftedCipher. All of these provide convenient ways to work with mono-alphabetic
simple substitution ciphers.

The Cipher class takes a plaintext alphabet (string) and a corresponding
mapped ciphertext alphabet (string). In other words, for a given index i (say), plaintext[i]
will map to ciphertext[i], when the text is encrypted. Both the alphabet strings must have
the same unique set of characters, and repetitions are not allowed.

To make the generation of ciphertext alphabets easier, The KeyedCipher and the
ShiftedCipher are provided. The KeyedCipher takes a keyword/key-phrase, paired with a suitable
plaintext alphabet and generates a Cipher with the characters provided pushed to the
beginning, with the rest of the unused characters appended at the end. Consequently, a
good key will lead to better encryption/mapping.

The ShiftedCipher simply shifts the entire plaintext alphabet by a given amount, with the
end wrapping around to the front. The Caesar Cipher is one of the instances of this Cipher.

There is also an option to get a Cipher by combining both the methods: the
get_combined_cipher()

Unique Behaviour:
=================

When using the alphabet with all ascii letters (string.ascii_letters), the keyword is
treated as case insensitive. That is, the plaintext alphabet is essentially the
combination of applying the keyword separately on lowercase and uppercase letters. While
this does restrict the alphabet, this makes it more convenient to use for general text
contained a mixture of cases and the cipher needed is based simply on the alphabet.

Subhomoy Haldar - 2019
HungryBlueDev.wordpress.com

"""
import string


##################
# Internal stuff #
##################


def _generate_keyword_based_ciphertext_alphabet(plaintext_alphabet, key):
    """
    Attempts to create a ciphertext alphabet string by moving the (first unique occurrence)
    of a character of the given keyword/key-phrase to the beginning and appending the unused
    characters to the end. If the key contains characters not contained in the
    plaintext alphabet, then an error is thrown.

    For example, if the alphabet is "0123456789" and the key is "5158414", the the
    generated ciphertext alphabet would be "5184023679".

    :param plaintext_alphabet: The universe to draw characters from.
    :param key: To determine which characters are moved up.
    :return: A ciphertext alphabet based on the key provided.
    """
    plaintext_list = list(plaintext_alphabet)
    ciphertext_list = []

    for char in key:
        try:
            position = plaintext_list.index(char)
            ciphertext_list.append(plaintext_list.pop(position))

        except ValueError:
            if char not in ciphertext_list:
                raise ValueError("Keyword contains character not contained in the alphabet: " + char)

    return _list_to_string(ciphertext_list + plaintext_list)


def _generate_case_handled_ciphertext_alphabet(plaintext_alphabet, key):
    """
    This method checks if the plaintext alphabet is that of all ascii letters. If it
    is so, the key is treated as case-insensitive. If not, it applies simple mapping.

    :param plaintext_alphabet: The universe to draw characters from.
    :param key: To determine which characters are moved up.
    :return: A ciphertext alphabet based on the key provided.
    """
    if plaintext_alphabet == string.ascii_letters:
        lower_half = _generate_keyword_based_ciphertext_alphabet(string.ascii_lowercase, key.lower())
        upper_half = _generate_keyword_based_ciphertext_alphabet(string.ascii_uppercase, key.upper())
        return lower_half + upper_half
    else:
        return _generate_keyword_based_ciphertext_alphabet(plaintext_alphabet, key)


def _generate_inverse(plaintext_list, ciphertext_list):
    """
    Given an existing mapping from a plaintext alphabet to a ciphertext alphabet,
    generate the inverse mapping, which essentially maps from the ciphertext back
    to the plaintext. In this case however, the ciphertext is permuted back to the
    plaintext, resulting in the plaintext being permuted accordingly.

    The advantage of this is that only one mapping method will work for both
    encryption and decryption of the text.
    """
    inverse_list = []
    for char in plaintext_list:
        position = ciphertext_list.index(char)
        inverse_list.append(plaintext_list[position])
    return inverse_list


def _list_to_string(char_list):
    """
    A simple utility method to help the code make sense.
    """
    return "".join(char_list)


def _apply_mapping(message_str, source_list, destination_list):
    """
    This method maps a character from the source alphabet to the destination
    alphabet. This can be used for both encryption and decryption.

    :param message_str: The message to be mapped.
    :param source_list: The source alphabet.
    :param destination_list: The destination alphabet.
    :return: A mapped message.
    """
    converted = []
    for char in message_str:
        try:
            position = source_list.index(char)
            converted.append(destination_list[position])
        except ValueError:
            converted.append(char)

    return _list_to_string(converted)


def _generate_shifted_alphabet(alphabet_string, shift_amount):
    """
    Generated a shifted alphabet for shift-based ciphers, with wrap-around.
    :param alphabet_string: The alphabet to be shifted.
    :param shift_amount: The shift amount to be shifted. May be negative.
    :return: The shifted alphabet.
    """
    # Restrict the shift amount to [0, len) so that it wraps
    # around gracefully, instead of ignoring large values.
    amount = shift_amount % len(alphabet_string)
    return alphabet_string[amount:] + alphabet_string[:amount]


################
# Public stuff #
################

# This is the alphabet for all printable ascii characters
PRINTABLE_ASCII_ALPHABET = ['\t'] + [chr(x) for x in range(32, 127)]


class Cipher:
    """
    A class that performs mono-alphabetic simple substitution on text based on
    a given mapping between the provided plaintext alphabet and the ciphertext alphabet.

    Using the encrypt() method, normal text is converted to ciphertext. Using the
    decrypt() method on encrypted text retrieves the normal text. Simple enough.

    In order to use this class, make sure you supply the proper ciphertext. It
    can be cumbersome to generate some frequently used styles of ciphertext by
    writing out explicit code, so you might look into the subclasses: KeyedCipher,
    and ShiftedCipher. Also, the get_get_combined_cipher() method which literally combines
    a KeyedCipher and a ShiftedCipher.
    """

    def __init__(self, ciphertext_alphabet, plaintext_alphabet=string.ascii_letters):
        """
        The ciphertext mapping provided must have the same characters as the plaintext
        alphabet. Also, there should not be repeated characters. Essentially, the
        ciphertext should be a permutation of the plaintext alphabet.

        :param ciphertext_alphabet: The mapped ciphertext alphabet.
        :param plaintext_alphabet: The plaintext alphabet.
        """
        self.plaintext_list = list(plaintext_alphabet)

        # Make sure that both alphabets have the same number of characters
        if len(plaintext_alphabet) != len(ciphertext_alphabet):
            raise ValueError("The plaintext and ciphertext have different character counts.")

        # Ignore the keyword, even if it is present. The mapping gets preference.
        self.ciphertext_list = list(ciphertext_alphabet)

        # Make sure that both alphabets are equal when the order is ignored
        if set(self.plaintext_list) != set(self.ciphertext_list):
            raise ValueError("The plaintext and the ciphertext are not the same set of characters.")

        self.inverse_list = _generate_inverse(self.plaintext_list, self.ciphertext_list)

    def __str__(self):
        return "PT: " + _list_to_string(self.plaintext_list) \
               + "\nCT: " + _list_to_string(self.ciphertext_list)

    def encrypt(self, message_string):
        """
        :param message_string: The message in plaintext to encrypt.
        :return: The encrypted message.
        """
        return _apply_mapping(message_string, self.plaintext_list, self.ciphertext_list)

    def decrypt(self, message_string):
        """
        :param message_string: The encrypted ciphertext.
        :return: The decrypted message.
        """
        return _apply_mapping(message_string, self.plaintext_list, self.inverse_list)


class KeyedCipher(Cipher):
    """
    A subclass of Cipher to make it easier to use, based on keys composed from
    the set of characters in the plaintext alphabet.
    """

    def __init__(self, key, plaintext_alphabet=None):
        """
        :param key: The key whose characters are to be pushed to the beginning.
        :param plaintext_alphabet: The alphabet of characters to source from.
        """
        if plaintext_alphabet is None:
            plaintext_alphabet = PRINTABLE_ASCII_ALPHABET

        if key is None or len(key) == 0:
            raise ValueError("The keyword has to be a non-null string.")

        ciphertext_alphabet = _generate_case_handled_ciphertext_alphabet(plaintext_alphabet, key)
        super().__init__(ciphertext_alphabet, plaintext_alphabet)


class ShiftedCipher(Cipher):
    """
    Helps create a cipher based on shifted alphabets.
    """

    def __init__(self, shift_amount, plaintext_alphabet=None):
        """
        :param shift_amount: The amount to shift the alphabet by. Can be negative.
        :param plaintext_alphabet: The alphabet of characters to source from.
        """
        if plaintext_alphabet is None:
            plaintext_alphabet = PRINTABLE_ASCII_ALPHABET

        ciphertext_alphabet = _generate_shifted_alphabet(plaintext_alphabet, shift_amount)
        super().__init__(ciphertext_alphabet, plaintext_alphabet)


def get_combined_cipher(key, shift_amount, plaintext_alphabet=None, shift_first=False):
    """
    Obtain a Cipher from both, a key and a shift amount. The order in which the operations
    are applied can also be specified. By default, the key is applied first, followed by
    the shift.

    :param key: The key to generate the ciphertext with.
    :param shift_amount: The amount by which the ciphertext will be shifted.
    :param plaintext_alphabet: The alphabet to source from.
    :param shift_first: False by default. Set to true if the shifting is desired first.
    :return: A shifted, keyed cipher.
    """
    if plaintext_alphabet is None:
        plaintext_alphabet = PRINTABLE_ASCII_ALPHABET

    if shift_first:
        plaintext_alphabet = _generate_shifted_alphabet(plaintext_alphabet, shift_amount)
        return KeyedCipher(key, plaintext_alphabet)
    else:
        plaintext_alphabet = _generate_case_handled_ciphertext_alphabet(plaintext_alphabet, key)
        return ShiftedCipher(shift_amount, plaintext_alphabet)
