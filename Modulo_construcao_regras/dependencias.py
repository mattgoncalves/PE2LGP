import spacy
import freeling


def dependencies_spacy(frases, freeling_values):
	"""
	Conhece-se a árvore de dependências entre os constituintes da frase em português.
	:param frases: frase em português, string
	:param freeling_values: parametros da ferramenta Freeling
	:return: Lista com as palavras da frase, Lista com as relações de dependencias, Lista com sublistas que identificam os filhos de cada nó/palavra.
	"""
	dep_tags = []
	indices_filhos = []

	model = spacy.load('pt_core_news_sm')

	dep_words = freeling.word_tokens(frases, freeling_values)

	x = [''.join(c for c in s if c not in ["!","?",".",",",";",":",'!','"','#','$','%','&','(',')','*','+','.','/',':',';','<','=','>','?','@','[',']','^','`','{','|','}','~']) for s in dep_words]
	dep_words = [s for s in x if s]
	for d in dep_words:
		if d == "-":
			dep_words.remove(d)
	frase_pt = " ".join(dep_words)

	doc = model(frase_pt)

	for token in doc:
		dep_tags.append(token.dep_)
		indices_filhos.append([child.i for child in token.children])
		#[child.i for child in token.children] retorna uma lista com os indices das palavras que dependem da palavra nesse indice.
		#ex: [[], [0, 4], [], [], [2, 3], [1, 6, 7], [], []]


	return dep_words, dep_tags, indices_filhos
