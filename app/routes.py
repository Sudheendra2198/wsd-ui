from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm
from app.disambiguator.get_best_sense import (
    disambiguate,
    translate_sentence,
    remove_stop_words,
    get_sense
)

from app.disambiguator.utils import (
    get_languages,
    stemmer,
    get_synsets,
    get_gloss,
    get_hyponyms,
    translate
)

# global variables across pages
synset_map = {}
last_synsets = {}
last_word = ""

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        op = disambiguate(form.username.data)
        flash(op)
        return redirect(url_for('index'))
    return render_template('login.html', title = 'disambiguate', form = form)

@app.route('/wsd_index', methods=['GET', 'POST'])
def wsd_index():
    return render_template('login.html', title = 'disambiguate')

@app.route('/wsd_process', methods=['GET', 'POST'])
def wsd_process():
    sentence = request.form['sentence']
    flash(sentence)
    translated = translate_sentence(sentence)
    sans_stop_words = remove_stop_words(translated)
    stemmed_words = stemmer(sans_stop_words)
    output = get_sense(stemmed_words)
    return render_template('display.html', 
        translated = translated,
        processed = sans_stop_words,
        stemmed_words = stemmed_words,
        output = output,
        title = 'disambiguate'
    )

@app.route('/iwn_index', methods=['GET', 'POST'])
def iwn_index():
    page = 'wordnet'
    languages = get_valid_languages()
    return render_template('iwn_index.html', title='iwn', languages = languages, page = page)

@app.route('/iwn_process/<string:selected_synset>', methods=['GET', 'POST'])
def iwn_process(selected_synset):
    global synset_map, last_synsets, last_word
    language = []
    word = ""
    translated_word = ""
    synsets = ""
    page = "synset"
    gloss = []
    hyponyms = []

    if (selected_synset == 'display'):
        language = request.form['language']
        word = request.form['word']
        translated_word = translate(word, language)
        synsets = get_synsets(translated_word, language)

        last_synsets = synsets
        last_word = word

        for synset in synsets:
            synset_map[str(synset)] = synset
    elif (selected_synset == 'navbar'):
        synsets = last_synsets
        word = last_word
    else:
        gloss = get_gloss(synset_map[selected_synset])
        hyponyms = get_hyponyms(synset_map[selected_synset])
        page = 'gloss'


    return render_template('iwn_process.html', title = 'iwn',
                            word = word,
                            language = language,
                            synsets = synsets,
                            selected_synset = selected_synset,
                            gloss = gloss,
                            hyponyms = hyponyms,
                            translated_word = translated_word,
                            page = page
                        )
                
@app.route('/translate', methods = ['GET','POST'])
def translate_index():
    languages = get_valid_languages()
    return render_template('translate.html', title='translate', languages = languages)

@app.route('/translate_process', methods = ['GET','POST'])
def translate_process():
    languages = get_valid_languages()

    language = request.form['language']
    sentence = request.form['sentence']

    translated_sentence = translate(sentence, language)

    return render_template('translate.html', title = 'translate', languages = languages, translated_sentence = translated_sentence, translated = True, selected_language = language)



def get_valid_languages():
    languages = get_languages()
    valid_languages = [ 'BENGALI',
                        'GUJARATI',
                        'HINDI',
                        'KANNADA',
                        'MALAYALAM',
                        'MARATHI',
                        'NEPALI',
                        'PUNJABI',
                        'TAMIL',
                        'TELUGU',
                        'URDU'
                     ]
    languages = filter(lambda language: language.name in valid_languages, languages)
    return languages

