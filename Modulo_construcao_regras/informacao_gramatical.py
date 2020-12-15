import json
import sys
import csv
import os
import re
from dependencias import dependencies_spacy
from elementos_sintaticos import set_elementos, set_elementos_extracao
from identifica_suj_pred import identifica_elementos
from Frase_pt import Frase_pt
import parserELAN
import freeling


def atualiza_listas(lista, indices):
	"""
	Atualiza listas.
	:param lista: lista.
	:param indices: indice a remover da lista
	:return:
	"""
	for l in sorted(indices, reverse=True):
		del lista[l]


def converte_anotacao_lgp(anotacao, dic):
	"""
	Converte as tags das ferramentas de NLP para as do corpus.
	:param anotacao: string com a tag
	:param dic: dicionário com o mapeamento entre as tags
	:return: string com a tag convertida
	"""
	convertido =[]

	for a in anotacao:
		if a.lower() in dic.keys():
			convertido.append(dic[a.lower()])


	return " ".join(convertido)



def estrutura_frasica(info_elan, freeling_model):
	"""
	As frases em português do corpus são analisadas sintática e morfossintaticamente. Um objeto
	da classe Frase_pt é criado para guardar as informações gramaticais da frase em pt.
	:param info_elan: Objecto da classe Anotacao com as informações da frase extraída do corpus
	:param freeling_model: modelo do Freeling
	:return: estrutura sintática da frase em pt (1º argumento) e da frase em LGP (2º argumento) e objeto da classe
	Frase_pt com as informações gramaticais da frase em pt.
	"""

	words, lemmas, _, pred_tags = freeling.main(info_elan.frase_pt, freeling_model)


	frase_pt = " ".join(words)

	dep_words, dependency, indices_filhos = dependencies_spacy(frase_pt, freeling_model)
	_, lemmas_lgp, _, _ = freeling.main(
		info_elan.frase_lgp, freeling_model)


	for ind, w in enumerate(info_elan.classes_gramaticais.keys()):

		info_elan.append_lemmas(w, lemmas_lgp[ind])


	pt = Frase_pt(frase_pt)

	index_removidos = []

	for indx, val in enumerate(pred_tags):


		if not val.startswith('F'):
			pt.append_classes_gramaticais(words[indx], val)
			pt.append_lemmas(words[indx], lemmas[indx])

		if not val.startswith("DI") or not val.startswith(
				"DA"):
			pt.append_classes_gramaticais(words[indx], val)
			pt.append_lemmas(words[indx], lemmas[indx])


		if val.startswith("DI") and val.startswith(
				"DA"):
			index_removidos.append(indx)



	atualiza_listas(dependency, index_removidos)

	pt.converter_classes_gramaticais()

	dependencies_tags = identifica_elementos(dependency, indices_filhos)

	estrutura_pt = set_elementos_extracao(dependencies_tags, pred_tags, words, pt)

	conversao = ""

	map_corpus_lgp = {'arg_ext[-]': "", 'arg_ext': 'S', 'arg_int': 'O', 'v_tran': 'V', 'v_intr': 'V', 'v_⌀cop': 'V_cop', 'v_cop': 'V_cop'}

	for k, t in info_elan.analise_sintatica.items():


		t = re.sub('\(\w+\)', '', t)

		t = re.sub('NEG-', '', t).split(" ")


		resultado = converte_anotacao_lgp(t, map_corpus_lgp)


		if resultado not in conversao.split(" ")[-1]:
			conversao = conversao + " " + resultado


	estrutura_lgp = conversao.strip()

	return estrutura_pt, estrutura_lgp, pt


def estatistica_estrutura(lgp, tipo, estatisticas):
	"""
	Frequência das regras frásicas
	:param lgp: estrutura frásica (string)
	:param tipo: tipo da frase (string)
	:param estatisticas: dicionário com as estatísticas
	:return: dicionário com as estatísticas
	"""

	if str(tipo) == "":
			tipo = "CAN"
	if str((str(lgp).replace(" ", ""), tipo)) in estatisticas.keys():
		estatisticas[str((lgp.replace(" ", ""), tipo))] +=1
	else:
		estatisticas[str((lgp.replace(" ", ""), tipo))] = 1

	return estatisticas


def guarda_estatisticas(estatisticas):
	"""
	Guarda as estatísticas das regras frásicas num ficheiro json para serem usadas no módulo de tradução.
	:param estatisticas: dicionário
	:return:
	"""
	with open('Estatisticas/estruturas_frasicas/regras_frasicas.json', 'w+') as json_file:
		json.dump(estatisticas, json_file)


def main(ficheiro_html):
	"""
	Função que permite guardas as informações gramaticais das frases em LGP e PT (a estrutura frásica base, a ordem dos constituintes morfossintáticos e os lemas
	das frases em português e os lemas dos gestos).
	Guarda a frequência e as regras frásicas.
	:return: lista com objetos da classe Frase_pt com as informação gramaticais das frases em português, lista com objetos da classe Anotação que contém as informações
	extraídas do corpus (frase em pt, frase em lgp, classes gramaticais e análise sintáticas das frases em LGP).
	"""
	freeling_model = freeling.load_freeling(False) #análise morfossintática da frase em PT

	info = parserELAN.main(ficheiro_html) #parse das informações do corpus (que estão num ficheiro html exportado do ELAN).

	estatisticas = {}


	if not os.path.exists('Estatisticas/estruturas_frasicas/'):
		os.makedirs('Estatisticas/estruturas_frasicas/', 0o777)

	for i in info:
		if not any(v for v in list(i.analise_sintatica.values())): #as frases do corpus que não são orações são removidas
			info.remove(i)

	info_todas_pt = []

	for i in info:

		if not os.path.exists('Regras_de_traducao/Regras_frasicas/'):
			os.makedirs('Regras_de_traducao/Regras_frasicas/', 0o777)

		if i.get_tipo_frase() == "INT":
			estrutura_pt, estrutura_lgp, info_pt = estrutura_frasica(i, freeling_model)

			with open('Regras_de_traducao/Regras_frasicas/int.csv', 'a+') as f:
				csvw = csv.writer(f, delimiter='\t')
				csvw.writerow([estrutura_pt, estrutura_lgp])


		elif i.get_tipo_frase() == "EXCL":
			estrutura_pt, estrutura_lgp, info_pt = estrutura_frasica(i, freeling_model)
			with open('Regras_de_traducao/Regras_frasicas/excl.csv', 'a+') as f:
				csvw = csv.writer(f, delimiter='\t')
				csvw.writerow([estrutura_pt, estrutura_lgp])

		elif i.get_tipo_frase() == "NEG":
			estrutura_pt, estrutura_lgp, info_pt = estrutura_frasica(i, freeling_model)



			with open('Regras_de_traducao/Regras_frasicas/neg.csv', 'a+') as f:
				csvw = csv.writer(f, delimiter='\t')
				csvw.writerow([estrutura_pt, estrutura_lgp])


		else:
			estrutura_pt, estrutura_lgp, info_pt = estrutura_frasica(i, freeling_model)

			with open('Regras_de_traducao/Regras_frasicas/can.csv', 'a+') as f:
				csvw = csv.writer(f, delimiter='\t')
				csvw.writerow([estrutura_pt, estrutura_lgp])

		info_todas_pt.append(info_pt)

		estatistica_estrutura(estrutura_lgp, i.get_tipo_frase(), estatisticas)
	guarda_estatisticas(estatisticas)


	return info_todas_pt, info


