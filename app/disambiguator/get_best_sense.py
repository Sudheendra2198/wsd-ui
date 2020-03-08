"""
    Run this script as follows: python process.py
    It will output the result to files
    input_text.txt contains input words
    sans_stop_words.txt contains the input text after removing stop words
    final_output.txt contains the result
"""

import pyiwn
from googletrans import Translator
from app.disambiguator.stem import stem_words


""" Sysnet initialization to Telugu"""
iwn = pyiwn.IndoWordNet(lang=pyiwn.Language.TELUGU)

def translate_sentence(sentence):
    """ 
        Translate sentence into Telugu 
    """
    translated_res = []
    translator = Translator()
    return translator.translate(sentence,dest='te').text 

def get_stop_words_list():
    """ 
        Convert stop words as a list from the file - stop-words-tr.txt
    """
    stop_words = []
    with open('app/disambiguator/stop-words-tr.txt','r') as stop_word:
        for line in stop_word:
            stop_words.extend(line.split())
    return stop_words

def remove_stop_words(translated_sentence):
    """ 
        Remove stop words by comparing with stop words list
    """
    processed_words = []
    stop_words = get_stop_words_list()

    if isinstance(translated_sentence, list):
        words = translated_sentence
    else:
        words = translated_sentence.split()

    for word in words:
        if word not in stop_words:
            processed_words.append(word)
    return processed_words

def get_sense(processed_words):

    """
        This function takes proceesed words as input and returns best sense
        of every word.
        The algorithm applied is Lesk 
    """

    rem_synsets = []
    matcher = []
    max_cnt = 0
    max_sense = []
    stop_words = get_stop_words_list()
    op_dict = {}
    for word in processed_words:
        max_cnt = 0
        max_sense = iwn.synsets(word)[len(iwn.synsets(word)) - 1]
        cnt = 0

        # Get Synsets of current word
        curr_synsets = iwn.synsets(word,pos=pyiwn.PosTag.NOUN)

        # Get the remaining words and their synsets into rem_synsets
        rem_words = []
        rem_synsets = []
        for rem_word in processed_words:
            if rem_word != word:
                rem_words.append(rem_word)
        for rem_word in rem_words:
            rem_synsets.append(iwn.synsets(rem_word,pos=pyiwn.PosTag.NOUN))
        

        # For each synset of remaining words, 
        # generate a list of words from the meanings of the synset and its hyponyms
        # o/p : rem_to_match - list of words from the meanings of the synset and its hyponyms
        rem_to_match = []
        for synset in rem_synsets:
            for each_synset in synset:
                hyponyms = iwn.synset_relation(each_synset, pyiwn.SynsetRelations.HYPONYMY)
                for hyponym in hyponyms:
                    rem_to_match.extend(hyponym.gloss().split())
                rem_to_match.extend(each_synset.gloss().split())
        rem_to_match = remove_stop_words(rem_to_match)
        

        # For each synset of current word,
        # match the words from its meaning to all the words in rem_to_match
        # If count matches increment it and if it is maximum, it is taken as the sense
        for synset in curr_synsets:
            matcher = []
            cnt = 0
            hyponyms = iwn.synset_relation(synset, pyiwn.SynsetRelations.HYPONYMY)
            for hyponym in hyponyms:
                matcher.extend(hyponym.gloss().split())
            matcher.extend(synset.gloss().split())
            matcher = remove_stop_words(matcher)
            
            for matcher_word in matcher:
                if matcher_word in rem_to_match:
                    cnt += 1
            if cnt >= max_cnt:
                max_cnt = cnt
                max_sense = synset
        op_dict[word] = max_sense.gloss()
    return op_dict
 
def disambiguate(sentence):
    # sentence = "silk saree is beautiful"
    translated_text = translate_sentence(sentence)
    processed_words = remove_stop_words(translated_text)
    stemmed_words = stem_words(processed_words)
    return get_sense(stemmed_words)





















