
## marxbot, tweetifying Das Kapital, Erster Band

This is the code and data I have used and produced while working on a twitterbot that tweets Karl Marx' book *Das Kapital*, Volume 1. You can check it out at <http://twitter.com/K_rlM_rx>.

The bot sends a tweet once per hour, using sentences or sentence groups with 140 characters max. If two sequential sentences together have less than 140 characters, they are grouped into one tweet. Tweets consist of one or more complete sentences, ergo: Sentences with more than 140 characters have been omitted. The tweets follow the linear order of the source text.

- marxbot.py: the actual script that is run on a server as a cronjob, once per hour, expects the following Python modules: tweepy, linecache
- kapital.tweets: the tweetified book as a list of tweets (single sentences or groups of sentences with 140 characters max)
- tweetbuilder.py: the functions used to download and process the text (preprocessing, tweetification) and finally build kapital.tweets, expects the following Python modules: nltk, bs4, wget

If you want to use these scripts to build your own bot, feel free to do so. But be advised that the degree of automation is not very high, meaning you will have to take a look at the tweetbuilder scripts and use the functions in your python console (e.g. Ipython). Once you have built the tweetfile, you need to register the program as an app with twitter and fill in your credentials in marxbot.py. See the [tweepy documentation](https://tweepy.readthedocs.io/en/v3.5.0/auth_tutorial.html) and the [twitter API docs](https://dev.twitter.com/overview/api) for more advice and technical background.



