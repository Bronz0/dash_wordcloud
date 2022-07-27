#imports
import nltk
from nltk import word_tokenize, sent_tokenize, Text
from nltk.stem.snowball import FrenchStemmer #import the French stemming library
from nltk.corpus import stopwords #import stopwords from nltk corpus
import re #import the regular expressions library; will be used to strip punctuation
from collections import Counter #allows for counting the number of occurences in a list
from os import listdir
from os.path import isfile, isdir, join
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import base64
import io
from itertools import islice


#TODO: download nlkt stopwords
nltk.download('punkt')

#reading in the raw text from the file
def get_raw_text(path):
    '''reads in raw text from a text file using the argument (path), which represents the path/to/file'''
    
    if isfile(path): # file
        if '.txt' in path:
            f = open(path,"r", encoding="utf-8") #open the file located at "path" as a file object (f) that is readonly
            raw = f.read() # read raw text into a variable (raw) after decoding it from utf8
            f.close() #close the file now that it isn;t being used any longer
        else: # not a txt file
            print('The file must be a .txt file.')
    elif isdir(path): # directory
        files = [f for f in listdir(path) if (isfile(join(path, f)) & ('.txt' in f))]
        if files == []:
            print('There is no txt file in that folder.')
            return ''
        else:
            raw = ''
            for file in files:
                f = open(join(path, file), 'r', encoding='utf-8')
                file_content = f.read()
                raw += file_content
                f.close()
    else: # string
        return path
    return raw

def get_tokens(raw):
    '''get the nltk tokens from a text'''
    tokens = word_tokenize(raw) #tokenize the raw UTF-8 text
    return tokens

def get_nltk_text(raw):
    '''create an nltk text using the passed argument (raw) after filtering out the commas'''
    #turn the raw text into an nltk text object
    no_commas = re.sub(r'[.|,|\'|’]',' ', raw) #filter out all the commas, periods, and appostrophes using regex
    tokens = word_tokenize(no_commas) #generate a list of tokens from the raw text
    text = Text(tokens) #create a nltk text from those tokens
    return text

def get_stopwords(type="veronis"):
    '''returns the veronis stopwords in unicode, or if any other value is passed, it returns the default nltk french stopwords'''
    if type=="veronis":
        #VERONIS STOPWORDS
        stopword_list = ["Ap.", "Apr.", "GHz", "MHz", "USD", "a", "afin", "ah", "ai", "aie", "aient", "aies", "ait", "alors", "après", "as", "attendu", "au", "au-delà", "au-devant", "aucun", "aucune", "audit", "auprès", "auquel", "aura", "aurai", "auraient", "aurais", "aurait", "auras", "aurez", "auriez", "aurions", "aurons", "auront", "aussi", "autour", "autre", "autres", "autrui", "aux", "auxdites", "auxdits", "auxquelles", "auxquels", "avaient", "avais", "avait", "avant", "avec", "avez", "aviez", "avions", "avons", "ayant", "ayez", "ayons", "b", "bah", "banco", "ben", "bien", "bé", "c", "c'", "c'est", "c'était", "car", "ce", "ceci", "cela", "celle", "celle-ci", "celle-là", "celles", "celles-ci", "celles-là", "celui", "celui-ci", "celui-là", "celà", "cent", "cents", "cependant", "certain", "certaine", "certaines", "certains", "ces", "cet", "cette", "ceux", "ceux-ci", "ceux-là", "cf.", "cg", "cgr", "chacun", "chacune", "chaque", "chez", "ci", "cinq", "cinquante", "cinquante-cinq", "cinquante-deux", "cinquante-et-un", "cinquante-huit", "cinquante-neuf", "cinquante-quatre", "cinquante-sept", "cinquante-six", "cinquante-trois", "cl", "cm", "cm²", "comme", "contre", "d", "d'", "d'après", "d'un", "d'une", "dans", "de", "depuis", "derrière", "des", "desdites", "desdits", "desquelles", "desquels", "deux", "devant", "devers", "dg", "différentes", "différents", "divers", "diverses", "dix", "dix-huit", "dix-neuf", "dix-sept", "dl", "dm", "donc", "dont", "douze", "du", "dudit", "duquel", "durant", "dès", "déjà", "e", "eh", "elle", "elles", "en", "en-dehors", "encore", "enfin", "entre", "envers", "es", "est", "et", "eu", "eue", "eues", "euh", "eurent", "eus", "eusse", "eussent", "eusses", "eussiez", "eussions", "eut", "eux", "eûmes", "eût", "eûtes", "f", "fait", "fi", "flac", "fors", "furent", "fus", "fusse", "fussent", "fusses", "fussiez", "fussions", "fut", "fûmes", "fût", "fûtes", "g", "gr", "h", "ha", "han", "hein", "hem", "heu", "hg", "hl", "hm", "hm³", "holà", "hop", "hormis", "hors", "huit", "hum", "hé", "i", "ici", "il", "ils", "j", "j'", "j'ai", "j'avais", "j'étais", "jamais", "je", "jusqu'", "jusqu'au", "jusqu'aux", "jusqu'à", "jusque", "k", "kg", "km", "km²", "l", "l'", "l'autre", "l'on", "l'un", "l'une", "la", "laquelle", "le", "lequel", "les", "lesquelles", "lesquels", "leur", "leurs", "lez", "lors", "lorsqu'", "lorsque", "lui", "lès", "m", "m'", "ma", "maint", "mainte", "maintes", "maints", "mais", "malgré", "me", "mes", "mg", "mgr", "mil", "mille", "milliards", "millions", "ml", "mm", "mm²", "moi", "moins", "mon", "moyennant", "mt", "m²", "m³", "même", "mêmes", "n", "n'avait", "n'y", "ne", "neuf", "ni", "non", "nonante", "nonobstant", "nos", "notre", "nous", "nul", "nulle", "nº", "néanmoins", "o", "octante", "oh", "on", "ont", "onze", "or", "ou", "outre", "où", "p", "par", "par-delà", "parbleu", "parce", "parmi", "pas", "passé", "pendant", "personne", "peu", "plus", "plus_d'un", "plus_d'une", "plusieurs", "pour", "pourquoi", "pourtant", "pourvu", "près", "puisqu'", "puisque", "q", "qu", "qu'", "qu'elle", "qu'elles", "qu'il", "qu'ils", "qu'on", "quand", "quant", "quarante", "quarante-cinq", "quarante-deux", "quarante-et-un", "quarante-huit", "quarante-neuf", "quarante-quatre", "quarante-sept", "quarante-six", "quarante-trois", "quatorze", "quatre", "quatre-vingt", "quatre-vingt-cinq", "quatre-vingt-deux", "quatre-vingt-dix", "quatre-vingt-dix-huit", "quatre-vingt-dix-neuf", "quatre-vingt-dix-sept", "quatre-vingt-douze", "quatre-vingt-huit", "quatre-vingt-neuf", "quatre-vingt-onze", "quatre-vingt-quatorze", "quatre-vingt-quatre", "quatre-vingt-quinze", "quatre-vingt-seize", "quatre-vingt-sept", "quatre-vingt-six", "quatre-vingt-treize", "quatre-vingt-trois", "quatre-vingt-un", "quatre-vingt-une", "quatre-vingts", "que", "quel", "quelle", "quelles", "quelqu'", "quelqu'un", "quelqu'une", "quelque", "quelques", "quelques-unes", "quelques-uns", "quels", "qui", "quiconque", "quinze", "quoi", "quoiqu'", "quoique", "r", "revoici", "revoilà", "rien", "s", "s'", "sa", "sans", "sauf", "se", "seize", "selon", "sept", "septante", "sera", "serai", "seraient", "serais", "serait", "seras", "serez", "seriez", "serions", "serons", "seront", "ses", "si", "sinon", "six", "soi", "soient", "sois", "soit", "soixante", "soixante-cinq", "soixante-deux", "soixante-dix", "soixante-dix-huit", "soixante-dix-neuf", "soixante-dix-sept", "soixante-douze", "soixante-et-onze", "soixante-et-un", "soixante-et-une", "soixante-huit", "soixante-neuf", "soixante-quatorze", "soixante-quatre", "soixante-quinze", "soixante-seize", "soixante-sept", "soixante-six", "soixante-treize", "soixante-trois", "sommes", "son", "sont", "sous", "soyez", "soyons", "suis", "suite", "sur", "sus", "t", "t'", "ta", "tacatac", "tandis", "te", "tel", "telle", "telles", "tels", "tes", "toi", "ton", "toujours", "tous", "tout", "toute", "toutefois", "toutes", "treize", "trente", "trente-cinq", "trente-deux", "trente-et-un", "trente-huit", "trente-neuf", "trente-quatre", "trente-sept", "trente-six", "trente-trois", "trois", "très", "tu", "u", "un", "une", "unes", "uns", "v", "vers", "via", "vingt", "vingt-cinq", "vingt-deux", "vingt-huit", "vingt-neuf", "vingt-quatre", "vingt-sept", "vingt-six", "vingt-trois", "vis-à-vis", "voici", "voilà", "vos", "votre", "vous", "w", "x", "y", "z", "zéro", "à", "ç'", "ça", "ès", "étaient", "étais", "était", "étant", "étiez", "étions", "été", "étée", "étées", "étés", "êtes", "être", "ô"]
    else:
        #get French stopwords from the nltk kit
        stopword_list = stopwords.words('french') #create a list of all French stopwords
    return stopword_list    

def filter_stopwords(text,stopword_list):
    '''normalizes the words by turning them all lowercase and then filters out the stopwords'''
    words=[w.lower() for w in text] #normalize the words in the text, making them all lowercase
    #filtering stopwords
    filtered_words = [] #declare an empty list to hold our filtered words
    for word in words: #iterate over all words from the text
        if word not in stopword_list and word.isalpha() and len(word) > 1: #only add words that are not in the French stopwords list, are alphabetic, and are more than 1 character
            filtered_words.append(word) #add word to filter_words list if it meets the above conditions
#     filtered_words.sort() #sort filtered_words list
    return filtered_words

def stem_words(words):
    '''stems the word list using the French Stemmer'''
    #stemming words
    stemmed_words = [] #declare an empty list to hold our stemmed words
    stemmer = FrenchStemmer() #create a stemmer object in the FrenchStemmer class
    for word in words:
        stemmed_word=stemmer.stem(word) #stem the word
        stemmed_words.append(stemmed_word) #add it to our stemmed word list
    stemmed_words.sort() #sort the stemmed_words
    return stemmed_words

def sort_dictionary(dictionary):
    '''returns a sorted dictionary (as tuples) based on the value of each key'''
    return sorted(dictionary.items(), key=lambda x: x[1], reverse=True)

def normalize_counts(counts):
    '''normalize the number of occurence for each word'''
    total = sum(counts.values())
    return dict((word, round(float(count)/total,3)) for word,count in counts.items())

def get_words_counts(words):
    '''get the number of occurence of each word in words'''
    return dict([(word, words.count(word)) for word in set(words)])

def tokenize(path):
    # read raw text
    raw = get_raw_text(path)
    # get nltk text
    nltk_text = get_nltk_text(raw)
    # get stopwords list
    stopwords = get_stopwords()
    # filter stop words
    filtered_tokens = filter_stopwords(nltk_text, stopwords)
    words_counts = get_words_counts(filtered_tokens)
    sorted_tokens = sort_dictionary(words_counts)
#     df = pd.DataFrame(list(sorted_tokens.items()), columns=["word", "count"])
    return sorted_tokens

def groupper(words_list, n_words=2):
    if n_words > 3:
        print("the number of words must be <= 3.")
    else:
        grouped_words = []
        for i in range(len(words_list)-(n_words-1)):
            grouped_words.append(" ".join(words_list[i:i+n_words]))
        return grouped_words

def text_to_frequencies(path, n_words=2):
    raw = get_raw_text(path)
    sentences = sent_tokenize(raw)
    stopwords = get_stopwords()
    tokenized_sentences = []
    for sentence in sentences:
        nltk_text = get_nltk_text(sentence)
        filtered = filter_stopwords(nltk_text, stopwords)
        grouped = groupper(filtered, n_words)
        tokenized_sentences.append(grouped)
    results = []
    for l in tokenized_sentences:
        results += l
    frequencies = get_words_counts(results)
    return frequencies

def frequencies_to_wordcloud(frequencies, max_words=100, width=1600, height=900, background_color='white', min_font_size=10, fig_w=24, fig_h=13.5):
    wordcloud = WordCloud(width=width, height=height, max_words=max_words,  background_color=background_color, min_font_size=min_font_size).generate_from_frequencies(frequencies)
    # set the figsize
    plt.figure(figsize=[fig_w,fig_h])
    plt.imshow(wordcloud, interpolation="bilinear")

def text_to_wordcloud(path, n_words=2, max_words=100, width=1600, height=900, background_color='white', min_font_size=10, fig_w=24, fig_h=13.5):    
    raw = get_raw_text(path)
    sentences = sent_tokenize(raw)
    stopwords = get_stopwords()
    tokenized_sentences = []
    for sentence in sentences:
        nltk_text = get_nltk_text(sentence)
        filtered = filter_stopwords(nltk_text, stopwords)
        grouped = groupper(filtered, n_words)
        tokenized_sentences.append(grouped)
    results = []
    for l in tokenized_sentences:
        results += l
    frequencies = get_words_counts(results)
    wordcloud = WordCloud(width=width, height=height, max_words=max_words,  background_color=background_color, min_font_size=min_font_size).generate_from_frequencies(frequencies)
    # set the figsize
    figure = plt.figure(figsize=[fig_w,fig_h])
    img = plt.imshow(wordcloud, interpolation="nearest")
    plt.axis('off')


    my_stringIObytes = io.BytesIO()
    plt.savefig(my_stringIObytes, format='jpg')
    my_stringIObytes.seek(0)
    my_base64_jpgData = 'data:image/png;base64,' + base64.b64encode(my_stringIObytes.read()).decode("utf-8")

    return my_base64_jpgData

def get_holoniq_wordcloud_data(path, n_words=2, max_words=50):
    raw = get_raw_text(path)
    sentences = sent_tokenize(raw)
    stopwords = get_stopwords()
    tokenized_sentences = []
    for sentence in sentences:
        nltk_text = get_nltk_text(sentence)
        filtered = filter_stopwords(nltk_text, stopwords)
        grouped = groupper(filtered, n_words)
        tokenized_sentences.append(grouped)
    results = []
    for l in tokenized_sentences:
        results += l
    frequencies = get_words_counts(results)
    # sort frequencies
    sorted_frequencies = sort_dictionary(frequencies)
    # get the top max_words words
    top_words = dict(islice(sorted_frequencies, max_words))
    data = []
    for item in top_words.items():
        data.append([item[0], item[1], "("+str(item[0])+": "+str(item[1])+")"])

    return data