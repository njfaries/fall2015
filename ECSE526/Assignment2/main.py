import simpleai
import random

sentenceToCorrect = ["<s>"] #initializing the sentence to correct

def read_vocab():
	return 0

def read_unigram():
	return 0

def read_bigram():
	return 0

def read_trigram():
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