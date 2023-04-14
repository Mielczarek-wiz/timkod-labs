import sys

from random import choices
from copy import deepcopy

'''
    Opennig file with filename and return content.
'''
def readFile(filename):
    with open(file=filename, encoding='utf-8') as file:
        return file.read()
''' 
    First task was to calculate propabilities for every word in given text.
'''
def firstTask(text):
    
    words = {}

    # Split text.
    text = text.split()

    # Counts how many times special word is appeared in given text.
    for word in text:
        if word in words.keys():
            words[word] += 1
        else:
            words[word] = 1
    
    # Calculate propability.
    for key in words.keys():
        words[key] /= len(text)

    # Return dictionary with propabilities.
    return words

'''
    Function which generate text (number words) based on propabilities and given starded text.
'''
def generateText(allPropabilities, number, startedWord = '', offset = 1):

    # If started word is not empty..
    if startedWord != '' and offset != 1:

        # ..check that in our propabilities exists key (or keys) which first word is like started word..
        specialDict = {}
        for key in allPropabilities.keys():
            if startedWord == key.split()[0]:
                specialDict[key] = allPropabilities[key]

        # ..and if it exists take words (key) with this word..
        if len(specialDict) != 0:
            newText = list(choices(population = list(specialDict.keys()), k = 1))
        # ..and if it not exists take start word and put it before random key from our propabilities (with equal propabilities).
        else:
            newText = [startedWord] + list(choices(population = list(allPropabilities.keys()), k = 1))

    # If his is the first order approximation and started word is not empty.
    elif startedWord != '' and offset == 1:
         newText = [startedWord]

    # If started text is empty take random key from our propabilities (with equal propabilities).
    else:
        newText = list(choices(population = list(allPropabilities.keys()), k = 1))

    # Convert newText to corect format (list of words).
    newText = (' '.join(newText)).split()

    # Generate text.
    for i in range(len(newText), number):

        tempKey = ' '.join(newText[i - offset : i])

        # Get random word.
        newText.append(*choices(population = list(allPropabilities[tempKey].keys()), weights = list(allPropabilities[tempKey].values()), k = 1))
        

    # Return generated text.
    return ' '.join(newText)

'''
    Function which calculate all propabilities based on offset.
'''
def getAllPropabilities(text, offset = 1):

    allPropabilities = {}

    # Split text
    text = text.split()

    # Calculate how many times word/words appeared in given text.
    for i in range(len(text) - offset):
        tempKey = ' '.join(text[i:i + offset])

        # Calculate sum and group it in dict like {str: {str : NUM}}
        if tempKey in allPropabilities:
            if text[i + offset] in allPropabilities[tempKey]:
                allPropabilities[tempKey][text[i + offset]] += 1
            else:
                allPropabilities[tempKey][text[i + offset]] = 1
        else:
            allPropabilities[tempKey] = {text[i + offset] : 1}

    # Calculate propabilities.    
    for key in allPropabilities.keys():
        sumOfWords = sum(allPropabilities[key].values())
        for word in allPropabilities[key].keys():
            allPropabilities[key][word] /= sumOfWords
    
    # Return dictionary with propabilities.
    return allPropabilities
'''
    Task two (and one task from task three) was to generate text based on first order approximation.
'''
def taskTwoAndThreePointOne(text, number):

    # Get all propabilities.
    allPropabilities = getAllPropabilities(deepcopy(text))

    # Get generated text.
    generatedText = generateText(allPropabilities, number)

    # Return generated text.
    return generatedText

'''
    Task three was to generate text based on second order approximation.
'''
def taskThree(text, number):

    # Get all propabilities.
    allPropabilities = getAllPropabilities(deepcopy(text), offset = 2)

    # Get generated text.
    generatedText = generateText(allPropabilities, number, startedWord = 'propability', offset = 2)

    # Return generated text.
    return generatedText

# Main function with given args.
def main():

    filename = str(sys.argv[1])

    number = int(sys.argv[2])
    
    outputFile = str(sys.argv[3])

    text = readFile(filename=filename)

    # Open file to write output.
    file = open(outputFile, 'w')

    if (len(sys.argv) > 4 and sys.argv[4] == '--all'):
        words = firstTask(deepcopy(text))
        print('\nPropabilites generated in first task:\n', file = file)
        print(words, file = file)

        generatedText = taskTwoAndThreePointOne(deepcopy(text), number = number)
        print('\nText generated for task two and three (first order approximation):\n', file = file)
        print(generatedText, file = file)

        generatedText = taskThree(deepcopy(text), number = number)
        print('\nText generated for task two and three (second order approximation):\n', file = file)
        print(generatedText, file = file)
    else:
        generatedText = taskTwoAndThreePointOne(deepcopy(text), number = number)
        print('\nText generated for task two and three (first order approximation):\n', file = file)
        print(generatedText, file = file)

        generatedText = taskThree(deepcopy(text), number = number)
        print('\nText generated for task two and three (second order approximation):\n', file = file)
        print(generatedText, file = file)
    
    file.close()

if __name__ == '__main__':
    main()