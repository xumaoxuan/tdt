import shutil

__author__ = 'Vibha Bhambhani and Shakshi Maheswari'
import os
import pickle
from config import MODEL_FILE
from config import TDT_OUT_DIR
from config import TDT_TEST_DIR
from config import LOG_FOLDER
import tdt_utils


root = TDT_OUT_DIR
topics = pickle.load(open(MODEL_FILE, "rb"))
logger = open(os.path.join(LOG_FOLDER, 'output.txt'), 'w')
docs = filter(lambda x: not x.startswith('.') and os.path.isfile(os.path.join(TDT_TEST_DIR, x)),
              os.listdir(TDT_TEST_DIR))

for topic in topics:
    dir_path = os.path.join(root, topic['topic'])
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

count = len(docs)
for doc in docs:
    print count
    count -= 1
    results = []
    logger.write('DOC NAME: %s\n'%(os.path.join(TDT_TEST_DIR, doc)))
    docOpen = open(os.path.join(TDT_TEST_DIR, doc), "r")
    tfRawD = {}
    uniqueWordsInDoc, DVector, lenD, tfRawD = tdt_utils.createDocumentVector(docOpen, tfRawD)

    for topic in topics:
        V = topic['V']
        N = topic['N'] + 1
        tdt_utils.extractVocabulary(V, uniqueWordsInDoc)
        avgLength = tdt_utils.updateAvgLength(topic['avgLength'], lenD, N - 1)
        tfD = tdt_utils.calculateTF(tfRawD, lenD, avgLength)
        tfT = tdt_utils.calculateTF(topic['tfRaw'], topic['length'], avgLength)
        idf = tdt_utils.calculateIdf(V, N)
        Dh = tdt_utils.calculateProduct(tfD, idf)
        Th = tdt_utils.calculateProduct(tfT, idf)
        similarityValue = tdt_utils.similarity(Dh, Th, V)
        normalizedValue = similarityValue / topic['Z']
        results.append([topic['topic'], normalizedValue])

    results = sorted(results, key=lambda x: x[1], reverse=True)
    logger.write('\n'.join(map(lambda x: '%s==%s'%(x[0], x[1]), results)))
    logger.write('\n')
    shutil.copyfile(os.path.join(TDT_TEST_DIR, doc), os.path.join(TDT_OUT_DIR, results[0][0], doc))
    logger.write('--------------------------------------------\n')
