import json
import operator
import re

def abrir_freq(file):
	"""
	Abre o ficheiro json com o dicionário das frequências das regras.
	:param file: ficheiro json
	:return: dicionário com as frequências das regras no corpus.
	"""
	with open(file) as f:
		freq_svo_dict = json.load(f)
	return freq_svo_dict

def estrutura_frase(max_keys):

	regras_max = []
	for key in max_keys.split():
		m = re.search('(?<=\')\w+(?=\')', key)
		if m != None:
			regras_max.append(m.group(0))
	return regras_max[0]


def freq(freq_svo_dict, tipo, cop):
	"""
	Devolve a estrutura frásica que melhor se ajusta à frase de entrada de acordo com o seu tipo de frase.
	:param freq_svo_dict: dicionário com as frequências das regras
	:param tipo: tipo da frase
	:param cop: verdadeiro se tiver verbos copulativos, caso contrário, falso.
	:return: string com a estrutura frásica, ex:SVO
	"""
	tipo = tipo[0][0]
	if tipo == "EXCL" or tipo == "NEG":
		tipo = "CAN"

	regra = {}
	regra_cop = {}
	regras_cop = []
	regras = []
	for key, fre in freq_svo_dict.items():

		m=[]
		for k in key.split():

			if re.search('(?<=\')\w+(?=\')',k) != None:
				m.append(re.search('(?<=\')\w+(?=\')',k).group(0))
		p = False
		for a in m:
			if "V_cop" in a:
				p = True
				m[m.index(a)] = a.replace("V_cop", "V")
				if m[-1] == tipo:
					regra_cop[str(tuple(m))] = fre

			else:
				if p ==False and m[-1] == tipo:
					regra[str(tuple(m))] = fre



	if cop:
		maxi_cop = max(regra_cop.items(), key=operator.itemgetter(1))[1]
		max_keys_cop = [k for k, v in regra_cop.items() if v == maxi_cop]
		estrutura = estrutura_frase(max_keys_cop[0])

	else:
		maxi = max(regra.items(), key=operator.itemgetter(1))[1]
		max_keys = [k for k, v in regra.items() if v == maxi]
		estrutura = estrutura_frase(max_keys[0])

	return estrutura



