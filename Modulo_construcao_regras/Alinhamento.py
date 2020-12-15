import collections
import json
import csv
import os
from operator import itemgetter
from pyjarowinkler import distance
import word_embeddings
import WordNet_NLTK

modelo_embeddings = None

threshold_wordembeddings = 0.3


def merge_sublistas(lista):

	sublistas_merged = [j for i in lista for j in i]
	return sublistas_merged


def alinhamento_max(lista_tokens_repetidos, lista_tokens_repetidos_2, alinhamento_wordNet):

	"""
	Escolhe o par com maior semelhança para uma dada palavra ou gesto.
	:param lista_tokens_repetidos: lista de palavras repetidas
	:param lista_tokens_repetidos_2: lista de gestos repetidos
	:param alinhamento_wordNet: lista com os pares alinhados e o valor de semelhança alinhados pela WordNet
	:return: lista com os pares alinhados e o valor de semelhança sem repetidos
	"""

	resultados_depois_WordNet = []


	if len(lista_tokens_repetidos) < len(lista_tokens_repetidos_2) and (
			len(lista_tokens_repetidos) != 0 and len(lista_tokens_repetidos_2) != 0):
		lista_tokens = lista_tokens_repetidos
		ind = 2
	elif len(lista_tokens_repetidos_2) == 0 and len(lista_tokens_repetidos) != 0:
		lista_tokens = lista_tokens_repetidos
		ind = 2
	elif len(lista_tokens_repetidos) == 0 and len(lista_tokens_repetidos_2) != 0:
		lista_tokens = lista_tokens_repetidos_2
		ind = 1
	elif len(lista_tokens_repetidos) == 0 and len(lista_tokens_repetidos_2) == 0:
		resultados_depois_WordNet = alinhamento_wordNet
		lista_tokens = lista_tokens_repetidos_2
		ind = 1
	elif len(lista_tokens_repetidos) == len(lista_tokens_repetidos_2) and (
			len(lista_tokens_repetidos) != 0 and len(lista_tokens_repetidos_2) != 0):
		lista_tokens = lista_tokens_repetidos
		ind = 2

	else:
		lista_tokens = lista_tokens_repetidos_2
		ind = 1


	if len(lista_tokens) != 0:
		for i in lista_tokens:
			key_word = max(filter(lambda x: x[ind] == i, alinhamento_wordNet), key=itemgetter(3))
			resultados_depois_WordNet.append((key_word[0], key_word[1], key_word[2], key_word[3]))

		resultados_depois_WordNet = resultados_depois_WordNet + [(a, b, c, d) for a, b, c, d in list(
			filter(lambda x: x[2] not in lista_tokens_repetidos and x[1] not in lista_tokens_repetidos_2,
				   alinhamento_wordNet))]

	return resultados_depois_WordNet


def alinhar_word_embbeding(embeddings, tuplos_nao_alinhados, alinhamento_wordNet_final):
	"""
	Calcula a semelhança entre word embeddings. É o último passo do alinhamento.
	Retorna o alinhamento final.
	:param embeddings: modelo GloVe de 600 dimensões pré-treinado
	:param tuplos_nao_alinhados: lista de tuplos que representam as palavras não alinhadas
	:param alinhamento_wordNet_final: lista com os pares palavra-glosa alinhados com a wordnet
	:return: lista com o alinhamento final, lista com os pares palavra-glosa alinhados com a wordnet, conjunto com os gestos alinhados, conjunto com as palavras alinhadas
	"""

	word_embeddings_values = []

	for a, n, j in tuplos_nao_alinhados:
		valor = word_embeddings.sim(n, j, embeddings)
		if valor > threshold_wordembeddings:
			word_embeddings_values.append((a, n, j, valor))


	if word_embeddings_values:
		lgp_words, pt_words = zip(
			*[(i[2], i[1]) for i in word_embeddings_values])
		lgp_words, pt_words = list(lgp_words), list(pt_words)

		gesto_word_embeddings_repetido = [item for item, count in collections.Counter(lgp_words).items() if count > 1]
		palavra_word_embeddings_repetida = [item for item, count in
											collections.Counter(pt_words).items() if count > 1]


		resultados_word_embeddings = alinhamento_max(gesto_word_embeddings_repetido, palavra_word_embeddings_repetida,
													 word_embeddings_values)
	else:
		resultados_word_embeddings = []


	resultados = alinhamento_wordNet_final + resultados_word_embeddings


	palavras_alinhadas = set(k[0] for k in resultados)
	gestos_alinhados = set(k[1] for k in resultados)


	return resultados, alinhamento_wordNet_final, gestos_alinhados, palavras_alinhadas




def separar_composicao(elemento_frasico_lgp):
	"""
	Separa gestos compostos por mais do que uma palavra em português, ex: TER-MUITO.
	:param elemento_frasico_lgp: lista de tuplos (gesto, lema, classe gramatical) dos gestos das frases em LGP do corpus.
	:return: lista com os gestos compostos separados, lista com os gestos compostos, lista com os gestos compostos identificados, lista com os gestos compostos identificados separados,
	dicionário com o mapeamento entre o resultado da separação dos gestos e o gesto composto inicial.
	"""

	gestos_sem_compostos = []
	gesto_composto = []
	gesto = []
	versao_velha = elemento_frasico_lgp
	classes = {}
	correspondencia = {}


	marcadores_composicao = ["-", "_"]

	for m in marcadores_composicao:
		for z, g, cg in elemento_frasico_lgp:

			if m in g and g not in gesto_composto:  # ex: ter-muito

				gesto_composto.append(g)

				gesto_dividido = g.split(m)

				gesto.append(gesto_dividido)  # [[ter, muito]]
				for i in gesto_dividido:
					correspondencia[i] = g
					classes[i] = cg

			if m not in g and g not in gesto_composto and len([i for i in gestos_sem_compostos if i[1] == g]) == 0:
				gestos_sem_compostos.append((z, g, cg))

	gestos_compostos = [(z.lower(), i, classes[i]) for j in gesto for i in j if gesto]  # [(ter,v),(muito,v)]

	elemento_frasico_lgp = gestos_compostos + gestos_sem_compostos


	return elemento_frasico_lgp, versao_velha, gestos_compostos, gesto, correspondencia


def sublista_gestos_compostos(gesto, m):
	"""
	Verifica se o gesto corresponde a um gesto composto.
	:param gesto: Lista com os gestos compostos unidos.
	:param m: gesto individual
	:return: Lista com os gestos compostos divididos, caso o gesto em m pertença a um gesto composto. Caso contrário retorna a lista com o gesto original.
	"""
	for g in gesto:
		if m in g:
			return g
	return [m]


def remove_tuplos_compostos(sim, sublista):
	"""
	Retorna as palavras e os seus lemas que foram alinhadas com gestos compostos.
	:param sim: lista com a semelhança entre gestos e palavras
	:param sublista: Lista com os gestos
	:return: palavras em português alinhadas com os gestos compostos, lemas dessas palavras
	"""
	pt_compostas = []
	pt_compostas_lemas = []
	for s in sublista:
		for i in range(len(sim)):
			if s in sim[i]:
				pt_compostas.append(sim[i][0])
				pt_compostas_lemas.append(sim[i][1])
				sim.pop(i)
				break

	return pt_compostas, pt_compostas_lemas


def get_lexico_lgp(correspondencia, m):
	"""
	Devolve o gesto original.
	:param correspondencia: Dicionário com o mapeamento entre os gestos compostos originais e os gestos separados.
	:param m: lista com tuplos (palavra, gesto, semelhança)
	:return: gesto. Se for um gesto composto, devolve um gesto composto.
	"""
	if m in correspondencia:
		lexico_lgp = correspondencia[m]
		return lexico_lgp
	else:
		lexico_lgp = m
		return lexico_lgp


def get_classe(palavra, classes_gramaticais, link):
	"""
	Devolve a classe gramatical (do gesto ou palavra) com o respetivo número de correspondência.
	:param palavra: string do gesto ou palavra
	:param classes_gramaticais: lista com as classes gramaticais, contém tuplos (palavra, classe)
	:param link: Número de correspondência das classes gramaticais do lado português da regra com o lado da LGP
	:return: String da classe gramatical (do gesto ou palavra) com o respetivo número de correspondência
	"""

	cl = list(filter(lambda x: x[0] == palavra, classes_gramaticais))

	return cl[0][1] + str(link)


def remover_tuplos_alinhados(combinacao, alinhamento):
	"""
	Remove da lista combinacao, os pares que já foram alinhados.
	:param combinacao: lista com tuplos com as combinações entre os gestos e palavras de uma frase em pt e em LGP
	:param alinhamento: lista com os pares alinhados e o valor de semelhança alinhados pela WordNet
	:return: Lista com os pares que ainda faltam alinhar. É uma lista de tuplos (palavra, lema_palavra, lema_gesto)
	"""

	for j in alinhamento:
		combinacao = [t for t in combinacao if t[1] != j[0][1] and t[2] != j[0][2]]


	return combinacao


def ordenar_alinhamento(elemento_frasico, alinhamento):
	"""
	Ordena os pares alinhados conforme as frases originais.
	:param elemento_frásico: lista de tuplos com as informações (palavra/gesto, lema, classe gramatical) do elemento frásico
	:param alinhamento: dicionário com as palavras/gestos alinhados e as suas classes gramaticais
	:return: Lista com as palavra/gestos alinhados ordenados conforme a sua ordem na frase original.
	"""

	alinhamento_ordenado = []

	for t in elemento_frasico:
		for k, v in alinhamento.items():
			if k == t[1]:
				alinhamento_ordenado.append(v)

	return alinhamento_ordenado


def compara_listas(elemento_frasico_regra_1, elemento_frasico_regra_2):
	"""
	Verifica se o mesmo lado das duas regras são equivalentes. Se forem retorna True, caso contrário, falso.
	Ex: compara_listas((['A1', 'B1', 'C2', 'D3'], 'INT'), (['A1', 'B1', 'C2', 'D3'], 'NEG')), "TRUE")
	:param elemento_frasico_regra_1: tuplo com a sequência das classes gramaticais e o tipo da frase da regra 1.
	:param elemento_frasico_regra_2: tuplo com a sequência das classes gramaticais e o tipo da frase da regra 2.
	:return: True, se forem equivalentes, False, caso contrário.
	"""
	map_regra = {}

	if len(elemento_frasico_regra_1[0]) != len(elemento_frasico_regra_2[0]):
		return False

	if elemento_frasico_regra_1[1]!=elemento_frasico_regra_2[1]:
		return False


	for i in range(len(elemento_frasico_regra_1[0])):
		key_pt = elemento_frasico_regra_1[0][i][-1]
		key_lgp = elemento_frasico_regra_2[0][i][-1]

		if elemento_frasico_regra_1[0][i][:-1] != elemento_frasico_regra_2[0][i][:-1]:
			return False

		if key_pt not in map_regra.keys() and key_lgp not in map_regra.values():
			map_regra[key_pt] = elemento_frasico_regra_2[0][i][-1]
			continue

		else:
			try:
				if map_regra[key_pt] == elemento_frasico_regra_2[0][i][-1]:
					continue
				else:

					return False


			except KeyError:
				return False


	return True


def compara_regra(regra_pt_1, regra_lgp_1, regra_pt_2, regra_lgp_2):
	"""
	Verifica se duas regras são a mesma.
	ex: regra_pt = [(['A1', 'B1', 'C2', 'D3'], 'INT'), (['A1', 'B1', 'C2', 'D3'], 'CAN')]
	regra_lgp = [(['M2', 'C3', 'J1'], 'INT'), (['M2', 'C3', 'J1'], 'CAN')]
	compara_regra(regra_pt[0], regra_lgp[0], regra_pt[1], regra_lgp[1])
	:param regra_pt_1: Lado português da regra 1.
	:param regra_lgp_1: Lado LGP da regra 1.
	:param regra_pt_2: Lado português da regra 2.
	:param regra_lgp_2: Lado LGP da regra 2.
	:return: True se forem iguais, False, caso contrário.
	"""

	return compara_listas(regra_pt_1, regra_pt_2) and compara_listas(regra_lgp_1, regra_lgp_2)


def estatistica_regras(regras_pt, regras_lgp):
	"""
	Contagem das regras morfossintáticas no corpus.
	:param regras_pt: Lado português das regras (lista)
	:param regras_lgp: Lado LGP das regras (lista)
	:return: Dicionário com a frequência de cada regra. Ex: {"(0, 'INT')": 1, "(1, 'CAN')": 1, "(2, 'INT')": 1}
	"""
	estatistica = {}
	repetido = set()


	for i in range(len(regras_pt)):

		tipo = regras_pt[i][1]
		if i in repetido:
			continue


		if tipo == "":
			tipo = "CAN"


		if str((i,tipo)) not in estatistica.keys():
			estatistica[str((i, tipo))]= 1


		for j in range(len(regras_pt)):

			a = regras_pt[i]
			b = regras_lgp[i]
			c = regras_pt[j]
			d = regras_lgp[j]



			if i >= j:
				continue

			if j in repetido:
				continue


			if compara_regra(a,b,c,d):
				repetido.add(j)
				tipo = regras_pt[j][1]

				if tipo == "":
					tipo = "CAN"


				estatistica[str((i,tipo))] +=1

				if str((j, tipo)) in estatistica.keys():
					del estatistica[str((j,tipo))]

			else:

				tipo = regras_pt[j][1]

				if tipo == "":
					tipo = "CAN"

				if str((j, tipo)) not in estatistica.keys():
					estatistica.setdefault(str((j,tipo)),0)
					estatistica[str((j, tipo))] += 1

	return estatistica

def converte_json(dic, opcao):
	"""
	Guarda a frequência de cada regra num ficheiro JSON.
	:param dic: Dicionário com as frequências.
	:param opcao: elemento frásico (sujeito, predicado ou modificador).
	:return:
	"""

	with open('Estatisticas/frequencia_regras_'+opcao+'.json', 'w+') as json_file:
		json.dump(dic, json_file)



def guardar_regras(cl_pt, cl_lgp, opcao, tipo):
	"""
	Guarda as regras morfossintáticas num ficheiro CSV.
	:param cl_pt: classe gramatical da palavra.
	:param cl_lgp: classes gramaticais do gesto.
	:param opcao: elemento frásico (sujeito, predicado ou modificador).
	:param tipo: tipo de frase.
	:return:
	"""
	if not os.path.exists('Regras_de_traducao/Regras_morfossintaticas/'):
		os.makedirs('Regras_de_traducao/Regras_morfossintaticas/', 0o777)



	with open('Regras_de_traducao/Regras_morfossintaticas/regras_de_' + opcao + '.csv', 'a+') as f:
		csvw = csv.writer(f, delimiter='\t')
		csvw.writerow([" ".join(cl_pt), " ".join(cl_lgp), tipo])



def alinhamento(elemento_frasico_pt, elemento_frasico_lgp, opcao, tipo):
	"""
	Função principal do alinhamento de palavras e gestos e construção do dicionário bilingue.
	:param elemento_frasico_pt: Lista com tuplos (palavra, lema, classe gramatical) ex:
	:param elemento_frasico_lgp: Lista com tuplos (gesto, lema, classe gramatical) ex:
	:param opcao: elemento frásico (sujeito, predicado ou modificador). ex: "pred"
	:param tipo: tipo de frase. ex: "NEG"
	:return:
	"""

	palavras = []
	gestos = []
	valores_wordNet = []
	alinhamento_wordNet = []
	tuplos_alinhados = []
	combinacao = []
	sim = []
	classes_gramaticais_pt = []
	classes_gramaticais_lgp = []


	# 1º passo: identificar e tratar dos gestos compostos (gestos que são compostos por mais do que uma palavra portuguesa, como: TER-MUITO -> Haver um grande)
	elemento_frasico_lgp, versao_velha, versao_nova, gesto, correspondencia = separar_composicao(elemento_frasico_lgp)


	for s, p, c in elemento_frasico_pt:  # tuplo
		for n, g, cg in elemento_frasico_lgp:

			palavras.append(p)
			gestos.append(g)
			combinacao.append((s, p, g))

			sim_valor = distance.get_jaro_distance(p, g, winkler=True, scaling=0.1)

			# 1ª caso - palavras e gestos com 100% de matching
			sim.append((s, p, g, sim_valor))

			if len(list(filter(lambda x: x[0] == p, tuplos_alinhados))) == 0 and len(
					list(filter(lambda x: x[1] == g, tuplos_alinhados))) == 0:
				if sim_valor == 1.0:
					classes_gramaticais_pt.append((p, c)) #ex: classes_gramaticais_pt = [('ostentar', 'V'), ('muito', 'ADV'), ('riqueza', 'N')]
					classes_gramaticais_lgp.append((g, cg)) #ex: classes_gramaticais_lgp = [('ter', 'V'), ('muito', 'ADJ'), ('rico', 'ADJ')]

					tuplos_alinhados.append((p, g))
					alinhamento_wordNet.append([(s, p, g, sim_valor)])

				# 2º caso - sujeito, objeto e verbo apenas com 1 termo (ex: Escrevo - Escrever)

				if len(elemento_frasico_pt) == 1 and len(elemento_frasico_lgp) == 1 and p == g:

					tuplos_alinhados.append((p, g))
					alinhamento_wordNet.append([(s, p, g, 1.0)])
					classes_gramaticais_pt.append((p, c))
					classes_gramaticais_lgp.append((g, cg))

				else:
					#3º caso: wordnet (compara-se os lemas da palavras com os lemas dos gestos)

					palavras_alinhadas, palavras_não_alinhadas, valores_semelhanca_jaro = WordNet_NLTK.synsets_similarity_values(s,
						p, g)
					valores_wordNet.append(valores_semelhanca_jaro)

					if palavras_alinhadas:
						alinhamento_wordNet.append(palavras_alinhadas)

	tuplos_nao_alinhados = remover_tuplos_alinhados(combinacao, alinhamento_wordNet)

	alinhamento_wordNet = merge_sublistas(alinhamento_wordNet)


	if alinhamento_wordNet:

		tokens_lgp_alinhados, tokens_pt_alinhados = zip(*[(i[2], i[1]) for i in alinhamento_wordNet])
		tokens_lgp_alinhados, tokens_pt_alinhados = list(tokens_lgp_alinhados), list(tokens_pt_alinhados)

		gestos_repetidos = [item for item, count in collections.Counter(tokens_lgp_alinhados).items() if count > 1]
		palavras_repetidas = [item for item, count in collections.Counter(tokens_pt_alinhados).items() if count > 1]


		alinhamento_wordNet_final = alinhamento_max(gestos_repetidos, palavras_repetidas,
													alinhamento_wordNet)

		# word_embeddings

		if tuplos_nao_alinhados:
			alinhamento_wordNet_final, resultados, gestos_alinhados, palavras_alinhadas = alinhar_word_embbeding(
				modelo_embeddings, tuplos_nao_alinhados, alinhamento_wordNet_final)

			for k in alinhamento_wordNet_final:
				classe_pt = list(filter(lambda x: x[1] == k[1], elemento_frasico_pt))[0][2]
				classe_lgp = list(filter(lambda x: x[1] == k[2], elemento_frasico_lgp))[0][2]

				classes_gramaticais_pt.append((k[1], classe_pt))
				classes_gramaticais_lgp.append((k[2], classe_lgp))

		else:
			for k in alinhamento_wordNet_final:
				classe_pt = list(filter(lambda x: x[1] == k[1], elemento_frasico_pt))[0][2]
				classe_lgp = list(filter(lambda x: x[1] == k[2], elemento_frasico_lgp))[0][2]

				classes_gramaticais_pt.append((k[1], classe_pt))
				classes_gramaticais_lgp.append((k[2], classe_lgp))



	else:

		alinhamento_wordNet_final, resultados, gestos_alinhados, palavras_alinhadas = alinhar_word_embbeding(modelo_embeddings,
			tuplos_nao_alinhados, alinhamento_wordNet)

		if alinhamento_wordNet_final:

			for k in alinhamento_wordNet_final:
				classe_pt = list(filter(lambda x: x[1] == k[1], elemento_frasico_pt))[0][2]
				classe_lgp = list(filter(lambda x: x[1] == k[2], elemento_frasico_lgp))[0][2]


				classes_gramaticais_pt.append((k[1], classe_pt))
				classes_gramaticais_lgp.append((k[2], classe_lgp))


		else:
			alinhamento_wordNet_final = alinhamento_wordNet

	if alinhamento_wordNet_final:

		tokens_lgp_alinhados, tokens_pt_alinhados = zip(*[(i[2], i[1]) for i in alinhamento_wordNet_final])
		tokens_lgp_alinhados, tokens_pt_alinhados = list(tokens_lgp_alinhados), list(tokens_pt_alinhados)

		gestos_repetidos = [item for item, count in collections.Counter(tokens_lgp_alinhados).items() if count > 1]
		palavras_repetidas = [item for item, count in collections.Counter(tokens_pt_alinhados).items() if count > 1]


		alinhamento_wordNet_final = alinhamento_max(gestos_repetidos, palavras_repetidas,
													alinhamento_wordNet_final)


		# tudo o que está para cima é o alinhamento
		# Para baixo, atribui um número de correspondência a cada classe gramatical e o dicionário bilingue é construído.


		link = 1 #número de correspondência
		classes_pt = []
		classes_lgp = []

		alinhamento_pt = {}
		alinhamento_lgp = {}

		sim = alinhamento_wordNet_final #ex:sim = [('ter', 'ter', 1.0),('muito', 'muito', 1.0), ('rico', 'rico', 1.0), ('pouco', 'pouco', 1.0)]

		while sim:

			m = sim[0]
			sublista = sublista_gestos_compostos(gesto, m[2])


			lexico_pt, lexico_pt_lema = remove_tuplos_compostos(sim, sublista)

			for t in lexico_pt_lema:
				classe = get_classe(t, classes_gramaticais_pt, link)
				classes_pt.append(classe)
				alinhamento_pt[t] = classe

			classes_lgp.append(get_classe(m[2], classes_gramaticais_lgp, link))
			alinhamento_lgp[m[2]] = get_classe(m[2], classes_gramaticais_lgp, link)

			lexico_lgp = get_lexico_lgp(correspondencia, m[2])


			if not os.path.exists('Dicionario/'):
				os.makedirs('Dicionario/', 0o777)

			with open('Dicionario/dicionario.csv', 'a+') as f:
				csvw = csv.writer(f, delimiter='\t')
				csvw.writerow([" ".join(lexico_pt)," ".join(lexico_pt_lema), lexico_lgp, classes_lgp[0][:-1]])



			link += 1


		# ordenar o alinhamento conforme as frases originais

		ordenado_pt = ordenar_alinhamento(elemento_frasico_pt, alinhamento_pt)

		ordenado_lgp = ordenar_alinhamento(elemento_frasico_lgp, alinhamento_lgp)

		# escrever no ficheiro, as regras
		guardar_regras(ordenado_pt, ordenado_lgp, opcao, tipo)

	else:
		ordenado_pt = []
		ordenado_lgp = []


	return ordenado_pt, ordenado_lgp




def valor_estatisticas(pt, lgp, elemento):
	"""
	Contagem das regras morfossintáticas.
	Guarda as estatísticas recolhidas sobre as regras morfossintáticas num ficheiro JSON.
	:param pt:
	:param lgp:
	:param elemento:
	:return:
	"""

	if pt and lgp:
		estatistica_suj = estatistica_regras(pt, lgp)
		converte_json(estatistica_suj, elemento)


def retira_pontuacao(info):
	"""
	Remove a pontuação das frases.
	:param info: frase
	:return:
	"""
	if info:
		classes_gramaticais = list(list(zip(*info))[2])
		indices_pontuacao = []
		for i, p in enumerate(classes_gramaticais):
			if p.startswith("F"):
				indices_pontuacao.append(i)

		for j in sorted(indices_pontuacao, reverse=True):
			del info[j]

def retira_artigos(info):
	"""
	Remove os determinantes artigos.
	:param info: frase
	:return:
	"""
	if info:
		classes_gramaticais = list(list(zip(*info))[2])
		lema = list(list(zip(*info))[1])
		indices_pontuacao = []
		for i, p in enumerate(classes_gramaticais):
			if p.startswith("DET") and (lema[i] in ["um","uma", "uns", "umas", "o","os", "as", "a"]):
				indices_pontuacao.append(i)

		for j in sorted(indices_pontuacao, reverse=True):
			del info[j]


def alinhamento_por_elemento(classes_pt,
								 classes_lgp, embeddings):
	"""
	Alinhamento por elemento frásico. Primeiro, removem-se as pontuações e os determinantes artigos definidos e depois
	procede-se ao alinhamento.
	:param classes_pt: lista com o objeto que guarda os elementos frásicos das frases em pt
	:param classes_lgp: lista com o objeto que guarda os elementos frásicos das frases em LGP
	:param embeddings: modelo pré-treinado com o algoritmo GloVe de 600 dimensões
	:return:
	"""

	global modelo_embeddings
	modelo_embeddings = embeddings


	pt_suj, lgp_suj, pt_pred, lgp_pred, pt_mod, lgp_mod = [], [], [], [], [], []

	for i in range(len(classes_lgp)):
		pt = classes_pt[i]
		lgp = classes_lgp[i]

		#retirar pontuacao
		retira_pontuacao(pt.sujeito)
		retira_pontuacao(pt.predicado)
		retira_pontuacao(pt.outros)

		#retira determinantes artigos
		retira_artigos(pt.sujeito)
		retira_artigos(pt.predicado)
		retira_artigos(pt.outros)

		if pt.sujeito and lgp.sujeito:
			a,b = alinhamento(pt.sujeito, lgp.sujeito, 'suj', lgp.tipo_frase)
			if a and b:
				pt_suj.append((a, lgp.tipo_frase))
				lgp_suj.append((b, lgp.tipo_frase))

		if pt.predicado and lgp.predicado:
			a, b = alinhamento(pt.predicado, lgp.predicado, 'pred', lgp.tipo_frase)
			if a and b:
				pt_pred.append((a, lgp.tipo_frase))
				lgp_pred.append((b, lgp.tipo_frase))

		if pt.outros and lgp.outros:
			a, b = alinhamento(pt.outros, lgp.outros, 'mod', lgp.tipo_frase)
			if a and b:
				pt_mod.append((a, lgp.tipo_frase))
				lgp_mod.append((b, lgp.tipo_frase))


	valor_estatisticas(pt_mod, lgp_mod, "mod")
	valor_estatisticas(pt_pred, lgp_pred, "pred")
	valor_estatisticas(pt_suj, lgp_suj, "suj")