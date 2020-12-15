import csv
import re

from EditDistance import *
from Edit_distance import Edit_distance
from freq_json import freq, abrir_freq
from EditDistance import SequenceMatcher


def concantena_tipo_input(classes, frase):
	classes += frase.tipo[0]


def concantena_tipo_regras(regras, tipo_regras):
	regras.append(tipo_regras)


def tirar_bijecao(line):
	"""
	Retira o número de correspondência das regras.
	:param line: lista com a regra
	:return: lista com a regra sem número de correspondência.
	"""
	regra_sem_bij = []
	for e in line:
		regra_sem_bij.append(e[:-1])

	return regra_sem_bij


def distancia(i, ele):
	"""
	Calcula a distância de edição de cada elemento frásico com todas as regras criadas.
	:param i: Objeto do tipo Frase_input, frase em português.
	:param ele: string, elemento frásico ex:"pred" para predicado
	:return: Lista com as distancias a todas as regras, Lista com os objetos da classe Edit_distance, dicionário com a frequência das regras desse elemento frásico (ele)
	"""
	distancia = []
	distancia_obj = []

	if ele == "mod":
		classes_ele_sint = i.classes_outro

		f = "../Modulo_construcao_regras/Regras_de_traducao/Regras_morfossintaticas/regras_de_mod.csv"
		freq_file = "../Modulo_construcao_regras/Estatisticas/frequencia_regras_mod.json"

	elif ele == "pred":
		classes_ele_sint = i.classes_pred

		f = "../Modulo_construcao_regras/Regras_de_traducao/Regras_morfossintaticas/regras_de_pred.csv"
		freq_file = "../Modulo_construcao_regras/Estatisticas/frequencia_regras_pred.json"


	else:

		classes_ele_sint = i.classes_suj
		f = "../Modulo_construcao_regras/Regras_de_traducao/Regras_morfossintaticas/regras_de_suj.csv"
		freq_file = "../Modulo_construcao_regras/Estatisticas/frequencia_regras_suj.json"


	freq_pred = abrir_freq(freq_file)


	if classes_ele_sint:

		concantena_tipo_input(classes_ele_sint, i)

		with open(f, "r") as csv_file:
			csv_reader = csv.reader(csv_file, delimiter='	')

			for lines in csv_reader:

				tipo_regras = lines[2]
				if tipo_regras == "":
					tipo_regras = "CAN"

				line_pt = lines[0].split()


				line_lgp = lines[1].split()

				regra_pt_sem_bij = tirar_bijecao(line_pt)
				regras_lgp_sem_bij = tirar_bijecao(line_lgp)


				concantena_tipo_regras(regra_pt_sem_bij, tipo_regras)



				if regra_pt_sem_bij:

					sm = SequenceMatcher(classes_ele_sint, regra_pt_sem_bij)  # PT = ['ADJ', 'N', 'ADV', 'INT']  LGP = ['ADJ', 'N', 'ADV', 'INT']
					distancia.append(sm.distance())

					dist = sm.distance()


					del regra_pt_sem_bij[-1]


					obj = Edit_distance(dist, regra_pt_sem_bij, regras_lgp_sem_bij, line_pt, line_lgp, tipo_regras)
					obj.set_regra_toda(tipo_regras)
					obj.set_regra_toda_bij(tipo_regras)

					distancia_obj.append(obj)
	else:
		distancia, distancia_obj, freq_pred = [], [], []


	return distancia, distancia_obj, freq_pred


def min_sim(distance):
	"""
	Calcula a distância minima.
	:param distance: Lista com as distâncias de um elemento frásico a todas as regras.
	:return: Lista de inteiros, Lista com os indices das regras com a menor distância.
	"""
	indexes_min = [i for i, x in enumerate(distance) if x == min(distance)]
	return indexes_min



def desempata_tamanho(indexes_max, dist_obj):
	"""
	Escolhe a regra com maior tamanho.
	:param indexes_max: Lista com os indices das regras com maior frequência no corpus.
	:param dist_obj: Lista com objetos do tipo Edit_distance que guardam as informações da distância do elemento frásico
	a cada regra.
	:return: Lista com os indices das regras com maior tamanho e tamanho igual.
	"""
	tamanho_regras = []
	for i in indexes_max:

		tamanho_regras.append(len(dist_obj[i].regra_toda_bij))

	indexes_max = [i for i, x in enumerate(tamanho_regras) if x == max(tamanho_regras)]

	return indexes_max


def desempata_alfabetica(indexes_max, dist_obj):
	"""
	Função que escolhe a regra com base na ordem alfabética, escolhe a primeira.
	:param indexes_max: Lista com os indices das regras com maior frequência no corpus.
	:param dist_obj: Lista com objetos do tipo Edit_distance que guardam as informações da distância do elemento frásico
	a cada regra.
	:return: String com a regra escolhida.
	"""
	alfa = []
	for i in indexes_max:
		alfa.append('-'.join(dist_obj[i].regra_toda_bij))

	alfa.sort()
	regra_nova = alfa[0].split("-")

	return regra_nova


def desempata(distancia_min, dist_obj, freq_pred):
	"""
	Função que escolhe a regra mais adequada. A regra mais frequente é a escolhida. Se
	houver empates, escolhe-se a que tiver maior tamanho e depois a que aparecer em primeiro
	na ordenação alfabética.
	:param distancia_min: Lista com os indices das regras com menor distância.
	:param dist_obj: Lista com objetos do tipo Edit_distance que guardam as informações da distância do elemento frásico
	a cada regra.
	:param freq_pred: Dicionário com as frequências de cada regra no corpus.
	:return: Indice da regra escolhida, Lista com a regra escolhida.
	"""

	numeros_regras = []
	valores_regras = []
	keys_freq = []
	values_freq = []

	for o in distancia_min:

		numero_regra = o

		for k,v in freq_pred.items():
			numeros_regras.append(re.search('(?<=\()[0-9]*(?=,)', k).group(0))
			valores_regras.append(v)

		if str(numero_regra) in numeros_regras:
			keys_freq.append(o)
			values_freq.append(valores_regras[numeros_regras.index(str(numero_regra))])

	indexes_max = [i for i, x in enumerate(values_freq) if x == max(values_freq)]


	if len(indexes_max) > 1:
		indexes_max = desempata_tamanho(indexes_max, dist_obj)

		if len(indexes_max)>1:
			regra_max = desempata_alfabetica(indexes_max, dist_obj)

		else:
			regra_max = keys_freq[indexes_max[0]]

	else:
		regra_max = keys_freq[indexes_max[0]]

	return regra_max, dist_obj[regra_max]


def bijecao_valor(regra):
	"""
	Descobre o valor de correspondência a atribuir à classe gramatical nova.
	:param regra: Lista com a regra escolhida.
	:return: valor de correspondência, inteiro.
	"""

	bij_valores = []
	for r in regra:
		if r[-1].isnumeric():
			bij_valores.append(int(r[-1]))
	bij_valor = max(bij_valores)


	return bij_valor


def insert_regra_lgp(valor_insert, bij_valor, primeiro_valor, valor_bij_adicionar, bij_anterior, regra_lgp_bij, tipo):
	"""
	Função que insere a nova classe no lado da LGP.
	:param valor_insert: valor a inserir
	:param bij_valor: valor de correspondência da classe que está antes do valor inserido no lado português da regra
	:param primeiro_valor: TRUE se a nova classe foi adicionada no inicio da regra no lado português, FALSE, caso contrário
	:param valor_bij_adicionar: número de correspondência a adicionar
	:param bij_anterior: número de correspondência anterior da classe que está antes do valor inserido na lado português da regra
	:param regra_lgp_bij: Lista com o lado LGP da regra.
	:param tipo: tipo da frase
	:return: Lista com a nova versão do lado LGP da regra
	"""


	insert_value = list(filter(lambda x: x[-1] == str(bij_anterior), regra_lgp_bij))


	if insert_value:


		ind_nova_lgp = regra_lgp_bij.index(insert_value[0])
		if primeiro_valor:
			indx_inserir = ind_nova_lgp
		else:
			indx_inserir = ind_nova_lgp + 1


		nova_versao_regra_lgp = regra_lgp_bij

		nova_versao_regra_lgp.insert(indx_inserir, valor_insert + str(valor_bij_adicionar))


	else:

		if not regra_lgp_bij[:-len(tipo)]:

			bij_valor = regra_lgp_bij[-1]
		else:
			bij_valor = bijecao_valor(regra_lgp_bij[:-len(tipo)])


		insert_value = list(filter(lambda x: x[-1] == str(bij_valor), regra_lgp_bij))


		ind_nova_lgp = regra_lgp_bij.index(insert_value[0])



		nova_versao_regra_lgp = regra_lgp_bij

		nova_versao_regra_lgp.insert(ind_nova_lgp + 1, valor_insert + str(valor_bij_adicionar))


	return nova_versao_regra_lgp


def insert_regra_pt(indice, indice_pt, regra_pt_bij,regra_lgp_bij, input_regra, tipo):
	"""
	Insere a nova classe no lado português da regra.
	:param indice: inteiro, indice da classe anterior à classe a inserir da regra
	:param indice_pt: inteiro, indice da classe gramatical da frase em português a inserir
	:param regra_pt_bij: Lista de strings, lado português da regra
	:param regra_lgp_bij: Lista de strings, lado LGP da regra
	:param input_regra: Lista de strings, Lista com as classes gramaticais do elemento frásico
	:param tipo: tipo da frase
	:return: Lista com o lado português da regra atualizado, Lista com o lado LGP da regra atualizado
	"""
	primeiro_valor = False

	if indice == 0 and indice_pt == 0:
		indice = indice-1 #indice é o indice da classe anterior à nova classe
	if indice == 0 and indice_pt != 0:
		indice = indice

	if indice_pt == 0:
		valor = input_regra[indice_pt] #valor é a classe a acrescentar

	else:
		valor = input_regra[indice_pt:indice_pt+1]


	tipo_regra = set(['EXCL', 'NEG', 'INT', 'CAN']).intersection(set(regra_pt_bij))


	if not tipo_regra:
		bij_valor = bijecao_valor(regra_pt_bij)
	else:
		bij_valor = bijecao_valor(regra_pt_bij[:-len(tipo_regra)])


	valor_bij_adicionar = bij_valor + 1

	nova_versao_regra_pt = regra_pt_bij

	# guardar valor de correspondência da classe antes da inserção

	if indice == -1:
		bij_anterior = regra_pt_bij[0][-1]
		primeiro_valor = True
	else:
		bij_anterior = regra_pt_bij[indice][-1]


	nova_versao_regra_pt.insert(indice+1, valor[0] + str(valor_bij_adicionar))


	nova_regra_lgp = insert_regra_lgp(valor[0], bij_valor, primeiro_valor, valor_bij_adicionar, bij_anterior, regra_lgp_bij, tipo)

	return nova_versao_regra_pt, nova_regra_lgp


def delete_regra_lgp(bij_valor, regra_lgp_bij):
	"""
	Remove a classe gramatical que está a mais no lado LGP da regra.
	:param bij_valor: inteiro, número de correspondência da classe gramatical a remover
	:param regra_lgp_bij: lista com o lado LGP da regra com os números de correspondência
	:return: Lista com o lado LGP da regra atualizado
	"""


	pop_valor = list(filter(lambda x: x[-1] == str(bij_valor), regra_lgp_bij))


	nova_versao_regra_lgp = regra_lgp_bij

	for v in pop_valor:
		nova_versao_regra_lgp.remove(v)

	return nova_versao_regra_lgp


def delete_regra_pt(indice, regra_pt_bij, regra_lgp_bij):
	"""
	Remove a classe gramatical que está a mais no lado português da regra.
	:param indice: inteiro, indice do valor a remover.
	:param regra_pt_bij: Lista com a estrutura do lado português da regra.
	:param regra_lgp_bij: Lista com a estrutura do lado LGP da regra.
	:return: Listas com as novas versões das estruturas do lado português e LGP da regra.
	"""


	bij_valor = bijecao_valor(regra_pt_bij[indice])


	nova_versao_regra_pt = regra_pt_bij


	nova_regra_lgp = delete_regra_lgp(bij_valor, regra_lgp_bij)

	nova_versao_regra_pt.pop(indice)


	return nova_versao_regra_pt, nova_regra_lgp



def operacoes_regra(backpointers, obj_regra_toda_final, input_regra, tipo):
	"""
	Função que realiza as operações de edição das regras para igual a estrutura das regras com as estruturas dos
	elementos frásicos (sujeito, predicado, modificador)
	:param backpointers: Lista com tuplos que identificam as operações de edição a realizar
	:param obj_regra_toda_final: Lista com a regra escolhida
	:param input_regra: Lista de strings, Lista com as classes gramaticais do elemento frásico
	:param tipo: Tipo da frase
	:return: Nova versão do lado português e do lado LGP da regra escolhida após as operações de edição
	"""
	nova_versao_regra_pt, nova_regra_lgp = obj_regra_toda_final.regra_pt_bij_tipo, obj_regra_toda_final.regra_lgp_bij_tipo

	offset = 0
	for o in backpointers:

		if o[0] == "insert":

			# 'insert' -> b[j1:j2] should be inserted at a[i1:i1]. Note that i1 == i2 in this case.
			indice = o[1] + offset
			indice_pt = o[4] #indice da classe gramatical da frase em português a inserir

			if indice_pt == 0:
				indice_pt = indice_pt
			else:
				indice_pt = indice_pt - 1


			nova_versao_regra_pt, nova_regra_lgp = insert_regra_pt(indice, indice_pt, nova_versao_regra_pt, nova_regra_lgp, input_regra, tipo)

			offset += 1

		if o[0] == "delete":

			# a[i1:i2] should be deleted. Note that j1 == j2 in this case.
			indice_del = o[1]
			if indice_del == 0:
				indice_del =indice_del + offset
			else:
				indice_del = indice_del + offset


			nova_versao_regra_pt, nova_regra_lgp = delete_regra_pt(indice_del, nova_versao_regra_pt, nova_regra_lgp)

			offset -= 1

		if o[0] == "replace":

			# a[i1:i2] should be replaced by b[j1:j2].
			indice_replace = o[2]
			if indice_replace == 0:
				indice_replace = indice_replace + offset
			else:
				indice_replace = indice_replace -1 + offset


			valor_replace = input_regra[indice_replace] #j2
			if valor_replace not in ["EXCL", "NEG", "CAN", "INT"]:
				valor_replace = valor_replace[0]
			else:
				valor_replace = valor_replace


			if indice_replace == len(nova_versao_regra_pt)-1:

				bij_valor = int(bijecao_valor(nova_versao_regra_pt[:-len(tipo)])) + 1

			else:
				bij_valor = nova_versao_regra_pt[indice_replace][-1]

			if valor_replace not in ["EXCL", "NEG", "CAN", "INT"]:
				nova_versao_regra_pt[indice_replace] = valor_replace[0] + str(bij_valor)
			else:
				nova_versao_regra_pt[indice_replace] = valor_replace


			count = conta_tipo(nova_regra_lgp)


			for i,r in enumerate(nova_regra_lgp[:-count]):

				if int(r[-1]) == int(bij_valor):

					nova_regra_lgp[i] = valor_replace + str(bij_valor)


			if int(indice_replace) == len(nova_versao_regra_pt)-1: #caso em que a susbtituicao é feita no tipo da frase

				bij_valor = int(bijecao_valor(nova_regra_lgp[:-count])) + 1

				nova_regra_lgp[-1] = valor_replace + str(bij_valor)


	return nova_versao_regra_pt, nova_regra_lgp



def transforma_regra(obj_regra_toda_final, input_regra, tipo):
	"""
	Descobre e realiza as operações de edição que tornam a estrutura da regra igual à estrutura do
	elemento frásico igual.
	:param obj_regra_toda_final: Lista com a estrutura da regra escolhida
	:param input_regra: Lista de strings, Lista com as classes gramaticais do elemento frásico
	:param tipo: Tipo da frase, string
	:return: Nova versão do lado português e do lado LGP da regra escolhida após as operações de edição
	"""

	tipo_regra = obj_regra_toda_final.tipo

	regra = obj_regra_toda_final.regra_pt
	regra.append(tipo_regra)


	sm = SequenceMatcher(regra, input_regra)
	backpointers = sm.get_opcodes() #ex: [['equal', 0, 1, 0, 1], ['equal', 1, 2, 1, 2], ['insert', 1, 1, 2, 3]]


	obj_regra_toda_final.set_regra_pt_bij_tipo(tipo_regra)
	obj_regra_toda_final.set_regra_lgp_bij_tipo(tipo_regra)

	nova_versao_regra_pt, nova_regra_lgp = operacoes_regra(backpointers, obj_regra_toda_final, input_regra, tipo)

	return nova_versao_regra_pt, nova_regra_lgp




def retira_tipo(regra):
	tipo = ['NEG', 'EXCL', 'CAN', 'INT']
	for t in tipo:
		for x in regra:
			if t in x:
				regra.remove(x)
	return regra

def conta_tipo(regra):
	tipo = ['NEG', 'EXCL', 'CAN', 'INT']
	count = 0
	for t in tipo:
		for x in regra:
			if t in x:

				count +=1
	return count



def lgp_uniforme(nova_regra_pt, nova_regra_lgp):
	"""
	Uniformiza a regra. Algumas regras ditam a troca de uma classe gramatical no lado da LGP, ex: um adjetivo
	pode ser um advérbio no lado da LGP. Esta função ignora essa transformação por não existirem ferramentas que
	permitam fazer essa transformação automaticamente.
	:param nova_regra_pt: Lista com a estrutura do lado português da regra
	:param nova_regra_lgp: Lista com a estrutura do lado LGP da regra
	:return:
	"""

	for r_pt in nova_regra_pt:
		for i in range(len(nova_regra_lgp)):

			if r_pt[-1] == nova_regra_lgp[i][-1]:

				nova_regra_lgp[i] = nova_regra_lgp[i].replace(nova_regra_lgp[i][:-1],r_pt[:-1])


def escolher_regra_melhor(i, sim_pred, dist_obj_pred, classes, freq):
	"""
	Escolhe a regra mais semelhante à estrutura do elemento frásico (sujeito, predicado e modificador) através
	da Distância de Edição.
	Aplica as operações de edição para igual a estrutura da regra à estrutura do elemento frásico.
	:param i: Objeto da classe Frase_input que contém as informações (gramaticais e lexicais) da frase em portugues
	a traduzir.
	:param sim_pred: Lista com as distâncias de um elemento frásico a todas as regras.
	:param dist_obj_pred: Lista com objetos do tipo Edit_distance que guardam as informações da distância do elemento frásico
	a cada regra.
	:param classes: Lista com a estrutura (classes gramaticais) do elemento frásico.
	:param freq: Dicionário com as frequências de cada regra no corpus.
	:return: Nova versão do lado português e do lado LGP da regra escolhida após as operações de edição
	"""
	distancia_min = min_sim(sim_pred)


	if len(distancia_min) > 1:
		indx_regra_final, obj_regra_toda_final = desempata(distancia_min, dist_obj_pred, freq)

		i.set_regra_escolhida(obj_regra_toda_final)
		i.set_ind_regra_escolhida(indx_regra_final)

		nova_versao_regra_pt, nova_regra_lgp = transforma_regra(obj_regra_toda_final, classes, i.tipo)

	else:
		#temos logo uma regra vencedora
		indx_regra_final = distancia_min[0]

		i.set_regra_escolhida(dist_obj_pred[indx_regra_final])
		i.set_ind_regra_escolhida(indx_regra_final)

		nova_versao_regra_pt, nova_regra_lgp = transforma_regra(dist_obj_pred[indx_regra_final], classes, i.tipo)

	nova_regra_pt = retira_tipo(nova_versao_regra_pt)
	nova_regra_lgp = retira_tipo(nova_regra_lgp)

	lgp_uniforme(nova_regra_pt, nova_regra_lgp)


	return nova_regra_pt, nova_regra_lgp