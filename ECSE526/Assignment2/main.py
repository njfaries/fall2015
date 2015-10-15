import simpleai
import random

sentenceToCorrect = ["<s>"] #initializing the sentence to correct

def read_file_line(index, filename):
	fp = open(filename)
	if i, line in enumerate(fp):
		if i == index:
			return line
	return None

def get_probability(line):
	wordlist = line.split()
	l = len(wordlist)
	return 10 ** wordlist[l-1]

def read_vocab(index):
	fp = open("data/vocab.txt")
	for i, line in enumerate(fp):
		if i == index:
			return line
	return None

def read_unigram(index):
	fp = open("data/unigram_counts.txt")
	return 0

def read_bigram():
	fp = open("data/bigram_counts.txt")
	return 0

def read_trigram():
	fp = open("data/trigram_counts.txt")
	return 0

def use_unigram():
	return 0

def use_bigram(word):
	return 0

def use_trigram(word, previous_word):
	return 0

def sentence_generator():
	sentence = ["<s>"] #initializing the sentence
	#sentence generation adds words until word = </s>
	#when i = 1, use bigram
	i = 1
	word = ""
	while word is not "</s>":
		if i == 1:

			#bigram stuff
		else:
			#trigram stuff
		sentence.append(word)
		i += 1
	return sentence

def sentence_corrector(sentence):
	return sentence

#main execution:
print "Generated sentence:"
print sentence_generator()
print "Correcting sentence " + sentenceToCorrect
print sentence_corrector(sentenceToCorrect)