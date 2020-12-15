import re
import argparse
from gensim.models import KeyedVectors
from Elementos_Frasicos import Elementos_frasicos
from Alinhamento import alinhamento_por_elemento
import informacao_gramatical


def criar_objeto(info_lingua, lingua):
	"""
	Guarda um tuplo com a palavra, lema e classe gramatical das palavras que constituem cada elemento frásico.
	:param info_lingua: lista com as informações gramaticais
	:param lingua: lgp ou pt
	:return: lista com o objeto que guarda os elementos frásicos
	"""
	classes = []

	for j in info_lingua:
		info = Elementos_frasicos() #objeto para guardar os elementos frasicos das frases em LGP

		if lingua == "lgp":
			info.tipo_de_frase(j.get_tipo_frase())

		for m,v in j.analise_sintatica.items():

			if "ARG_EXT" in v:
				info.append_sujeito(m.lower(), j.lemmas[m], j.classes_gramaticais[m])

			if "ARG_INT" in v:

				info.append_objeto(m.lower(),j.lemmas[m], j.classes_gramaticais[m])
				info.append_predicado(m.lower(),j.lemmas[m], j.classes_gramaticais[m])

			if len(re.findall(r"v\w*", v.lower()))>0:

				info.append_verbo(m.lower(),j.lemmas[m], j.classes_gramaticais[m])
				info.append_predicado(m.lower(),j.lemmas[m], j.classes_gramaticais[m])

			if v=="":
				info.append_outros(m.lower(),j.lemmas[m],j.classes_gramaticais[m])

		classes.append(info)


	return classes




def main():
	"""
	Função principal para a construção de regras de tradução automáticas.
	Analisa sintatica e morfossintática.
	Alinhamento das palavras e gestos.
	Guarda a frequência das regras de tradução.
	Guarda as regras de tradução.

	:return:
	"""

	parser = argparse.ArgumentParser()

	parser.add_argument('file', help='ficheiro do ELAN')

	argss = parser.parse_args()

	ficheiro_html = argss.file

	info_pt, info_lgp = informacao_gramatical.main(ficheiro_html)

	classes_pt = criar_objeto(info_pt, "pt")
	classes_lgp = criar_objeto(info_lgp, "lgp")


	embeddings = KeyedVectors.load_word2vec_format(
		'Word_embeddings/glove_s600.txt', binary=False,
		unicode_errors="ignore")


	alinhamento_por_elemento(classes_pt, classes_lgp, embeddings)

 
main()

