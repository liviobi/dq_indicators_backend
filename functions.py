from http import server
import os
import random
from threading import Thread
import time
import string
from config import cfg
import nltk
import enchant
from spello.model import SpellCorrectionModel
import re
import textstat


sp = SpellCorrectionModel(language='en')
# sp.load('./spello_model/en_large.pkl')
sp.load('./spello_model/en.pkl')


def getListOfFilesNames(dirName):
    return os.listdir(dirName)


def deleteFileFromFolder(path):
    try:
        os.remove(path)
    except OSError as e:  # if failed, report it back to the user ##
        print("Error: %s - %s." % (e.filename, e.strerror))


def removePunctuationFromTokenized(contentsTokenized):
    excludePuncuation = set(string.punctuation)

    # manually add additional punctuation to remove
    doubleSingleQuote = '\'\''
    doubleDash = '--'
    doubleTick = '``'

    excludePuncuation.add(doubleSingleQuote)
    excludePuncuation.add(doubleDash)
    excludePuncuation.add(doubleTick)

    filteredContents = [
        word for word in contentsTokenized if word not in excludePuncuation]
    return filteredContents


def computeConfidenceTokenizer(files, filename, indicator):
    print(f"running computation of {indicator} for {filename}")
    time.sleep(random.randint(1, 30))
    files[filename][indicator] = "completed"


def computeConfidencePos(files, filename, indicator):
    print(f"running computation of {indicator} for {filename}")
    time.sleep(random.randint(1, 30))
    files[filename][indicator] = "completed"


def computeConfidenceNer(files, filename, indicator):
    print(f"running computation of {indicator} for {filename}")
    time.sleep(random.randint(1, 30))
    files[filename][indicator] = "completed"


def computeConfidenceChunker(files, filename, indicator):
    print(f"running computation of {indicator} for {filename}")
    time.sleep(random.randint(1, 30))
    files[filename][indicator] = "completed"


def computeParsable(files, filename, indicator):
    print(f"running computation of {indicator} for {filename}")
    sleepTime = random.randint(1, 30)
    time.sleep(sleepTime)
    mockResult = random.uniform(0, 1)
    mockResult = str(mockResult*100)[0:4]
    files[filename][indicator] = f"{mockResult}"


def computeFit(files, filename, indicator):
    print(f"running computation of {indicator} for {filename}")
    sleepTime = random.randint(1, 30)
    time.sleep(sleepTime)
    mockResult = random.uniform(0, 1)
    mockResult = str(mockResult*100)[0:4]
    files[filename][indicator] = f"{mockResult}"


def computeSpellingMistakes(files, filename, indicator):
    print(f"running computation of {indicator} for {filename}")
    with open(os.path.join(cfg["uploadDir"], filename), "r") as f:
        raw_text = f.read()
        text_tokenized = removePunctuationFromTokenized(
            nltk.word_tokenize(raw_text))
        corrected = sp.spell_correct(raw_text)
        mistakes = 0
        for w in text_tokenized:
            if(w in corrected['correction_dict']):
                mistakes += 1
        result = (1 - (mistakes / len(text_tokenized)))*100
        files[filename][indicator] = str(result)[0:4]
        f.close()


def computePresentInDictionary(files, filename, indicator):
    print(f"running computation of {indicator} for {filename}")
    with open(os.path.join(cfg["uploadDir"], filename), "r") as f:
        raw_text = f.read()
        text_tokenized = removePunctuationFromTokenized(
            nltk.word_tokenize(raw_text))

        d = enchant.Dict("en_US")
        correct = 0
        for word in text_tokenized:
            if d.check(word):
                correct += 1
        result = (correct / len(text_tokenized))*100
        files[filename][indicator] = str(result)[0:4]
        f.close()


def wordcount(s):
    """Split sentence s on punctuation
    and return number of non-empty words
    """
    punct = r"\W"  # non-word characters
    return len([w for w in re.split(punct, s) if w])


def computeAvgSentLen(files, filename, indicator):
    print(f"running computation of {indicator} for {filename}")
    with open(os.path.join(cfg["uploadDir"], filename), "r") as f:
        raw_text = f.read()
        terminating_punct = "[!?.]"
        sentences = [
            s.strip()  # without trailing whitespace
            for s in re.split(
                terminating_punct,
                "".join(raw_text).replace("\n", " "),  # text as 1 string
            )
            if s.strip()  # non-empty
        ]
        # map each sentece to its wordcount then sum all the wordcounts
        avgSentenceLength = sum(map(wordcount, sentences)) / len(sentences)
        optimalSentenceLen = cfg["optimal_sentence_length"]
        if avgSentenceLength > 2*optimalSentenceLen:
            avgSentenceLength = 2*optimalSentenceLen
        result = (1 - abs(optimalSentenceLen - avgSentenceLength) /
                  optimalSentenceLen) * 100
        files[filename][indicator] = str(result)[0:4]
        f.close()


def computePercLowercase(files, filename, indicator):
    print(f"running computation of {indicator} for {filename}")
    time.sleep(random.randint(1, 30))
    files[filename][indicator] = "completed"


def computePercUppercase(files, filename, indicator):
    print(f"running computation of {indicator} for {filename}")
    time.sleep(random.randint(1, 30))
    files[filename][indicator] = "completed"


def computeLexicalDiversity(files, filename, indicator):
    print(f"running computation of {indicator} for {filename}")
    with open(os.path.join(cfg["uploadDir"], filename), "r") as f:
        raw_text = f.read()
        text_tokenized = removePunctuationFromTokenized(
            nltk.word_tokenize(raw_text))

        # TODO normalize

        result = (len(set(text_tokenized)) / len(text_tokenized))*100
        files[filename][indicator] = str(result)[0:4]
        f.close()


def computeRecognizedByPOS(files, filename, indicator):
    print(f"running computation of {indicator} for {filename}")
    with open(os.path.join(cfg["uploadDir"], filename), "r") as f:
        raw_text = f.read()
        text_tokenized = removePunctuationFromTokenized(
            nltk.word_tokenize(raw_text))

        text_tagged = nltk.pos_tag(text_tokenized, tagset='universal')
        unknown = 0
        for t in text_tagged:
            if t[1] == "X":
                unknown += 1
        result = (1 - (unknown/len(text_tagged)))*100
        files[filename][indicator] = str(result)[0:4]
        f.close()


def computeReadabilityCli(files, filename, indicator):
    print(f"running computation of {indicator} for {filename}")
    with open(os.path.join(cfg["uploadDir"], filename), "r") as f:
        raw_text = f.read()
        score = textstat.coleman_liau_index(raw_text)
        optimalScore = 3
        worstScore = 18

        if(score > worstScore):
            score = worstScore

        result = (1 - abs(optimalScore - score) /
                  (worstScore - optimalScore)) * 100
        files[filename][indicator] = str(result)[0:4]
        f.close()


def computeReadabilityAri(files, filename, indicator):
    print(f"running computation of {indicator} for {filename}")
    with open(os.path.join(cfg["uploadDir"], filename), "r") as f:
        raw_text = f.read()
        score = textstat.automated_readability_index(raw_text)
        optimalScore = 3
        worstScore = 18

        if(score > worstScore):
            score = worstScore

        result = (1 - abs(optimalScore - score) /
                  (worstScore - optimalScore)) * 100
        files[filename][indicator] = str(result)[0:4]
        f.close()


def computeAcronyms(files, filename, indicator):
    print(f"running computation of {indicator} for {filename}")
    time.sleep(10)
    files[filename][indicator] = "completed"


def computeIndicator(files, filename, indicator):
    if(indicator == "confidence_tokenizer"):
        Thread(target=computeConfidenceTokenizer, kwargs={
               'files': files, 'filename': filename, 'indicator': indicator}).start()
    elif(indicator == "confidence_pos"):
        Thread(target=computeConfidencePos, kwargs={
               'files': files, 'filename': filename, 'indicator': indicator}).start()

    elif(indicator == "confidence_ner"):
        Thread(target=computeConfidenceNer, kwargs={
               'files': files, 'filename': filename, 'indicator': indicator}).start()

    elif(indicator == "confidence_chunker"):
        Thread(target=computeConfidenceChunker, kwargs={
               'files': files, 'filename': filename, 'indicator': indicator}).start()

    elif(indicator == "parsable"):
        Thread(target=computeParsable, kwargs={
               'files': files, 'filename': filename, 'indicator': indicator}).start()

    elif(indicator == "fit"):
        Thread(target=computeFit, kwargs={
               'files': files, 'filename': filename, 'indicator': indicator}).start()

    elif(indicator == "spelling_mistakes"):
        Thread(target=computeSpellingMistakes, kwargs={
               'files': files, 'filename': filename, 'indicator': indicator}).start()

    elif(indicator == "avg_sentence_len"):
        Thread(target=computeAvgSentLen, kwargs={
               'files': files, 'filename': filename, 'indicator': indicator}).start()

    elif(indicator == "perc_lowercase"):
        Thread(target=computePercLowercase, kwargs={
               'files': files, 'filename': filename, 'indicator': indicator}).start()

    elif(indicator == "perc_uppercase"):
        Thread(target=computePercUppercase, kwargs={
               'files': files, 'filename': filename, 'indicator': indicator}).start()

    elif(indicator == "lexical_diversity"):
        Thread(target=computeLexicalDiversity, kwargs={
               'files': files, 'filename': filename, 'indicator': indicator}).start()

    elif(indicator == "recognized_by_pos"):
        Thread(target=computeRecognizedByPOS, kwargs={
               'files': files, 'filename': filename, 'indicator': indicator}).start()

    elif(indicator == "acronyms"):
        Thread(target=computeAcronyms, kwargs={
               'files': files, 'filename': filename, 'indicator': indicator}).start()
    elif(indicator == "present_in_dictionary"):
        Thread(target=computePresentInDictionary, kwargs={
               'files': files, 'filename': filename, 'indicator': indicator}).start()
    elif(indicator == "readability_cli"):
        Thread(target=computeReadabilityCli, kwargs={
               'files': files, 'filename': filename, 'indicator': indicator}).start()
    elif(indicator == "readability_ari"):
        Thread(target=computeReadabilityAri, kwargs={
               'files': files, 'filename': filename, 'indicator': indicator}).start()
