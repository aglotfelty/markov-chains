from random import choice


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

# Return a random element from the non-empty sequence seq. If seq is empty, raises IndexError.
input_path = "green-eggs.txt"

# Open the file and turn it into one long string
input_text = open_and_read_file(input_path)

# Get a Markov chain 
chains = make_chains(input_text)

# Produce random text
random_text = make_text(chains)

print random_text
