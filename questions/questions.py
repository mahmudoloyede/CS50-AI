import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files = {}
    for doc in os.listdir(directory):
        with open(os.path.join(directory, doc), encoding='utf8') as f:
            files[doc] = f.read()
    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    words = []

    for w in nltk.word_tokenize(document):
        w = w.lower()
        if w in string.punctuation or w in nltk.corpus.stopwords.words('english'):
            continue
        words.append(w)
    return words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idfs = {}
    freq = {}
    words = set()
    num_of_docs = len(documents)

    for k in documents:
        words.update(documents[k])

    for word in words:
        for d in documents:
            if word in documents[d]:
                if word not in freq:
                    freq[word] = 1
                else:
                    freq[word] += 1
    
    for word in words:
        idfs[word] = math.log(num_of_docs / freq[word])
    
    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tf = {}
    for f in files:
        word_count = {}
        for w in files[f]:
            if w not in word_count:
                word_count[w] = 1
            else:
                word_count[w] += 1
        tf[f] = word_count
    
    f_t = {}
    for f in files:
        f_t[f] = []
        for a in query:
            if a in files[f]:
                f_t[f].append(tf[f][a] * idfs[a])

    f_tfidf = []
    for z in f_t:
        f_tfidf.append((z, sum(f_t[z])))

    f_tfidf.sort(key=lambda j: j[1], reverse=True)
    top_file = []
    for b in f_tfidf[:n]:
        top_file.append(b[0])
    return top_file


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    qtd = {}
    for s in sentences:
        matches = 0
        for q in query:
            if q in sentences[s]:
                matches += 1
        qtd[s] = matches / len(sentences[s])
        
    s_i = {}
    for b in sentences:
        s_i[b] = []
        for a in query:
            if a in sentences[b]:
                s_i[b].append(idfs[a])
    s_i_q = []
    for f in s_i:
        s_i_q.append((f, sum(s_i[f]), qtd[f]))
    
    s_i_q.sort(key=lambda j: (j[1], j[2]), reverse=True)
    top_sen = []
    for d in s_i_q[:n]:
        top_sen.append(d[0])
    return top_sen


if __name__ == "__main__":
    main()
