import string, sys

from random import choices
from copy import deepcopy

'''
    Opennig file with filename and return content.
'''
def readFile(filename):
    with open(file=filename, encoding='utf-8') as file:
        return file.read()

'''
    Generate string with equals probability of characters.
'''
def generateStrings(alphabet, number):

    # Generate string from random characters with equals probability.
    randomize = ''.join(choices(population=alphabet, k=number))

    newText = ''

    # Make string without reapeted spaces.
    for word in randomize.split(" "):
        newText += word.strip(" ")
        newText += " "

    # Return string.
    return newText

'''
    Caclulate averange word length in given string.
'''
def findAWL(text):
    letterCount = 0
    textSplited = text.split()

    # Calculate sum of letter in all words.
    for word in textSplited:
        letterCount += len(word)
    
    # Calculate averange lenght.
    return letterCount / len(textSplited)

'''
    Caclulate how many times character appeared in the string.
'''
def findTokens(alphabet, text):

    # Make a alphabet with counters = 0 in dictionary.
    alphabet = dict.fromkeys(alphabet, 0)
    
    # Split text to get all characters.
    textSplited = list(text)

    # Calculate how many times character appeared in the string.
    for key in alphabet.keys():
        alphabet[key] = textSplited.count(key)
    
    # Return dictionary.
    return alphabet

'''
    Function which generate text for first order approximation.
'''
def firstOrderApproximation(text, number):

    # Alphabet + space.
    alphabet = list(string.ascii_lowercase) + [' ']

    # Calculate all propabilities of  appearances of bigrams in given text.
    propabilities = findPropabilities(deepcopy(text), 1)

    # The started text had to be 'propability'
    newText = 'propability'

    # Random generate character based on conditional propabilities.
    for i in range(number - 1):

        # Case when the string with 1 characters not appeared in given text.
        if newText[-1] not in propabilities.keys():
            randomChar = str(''.join(choices(population=alphabet, k =1)))
        else: 
            # Get random character.
            randomChar = ''.join(choices(population = list(propabilities[newText[-1]].keys()), weights = list(propabilities[newText[-1]].values()), k = 1))
        
        # Concatenate.
        newText += str(randomChar)

    # Return first order approximation text.
    return newText

'''
    Function which generate text for third order approximation.
'''
def thirdOrderApproximation(text, number):

    # Alphabet + space.
    alphabet = list(string.ascii_lowercase) + [' ']

    # Calculate all propabilities.
    propabilities = findPropabilities(deepcopy(text), 3)

    # The started text had to be 'propability'
    newText = 'propability'

    # Random generate character based on conditional propabilities.
    for i in range(number - 1):

        # Case when the string with 3 characters not appeared in given text.
        if newText[(len(newText) - 3):] not in propabilities.keys():
            randomChar = str(''.join(choices(population=alphabet, k =1)))
        else: 
            # Get random character.
            randomChar = ''.join(choices(population = list(propabilities[newText[(len(newText) - 3):]].keys()), weights = list(propabilities[newText[(len(newText) - 3):]].values()), k = 1))
        
        # Concatenate.
        newText += str(randomChar)

    # Return third order approximation text.
    return newText

'''
    Function which generate text for fifth order approximation.
'''
def fifthOrderApproximation(text, number):

    # Calculate all propabilities.
    propabilities = findPropabilities(deepcopy(text), 5)

    # The started text had to be 'propability'
    newText = 'propability'
    
    # Alphabet + space.
    alphabet = list(string.ascii_lowercase) + [' ']

    # Random generate character based on conditional propabilities.
    for i in range(number - 1):

        # Case when the string with 5 characters not appeared in given text.
        if newText[(len(newText) - 5):] not in propabilities.keys():
            randomChar = str(''.join(choices(population=alphabet, k =1)))
        else: 
            # Get random character.
            randomChar = ''.join(choices(population = list(propabilities[newText[(len(newText) - 5):]].keys()), weights = list(propabilities[newText[(len(newText) - 5):]].values()), k = 1))
        
        # Concatenate.
        newText += str(randomChar)

    # Return fifth order approximation text.
    return newText

'''
    First task was to generate random string 26 letters + space
    with equals propability.
'''
def firstTask(alphabet, number):
    return findAWL(generateStrings(alphabet, int(number)))

'''
    Second task was to find out how many times
    character appearance in given text.
'''
def secondTask(alphabet, text):
    return findTokens(alphabet, text)

'''
    Third task was to generate random string,
    but probability was based on text given in second task.
'''
def thirdTask(hist, number):

    # Calculate sum --how many times character appeared in string--
    # of all characters in string.
    sumOfCountedLetters = sum(list(hist.values()))

    # Calculate propability for every character
    # (number_of_appearances / sum_of_all_letters).
    for key, value in hist.items():
        hist[key] = float(value/sumOfCountedLetters)
    
    # Generate string from characters with different probability.
    randomize = ''.join(choices(population = list(hist.keys()), weights = list(hist.values()), k=int(number)))

    # Return averange word length of generated string.
    return findAWL(randomize)

'''
    The fourth task was to calculate propability of appearance two characters (i, j) 
    next to each other only in two mostly used characters.
'''
def fourthTask(text, hist):

    # Sorting the dictionary with propabilities calculated before.
    histSorted = sorted(hist.items(), key=lambda x: x[1], reverse=True)

    # Calculate all appearances of bigrams in given text.
    propabilities = findPropabilities(deepcopy(text), 1)

    # Calculate the propabilities with first character.
    firstLetterPropabilities = propabilities[histSorted[0][0]]

    # Calculate the propabilities with second character.
    secondLetterPropabilities = propabilities[histSorted[1][0]]

    # Return propabilities.
    return firstLetterPropabilities, secondLetterPropabilities

'''
    The fifth task has three etaps. 
    Etap 1: Generate text based on conditional propabilities called first order approximation.
    Etap 2: Generate text based on conditional propabilities called third order approximation.
    Etap 3: Generate text based on conditional propabilities called fifth order approximation.

    At the end program has to calculate averange word length in generated texts.
'''
def fifthTask(text, number, outputFile, option):

    # Open file to write output with specific option.
    file = open(outputFile, str(option))

    print("\nTask five:", file=file)
    
    # Generating first order appropximation.
    generatedText = firstOrderApproximation(deepcopy(text), number)
    
    print("\nGenerated text for first order approximation:\n" + generatedText, file=file)
    print("\nAverange word length for first order approximation:\n" + str(findAWL(generatedText)), file=file)

    # Generating third order appropximation.
    generatedText = thirdOrderApproximation(deepcopy(text), number)

    print("\nGenerated text for third order approximation:\n" + generatedText, file=file)
    print("\nAverange word length for third order approximation:\n" + str(findAWL(generatedText)), file=file)

    # Generating fifth order appropximation.
    generatedText = fifthOrderApproximation(deepcopy(text), number)
    print("\nGenerated text for fifth order approximation:\n" + generatedText, file=file)
    print("\nAverange word length for fifth order approximation:\n" + str(findAWL(generatedText)), file=file)

    # Close file.
    file.close()


'''
    Deleting numbers in given text and after that delete additional spaces.
'''
def preprocessing(text):

    newText = []

    # Deleting digits.
    for i in range(len(text)):

        if not(text[i].isnumeric()):
            newText.append(text[i])

    # Deleting additional spaces.
    newText = ''.join(newText)
    newText = newText.split()

    # Return converted text.
    return ' '.join(newText)

'''
    Function which finds propability on every character which can appear after some character/characters.
'''
def findPropabilities(text, offset):
    
    # Special dictionary which contains offset and
    # all propabilities on each character e.g. {'abc': {'a' : 0.25, 'b' : 0.02, ..}}.
    allCharPropability = {}

    # Calculate how many times special key appeared in given text and propability on character after this key.
    for i in range(offset, len(text)):
        
        # Check if special key was already in dictionary. 
        if text[i - offset : i] in allCharPropability.keys():
            
            # Check if second dictionary contains the character.
            if text[i] in allCharPropability[text[i - offset : i]].keys():
                allCharPropability[text[i - offset : i]][text[i]] += 1
            else:
                allCharPropability[text[i - offset : i]][text[i]] = 1
        else:
            allCharPropability[text[i - offset : i]] = {text[i] : 1}

    # Calcualte propability.
    for key in allCharPropability.keys():
        allCharPropabilitySum = sum(list(allCharPropability[key].values()))
        for char in allCharPropability[key].keys():
            allCharPropability[key][char] /= float(allCharPropabilitySum)
            
    # Return dictionary with proper propabilities.
    return allCharPropability

def main():

    # Run app with special arguments.
    if(len(sys.argv) == 4):
        filename =sys.argv[1]
        number = int(sys.argv[2])
        outputFile = sys.argv[3]
        showAll = ''
    else:
        filename =sys.argv[1]
        number = int(sys.argv[2])
        outputFile = sys.argv[3]
        showAll = '--all'

    # Text without digits and additional spaces.
    text = preprocessing(readFile(filename))

    # Alphabet + space.
    alphabet = list(string.ascii_lowercase) + [' ']

    # Open file to write output.
    file = open(outputFile, 'w')

    if(showAll == '--all'):

        # Information.
        print('\nRemember, if you do not see the propability it means that it is equal to 0.0.\n', file=file)

        # First task.
        print("\nAverange word length in first task:\n" + str(firstTask(deepcopy(alphabet), number)), file=file)

        # Get the dictionary from the second task. (We use it later).
        hist = secondTask(deepcopy(alphabet), deepcopy(text))

        # Second task.
        print("\nCalculated characters apperance in second task:\n" + str(hist), file=file)
        
        # Third task.
        print("\nAverange word length in third task:\n" + str(thirdTask(deepcopy(hist), number)), file=file)

        # Fourth task.
        first, second = fourthTask(deepcopy(text), deepcopy(hist))
        print("\nPropabilities calculated for fourth task:", file=file)
        print("\nPropabilities for first most used character:\n" + str(first), file=file)
        print("\nPropabilities for second most used character:\n" + str(second), file=file)
        
        # Close file.
        file.close()

        #Fifth task.
        fifthTask(deepcopy(text), number, outputFile, 'a')

    else:
        #Fifth task.
        fifthTask(deepcopy(text), number, outputFile, 'w')

    # Close file.
    file.close()

if __name__ == '__main__':
    main()