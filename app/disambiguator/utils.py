import pyiwn
from googletrans import Translator

from app.disambiguator.stem import stem_words

iwn = ""

map_languages = {
    'Language.BENGALI' : pyiwn.Language.BENGALI,
    'Language.GUJARATI' : pyiwn.Language.GUJARATI,
    'Language.HINDI' : pyiwn.Language.HINDI,
    'Language.KANNADA' : pyiwn.Language.KANNADA,
    'Language.MALAYALAM' : pyiwn.Language.MALAYALAM,
    'Language.MARATHI' : pyiwn.Language.MARATHI,
    'Language.NEPALI' : pyiwn.Language.NEPALI,
    'Language.PUNJABI' : pyiwn.Language.PUNJABI,
    'Language.TAMIL' : pyiwn.Language.TAMIL,
    'Language.TELUGU': pyiwn.Language.TELUGU,
    'Language.URDU' : pyiwn.Language.URDU,
}


def get_languages():
    languages = []
    languages_list = list((pyiwn.Language))
    return languages_list

def stemmer(processed_words):
    return stem_words(processed_words)

def get_synsets(word, language):
    global iwn
    iwn = pyiwn.IndoWordNet(lang=map_languages[language])
    return iwn.synsets(word)

def get_gloss(synset):
    return synset.gloss()

def get_hyponyms(synset):
    global iwn
    return iwn.synset_relation(synset, pyiwn.SynsetRelations.HYPONYMY)

def translate(word, language):
    translator = Translator()
    return translator.translate(word,dest=language[9 : ].lower()).text 