import re
from tqdm import tqdm
import enchant

def displayList(list):
    for i, x in enumerate(list):
        print(x, end=", ") if i != len(list)-1 else print(x)

def getGuessManual(i):
    guess = input(f"Input your guess #{i}: ").strip().lower()
    while (not guess.isalpha()) or (len(guess) != 5):
        print("Your guess has to be a 5 letter word!")
        guess = input(f"Input your guess #{i}: ")

    return guess

def getLetterColorsManual(guess):
    letterColors = [-1 for _ in range(len(guess))]

    for i in range(len(guess)):
        value = -1
        while value < 0 or value > 2:
            try:
                value = int(input(f"Color of {guess[i]}? (0=grey, 1=orange, 2=green): "))
                if value < 0 or value > 2:
                    print("Invalid input! Input either 0, 1, or 2!")

            except ValueError:
                print("Invalid input! Input either 0, 1, or 2!")

        letterColors[i] = value

    return letterColors

def processGuess(guess, letterColors, possibleLetters, mustInclude, totalNumFound):
    containsNonGreens = False
    numPresent = {}
    orangePresent = set()
    for i, c in enumerate(guess):
        if letterColors[i] == 0:
            containsNonGreens = True
            if c in orangePresent:
                possibleLetters[i] = possibleLetters[i].replace(c, "")
            else:
                for j in range(len(possibleLetters)):
                    if len(possibleLetters[j]) != 1:
                        possibleLetters[j] = possibleLetters[j].replace(c, "")
            
            totalNumFound.add(c)

        elif letterColors[i] == 1:
            containsNonGreens = True
            possibleLetters[i] = possibleLetters[i].replace(c, "")
            orangePresent.add(c)
            if c in numPresent:
                numPresent[c] += 1
            else:
                numPresent[c] = 1

        elif letterColors[i] == 2:
            possibleLetters[i] = c
            if c in numPresent:
                numPresent[c] += 1
            else:
                numPresent[c] = 1

    for key in numPresent:
        mustInclude[key] = max(numPresent[key], mustInclude[key])

    return not containsNonGreens

def makeRePattern(possibleLetters, mustInclude, totalNumFound):
    patternString = ""
    for x in range(97, 123):
        if mustInclude[chr(x)] > 0:
            surroundingVal = ".*" if chr(x) not in totalNumFound else makeRangeExcluding(chr(x)) + "*"
            patternString += f"(?=^{surroundingVal}"
            for _ in range(mustInclude[chr(x)]):
                patternString += chr(x) + surroundingVal
            patternString += "$)"
    patternString += "^"
    for x in possibleLetters:
        patternString += f"[{x}]"
    patternString += "$"

    return re.compile(patternString)

def makeRangeExcluding(c):
    if c == "a":
        return "[b-z]"
    if c == "z":
        return "[a-y]"
    
    return "[a-" + chr(ord(c)-1) + chr(ord(c)+1) + "-z]"

def findPossibilities(pattern):
    possibilities = []
    with open("words_alpha.txt") as wordList:
        for word in wordList:
            if re.match(pattern, word):
                possibilities.append(word.strip())

    return possibilities

def filterWithDictionary(possibilities):
    realPossibilities = []
    numEliminated = 0
    pbar = tqdm(possibilities)
    for p in pbar:
        pbar.set_description(f"Words eliminated: {numEliminated}")
        if enchant.Dict("en_US").check(p):
            realPossibilities.append(p)
        else:
            numEliminated += 1

    return realPossibilities

def manualWordleHelper():
    possibleLetters = ["abcdefghijklmnopqrstuvwxyz" for x in range(5)]
    mustInclude = {chr(x):0 for x in range(97, 123)}
    totalNumFound = set()

    for i in range(1, 7):
        guess = getGuessManual(i)
        letterColors = getLetterColorsManual(guess)
        if processGuess(guess, letterColors, possibleLetters, mustInclude, totalNumFound):
            print(f"Congrats! You found the word: {guess}")
            return 1

        pattern = makeRePattern(possibleLetters, mustInclude, totalNumFound)
        possibilities = findPossibilities(pattern)

        print(f"Number of possibilities: {len(possibilities)}")
        if input("Show possibilites? (y/n): ") == "y":
            displayList(possibilities)

        if input(f"Narrow down with dictionary? WARNING ~60 searches/sec! (y/n): ") == "y":
            realPossibilities = filterWithDictionary(possibilities)
            print(f"Number of possibilities in the dictionary: {len(realPossibilities)}")
            if input("Show possibilites? (y/n): ") == "y":
                displayList(realPossibilities)

    print("GAME OVER!")
    return -1


if __name__ == "__main__":
    manualWordleHelper()
