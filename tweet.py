import twitter
import markov
import os
import sys

api = twitter.Api(consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
                  consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
                  access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
                  access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

print(api.VerifyCredentials())


input_path = sys.argv[1]

# Open the file and turn it into one long string
input_text = markov.open_and_read_file(input_path)


# Get a Markov chain
chains = markov.make_n_gram_chains(input_text, 2)

while True:
    # Produce random phrase of given character length
    # print generate_phrase(chains)
    tweet = markov.make_a_phrase(chains)

    # Send a tweet:
    status = api.PostUpdate(tweet)
    print status.text
    print "Would you like to Tweet again? (If yes press Enter, if no, press q: "
    answer = raw_input(">> ")
    if answer == "":
        continue
    else:
        break