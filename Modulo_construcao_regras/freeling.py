#!/usr/bin/python3

import sys

from freeling_values import freeling_values

sys.path.append('/usr/local/share/freeling/APIs/python3')
import pyfreeling


def ProcessSentences(ls):
	words = [] #lista de cada palavra
	lemmas = [] #lista com cada lemma
	tags = [] #lista com cada tag de cada palavra
	lemma_verdadeiro = [] #sem a tranformacao de numeros para escrito (ex: dois = 2)

	# for each sentence in list
	for s in ls :
	# for each word in sentence
		for w in s :
			if w.get_tag() == "Z" or w.get_tag().startswith("P"):
				words.append(w.get_form())
				lemmas.append(w.get_form().lower())
				lemma_verdadeiro.append(w.get_lemma())
				tags.append(w.get_tag())
			else:
				words.append(w.get_form())
				lemmas.append(w.get_lemma())
				lemma_verdadeiro.append(w.get_lemma())
				tags.append(w.get_tag())



	return words, lemmas, lemma_verdadeiro, tags


def word_tokens(frase, freeling_values):

	# tokenize input line into a list of words
	lw = freeling_values.tk.tokenize(frase)
	# split list of words in sentences, return list of sentences
	ls = freeling_values.sp.split(lw)

	# ner_tags=NerTagger(lm)
	# perform morphosyntactic analysis and disambiguation
	ls = freeling_values.morfo.analyze(ls)

	# ls = nec.analyze(ls) #ner.analyze é ner e nec é named entity classification

	ls = freeling_values.tagger.analyze(ls)

	words = [] #lista com cada lemma

	# for each sentence in list
	for s in ls :
	# for each word in sentence
		for w in s :
			words.append(w.get_form())

	return words


## -----------------------------------------------
## Set desired options for morphological analyzer
## -----------------------------------------------
def my_maco_options(lang,lpath) :

	# create options holder
	opt = pyfreeling.maco_options(lang);

	# Provide files for morphological submodules. Note that it is not
	# necessary to set file for modules that will not be used.
	opt.UserMapFile = "";
	opt.LocutionsFile = lpath + "locucions.dat";
	opt.AffixFile = lpath + "afixos.dat";
	opt.ProbabilityFile = lpath + "probabilitats.dat";
	opt.DictionaryFile = lpath + "dicc.src";
	opt.NPdataFile = lpath + "np.dat";  #name recognition
	opt.PunctuationFile = lpath + "../common/punct.dat";


	return opt;

def load_freeling(valor):
	# set locale to an UTF8 compatible locale
	pyfreeling.util_init_locale("default");
	# get requested language from arg1, or English if not provided
	lang = "pt"

	ipath = "/usr/local";

	# path to language data
	lpath = ipath + "/share/freeling/" + lang + "/"

	# create analyzers
	tk = pyfreeling.tokenizer(lpath + "tokenizer.dat");
	sp = pyfreeling.splitter(lpath + "splitter.dat");

	# create the analyzer with the required set of maco_options
	morfo = pyfreeling.maco(my_maco_options(lang, lpath));
	#  then, (de)activate required modules
	morfo.set_active_options(False,  # UserMap
							 True,  # NumbersDetection,
							 True,  # PunctuationDetection,
							 False,  # DatesDetection,
							 True,  # DictionarySearch,
							 True,  # AffixAnalysis,
							 False,  # CompoundAnalysis,
							 True,  # RetokContractions,
							 valor,  # MultiwordsDetection,
							 valor,  # NERecognition,
							 True,  # QuantitiesDetection,
							 True);  # ProbabilityAssignment

	# create tagger
	tagger = pyfreeling.hmm_tagger(lpath + "tagger.dat", True, 2)

	valores_freeling = freeling_values(lpath, tk, sp, morfo, tagger)


	return valores_freeling

def main(text, valores_freeling):
	## ----------------------------------------------
	## -------------    MAIN PROGRAM  ---------------
	## ----------------------------------------------
	# process input text

	# tokenize input line into a list of words
	lw = valores_freeling.tk.tokenize(text)
	# split list of words in sentences, return list of sentences
	ls = valores_freeling.sp.split(lw)

	# perform morphosyntactic analysis and disambiguation
	ls = valores_freeling.morfo.analyze(ls)

	ls = valores_freeling.tagger.analyze(ls)

	words, lemmas, lemma_verdadeiro, pred_tags = ProcessSentences(ls)

	return words, lemmas, lemma_verdadeiro, pred_tags

