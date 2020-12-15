###########################################################################################
#Funções que permitem extrair as seguintes informações do ficheiro html exportado do ELAN:#
# - LG_P1 transcrição -> Tradução para português do enunciado                             #
# - Glosas_p1 -> Glosas que representam o vocabulário em LGP da mão dominante             #
# - M1_classGram -> Classes gramaticais da glosa mão dominante                            #
# - M1_Constituintes -> Análise Sintática da frase em LGP da mão dominante				  #
# - Come_P1Literal -> identificam o tipo de frase                                         #
###########################################################################################
import sys
from Corpus import Info_Corpus
import os
import xml.etree.ElementTree as ET
from collections import defaultdict


def readTable(frases, root):


	glosas = []

	myDict = defaultdict(list)

	# LP_P1_transcricao_livre
	for i in root.findall(".//*[@class='ti-0']"):
		frase = Info_Corpus()
		index = 0

		for n in range(100):
			col = "colspan=" + '"' + str(n) + '"'
			if i.findall("*[@" + col + "]"):
				for j in i.findall("*[@" + col + "]"):
					text = j.text
					if text:
						frase_pt = text
						frase.set_frase_pt(frase_pt)
						index += 1
						myDict[index].append(text)

		frases.append(frase)

	#tipo de frase
	for i in root.findall(".//*[@class='ti-1']"):
		index = 0
		for n in range(100):
			col = "colspan=" + '"' + str(n) + '"'
			if i.findall("*[@" + col + "]"):
				for j in i.findall("*[@" + col + "]"):
					text = j.text
					if text:
						index += 1
						frase.append_tipo_frase(text)
						myDict[index].append(text)

	# LGlosas_p1
	for i in root.findall(".//*[@class='ti-2']"):
		index = 0
		for n in range(100):
			col = "colspan=" + '"' + str(n) + '"'
			if i.findall("*[@" + col + "]"):
				for l, j in enumerate(i.findall("*[@" + col + "]")):

					glosa = j.text
					if glosa:
						glosas.append(glosa)
						frase.append_frase_lgp(glosa)
						index += 1
						myDict[index].append(glosa)

	# M1_clasgram
	for i in root.findall(".//*[@class='ti-3']"):
		index = 0
		for n in range(100):
			col = "colspan=" + '"' + str(n) + '"'
			if i.findall("*[@" + col + "]"):
				for l, j in enumerate(i.findall("*[@" + col + "]")):
					text = j.text
					if text:
						frase.append_classes_gramaticais(glosas[l], text)
						index += 1
						myDict[index].append(text)

	# M1_constituintes
	for i in root.findall(".//*[@class='ti-4']"):
		index = 0
		for n in range(100):
			col = "colspan=" + '"' + str(n) + '"'
			if i.findall("*[@" + col + "]"):
				for l,j in enumerate(i.findall("*[@" + col + "]")):
					text = j.text
					if text:
						frase.append_analise_sintatica(glosas[l], text)
						index += 1
						myDict[index].append(text)
					else:
						frase.append_analise_sintatica(glosas[l], "")


	return frases



def parse_file(ficheiro_html):

	global root, outputfile

	inputfile = open(ficheiro_html, "r", encoding='utf-8')
	file = open("aux_file.html", "w+", encoding='utf-8')

	for line in inputfile:
		if "nbsp;" in line:
			line = ""
		file.write(line)


	file.seek(0)
	tree = ET.parse(file)
	root = tree.getroot()

	frases = []
	for j in root.findall(".//td/table"): #processa as frases todas de uma vez
		frases = readTable(frases, j)


	indices =[]
	for m, i in enumerate(frases):
		if i.frase_pt == "" and i.frase_lgp == "":
			indices.append(m)

	for h in sorted(indices, reverse=True):
		del frases[h]


	file.close()
	os.remove("aux_file.html")

	return frases

def main(ficheiro_html):
	"""
	Extração das informações do ficheiro html exportado do ELAN.
	:return:
	"""
	info_elan = parse_file(ficheiro_html)
	return info_elan







