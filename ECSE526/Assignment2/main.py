# import simpleai
import random
import math

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
		wordindex = int (line.split()[0])
		if wordindex == index:
			lines.append(line)
	return lines

def get_lines_of_trigram(word, second_word):
	fp = open("data/trigram_counts.txt")
	index = get_index_of_word(word)
	second_index = get_index_of_word(second_word)
	lines = []
	for i, line in enumerate(fp):
		wordindex = int (line.split()[0])
		secondwordindex = int (line.split()[1])
		if wordindex == index and secondwordindex == second_index:
			lines.append(line)
	return lines

def get_index_of_word(word):
	fp = open("data/vocab.txt")
	for i, line in enumerate(fp):
		wordlist = line.split()[1]
		if wordlist == word:
			return i + 1
	return None

#def minimumEditDistance has been copied from rosettacode.org

def minimumEditDistance(s1,s2):
    if len(s1) > len(s2):
        s1,s2 = s2,s1
    distances = range(len(s1) + 1)
    for index2,char2 in enumerate(s2):
        newDistances = [index2+1]
        for index1,char1 in enumerate(s1):
            if char1 == char2:
                newDistances.append(distances[index1])
            else:
                newDistances.append(1 + min((distances[index1], distances[index1+1], newDistances[-1])))
        distances = newDistances
    return distances[-1]
 

def read_unigram():
	fp = open("data/vocab.txt")
	for line in fp:
		print line.split()[1]
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

def use_bigram(previous_word):
	max_probability = 0
	word = None
	lines = get_lines_of_bigram(previous_word)
	for line in lines:
		probability = get_probability(line)
		if probability > max_probability:
			max_probability = probability
			word = get_vocab_word(int (line.split()[1]))
	return word

def use_trigram(previous_word, second_word):
	max_probability = 0
	lines = get_lines_of_trigram(previous_word, second_word)
	word = None
	for line in lines:
		probability = get_probability(line)
		if probability > max_probability:
			max_probability = probability
			word = get_vocab_word(int (line.split()[2]))
	return word

def sentence_generator():
	sentence = ["<s>"] #initializing the sentence
	#sentence generation adds words until word = </s>
	#when i = 1, use bigram
	i = 1
	word = ""
	while word is not "</s>":
		previous_word = sentence[len(sentence)-1]
		if i > 1:
			second_word = sentence[len(sentence)-2]
			#trigram stuff
			#this isn't fully correct. trigram stuff needs to also incorporate the bigram bit. fml
			# print "Trying trigram with previous word: " + previous_word + " and second word: " + second_word
			word = use_trigram(previous_word, second_word)
			# print word
			if word is None:
				i = 0 #sets i to 0. it will be incremented at the end of the loop.  This isn't pretty but it works...i hope
			else:
				print "Trigram: " + word
				sentence.append(word)
		else:
			#bigram stuff
			word = use_bigram(previous_word)
			print "Bigram: " + word	
			if word is None:
				word = use_unigram()
				print "Unigram: " + word
			sentence.append(word) #at this point there SHOULD be a word cause unigram gives no f***s
		i += 1
	return sentence

def poisson_probability(observation, actual):
	k = minimumEditDistance(observation, actual)
	l = 0.01
	probability = ((l ** k) * math.exp(l))/math.factorial(k)
	return probability

def get_bigram_probability(possible_word, previous_word):
	possible_lines = get_lines_of_bigram(previous_word)
	# print possible_lines
	i = 0
	for line in possible_lines:
		# print "Checking line " + str(i) + "..."
		if int (line.split()[0]) == get_index_of_word(previous_word) and int (line.split()[1]) == get_index_of_word(possible_word):
			return get_probability(line)
		i += 1
	return 0
 
def sentence_corrector(sentence):
	words = sentence.split()
	words.reverse()
	sentence_corrector_recursive(words)
	return "something..."

def sentence_corrector_recursive(words):	
	fp = open("data/vocab.txt")
	vocab_words = []
	for line in fp:
		vocab_words.append(line.split()[1])
	max_probability_sequence = []
	max_probability = 0
	for i in range(0, (len(words) - 1)):
		print i
		if len(words) == 1:
			previous_word = "<s>"
			print "done"
		else:			
			previous_word = words[i-1]
			word = words[i]
			print "Previous word: " + previous_word + " Current word: " + word
			for possible_word in vocab_words:
				probability = poisson_probability(word, possible_word) * (get_bigram_probability(possible_word, previous_word) * sentence_corrector_recursive(words[1:]))
				if probability > max_probability:
					max_probability = probability
	return max_probability

#main execution:
# print "Generated sentence:"
# print sentence_generator()
# print "Correcting sentence " + sentenceToCorrect
# print sentence_corrector(sentenceToCorrect)
# print use_trigram("believe", "I")
print sentence_corrector("This is a test")
