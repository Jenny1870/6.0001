# Hangman With Hints
# -----------------------------------

import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------


# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()

# -----------------------------------


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    win = True
    for letter in secret_word:
        if letter not in letters_guessed:
            win = False
    return win


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    guessed_word = []                           #creates a list that shows letters and _ for letters we have yet to guess
    for letter in secret_word:                  #iterates through each character in computers word
        if letter not in letters_guessed:       #for every character in computers word that has not been guessed yet
            guessed_word.append('_ ')           #place an _
        else:                                   #if character has been guessed
            guessed_word.append(letter)         #place that character there
    return ''.join(guessed_word)                #makes the list into a string


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    alphabet = list(string.ascii_lowercase)     #imports lowercase alphabet and turns it into a list
    for letter in alphabet[:]:                  #for every character in a copy of the alphabet list
        if letter in letters_guessed:           #if character has been guessed
            alphabet.remove(letter)             #remove charcter from original list
    return ' '.join(alphabet)                   #makes the list into a string, separated by spaces



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word

    other_word: string, regular English word
    
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        
        False otherwise: 
    '''
    my_word_list = list(my_word)
    other_word_list = list(other_word)
    
    for char in my_word_list[:] :
        if char == ' ' :
            my_word_list.remove(char)                                       #removes spaces between underscores
            
    match = True
    if len(my_word_list) != len(other_word_list) :                          #do word length match?
        match = False
    else :                                                                  #if lengths do match
        for char_index in range(len(my_word_list)) :                        #take the index
            if my_word_list[char_index] != '_' :                            #just looking at letters
                if my_word_list[char_index] != other_word_list[char_index]: #is letter in both words?
                    match = False
            else:                                                           #if letter is in both words
                if other_word_list[char_index] in my_word_list:             #if letter in computers word is already somewhere in my word, then it can't be a match
                    match = False
    return match


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    matches = []

    for other_word in wordlist :                        #pulls words from wordlist
        if match_with_gaps(my_word, other_word) :       #that matches the word we've guessed so far with gaps
            matches.append(other_word)                  #adds those words to the list we made called matches

    if len(matches) == 0 :                              #if no words match
        print('No matches found')
    
    return ' '.join(matches)                           #returns the list matches, separated by spaces


def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''

    # Startup message
    secret_word = choose_word(wordlist)
    guessesleft = 6
    letters_guessed = [] 
    warnings = 3
    
    print('--------------------------------------------------------------------------------\n\n\n\nWelcome to the game Hangman!\n\nI am thinking of a word that is',len(secret_word),
          'letters long.',get_guessed_word(secret_word, letters_guessed),'\n\nYou get 6 guesses and',warnings,'warnings.\n\nIf you need a hint type an asterick (*).\n\nAvailable letters:',get_available_letters(letters_guessed))

   
    # Game loop
    
    while not is_word_guessed(secret_word, letters_guessed) and guessesleft > 0 :

        print('\n',get_guessed_word(secret_word, letters_guessed))
        guess = (input('\n\nPlease guess a letter: ').lower())
        print('\n----------------------------------------\n')
        
        if guess == '*' :
            print('Possible word matches are:\n',show_possible_matches(get_guessed_word(secret_word, letters_guessed)))
        
        if guess not in string.ascii_letters and guess != '*' :
            if warnings > 0 :
                warnings -= 1
                print('\nOops! That is not a valid letter. You lose a warning.\nYou have',warnings,'warnings left.\n\nYou have',guessesleft,'guesses left.\nAvailable letters:',get_available_letters(letters_guessed))
                
            else:
                guessesleft -= 1
                if guessesleft > 0 :
                    warnings = 0
                    print('\nOops! That is not a valid letter.\n\nYou have no warnings left, so you lose one guess.',get_guessed_word(secret_word, letters_guessed),'\n\nYou have',guessesleft,'guesses left.\nAvailable letters:',get_available_letters(letters_guessed))
                else:
                    print('\nOops! That is not a valid letter.\n\nYou have no warnings left, so you lose one guess.',get_guessed_word(secret_word, letters_guessed),'\n\nYou have',guessesleft,'guesses left.')
                
        elif guess in letters_guessed :
            if warnings > 0 :
                warnings -= 1
                print('\nOops! You\'ve already guessed that letter. You lose a warning.\n\nYou have',warnings,'warnings left.\n\nYou have',guessesleft,'guesses left.\nAvailable letters:',get_available_letters(letters_guessed))
                
            else:
                guessesleft -= 1
                if guessesleft > 0 :
                    warnings = 0
                    print('\nOops! You\'ve already guessed that letter.\n\nYou have no warnings left, so you lose one guess.',get_guessed_word(secret_word, letters_guessed),'\n\nYou have',guessesleft,'guesses left.\nAvailable letters:',get_available_letters(letters_guessed))
                else:
                    print('\nOops! You\'ve already guessed that letter.\n\nYou have no warnings left, so you lose one guess:',get_guessed_word(secret_word, letters_guessed),'\n\nYou have',guessesleft,'guesses left.')
            
        elif guess != '*' :
            letters_guessed.append(guess)
            if guess in secret_word :
                if is_word_guessed(secret_word, letters_guessed) :
                    print('\nGood guess:',get_guessed_word(secret_word, letters_guessed),'\n')
                else:
                    print('\nGood guess:',get_guessed_word(secret_word, letters_guessed),'\n\nYou have',guessesleft,'guesses left.\nAvailable letters:',get_available_letters(letters_guessed))
                
            else :
                guessesleft -= 1
                if guessesleft > 0 :
                    print('\nOops! That letter is not in my word:',get_guessed_word(secret_word, letters_guessed),'\n\nYou have',guessesleft,'guesses left.\nAvailable letters:',get_available_letters(letters_guessed))
                else:
                    print('\nOops! That letter is not in my word:',get_guessed_word(secret_word, letters_guessed),'\n\nYou have',guessesleft,'guesses left.')
                
    
    # Exit Game Loop
   
    if guessesleft == 0 :
        print('\nSorry, you ran out of guesses. The word was',secret_word + '.')
    else:
        print('\nCongratulations, you won!\n\n''Your total score for this game is: ',guessesleft * len(set(secret_word)) )
 



if __name__ == "__main__":

    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)