import math
from bitarray import bitarray

'''
    Class for Huffman's tree.
'''
class Tree:

    def __init__(self, label = None, prob = 0, left = None, right = None):

        self.left = left
        self.right = right
        self.label = label
        self.prob = prob

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

    # Take sum of all character sum of appearances.
    sum_values = sum(counter.values())

    # Divide all character appearances by sum of appearances.
    for key in counter.keys():
        counter[key] /= sum_values

    # Return sorted list.
    return sorted(counter.items(), key = lambda t: t[1])

'''
    Function used to build the Huffman's tree.
'''
def build_tree(count_list: list) -> Tree:

    # List (Main list) for holding all trees during processing.
    tree_list = []

    # For every element build a tree with only one node (root).
    for el in count_list:
        tree_list.append(Tree(el[0], el[1]))

    # Add 'EOF' sign.
    tree_list.append(Tree('EOF', 0.0))

    # Sort list by probability.
    tree_list = sorted(tree_list, key = lambda tree: tree.prob)

    # While list has more than one tree..
    while len(tree_list) > 1:
        # Take first two trees.
        t1 = tree_list[0]
        t2 = tree_list[1]

        # Delete them from main list.
        del tree_list[0]
        del tree_list[0]
        
        # Build new tree with left child - t1, and right child - t2.
        new_tree = Tree(t1.label + t2.label, t1.prob + t2.prob, t1, t2)

        # Add new tree to main list.
        tree_list.append(new_tree)

        # Sort main list.
        tree_list = sorted(tree_list, key = lambda tree: tree.prob)

    # Return Huffman's tree.
    return tree_list[0]

'''
    Recursive function used to find leafs. 
'''
def find_leafs(tree: Tree, code: dict[str, str], bits: str = ''):

    # If the node is leaf save code in dictionary.
    if (tree.left == None) and (tree.right == None):
        code[tree.label] = bits

    # Else use recursion in left and right way.
    else:
        find_leafs(tree.left, code, bits + '0')
        find_leafs(tree.right, code, bits + '1')
    
'''
    Function used to calculate efficiency.
'''
def calculate_avg_length_and_efficiency(code: dict[str, str], count_list: list) -> tuple((float, float)):

    # Averange length.
    avg_l = 0.0

    # Initialize entropy.
    entropy = 0.0

    # Calculate avg_l.
    for el in count_list:
        avg_l += float(el[1]) * float(len(code[el[0]]))
        entropy += el[1] * math.log2(el[1])

    return (avg_l, -entropy/avg_l)
'''
    Function used to create code for compressing.
'''
def create(text: str) -> dict[str, str]:

    # Make a dict which contains how many times letter appeared in text.
    count_list = count_letters(text)

    # Build Huffman's tree.
    tree = build_tree(count_list)
    
    # Create dictionary for codes
    code = {}

    # Use recursion to find all leafs (so the codes).
    find_leafs(tree, code)

    # Calculating efficiency and averange code length.
    avg_l , eff = calculate_avg_length_and_efficiency(code, count_list)

    # Print efficiency and averange code length.
    print("Averange code length: "+ str(round(avg_l, 2)) +"\nEfficiency: " + str(round(eff * 100, 2)) + "%")

    # Return code.
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

    # Add code of EOF sign.
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

    # Temporary list to hold a sequence of bits.
    temp_bits = []

    decoding_keys = decoding_dict.keys()

    # Decode text.
    for bit in list(bits):

        # Add next bit to list.
        temp_bits.append(str(bit))

        # Check that the sequence of bits is in code (in special decoding_dict).
        if ''.join(temp_bits) in decoding_keys:

            # If it is - take the sign assigned to it.
            decoded_letter = decoding_dict[''.join(temp_bits)]

            # If the bits coded EOF sign - stop decoding.
            if decoded_letter == 'EOF':
                break
            else:

                # Add letter to output list.
                output_string.append(decoded_letter)

                # Empty the temporary list for new sequence of bits.
                temp_bits = []

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
        3. create     -> creats code (by using Huffman's coding) used to encode text
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