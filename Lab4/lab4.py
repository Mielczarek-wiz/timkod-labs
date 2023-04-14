from bitarray import bitarray

'''
    Opennig file with filename and return content.
'''
def read_file(filename: str) -> str:
    with open(file=filename, encoding='utf-8') as file:
        return file.read()

'''
    Function used to calculate how many times character appeared in text.
    Returning sorted list by number of occurrences.
'''
def count_letters(text: str, offset: int = 1) -> list:
    
    # Make dictionary.
    counter = {}

    # Calculate how many times key (char or word) appeared in given text.
    for i in range(len(text) - offset + 1):
        counter[text[i:i + offset]] = counter.get(text[i:i + offset],0) + 1

    # Return sorted list.
    return sorted(counter.items(), key=lambda t: t[1])[::-1]

'''
    Function used to create code for compressing.
'''
def create(text: str) -> dict[str, str]:

    # Make a dict which contains how many times letter appeared in text.
    count_list = count_letters(text)

    # Make a dict with codes.
    code = {}

    # Give the letter unique code.
    for i in range(len(count_list)):

        # Take a letter with her appearing frequency.
        t = count_list[i]

        # Make a bitarray (it is not neccecary)
        x = bitarray(f"{i:06b}")

        # Add letter with her code to the dict.
        code[t[0]] = x.to01()

    # Add special character EOF.
    code['EOF'] = f"{63:06b}"

    # Return dict with code.
    return code

'''
    Function used to encode text by using generated code.
'''
def encode(text: str, code: dict[str, str]) -> bitarray:
    
    # Make a main bitarray.
    bits = bitarray()

    # Encode text symbol by symbol.
    for i in range(len(text)):

        # Add letter code to the main bitarray.
        bits += bitarray(code[text[i]])

    # Add code of EOF sign. (We are compressing text so we are not coding by using 8bits (like ASCII) but 6bits).
    bits += code['EOF']

    # Return encoded text.
    return bits

'''
    Function used to decode text by using generated code.
'''
def decode(bits: bitarray, code: dict[str, str]) -> str:
    
    # Create list which will contains every decoded symbol.
    output_string = []

    # Create a reverse dict with (value, key) pairs to speed up processing.
    decoding_dict = {v:k for k,v in code.items()}

    # Decode text.
    for i in range(0, len(bits), 6):
        decoded_letter = decoding_dict[bits[i:i+6].to01()]

        # If the bits coded EOF sign - stop decoding.
        if decoded_letter == 'EOF':
            break
        else:

            # Add letter to output list.
            output_string.append(decoded_letter)

    # Return decoded string.
    return ''.join(output_string)

'''
    Function used to save text and code to file.
'''
def save(encoded_text: bitarray,
         code: dict[str, str],
         output_text_file: str = "binary.bin",
         output_code_file: str = "code.txt"):

    # Open file to save code.
    file = open(output_code_file, "w")

    # Write code to the file.
    for key in code.keys():
        file.write(str(key) + "," + str(code[key]) + '\n')

    # Close file stream.
    file.close()
    
    # Open file to save encoded text.
    file = open(output_text_file, "wb")

    # Write encoded text to the file.
    file.write(encoded_text)

    # Close file stream.
    file.close()

'''
    Function used to load text and code from file.
'''
def load(input_file: str = "binary.bin", code_file: str = "code.txt") -> tuple((bitarray, dict[str, str])):

    # Open file with code.
    file = open(code_file, "r")

    # Read code.
    output_from_file = file.readlines()

    # Make a dict.
    code = {}

    # Exctract codes from readed string.
    for element in output_from_file:
        splited_element = element.split(",")
        code[splited_element[0]] = splited_element[1][:-1]

    # Close file.
    file.close()
    
    # Make an bitarray.
    content = bitarray()

    # Open file with bytes writed.
    file = open(input_file, "rb")

    # Read bytes and add them to the bitarray.
    content.frombytes(file.read())

    # Close file.
    file.close()

    # Return content and code.
    return content, code

'''
    Function used to check that both text are the same.
'''
def check_out(input_text: str, text_to_check: str) -> str:

    # Check if both texts are the same.
    if(input_text != text_to_check):
        return "Texts are not the same!"

    return "Texts are the same!"

'''
    Function main.

    OPERATIONS YOU CAN USE:

        1. check_out  -> checks that input text and output text (after decode) are the same
        2. read_file  -> loads file you want to encode
        3. create     -> creats code used to encode text
        4. encode     -> encode given text
        5. decode     -> decode text by using code
        6. save       -> save encoded text and code in file
        7. load       -> load text and code from files
'''
def main():

    text = read_file("input/norm_wiki_sample.txt")

    code = create(text)

    sequence_encoded = encode(text, code)

    save(sequence_encoded, code)

    sequence, code = load()

    decoded_text = decode(sequence, code)

    print(check_out(text,decoded_text))


'''
    Starting position.
'''
if __name__ == '__main__':
    main()