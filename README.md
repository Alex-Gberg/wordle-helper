# Wordle Helper
> This terminal based program helps you with solving wordle puzzles by showing all the possibile words given your previous guesses

## Table of Contents
* [General Information](#general-information)
* [Technologies Used](#technologies-used)
* [Features](#features)
* [Setup](#setup)
* [Usage](#usage)
* [Project Status](#project-status)
* [Room for Improvement](#room-for-improvement)
* [Acknowledgements](#acknowledgements)


## General Information
- This program does not solve wordle puzzles on its own, nor does it tell you what to guess next
- Instead, after each guess it shows you a list of all the words that could possibly be the final solution
- This can help you to choose a next guess or may reveal the answer once enough letters are known

## Technologies used
- Python 3.8.10

## Features
- Input your guesses and the resulting colors through the terminal
- Receive a list of possible solutions
- Filter this list down to only the words that appear in the dictionary

## Setup
- Use `python3 wordleHelper.py` to run the program

## Usage
- Follow the prompts and fill in the information requested in the terminal
- You will first be asked to input the word that you guessed
- Then you will be asked the color of each letter
- You'll then be told how many possibilities of solutions still exist and asked whether or not you want to display them all
- This list can then optionally be filtered down to only those that exist in the dictionary (It checks at about 60 words/second so be aware that large lists may take several minutes)
- Finally you'll be asked whether to display this list
- This process repeats until the game is over

## Project Status
This project is complete but I may use parts of it in future wordle projects, perhaps one that provides the best next guess

## Room for Improvement
- Retrieve user guesses and letter colors automatically:
    - At the moment the manual input can be slow and annoying. It would be great if this information was retrieved from the game's html.
- Prettier interface:
    - The terminal interface can become hard to read, especially with huge lists of words being displayed.

## Acknowledgements
- The list of English words `filtered_words.txt` comes from [here](https://github.com/dwyl/english-words) and was filtered using [pyenchant](https://pypi.org/project/pyenchant/)
