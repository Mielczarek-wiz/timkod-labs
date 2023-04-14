import math
import numpy as np


'''
    Opennig file with filename and return content.
'''
def read_file(filename):
    with open(file=filename, encoding='utf-8') as file:
        return file.read()

'''
    Function used to calculating propabilities.
'''
def prob_words_or_letters(text, offset = 1):
    
    # Make dictionary.
    prob = {}

    # Calculate how many times key (char or word) appeared in given text.
    for i in range(len(text) - offset + 1):
        prob[tuple(text[i:i + offset])] = prob.get(tuple(text[i:i + offset]),0) + 1

    # Calculate sum of values of whole dict.
    sumOfKeys = sum(list(prob.values()))

    # Calculate propabilities.
    for propability in prob.keys():
        prob[propability] /= sumOfKeys

    # Return dictionary with probabilities.
    return prob

'''
    Function used to calculating entropy.
'''
def calculate_entropy(prob):

    # Initialize entropy.
    entropy = 0.0

    # Calculating entropy.
    for key in prob.keys():
        entropy += prob[key] * math.log2(prob[key])

    # Return entropy.
    return -entropy

'''
    Function used to calculating conditional entropy.
'''
def calculate_conditional_entropy(prob_sec, prob_first):

    # Initialize entropy.
    con_entropy = 0.0

    # Calculating conditional probability.
    for key in prob_sec.keys():
        con_probabliity = prob_sec[key] / prob_first[key[:-1]]
        con_entropy += prob_sec[key]  * math.log2(con_probabliity)
    
    # Return conditional entropy.
    return -con_entropy

'''
    Function used to calculating all entriopies for chars.
'''
def calculate_entropies_for_chars(text):

    # Create output list.
    output_list = []

    # Calculate probabilities.
    probabilities = prob_words_or_letters(text) 

    # Add to list calculated entropy.
    output_list.append(calculate_entropy(probabilities))

    # Calculate conditional entropies.
    for i in [1,2,3,4,5]:

        # Get next order probability.
        tmp_prob = prob_words_or_letters(text, i+1)

        # Calculate conditional entropy.
        output_list.append(calculate_conditional_entropy(tmp_prob, probabilities))

        # Add to list calculated conditional entropy.
        probabilities = tmp_prob

    # Return list with entropies.
    return output_list

'''
    Function used to calculating all entriopies for words.
'''
def calculate_entropies_for_words(words):

    # Create output list.
    output_list = []

    # Calculate probabilities.
    probabilities = prob_words_or_letters(words) 

    # Add to list calculated entropy.
    output_list.append(calculate_entropy(probabilities))

    # Calculate conditional entropies.
    for i in [1,2,3,4,5]:

        # Get next order probability.
        tmp_prob = prob_words_or_letters(words, i+1)

        # Calculate conditional entropy.
        output_list.append(calculate_conditional_entropy(tmp_prob, probabilities))

        # Add to list calculated conditional entropy.
        probabilities = tmp_prob

    # Return list with entropies.
    return output_list

'''
    Function used to generate all entriopies for file.
'''
def generate_entropies(file):

    # Read text from file.
    text = read_file(filename=file)

    # Calculate entropies for chars.
    chars_entropies_list = calculate_entropies_for_chars(text)

    print("Chars entropies:")

    # Show entropies for chars.
    for i in range(len(chars_entropies_list)):
        if i == 0:
            print("Entropy: " + str(chars_entropies_list[i]))
        else:
            print(str(i) + " conditional entropy: " + str(chars_entropies_list[i]))
        
    # Calculate entropies for words.
    words_entropies_list = calculate_entropies_for_words(list(text.split()))

    # Show entropies for words.
    for i in range(len(words_entropies_list)):
        if i == 0:
            print("Entropy: " + str(words_entropies_list[i]))
        else:
            print(str(i) + " conditional entropy: " + str(words_entropies_list[i]))

    return [chars_entropies_list[1:], words_entropies_list[1:]]

'''
    Function used to decide if given sample is language or not.
'''
def check_entropies(sample_entropies, chars_min_max, words_min_max):

    # Initialize counter.
    counter = 0

    # Check all conditional entropies that they are in between [min, max].
    for i in range(len(sample_entropies[0])):

        if sample_entropies[0][i] >= chars_min_max[i][0] and sample_entropies[0][i] <= chars_min_max[i][1]:
            counter += 1
        if sample_entropies[1][i] >= words_min_max[i][0] and sample_entropies[1][i] <= words_min_max[i][1]:
            counter += 1
    
    # If they are at minimum 50% (treshold) program recognize it as a language. 
    if counter >= len(sample_entropies[0]):
        return "Yes"
    else:
        return "No"

'''
    Function main.
'''
def main():

    # Matrixes for all entropies (chars and words) for every file.
    matrix_entropies_chars = []
    matrix_entropies_words = []

    # All files.
    filenames = ["norm_wiki_en.txt", "norm_wiki_la.txt", "norm_wiki_eo.txt", "norm_wiki_et.txt", "norm_wiki_ht.txt", "norm_wiki_nv.txt", "norm_wiki_so.txt"]

    # Start generating for file.
    for file in filenames:
        print("Entropies for file: " + file)
        result = generate_entropies(file)
        matrix_entropies_chars.append(result[0])
        matrix_entropies_words.append(result[1])
    
    # Matrixes for [min, max] for all 5 conditional entropies degrees.
    chars_min_max = []
    words_min_max = []

    # Transpose matrixes to get [min, max] in easy way.
    matrix_entropies_chars = np.transpose(matrix_entropies_chars)
    matrix_entropies_words = np.transpose(matrix_entropies_words)

    # Get [min, max].
    for i in range(5):
        chars_min_max.append([min(matrix_entropies_chars[i]), max(matrix_entropies_chars[i])])
        words_min_max.append([min(matrix_entropies_words[i]), max(matrix_entropies_words[i])])

    print("\n---------->SAMPLES<----------\n")

    # All sample files.
    sample_names = ["sample0.txt", "sample1.txt", "sample2.txt", "sample3.txt", "sample4.txt", "sample5.txt"]


    # Start generating for sample and point if it is language or not.
    for file in sample_names:
        print("Entropies for file: " + file)
        result = generate_entropies(file)
        print()
        print("Is it a language?: " + file + ": " + str(check_entropies(result, chars_min_max, words_min_max)))
        print()

# Starting position.
if __name__  == '__main__':
    main()