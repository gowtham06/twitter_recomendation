#!/usr/bin/env python
import numpy
import os
import glob
class LDA:
    def __init__(self, numberOfTopics, alpha, beta, docs, V):
        self.numberOfTopics = numberOfTopics
        self.alpha = alpha # parameter of topics prior
        self.beta = beta   # parameter of words prior
        self.docs = docs
        self.V = V

        self.assignedTopics = [] # topics of words of documents
        self.n_m_z = numpy.zeros((len(self.docs), numberOfTopics)) + alpha     # word count of each document and topic
        self.n_z_t = numpy.zeros((numberOfTopics, V)) + beta # word count of each topic and vocabulary
        self.n_z = numpy.zeros(numberOfTopics) + V * beta    # word count of each topic

        self.N = 0
        for m, doc in enumerate(docs):
            self.N += len(doc)
            z_n = []
            for t in doc:
                p_z = self.n_z_t[:, t] * self.n_m_z[m] / self.n_z
                z = numpy.random.multinomial(1, p_z / p_z.sum()).argmax()
                z_n.append(z)
                self.n_m_z[m, z] += 1
                self.n_z_t[z, t] += 1
                self.n_z[z] += 1
            self.assignedTopics.append(numpy.array(z_n))

    def inference(self):
        #learning in ever iteration
        for m, doc in enumerate(self.docs):
            z_n = self.assignedTopics[m]
            n_m_z = self.n_m_z[m]
            for n, t in enumerate(doc):
                # discount for n-th word t with topic z
                z = z_n[n]
                n_m_z[z] -= 1
                self.n_z_t[z, t] -= 1
                self.n_z[z] -= 1

                # sampling topic new_z for t
                p_z = self.n_z_t[:, t] * n_m_z / self.n_z
                new_z = numpy.random.multinomial(1, p_z / p_z.sum()).argmax()

                # set z the new topic and increment counters
                z_n[n] = new_z
                n_m_z[new_z] += 1
                self.n_z_t[new_z, t] += 1
                self.n_z[new_z] += 1

    def wordDistribution(self):
               return self.n_z_t / self.n_z[:, numpy.newaxis]

    def perplexity(self, docs=None):
        if docs == None: docs = self.docs
        phi = self.wordDistribution()
        log_per = 0
        N = 0
        Kalpha = self.numberOfTopics * self.alpha
        for m, doc in enumerate(docs):
            theta = self.n_m_z[m] / (len(self.docs[m]) + Kalpha)
            for w in doc:
                log_per -= numpy.log(numpy.inner(phi[:,w], theta))
            N += len(doc)
        return numpy.exp(log_per / N)
def findWordFunction(search_word,corpus_filename):
    #print("Start Function");
    wordPresenceFlag=0;
    file_open=open(corpus_filename,'r');
    for line in file_open:
        if line.strip() == search_word:
            wordPresenceFlag=1;
            break
    return wordPresenceFlag

def lda_learning(lda, iteration, voca):
    pre_perp = lda.perplexity()
    #print "initial perplexity=%f" % pre_perp
    for i in range(iteration):
        lda.inference()
        perp = lda.perplexity()
        #print "-%d p=%f" % (i + 1, perp)
        if pre_perp:
            if pre_perp < perp:
                output_word_topic_dist(lda, voca)
                pre_perp = None
            else:
                pre_perp = perp
    output_word_topic_dist(lda, voca)

def output_word_topic_dist(lda,voca):
    import glob
    import os
    zcount = numpy.zeros(lda.numberOfTopics, dtype=int)
    wordcount = [dict() for k in xrange(lda.numberOfTopics)]
    files_directory="/home/rooney/PythonProjects/TOPICS"
    for xlist, zlist in zip(lda.docs, lda.z_n_m):
        for x, z in zip(xlist, zlist):
            zcount[z] += 1
            if x in wordcount[z]:
                wordcount[z][x] += 1
            else:
                wordcount[z][x] = 1
    file_dir="/home/rooney/dataMiningPackage/TOPICS/"
    file_list=[]
    os.chdir(file_dir)
    for file in glob.glob("*.txt"):
        file_list.append(file);    #List containing the names of each topic corpus
    fuzzyValue=[];
    for i in range(0, len(file_list)):
        fuzzyValue.append(0)

    phi = lda.wordDistribution()
    for numberOfTopics in xrange(lda.numberOfTopics):
        #print "\n-- topic: %d (%d words)" % (k, zcount[k])
        for w in numpy.argsort(-phi[k])[:20]:
            #print "%s: %f (%d)" % (voca[w], phi[k,w], wordcount[k].get(w,0))
            for file_loop in range(0, len(file_list)):
                corpus_filename=file_list[file_loop];
                corpus_filename=file_dir+corpus_filename;
                #print(corpus_filename)
                wordPresenceFlag=findWordFunction(voca[w],corpus_filename);
                if(wordPresenceFlag==1):
                    fuzzyValue[file_loop]=fuzzyValue[file_loop]+phi[k,w]*wordcount[k].get(w,0); #add weight phi*word count of each value if that particular word is found in that particular topic corpus
                else:
                    fuzzyValue[file_loop]=fuzzyValue[file_loop]; #fuzzyValue for each value is unchanged if a particular word is not found in the topic corpus
    sortedFuzzyValues=numpy.sort(fuzzyValue);
    #print(sortedFuzzyValues)
    
    

     
def main():
    import optparse
    import vocabulary
    parser = optparse.OptionParser()
    parser.add_option("-f", dest="corpus_filename", help="corpus filename")
    parser.add_option("--alpha", dest="alpha", type="float", help="parameter alpha", default=0.5)
    parser.add_option("--beta", dest="beta", type="float", help="parameter beta", default=0.5)
    parser.add_option("-k", dest="K", type="int", help="number of topics", default=20)
    parser.add_option("-i", dest="iteration", type="int", help="iteration count", default=100)
    #parser.add_option("-s", dest="smartinit", action="store_true", help="smart initialize of parameters", default=False)
    parser.add_option("--stopwords", dest="stopwords", help="exclude stop words", action="store_true", default=False)
    parser.add_option("--seed", dest="seed", type="int", help="random seed")
    parser.add_option("--df", dest="df", type="int", help="threshold of document frequency to cut words", default=0)
    (options, args) = parser.parse_args()  
    if options.corpus_filename:
        corpus = vocabulary.load_file(options.corpus_filename)
    else:
        corpus = null;
        if not corpus: parser.error("corpus range(-c) forms 'start:end'")
    if options.seed != None:
        numpy.random.seed(options.seed)

    voca = vocabulary.Vocabulary(options.stopwords)
    docs = [voca.doc_to_ids(doc) for doc in corpus]
    if options.df > 0: docs = voca.cut_low_freq(docs, options.df)

    lda = LDA(options.K, options.alpha, options.beta, docs, voca.size())
    #print "corpus=%d, words=%d, K=%d, a=%f, b=%f" % (len(corpus), len(voca.vocas), options.numberOfTopics, options.alpha, options.beta)

    lda_learning(lda, options.iteration, voca)

if __name__ == "__main__": 
    main()
