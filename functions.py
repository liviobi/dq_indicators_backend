import os
import random
from threading import Thread
import time


def getListOfFilesNames(dirName):
    return os.listdir(dirName)


def deleteFileFromFolder(path):
    try:
        os.remove(path)
    except OSError as e:  # if failed, report it back to the user ##
        print("Error: %s - %s." % (e.filename, e.strerror))


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
    time.sleep(random.randint(1, 30))
    files[filename][indicator] = "completed"


def computeAvgSentLen(files, filename, indicator):
    print(f"running computation of {indicator} for {filename}")
    time.sleep(random.randint(1, 30))
    files[filename][indicator] = "completed"


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
    time.sleep(random.randint(1, 30))
    files[filename][indicator] = "completed"


def computeUnknownWords(files, filename, indicator):
    print(f"running computation of {indicator} for {filename}")
    time.sleep(10)
    files[filename][indicator] = "completed"


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

    elif(indicator == "unknown_words"):
        Thread(target=computeUnknownWords, kwargs={
               'files': files, 'filename': filename, 'indicator': indicator}).start()

    elif(indicator == "acronyms"):
        Thread(target=computeAcronyms, kwargs={
               'files': files, 'filename': filename, 'indicator': indicator}).start()
