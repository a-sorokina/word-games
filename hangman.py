# Problem Set 2, hangman.py

# The file contains two variations of the game: with and without hints


from curses.ascii import isalpha
import random
import string
from xmlrpc.client import Boolean

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
  
    inFile = open(WORDLIST_FILENAME, 'r')
    line = inFile.readline()
    wordlist = line.split()
    return wordlist

wordlist = load_words()


def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    letters_in_word = set(secret_word)
    return letters_in_word.issubset(letters_guessed)


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    letters_in_word = list(secret_word)
    guessed_word = []
    for item in letters_in_word: 
      guessed_word.append('_ ')
    
    list_of_index = []

    for item in letters_guessed:
      guessed_letter = item
      for (index, item) in enumerate(letters_in_word):
        if item == guessed_letter:
          guessed_word = guessed_word[:index]+[item]+guessed_word[index+1:]
  

    return guessed_word
  

def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    available_letters = string.ascii_lowercase

    for item in letters_guessed: 
      available_letters = available_letters.replace(item, "")

    return available_letters


def is_good_guess(letter, secret_word):
  if letter in secret_word: 
    return True
  else:
    return False


def no_warnings(number_of_warnings)->Boolean:
    if number_of_warnings == 0: 
      return True
    else: 
      return False 
     

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''

    print('Welcome to the game Hangman!')
    print(f'I am thinking of a word that is {len(secret_word)} letters long.')
    number_of_guesses = 6
    number_of_warnings = 3

    letters_guessed = []

    while number_of_guesses > 0:
      if number_of_guesses == 1: 
        print (f'You have {number_of_guesses} guess left.')
      else: 
        print(f'You have {number_of_guesses} guesses left.')

      input_guess = input('Please guess a letter: ').lower()

      if not input_guess.isalpha():
        if not no_warnings(number_of_warnings): 
          number_of_warnings -= 1 
          if number_of_warnings != 1:
            print(f'Invalid input, please only use latin letters, one per time. You have {number_of_warnings} warnings left.')
          else:
            print(f'Invalid input, please only use latin letters, one per time. You have {number_of_warnings} warning left.')
        else: 
          number_of_guesses -= 1 
          print(f'Invalid input, please only use latin letters, one per time.')
        continue

      if input_guess in letters_guessed: 
        if not no_warnings(number_of_warnings): 
          number_of_warnings -= 1
          if number_of_warnings != 1:
            print(f'You have already tried this letter. You have {number_of_warnings} warnings left.')
          else: 
            print(f'You have already tried this letter. You have {number_of_warnings} warning left.')       
        else: 
          number_of_guesses -=1 
          print(f'You have already tried this letter.')
        continue
 
      letters_guessed.append(input_guess)
      if not is_good_guess(input_guess, secret_word): 
        print('This letter is not in the secret word.')
        if input_guess in ['a', 'o', 'i', 'u', 'e']: 
          number_of_guesses -= 2
        else: 
          number_of_guesses -= 1

      print(f'Available letters: {get_available_letters(letters_guessed)}')
      print(' '.join(get_guessed_word(secret_word, letters_guessed)))
      
        
      if is_word_guessed(secret_word, letters_guessed): 
        final_string = ''.join(get_guessed_word(secret_word, letters_guessed))
        print(f'Congratulations! The secret word is {final_string}. Your score is {number_of_guesses*len(set(secret_word))}')
        break
      
      print('-----------------------')

    if not is_word_guessed(secret_word, letters_guessed): 
      print('Sorry! The secret word was', secret_word)

    return 

#hangman(choose_word(load_words()))
#hangman('apple')


def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    hidden_letters = []
    guessed_word = my_word.replace(" ", "")
    if len(guessed_word) == len(other_word):
      zipper = zip(guessed_word, other_word)

      for tuple in zipper:
        if tuple[0] == '_':
          hidden_letters += tuple[1]
        elif tuple[0] == tuple[1]:
          continue
        else:
          return False 
      for letter in hidden_letters:
        if letter in guessed_word:
          return False
      else:
        return True
    else:
      return False
           

def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    matching_words = []
    for word in wordlist:
      if match_with_gaps(my_word, word):
        matching_words.append(word)
    if not matching_words:
      return 'no matching words'
    return matching_words
   

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

    print('Welcome to the game Hangman!')
    print(f'I am thinking of a word that is {len(secret_word)} letters long.')
    number_of_guesses = 6
    number_of_warnings = 3

    letters_guessed = []

    while number_of_guesses > 0:
      if number_of_guesses == 1: 
        print (f'You have {number_of_guesses} guess left.')
      else: 
        print(f'You have {number_of_guesses} guesses left.')

      input_guess = input('Please guess a letter: ').lower()

      if not input_guess.isalpha():
        if input_guess == '*':
          print(show_possible_matches(ham))

        elif not no_warnings(number_of_warnings): 
          number_of_warnings -= 1 
          if number_of_warnings != 1:
            print(f'Invalid input, please only use latin letters, one per time. You have {number_of_warnings} warnings left.')
          else:
            print(f'Invalid input, please only use latin letters, one per time. You have {number_of_warnings} warning left.')
        else: 
          number_of_guesses -= 1 
          print(f'Invalid input, please only use latin letters, one per time.')
        continue

      if input_guess in letters_guessed: 
        if not no_warnings(number_of_warnings): 
          number_of_warnings -= 1
          if number_of_warnings != 1:
            print(f'You have already tried this letter. You have {number_of_warnings} warnings left.')
          else: 
            print(f'You have already tried this letter. You have {number_of_warnings} warning left.')       
        else: 
          number_of_guesses -=1 
          print(f'You have already tried this letter.')
        continue
 
      letters_guessed.append(input_guess)
      if not is_good_guess(input_guess, secret_word): 
        print('This letter is not in the secret word.')
        if input_guess in ['a', 'o', 'i', 'u', 'e']: 
          number_of_guesses -= 2
        else: 
          number_of_guesses -= 1

      print(f'Available letters: {get_available_letters(letters_guessed)}')
      ham = ' '.join(get_guessed_word(secret_word, letters_guessed))
      print(ham)
      
        #letters_guessed.append(input_guess.lower())

      #print(letters_guessed)
        
      if is_word_guessed(secret_word, letters_guessed): 
        final_string = ''.join(get_guessed_word(secret_word, letters_guessed))
        print(f'Congratulations! The secret word is {final_string}. Your score is {number_of_guesses*len(set(secret_word))}')
        break
      
      print('-----------------------')

    if not is_word_guessed(secret_word, letters_guessed): 
      print('Sorry! The secret word was', secret_word)

    return 
    
#hangman_with_hints('apple')    
hangman_with_hints(choose_word(load_words()))
