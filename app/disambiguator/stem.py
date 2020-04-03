def stem(word):
    len_8 = ['తున్నాడు']
    len_5 = ['తోంది','తుంది']
    len_2 = ['పై','లో','గా','కు']
    len_1 = ['ల']
    exceptions = {
        'అంశంపై' :'అంశం',
        'ఇంటికి' : 'గృహం', 'యింటికి' : 'గృహం', 'హౌస్' : 'గృహం', 'హోమ్' : 'గృహం',
        'వెళ్తున్నాను' : 'వెళ్ళు', 'వెళ్తున్నారు' : 'వెళ్ళు', 'వెళ్ళుతున్నాడు' : 'వెళ్ళు', 'వెళ్ళాలి' : 'వెళ్ళు',
        'లాంగ్వేజ్' : 'భాష',
        'పాఠశా' : 'విద్యాలయం',
        'ప్రవర్తిస్తున్న' : 'నాట్యం', 'నటిస్తున్నాడు' : 'నాట్యం', 'నటన' : 'నాట్యం',
        'ప్రయత్నించడం' : 'ప్రయత్నం', 'ప్రయత్నించండి' : 'ప్రయత్నం', 'ప్రయత్నిస్తాను' : 'ప్రయత్నం'
        
    }
    replace_5 = {'ానికి':'ం'}
    if len(word) >= 8:
        if word[len(word) - 8 : ] in len_8:
            word = word[ : len(word) - 8]
    if len(word) >= 5:
        if word[len(word) - 5 : ] in len_5:
            word = word[ : len(word) - 5]
        if word[len(word) - 5 : ] in replace_5:
            key = word[len(word) - 5 :]
            word = word[ : len(word) - 5]
            word = word + replace_5.get(key)
    if len(word) >= 2:
        if word[len(word) - 2 : ] in len_2:
            word = word[ : len(word) - 2]
        if word[len(word) - 1 : ] in len_1:
            word = word[ : len(word) - 1]
    if word in exceptions:
        word = exceptions.get(word)
    return word

def stem_words(words):
    stemmed_words = []
    for word in words:
        stemmed_words.append(stem(word))
    return stemmed_words
