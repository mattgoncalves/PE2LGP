#########################################
#Módulo de tradução de português para LGP
#########################################
import csv
import sys
import re
import string
from escolhaRegra import *
from geracao_fase import geracao
from processarFrasePT import *
from nltk import sent_tokenize
from escolhaRegra import distancia, escolher_regra_melhor
from freq_json import freq, abrir_freq
sys.path.append('../Modulo_construcao_regras')
from freeling import load_freeling


def update_elemento_sintatico(i, frase, gesto, classe_gesto):
	"""
	Atualiza a lista do elemento frásico (sujeito, predicado, verbo e modificador) a que pertence a palavra com as características
	do gesto correspondente.
	:param i: inteiro, indice da palavra
	:param frase: frase em português, objeto da classe Frase_input
	:param gesto: string, gesto
	:param classe_gesto: string, classe gramatical do gesto
	:return:
	"""

	for j in frase.indices_verbo:
		if j == i:
			frase.classes_verbo[frase.indices_verbo.index(j)] = classe_gesto
			frase.classes_antes_verbo[frase.indices_verbo.index(j)] = (gesto, classe_gesto)

	for j in frase.indices_suj:
		if j == i:
			frase.classes_suj[frase.indices_suj.index(j)] = classe_gesto
			frase.classes_antes_suj[frase.indices_suj.index(j)] = (gesto, classe_gesto)
	for j in frase.indices_obj:
		if j == i:
			frase.classes_obj[frase.indices_obj.index(j)] = classe_gesto
			frase.classes_antes_obj[frase.indices_obj.index(j)] = (gesto, classe_gesto)
	for j in frase.indices_outros:
		if j == i:
			frase.classes_outro[frase.indices_outros.index(j)] = classe_gesto
			frase.classes_antes_outro[frase.indices_outros.index(j)] = (gesto, classe_gesto)
	for j in frase.indices_pred:
		if j == i:
			frase.classes_pred[frase.indices_pred.index(j)] = classe_gesto
			frase.classes_antes_pred[frase.indices_pred.index(j)] = (gesto, classe_gesto)


def del_elemento_sintatico(i, frase, gesto, classe_gesto):
	"""
	Elimina do elemento frásico original a palavra que com a conversão de léxico passou a pertencer ao verbo.
	Atualiza todas as listas que tinham essa palavra.
	:param i: inteiro, indice da palavras na frase
	:param frase: frase em português, objeto da classe Frase_input
	:param gesto: gesto correspondente
	:param classe_gesto: classe gramatical do gesto
	:return:
	"""
	for j in frase.indices_verbo:
		if j == i:
			frase.classes_verbo[frase.indices_verbo.index(j)] = classe_gesto
			frase.classes_antes_verbo[frase.indices_verbo.index(j)] = (gesto, classe_gesto)

	for j in frase.indices_suj:
		if j == i:
			del frase.classes_suj[frase.indices_suj.index(j)]
			del frase.classes_antes_suj[frase.indices_suj.index(j)]
	for j in frase.indices_obj:
		if j == i:
			del frase.classes_obj[frase.indices_obj.index(j)]
			del frase.classes_antes_obj[frase.indices_obj.index(j)]
	for j in frase.indices_outros:
		if j == i:
			del frase.classes_outro[frase.indices_outros.index(j)]
			del frase.classes_antes_outro[frase.indices_outros.index(j)]
	for j in frase.indices_pred:
		if j == i:
			del frase.classes_pred[frase.indices_pred.index(j)]
			del frase.classes_antes_pred[frase.indices_pred.index(j)]

	del frase.classes[i]
	del frase.dep_tags[i]


def update_frase(index_pt, c, classes, gesto, frase):
	"""
	Atualiza o elemento frásico (sujeito ou predicado ou modificador) e a frase em português de acordo com
	o correspondente gesto.
	:param index_pt: Lista com os indices das palavras
	:param c: Indice da classe gramatical da palavra
	:param classes: Lista com as classes gramaticais das palavras.
	:param gesto: String, gesto correspondente
	:param frase: Frase em português, objeto da classe Frase_input
	:return:
	"""

	classe_gesto = classes[c]
	frase.frase_sem_det[index_pt[c]] = (gesto, gesto, classe_gesto)
	update_elemento_sintatico(index_pt[c], frase, gesto, classe_gesto)

	del index_pt[c]

	for i in sorted(index_pt, reverse=True):

		del frase.frase_sem_det[i]

		del_elemento_sintatico(i, frase, gesto, classe_gesto)


def saber_glosa(palavra, palavras_glosas, freq, classe, palavra_pt):
	"""
	Retorna a glosa/gesto mais frequente associado à palavra.
	:param palavra: lema(s) palavra(s) em português
	:param palavras_glosas: Lista com as entradas do dicionário
	:param freq: Lista com as frequências das entradas no dicionário
	:param classe: Classe gramatical da(s) palavra(s)
	:param palavra_pt: Palavra(s) em português
	:return: Gesto
	"""
	freq_indices = []
	indices = []
	for i,v in enumerate(palavras_glosas):
		if classe[0] !="N":

			if v[1] == palavra:
				freq_indices.append(freq[i])
				indices.append(i)

			else:
				continue
		else:
			if v[0] == palavra_pt:
				freq_indices.append(freq[i])
				indices.append(i)
			else:
				continue

	gesto = palavras_glosas[indices[freq_indices.index(max(freq_indices))]][2]

	return gesto



def update_elemento(frase, indices_outro, c):
	"""
	Atualiza os modificadores de frase.
	:param frase: frase em português
	:param indices_outro: lista com os indices de palavras que pertencem a modificadores
	:param c: inteiro, indice da palavra que deixou de pertencer ao modificador
	:return:
	"""
	try:
		del frase[indices_outro.index(c)]
	except:
		del frase[0]






def transferencia_lexical(frase, palavras_glosas, freq):
	"""
	Realiza a conversão do léxico português no léxico da LGP.
	:param frase: Frase em português
	:param palavras_glosas: Lista com as entradas do dicionário, Lista de tuplos.
	:param freq: Lista com as frequências das entradas do dicionário no dicionário.
	:return:
	"""

	for i,v in enumerate(palavras_glosas):
		palavra_pt = list(list(zip(*frase.frase_sem_det))[1])
		palavra_pt_not_lema = list(list(zip(*frase.frase_sem_det))[0])

		for s,p in enumerate(palavra_pt):
			palavra_pt[s] = p.translate(str.maketrans('', '', string.punctuation))

		palavras = " ".join(palavra_pt)
		classes_pt = list(list(zip(*frase.frase_sem_det))[2])
		palavra = re.search(r'\b(?<![\w-])' + v[1] + r'(?![\w-])\b', palavras.lower())

		if palavra:
			palavras_pt = palavra.group(0).split()

			classes = []
			index_pt = []
			pt = []

			for p in palavras_pt:
				if p in palavra_pt:
					index_pt.append(palavra_pt.index(p))

			for i in index_pt:
				classes.append(classes_pt[i])
				pt.append(palavra_pt_not_lema[i])

			# No caso em que mais do que uma palavra é convertida num gesto. Ex: haver grande -> TER-MUITO
			if classes:

				gesto = saber_glosa(v[1], palavras_glosas, freq, classes, pt)

				tags_c = []
				if frase.classes_antes_outro:
					tags_c = list(list(zip(*frase.classes_antes_outro))[1])

				for c in range(len(classes)):

					if all(e in frase.classes_antes_verbo for e in classes) and any(e in tags_c for e in classes):
						update_elemento(frase.classes_outro, frase.indices_outros, index_pt[c])
						update_elemento(frase.classes_antes_outro, frase.indices_outros, index_pt[c])
						update_elemento(frase.indices_outros, frase.indices_outros, index_pt[c])


					if len(index_pt)>1:

						update_frase(index_pt, c, classes, gesto, frase)
						break
					if len(index_pt)<=1:
						classe_gesto = classes[c]
						frase.frase_sem_det[index_pt[c]] = (gesto, gesto, classe_gesto)
						update_elemento_sintatico(index_pt[c], frase, gesto, classe_gesto)


def map_bijecao(pred_pt, classes_antes_pred):
	"""
	Mapea as classes gramaticais com as palavra originais da frase.
	Ex: {"ADV3": ("rato", "n")}
	:param pred_pt:
	:param classes_antes_pred:
	:return: Um dicionário com o mapeamento. Ex: {"ADV3": ("rato", "n")}
	"""
	map_bij = {}
	for n, b in enumerate(pred_pt):
		if b not in map_bij.keys():
			map_bij[b] = classes_antes_pred[n]

	return map_bij


def freq_dicionario():
	"""
	Contabiliza a frequência de uma entrada (lema, palabra, gesto) no dicionário.
	:return: duas listas, uma com os tuplos com lema, palavra e gesto e outra com a frequência de cada tuplo no dicionário.
	"""
	with open("../Modulo_construcao_regras/Dicionario/dicionario.csv") as f:
		csvreader = csv.reader(f, delimiter="\t")
		palavra_glosas = []
		frequencia = []

		for row in csvreader:
			if (row[0].lower(), row[1].lower(), row[2].lower()) in palavra_glosas:
				frequencia[palavra_glosas.index((row[0].lower(), row[1].lower(), row[2].lower()))] +=1
			else:
				palavra_glosas.append((row[0].lower(), row[1].lower(), row[2].lower()))
				frequencia.append(1)

	return palavra_glosas, frequencia


def ordena_palavras(i):
	"""
	Ordena as palavras na frase de acordo com a ordem original das mesmas.
	:param i: objeto do tipo Frase_input, frase em português.
	:return:
	"""

	dict_lemas = {}
	for j in i.frase_sem_det:
		dict_lemas[j[0]] = j[1]
	i.reset_frase_sem_det()
	for l,v in enumerate(i.traducao):
		i.traducao[l] = (v[0],dict_lemas[v[0]], v[1])
		i.update_frase_sem_det((v[0],dict_lemas[v[0]], v[1]))


def retira_cor_de(f, palavras_unidas):
	"""
	Retira as palavras "cor de" nas cores.
	:param f: string, palavra em português
	:param palavras_unidas: lista com as excepções de cores.
	:return: string, cor sem as palavras "cor de".
	"""

	for i in palavras_unidas:
		laranja = i.split()[-1]

		cor_de = re.search(i, f)
		if cor_de:
			f =f.replace(cor_de.group(0), laranja)

	return f

def verifica_frase(f, frases_comuns):

	for i in frases_comuns:

		if i[:-1] in f.lower().translate(str.maketrans('', '', string.punctuation)):
			return True
		else:
			continue

def set_traducao_regras(classes_antes_verbo, traducao_regras_pred):
	"""
	Divide o verbo e os objetos do predicado.
	:param classes_antes_verbo: Lista com as classes gramaticais dos verbos.
	:param traducao_regras_pred: Lista com as classes gramaticais pertencentes ao predicado.
	:return: Lista com as classes que pertencem ao objeto e lista com as classes que pertencem aos verbos.
	"""
	objs = []
	verbos = []
	for l in classes_antes_verbo:
		verbos.append(l)

	for k in traducao_regras_pred:
		if k not in verbos:
			objs.append(k)

	return objs, verbos


def abre_corpus_teste(corpus):
	references = []
	with open(corpus) as csvfile:
		for l in csv.reader(csvfile, delimiter='\t'):
			references.append(l[0])
	return references

def tradutor_main():
	"""
	Função principal do tradutor.
	Segmenta o input em frases.
	As frases são analisadas sintatica e morfossintaticamente.
	Executa a transferência gramatical.
	Executa a fase de geração.
	:param frases: string, uma ou mais frases em português.
	:return: string, uma ou mais frases em LGP
	"""

	try:

		#Carregar o modelo do freeling
		freeling_model = load_freeling(True)
		palavras_glosas, freq_dic = freq_dicionario()

		while (True):

			frase_lgp = []

			frase = input("Escreva a frase a traduzir: ")

			modo = input("Carregue na tecla F depois enter, caso queira o modo formal, caso contrário, carregue enter :")

			frases_input = []

			frases_comuns = ["bom dia", "boa tarde", "boa noite", "por favor"] #listas de palavras que não devem ser processadas pelo tradutor

			palavras_unidas = ["cor de rosa", "cor de laranja"]



			frases = sent_tokenize(frase)


			for f in frases:

				if verifica_frase(f, frases_comuns) and len(f.lower().translate(str.maketrans('', '', string.punctuation)).split())< 3:
					lgp = f.upper().translate(str.maketrans('', '', string.punctuation))
					lgp = "-".join(lgp.split())
					#frase_lgp = [lgp.upper()]
					frase_lgp.append(lgp.upper())

				else:
					if verifica_frase(f, frases_comuns):
						for i in frases_comuns:
							except_palavra = re.search(i, f[:-1].lower())
							if except_palavra:
								glosa = "-".join(except_palavra.group(0).split())
								f = f.lower().replace(except_palavra.group(0), glosa)

						nova_frase = retira_cor_de(f, palavras_unidas)
						frases_input.append(preprocessar(nova_frase, freeling_model)) #fase de análise
					else:
						if len(f.lower().translate(str.maketrans('', '', string.punctuation)).split()) == 1:
							#frase_lgp = [f.upper().translate(str.maketrans('', '', string.punctuation))]
							frase_lgp.append(f.upper().translate(str.maketrans('', '', string.punctuation)))

						else:
							nova_frase = retira_cor_de(f, palavras_unidas)
							frases_input.append(preprocessar(nova_frase, freeling_model)) #fase de análise

			for i in frases_input:

				# fase de transferência lexical
				transferencia_lexical(i, palavras_glosas, freq_dic)

				sim_pred, dist_obj_pred, freq_pred = distancia(i, "pred")
				sim_suj, dist_obj_suj, freq_suj = distancia(i, "suj")
				sim_mod, dist_obj_mod, freq_mod = distancia(i, "mod")

				# Escolha da regra mais semelhante por elemento frásico
				if dist_obj_pred:


					pred_pt, pred_lgp = escolher_regra_melhor(i, sim_pred, dist_obj_pred, i.classes_pred, freq_pred)

					map_valor = map_bijecao(pred_pt, i.classes_antes_pred)

					traducao_ordenado = list(map(lambda x: map_valor[x], pred_lgp))

					i.set_traducao_regras_pred(traducao_ordenado)

					objs, verbos = set_traducao_regras(i.classes_antes_verbo, i.traducao_regras_pred)
					i.set_traducao_regras_obj(objs)
					i.set_traducao_regras_verbo(verbos)

				if dist_obj_suj:

					suj_pt, suj_lgp = escolher_regra_melhor(i, sim_suj, dist_obj_suj, i.classes_suj, freq_suj)
					map_valor_suj = map_bijecao(suj_pt, i.classes_antes_suj)
					traducao_ordenado_suj = list(map(lambda x: map_valor_suj[x], suj_lgp))
					i.set_traducao_regras_suj(traducao_ordenado_suj)

				if dist_obj_mod:

					mod_pt, mod_lgp = escolher_regra_melhor(i, sim_mod, dist_obj_mod, i.classes_outro, freq_mod)
					map_valor_o = map_bijecao(mod_pt, i.classes_antes_outro)
					traducao_ordenado_o = list(map(lambda x: map_valor_o[x], mod_lgp))
					i.set_traducao_regras_outro(traducao_ordenado_o)


				freq_estrutura = abrir_freq("../Modulo_construcao_regras/Estatisticas/estruturas_frasicas/regras_frasicas.json")

				if "cop" in i.dep_tags:
					max_keys = freq(freq_estrutura, i.tipo, True)
				else:
					max_keys = freq(freq_estrutura, i.tipo, False)

				estrutura = max_keys.lower()


				#Ordenar os elementos frásicos consoante a ordem frásica
				if modo !="": #Ordem SOV
					suj = i.traducao_regras_outro + i.traducao_regras_suj
					i.set_traducao(suj, i.traducao_regras_obj, i.traducao_regras_verbo)
					ordena_palavras(i)
				else:
					suj = i.traducao_regras_outro + i.traducao_regras_suj

					if len(i.traducao_regras_suj) == 1 and i.traducao_regras_suj[0][1].startswith("PT"):
						#interrogativas parciais de sujeito
						int_suj = True
					else:
						int_suj = False

					if estrutura.startswith('svo'):
						i.set_traducao(suj, i.traducao_regras_verbo, i.traducao_regras_obj)
						ordena_palavras(i)

					if estrutura.startswith('osv'):
						i.set_traducao(i.traducao_regras_obj, suj, i.traducao_regras_verbo)
						ordena_palavras(i)
					if estrutura.startswith('vos'):
						i.set_traducao(i.traducao_regras_verbo, suj, i.traducao_regras_suj)
						ordena_palavras(i)
					if estrutura.startswith('sov'):
						if int_suj:
							i.set_traducao(i.traducao_regras_verbo,i.traducao_regras_obj, suj)
						else:
							i.set_traducao(suj, i.traducao_regras_obj, i.traducao_regras_verbo)
						ordena_palavras(i)
					if estrutura == 'vso':
						i.set_traducao(i.traducao_regras_verbo, i.traducao_regras_suj, i.traducao_regras_obj)
						ordena_palavras(i)

					if estrutura == 'sv':
						if int_suj:
							i.set_traducao(i.traducao_regras_verbo,i.traducao_regras_obj, suj)
						else:
							i.set_traducao(suj, i.traducao_regras_verbo, i.traducao_regras_obj)
						ordena_palavras(i)

					if estrutura == 'vs':
						if int_suj:
							i.set_traducao(i.traducao_regras_verbo,i.traducao_regras_obj, suj)
						else:
							i.set_traducao(i.traducao_regras_verbo, i.traducao_regras_obj, suj)
						ordena_palavras(i)

					if estrutura == 'vo':
						i.set_traducao(suj, i.traducao_regras_verbo, i.traducao_regras_obj)
						ordena_palavras(i)

					if estrutura == 'ov':
						if int_suj:

							i.set_traducao(i.traducao_regras_verbo,i.traducao_regras_obj, suj)
						else:
							i.set_traducao(suj, i.traducao_regras_obj, i.traducao_regras_verbo)
						ordena_palavras(i)

				#fase de geracao
				f_lgp = geracao(i)
				frase_lgp.append(f_lgp)

			traducao_lgp = " ".join(frase_lgp)


			print("Frase em LGP", traducao_lgp)


			#return traducao_lgp

	except KeyboardInterrupt:
		pass

tradutor_main()
