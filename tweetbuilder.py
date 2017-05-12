# coding: utf-8

import nltk
from bs4 import BeautifulSoup
import wget

def getSources(url):
    '''
    downloads the html-files containing the subchapters of a book in the Marx-Engels-Werke into a folder html (building this folder in the current working directory), 
    using ordinal numbers for filenames so the correct order of the files can be kept.
    takes one argument, namely the URL for a bookpage that lists all its subchapters, e.g. http://www.dearchiv.de/php/brett.php?archiv=mew&brett=MEW023&menu=mewinh 
    '''
    
    base_url = 'http://www.dearchiv.de/php/'
    with open(url, 'r') as linkfile:
        html = linkfile.read()
    soup = BeautifulSoup(html, 'lxml')
    linkliste = []
    for link in soup.find_all('a'):
        if link.get('href') != None:
            linkliste.append(link.get('href'))
    del linkliste[0], linkliste[-1]                # remove the links for site navigation
    for i in range(len(linkliste)):
        wget.download(base_url + linkliste[i], out='html/' + str(i).zfill(3) + '.html')
    
    print('Done! All files have been downloaded to the folder html and are ready for further processing.')



def sentences2tweets(satzliste):
    '''
    takes in a list of sentences and then groups these sentences sequentially, then
    returns a list of sentences or groups of sentences, where each element of the list has 140 characters max.
    '''
    tweets = []
    count = 1
    tweet = ''
    while count < len(satzliste) - 1:
        if len(tweet) + len(satzliste[count]) <= 140:
            tweet = satzliste[count]
            if count < len(satzliste) - 1:
                count += 1
                print count, len(satzliste) 
                if len(tweet) + len(satzliste[count]) < 140:
                    tweet += ' ' + satzliste[count]
                    if count < len(satzliste) - 1:
                        count += 1
                
                        if len(tweet) + len(satzliste[count]) < 140:
                            tweet += ' ' + satzliste[count]
                            if count < len(satzliste) -1:
                                count += 1
            
            tweets.append(tweet)
            tweet = ''
        else:
            if count < len(satzliste) -1:
                count += 1
    return tweets




def tweets2file(tweetlist, outfile='marxtweets'):
    '''
    writes a list of tweets into the marxtweets file
    '''
    with open(outfile, 'a') as tweetfile:
        for tweet in tweetlist:
            tweetfile.write(tweet.encode('utf8'))
            tweetfile.write('\n')


def beautify(tweet):
    '''
    deletes linebreaks and the all too many spaces
    '''
    return tweet.replace('-\r\n       ', '').replace('\r\n      ', '').replace('   ', ' ').replace('  ', ' ')


def tweetify(htmlfile, tweetfile='marx.tweets'):
    '''
    takes a html-file (subchapter, the files that include the actual texts) from the mew (http://www.dearchiv.de/php/mewinh.php) and 
    writes all sentences or groups of sentences with a length of less than 140 characters to the given textfile, one tweet per line. 
    If two or three sentences joined together count less than 140 characters, they will be joined.
    '''
    print("Loading html-file" + htmlfile + '.')

    with open(htmlfile, 'r') as source:   # read the contents of the html file into a variable
        html = source.read()

    soup = BeautifulSoup(html, 'lxml')  # make the soup
    
    print("Extracting text and building tweets from file.")

    text = ''               # extract the actual text from the file
    for string in soup.tt.strings:
        text += string

    text = text[15:-10]     # remove the 'zurück' buttons

    satzliste = nltk.sent_tokenize(text, language = 'german')   # split the text into a list of sentences, using the nltk tokenizer
    
    satzliste = [beautify(satz) for satz in satzliste]          # remove linebreaks and whitespace overkill
    print ("Der Text besteht aus " + str(len(satzliste)) + " Sätzen.")

    tweets = sentences2tweets(satzliste)                        # use the function defined above to make a list of tweets
    print('Im Text stecken ' + str(len(tweets)) + ' Tweets.')
    tweets2file(tweets, tweetfile)                              # write the tweets to the specified file, one tweet per line

    print("Done! The text has been sucessfully tweetified and saved as " + tweetfile + ".")

