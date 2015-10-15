# import simpleai
import random

sentenceToCorrect = ["<s>"] #initializing the sentence to correct

def read_file_line(index, filename):
	fp = open(filename)
	for i, line in enumerate(fp):
		if i == index:
			return line
	return None

#get_probability(line)
#given a line from a file, this function
#strips the probability from the line and
#computes the actual value (as it's stored
#as log10)

def get_probability(line):
	wordlist = line.split()
	l = len(wordlist)
	return 10 ** float(wordlist[l-1])

def get_vocab_word(index):
	fp = open("data/vocab.txt")
	for i, line in enumerate(fp):
		if i == index:
			wordlist = line.split()
			l = len(wordlist)
			return wordlist[l-1]
	return None

def get_lines_of_bigram(word):
	fp = open("data/bigram_counts.txt")
	index = get_index_of_word(word)
	lines = []
	for i, line in enumerate(fp):
		print line.split()[0]
		wordindex = int (line.split()[0])
		if wordindex == index:
			lines.append(line)
	return lines



def get_index_of_word(word):
	fp = open("data/vocab.txt")
	for i, line in enumerate(fp):
		wordlist = line.split()[1]
		if wordlist == word:
			return i + 1
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
	fp = open("data/unigram_counts.txt")
	ran = random.random()
	s = 0
	i = 0	
	for line in fp:
		s += get_probability(line)
		if s > ran:
			return get_vocab_word(i)
		else:
			i += 1
	word = get_vocab_word(max_probability_index)
	return word

def use_bigram(previous_word):
	fp = open("data/bigram_counts.txt")
	ran = random.random()
	s = 0
	i = 0
	# for line in fp:

	return 

def use_trigram(previous_word, second_word):
	return 0

def sentence_generator():
	sentence = ["<s>"] #initializing the sentence
	#sentence generation adds words until word = </s>
	#when i = 1, use bigram
	i = 1
	word = ""
	while word is not "</s>":
		previous_word = sentence[i-1]
		if i > 1:
			second_word = sentence[i-2]
			#trigram stuff
			#this isn't fully correct. trigram stuff needs to also incorporate the bigram bit. fml
			word = use_trigram(previous_word, second_word)
			if word is None:
				i = 0 #sets i to 0. it will be incremented at the end of the loop.  This isn't pretty but it works...i hope
			else:
				sentence.append(word)
		else:
			#bigram stuff
			word = use_bigram(previous_word)
			if word is None:
				word = use_unigram()
			sentence.append(word) #at this point there SHOULD be a word cause unigram gives no f***s
		i += 1
	return sentence

def sentence_corrector(sentence):
	return sentence

#main execution:
# print "Generated sentence:"
# print sentence_generator()
# print "Correcting sentence " + sentenceToCorrect
# print sentence_corrector(sentenceToCorrect)
print get_lines_of_bigram("by")