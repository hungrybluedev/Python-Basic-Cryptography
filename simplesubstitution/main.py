from simplesubstitution.Cipher import PRINTABLE_ASCII_ALPHABET, get_combined_cipher


def open_as_utf8(file_string, mode):
    return open(file_string, mode, encoding="utf-8")


def generate_files(custom_cipher):
    input_file = open_as_utf8("data/input.txt", "r")
    output_file = open_as_utf8("data/output.txt", "w")
    decrypted_file = open_as_utf8("data/output_decrypt.txt", "w")
    print("Files have been opened.")

    message = input_file.read()
    print("File has been read.")

    encrypted = custom_cipher.encrypt(message)
    decrypted = custom_cipher.decrypt(encrypted)
    assert message == decrypted

    output_file.write(encrypted)
    print("File has been encrypted.")

    decrypted_file.write(decrypted)
    print("File has been decrypted.")

    input_file.close()
    output_file.close()
    decrypted_file.close()


def verify_files_are_equal():
    input_file = open_as_utf8("data/input.txt", "r")
    decrypted_file = open_as_utf8("data/output_decrypt.txt", "r")

    assert input_file.read() == decrypted_file.read()
    input_file.close()
    decrypted_file.close()
    print("Contents verified to be equal.")


if __name__ == '__main__':
    alphabet = PRINTABLE_ASCII_ALPHABET
    cipher = get_combined_cipher("The Enigma Machine had a fatal flaw. A character never mapped to itself.", -42000,
                                 alphabet, True)

    generate_files(cipher)
    verify_files_are_equal()
