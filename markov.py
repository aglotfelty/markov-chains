from random import choice
import sys

def open_and_read_file(file_path):
    """Takes file path as string; returns text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """
    contents = open(file_path).read()
    # your code goes here

    return contents


def make_chains(text_string):
    """Takes input text as string; returns _dictionary_ of markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> make_chains("hi there mary hi there juanita")
        {('hi', 'there'): ['mary', 'juanita'], ('there', 'mary'): ['hi'], ('mary', 'hi': ['there']}
    """

    chains = {}

    # your code goes here
    words = text_string.split()
    string_length = len(words)
    for index in range(string_length - 1):
        bi_gram = (words[index], words[index + 1])
        
        # Checking if we've hit the last two indices of the words list
        # Add [None] to list of values associated with the last tuple of words
        try:
            chains[bi_gram] = chains.get(bi_gram, []) + [words[index + 2]]
        except IndexError:
            chains[bi_gram] = chains.get(bi_gram, []) + [None]

    return chains

def make_n_gram_chains(text_string, n):
    """Takes input text as string and n as length of n_gram; 
    returns _dictionary_ of markov chains.

    A chain will be a key that consists of a tuple of (word1, word2, ... wordn)
    and the value would be a list of the word(s) that follow those n
    words in the input text.

    For example:

        >>> make_chains("hi there mary hi there juanita", 2)
        {('hi', 'there'): ['mary', 'juanita'], ('there', 'mary'): ['hi'], ('mary', 'hi': ['there']}
    """

    chains = {}

    # your code goes here
    words = text_string.split()
    string_length = len(words)
    for index in range(string_length - (n-1)):
        n_gram = tuple(words[index:index + n])

        # ALTERNATIVE SOLUTION:
        # n_gram = []
        # while len(n_gram) < n:
        #     n_gram.append(words[index])
        #     index += 1
        # n_gram = tuple(n_gram) 
        # post_while_loop_index = index  # index updated during while loop  
        # END ALTERNATIVE

        # Checking if we've hit the last n indices of the words list
        # Add [None] to list of values associated with the last tuple of words
        try:
            chains[n_gram] = chains.get(n_gram, []) + [words[index + n]]
        except IndexError:
            chains[n_gram] = chains.get(n_gram, []) + [None]

    return chains


def make_text(chains):
    """Takes dictionary of markov chains; returns random text."""

    # Choose a random tuple from list of keys
    link = choice(chains.keys())

    # Initialize the text string with the words in the chosen tuple
    text = link[0] + ' ' + link[1]

    # Add words to the text until reach next_word == None
    while True:
        word_options = chains[link]
        next_word = choice(word_options)
        # If next_word = None because it was the last value added to the dict
        if not next_word:
            break
        text += ' ' + next_word
        link = (link[1], next_word)

    return text

def make_n_gram_text(chains, cap_at_sentence=False):
    """Takes dictionary of markov chains; returns random text."""

    # Choose a random tuple from list of keys that starts with a capital letter
    while True:
        link = choice(chains.keys())
        if link[0][0].isupper():  # Check if first letter of first word in tuple is capital
            break

    # Initialize the text list 
    text = list(link)

    # Add words to the text until reach next_word == None
    while True:
        word_options = chains[link]
        next_word = choice(word_options)
        # If next_word = None because it was the last value added to the dict
        if not next_word:
            break
        text.append(next_word)
        if cap_at_sentence:
            if next_word[-1] in ".!?":
                break 
        link = link[1:] + (next_word,) # Turn link into a list to add next_word
        # link = tuple(link) # Change link list back into a tuple

    text = " ".join(text) # Turn list into a string separated by spaces

    return text

def generate_phrase(chains, char_length=140):
    """Generates a random phrase of given character length (default is 140)"""

    phrase = ""
    tries = 0

    while tries < 200:
        sentence = make_n_gram_text(chains, True)
        tries += 1
        if len(sentence) <= char_length:
            phrase += sentence + " "
            char_length = char_length - len(sentence) - 1
            if char_length == 0:
                break
        else:
            continue
       
    return phrase.strip()

def make_a_phrase(chains, char_length=140):
    """Takes a markov dictionary and tries to create phrase at specified length"""

    # Make sure origin sentence is within character count limit
    while True:
        sentence = make_n_gram_text(chains, cap_at_sentence=True)
        if len(sentence) <= char_length:
            break
        else:
            continue

    # Create variables for origin sentence words & tuple
    origin_sentence_words = sentence.split(" ")
    origin_tuple = tuple(origin_sentence_words[-2:])
    tries = 0

    # If the sentence is less than character length, 
    # try to generate a second sentence within limits
    
    words_in_sentence = sentence.split(" ")
    last_two_words = tuple(words_in_sentence[-2:])

    while tries < 200:
        word_options = chains[last_two_words]
        next_word = choice(word_options)
        tries += 1
        
        # If next_word = None because it was the last value added to the dict
        if not next_word:
            break
        
        words_in_sentence.append(next_word)
        
        # Return phrase if it ends in punctuation
        if next_word[-1] in ".!?":
            phrase = " ".join(words_in_sentence)  # Turn list into a string separated by spaces
            if len(phrase) <= char_length:
                return phrase
            # If new phrase is too long, try again with a new sentence starting with origin info
            else:
                last_two_words = origin_tuple
                words_in_sentence = origin_sentence_words
                continue
        last_two_words = last_two_words[1:] + (next_word,) # Create new tuple
                 
    return sentence          



# Return a random element from the non-empty sequence seq. If seq is empty, raises IndexError.
# input_path = "gettysburg.txt"
input_path = sys.argv[1]

# Open the file and turn it into one long string
input_text = open_and_read_file(input_path)

# Get a Markov chain 
# chains = make_chains(input_text)

# Get a Markov chain 
chains = make_n_gram_chains(input_text, 2)

# Produce random text
# random_text = make_text(chains)

# Produce random text with n_gram
random_text = make_n_gram_text(chains, True)

# Produce random phrase of given character length
# print generate_phrase(chains)
print make_a_phrase(chains)

#print random_text
