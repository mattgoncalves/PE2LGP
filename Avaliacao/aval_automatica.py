# -*- coding: utf-8 -*-
import csv
import sys
import pyter
from nltk.translate.bleu_score import corpus_bleu


def aval_corpus_bleu(references, candidates):
	"""
	Calcula os valores de BLEU cumulativos até 4-gramas.
	:param references: Lista com as traducoes no corpus de teste.
	:param candidates: Lista com as traducoes do sistema de traducao.
	:return: valor de bleu total, valor de bleu de 1 grama até 4 gramas
	"""
	score_bleu = corpus_bleu(references, candidates)

	one_gram = corpus_bleu(references, candidates, weights=(1, 0, 0, 0))
	two_grams = corpus_bleu(references, candidates, weights=(0.5, 0.5, 0, 0))
	three_grams = corpus_bleu(references, candidates, weights=(0.33, 0.33, 0.33, 0))
	four_grams = corpus_bleu(references, candidates, weights=(0.25, 0.25, 0.25, 0.25))


	return score_bleu, one_gram, two_grams, three_grams, four_grams


def escolha_ref_ter(references, candidate):
	"""
	No TER usa-se a referência mais próxima do output do tradutor.
	Esta função calcula para todas as referências o valor TER e escolhe o menor.
	:param references: Lista com as traducoes no corpus de teste.
	:param candidate: Lista com as traducoes do sistema de traducao.
	:return: TER minimo, a traducao de referencia usada para calcular o TER minimo
	"""
	score = []
	for r in references:
		score.append(pyter.ter(candidate, r))

	index_score = score.index(min(score))
	reference_escolhida = references[index_score]

	return min(score), reference_escolhida


def aval_corpus_ter(references, candidates):
	scores_totais = []
	references_escolhidas = []
	score_0 = []
	for i, r in enumerate(references):
		score_ter, reference = escolha_ref_ter(r, candidates[i])
		scores_totais.append(score_ter)
		if score_ter > 0:
			score_0.append(i+1)
		references_escolhidas.append(reference)

	score_average = sum(scores_totais) / len(scores_totais)

	return score_average

def abrir_csv(corpus, traducoes):
	"""
	Abre os ficheiros com as traduções de referência e as traduções do sistema.
	:param corpus: Ficheiro CSV com as referências
	:param traducoes: Ficheiro CSV com as traduções do sistema
	:return: As linhas do csv referentes traduçoes no corpus de teste e as traduçoes do sistema.
	"""
	references = []
	candidates = []
	with open(corpus) as csvfile:
		for l in csv.reader(csvfile, delimiter='\t'):
			references.append(l[1])
	with open(traducoes) as csvfile:
		for l in csv.reader(csvfile, delimiter='\t'):
			candidates.append(l[0])
	return references, candidates

def convert_lines(linhas_ref, linhas_cand):
	"""
	Converte a estrutura das traduções de acordo com a estrutura que as medidas recebem.
	:param lines: lista com as traduções.
	:return: Lista com as frases com a nova estrutura.
	"""
	references = []
	candidates = []
	for j, r in enumerate(linhas_ref):
		ref = r.split("; ")  # ["ref1", "ref2",...]
		for i, v in enumerate(ref):
			ref[i] = v.split()  # [["ref1"],["ref2"],["ref3"]]
		references.append(ref)  # [[["ref1"],["ref2"],["ref3"]]]
		candidates.append(linhas_cand[j].split())  # "[cand1]"


	return references, candidates

def aval_auto():
	"""
	Realiza a avaliação automática do sistema de tradução. Calcula o TER e o BLEU.
	Recebe DOIS ficheiros CSV na linha de comandos: o primeiro é o corpus de teste e o outro, as traduções do sistema.
	:return: O ficheiro resultados.txt com os valores das medidas TER e BLEU.
	"""

	args = sys.argv

	#abre os ficheiros CSV input
	linhas_ref, linhas_cand = abrir_csv(args[1], args[2])
	references, candidates = convert_lines(linhas_ref, linhas_cand)


	#calcula o TER
	score_average = aval_corpus_ter(references, candidates)
	
	#calcula o BLEU
	score_bleu, one_gram, two_grams, three_grams, four_grams = aval_corpus_bleu(references, candidates)

	#guarda os valores num ficheiro txt
	f = open("resultados.txt", "w")
	f.writelines(["TER: ", str(score_average),"\n", "BLEU: ", str(score_bleu),"\n", "BLEU 1-grama: ", str(one_gram),"\n", "BLEU 2-gramas: ", str(two_grams),"\n", "BLEU 3-gramas: ", str(three_grams),"\n", "BLEU 4-gramas: ", str(four_grams),"\n"])
	f.close()

aval_auto()