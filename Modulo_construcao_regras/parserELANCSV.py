###########################################################################################
# Funções que permitem extrair as seguintes informações do ficheiro txt exportado do ELAN: #
# - LG_P1 transcrição -> Tradução para português do enunciado                             #
# - Glosas_p1 -> Glosas que representam o vocabulário em LGP da mão dominante             #
# - M1_classGram -> Classes gramaticais da glosa mão dominante                            #
# - M1_Constituintes -> Análise Sintática da frase em LGP da mão dominante				  #
# - Come_P1Literal -> identificam o tipo de frase                                         #
###########################################################################################

import csv, sqlite3
from Corpus import Info_Corpus


def parse_file(ficheiro_html):
	con = sqlite3.connect(":memory:")
	cur = con.cursor()
	cur.execute(
		"CREATE TABLE t (frase_pt, glosas_lgp, classes_gramaticais, analise_sintatica);")  # use your column names here

	# /home / matilde / Documents / ExtracaoGramatical / Codigo / video_140_processado.csv

	with open(ficheiro_html, 'r') as fin:
		dr = csv.DictReader(fin, delimiter='	')
		info_elan = []

		# cada ciclo é uma linha

		# para cada linha do ficheiro csv existe um dicionário:
		# linha 1: OrderedDict([('LP_P1 transcrição livre', ''), ('GLOSAS_P1', ''), ('M1_ClassGram', ''), ('M1_Constituintes', '')])
		# linha 2: OrderedDict([('LP_P1 transcrição livre', 'Cultura, Arte, Teatro.'), ('GLOSAS_P1', ''), ('M1_ClassGram', ''), ('M1_Constituintes', '')])
		# linha 3: OrderedDict([('LP_P1 transcrição livre', ''), ('GLOSAS_P1', 'CULTURA'), ('M1_ClassGram', 'N'), ('M1_Constituintes', '')])

		# TENHO QUE IR PELO TEMPO PARA SABER SE COMEÇAMOS NOVA TRILHA OU NÃO, MAS NÃO CORRIGE
		# O PROBLEMA DE IDENTIFICAÇÃO DOS CONSTITUINTES
		for row in dr:
			print(row)
			print("rooow", row['Come_P1Literal'])
			if row['LP_P1 transcrição livre'] != "":
				frase_pt = row['LP_P1 transcrição livre']
				info_elan.append(Info_Corpus(frase_pt))
				if row['Come_P1Literal'] != "":
					print("tipo de frase", row['Come_P1Literal'])
					info_elan[-1].append_tipo_frase(row['Come_P1Literal'])
				info_elan[-1].append_frase_lgp(row['GLOSAS_P1'])
				info_elan[-1].append_classes_gramaticais(row['GLOSAS_P1'], row['M1_ClassGram'])
				info_elan[-1].append_analise_sintatica(row['GLOSAS_P1'], row['M1_Constituintes'])

			else:
				info_elan[-1].append_frase_lgp(row['GLOSAS_P1'])
				info_elan[-1].append_classes_gramaticais(row['GLOSAS_P1'], row['M1_ClassGram'])
				info_elan[-1].append_analise_sintatica(row['GLOSAS_P1'], row['M1_Constituintes'])
		print("tamanhooo", len(info_elan))
		for i in info_elan:
			print("PT", i.frase_pt)
			print("LGP", i.frase_lgp)
			print("Tipo de frase", i.tipo_frase)
	# print("classes gramaticais",i.classes_gramaticais)
	# print("analise sintatica",i.analise_sintatica)

	# cur.executemany("INSERT INTO t (col1, col2) VALUES (?, ?);", to_db)
	# con.commit()
	con.close()

	return info_elan


def main(ficheiro_html):
	info_elan = parse_file(ficheiro_html)
	return info_elan

# main()