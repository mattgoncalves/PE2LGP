def estrutura_sintatica_frase(dependencies_tags, pred_tags, dep_words, frase):
	"""
	Define a ordem frásica da frase em português (ex: "SVO") com base nas relações de dependência retornadas pelo SpaCy.
	:param dependencies_tags: lista com as etiquetas de dependencia da frase dadas pelo SpaCy
	:param pred_tags: lista com as etiquetas morfossintáticas da frase dadas pelo Freeling
	:param dep_words: lista com as palavras da frase
	:param frase: objeto de uma das classes Frase_pt ou Frase_input que guarda informações sobre a frase em português
	:return: uma string com a estrutura frásica da frase (ex: "SVO") e os indices do verbo e sujeito na frase
	"""

	estrutura = []
	indice_verbo = -1
	indice_subj = -1

	for index, item in enumerate(dependencies_tags):
		if "nsubj" in item:
			estrutura.append("S")
			indice_subj = index
		if "obj" in item:
			estrutura.append("O")
		if "amod" in item and pred_tags[index].startswith("V") and "ROOT" in dependencies_tags:
			estrutura.append("V")
			frase.set_classes_v(pred_tags[index])
			frase.set_classes_antes_v(dep_words[index], pred_tags[index])
			indice_verbo = index
		if "ROOT" in item and "cop" not in dependencies_tags and pred_tags[index].startswith("V"):
			estrutura.append("V")
			indice_verbo = index
		if "ROOT" in dependencies_tags and pred_tags[index].startswith("V"):
			estrutura.append("V")
			indice_verbo = index
		if "cop" in item and "ROOT" in dependencies_tags and pred_tags[index].startswith("V"):
			estrutura.append("V")
			indice_verbo = index
		if "ROOT" in item and "cop" in dependencies_tags:
			#é o caso do predicativo do sujeito
			estrutura.append("V")


	estrutura = list(dict.fromkeys(estrutura))


	return "".join(estrutura), indice_verbo, indice_subj



def set_elementos(dependencies_tags, pred_tags, dep_words, frase):

	"""
	Define as palavras que pertencem a cada elementoo frásico (sujeito, predicado e modificador de frase) da frase em português.
	:param dependencies_tags: lista com as etiquetas de dependencia da frase dadas pelo SpaCy
	:param pred_tags: lista com as etiquetas morfossintáticas da frase dadas pelo Freeling
	:param dep_words: lista com as palavras da frase
	:param frase: objeto de uma das classes Frase_pt ou Frase_input que guarda informações sobre a frase em português
	:return:
	"""

	estrutura, indice_verbo, indice_subj = estrutura_sintatica_frase(dependencies_tags, pred_tags,dep_words, frase)

	frase.set_estrutura(estrutura)

	for i, d in enumerate(dependencies_tags):

		if "nsubj" in d:
			frase.set_classes_suj(pred_tags[i])
			frase.set_classes_antes_suj(dep_words[i], pred_tags[i])
			frase.set_indices_suj(i)

		if "appos" in d:
			frase.set_classes_suj(pred_tags[i])
			frase.set_classes_antes_suj(dep_words[i], pred_tags[i])
			frase.set_indices_suj(i)

		if "det" in d:
			frase.set_classes_suj(pred_tags[i])
			frase.set_classes_antes_suj(dep_words[i], pred_tags[i])
			frase.set_indices_suj(i)

		if d == "csubj":
			frase.set_classes_obj(pred_tags[i])
			frase.set_classes_antes_obj(dep_words[i], pred_tags[i])
			frase.set_indices_obj(i)

		if (d == "amod" or d=="case") and indice_verbo!= dependencies_tags.index("ROOT") and i > indice_verbo:
			frase.set_classes_obj(pred_tags[i])
			frase.set_classes_antes_obj(dep_words[i], pred_tags[i])
			frase.set_indices_obj(i)

		if (d == "amod" or d=="case") and indice_subj==-1 and indice_verbo!= dependencies_tags.index("ROOT") and i < indice_verbo:
			frase.set_classes_outros(pred_tags[i])
			frase.set_classes_antes_outro(dep_words[i], pred_tags[i])
			frase.set_indices_outros(i)

		if d == "ROOT" and not pred_tags[i].startswith("V") and i < indice_verbo:
			frase.set_classes_suj(pred_tags[i])
			frase.set_classes_antes_suj(dep_words[i], pred_tags[i])
			frase.set_indices_suj(i)

		if d == "ROOT" and not pred_tags[i].startswith("V") and i > indice_verbo:
			frase.set_classes_obj(pred_tags[i])
			frase.set_classes_antes_obj(dep_words[i], pred_tags[i])
			frase.set_indices_obj(i)

		if "acl" in d:
			frase.set_classes_obj(pred_tags[i])
			frase.set_classes_antes_obj(dep_words[i], pred_tags[i])
			frase.set_indices_obj(i)

		if indice_subj!=-1:
			if d == "advmod" and i < indice_verbo and i < indice_subj:  # estamos perante um modificador de frase
				frase.set_classes_outros(pred_tags[i])
				frase.set_classes_antes_outro(dep_words[i], pred_tags[i])
				frase.set_indices_outros(i)

			if d == "advmod" and i < indice_verbo and i > indice_subj:  # estamos perante um modificador de grupo verbal
				frase.set_classes_obj(pred_tags[i])
				frase.set_classes_antes_obj(dep_words[i], pred_tags[i])
				frase.set_indices_obj(i)

			if d == "advmod" and i > indice_verbo and i > indice_subj:  # estamos perante um modificador do grupo verbal, portanto faz parte do obj
				frase.set_classes_obj(pred_tags[i])
				frase.set_classes_antes_obj(dep_words[i], pred_tags[i])
				frase.set_indices_obj(i)

		else:
			if d == "advmod" and i < indice_verbo:  # estamos perante um modificador de frase
				frase.set_classes_outros(pred_tags[i])
				frase.set_classes_antes_outro(dep_words[i], pred_tags[i])
				frase.set_indices_outros(i)

			if d == "advmod" and i > indice_verbo:  # estamos perante um modificador de grupo verbal
				frase.set_classes_obj(pred_tags[i])
				frase.set_classes_antes_obj(dep_words[i], pred_tags[i])
				frase.set_indices_obj(i)

		if "obj" in d or "iobj" in d:
			frase.set_classes_obj(pred_tags[i])
			frase.set_classes_antes_obj(dep_words[i], pred_tags[i])
			frase.set_indices_obj(i)

		if d == "xcomp" or d == "ccomp" or d == "advcl" or d == "conj":
			frase.set_classes_obj(pred_tags[i])
			frase.set_classes_antes_obj(dep_words[i], pred_tags[i])
			frase.set_indices_obj(i)

		if d == "cc" and i == 0 and "advmod" in dependencies_tags: #estamos perante uma conjunção pertencente a um modificador
			frase.set_classes_outros(pred_tags[i])
			frase.set_classes_antes_outro(dep_words[i], pred_tags[i])
			frase.set_indices_outros(i)
			
		if d == "cc" and i == 0 and "advmod" not in dependencies_tags: #estamos perante uma conjunção pertencente a um modificador
			frase.set_classes_suj(pred_tags[i])
			frase.set_classes_antes_suj(dep_words[i], pred_tags[i])
			frase.set_indices_suj(i)

		if d == "cc" and i != 0 and i>indice_verbo: #conjunção coordenativa
			frase.set_classes_obj(pred_tags[i])
			frase.set_classes_antes_obj(dep_words[i], pred_tags[i])
			frase.set_indices_obj(i)

		if d == "cc" and i != 0 and i<indice_verbo: #conjunção coordenativa
			frase.set_classes_suj(pred_tags[i])
			frase.set_classes_antes_suj(dep_words[i], pred_tags[i])
			frase.set_indices_suj(i)


		if "obl" in d:  # estamos perante um modificador do grupo verbal ou complemento oblíquo
			frase.set_classes_obj(pred_tags[i])
			frase.set_classes_antes_obj(dep_words[i], pred_tags[i])
			frase.set_indices_obj(i)

		if d == "ROOT" and "cop" not in dependencies_tags and pred_tags[i].startswith("V"):
			frase.set_classes_v(pred_tags[i])
			frase.set_classes_antes_v(dep_words[i], pred_tags[i])
			frase.set_indices_verbo(i)

		if d == "amod" and "ROOT" in dependencies_tags and pred_tags[i].startswith("V"):
			frase.set_indices_verbo(i)


		if d == "ROOT" and "cop" in dependencies_tags and pred_tags[i].startswith("V"):
			frase.set_classes_obj(pred_tags[i])
			frase.set_classes_antes_obj(dep_words[i], pred_tags[i])
			frase.set_indices_obj(i)

		if d == "cop" and "ROOT" in dependencies_tags :
			frase.set_classes_v(pred_tags[i])
			frase.set_classes_antes_v(dep_words[i], pred_tags[i])
			frase.set_indices_verbo(i)

		if "aux" in d:
			frase.set_classes_v(pred_tags[i])
			frase.set_classes_antes_v(dep_words[i], pred_tags[i])
			frase.set_indices_verbo(i)

		if "mark" in d and "nsubj" in dependencies_tags:
			frase.set_classes_suj(pred_tags[i])
			frase.set_classes_antes_suj(dep_words[i], pred_tags[i])
			frase.set_indices_suj(i)

		if "flat:name" in d:
			frase.set_classes_obj(pred_tags[i])
			frase.set_classes_antes_obj(dep_words[i], pred_tags[i])
			frase.set_indices_obj(i)

		if "nmod" in d:
			frase.set_classes_obj(pred_tags[i])
			frase.set_classes_antes_obj(dep_words[i], pred_tags[i])
			frase.set_indices_obj(i)

		if (d == "amod" or d == "case") and indice_verbo== dependencies_tags.index("ROOT"):
			frase.set_classes_outros(pred_tags[i])
			frase.set_classes_antes_outro(dep_words[i], pred_tags[i])
			frase.set_indices_outros(i)


	frase.set_classes_pred(frase.classes_verbo + frase.classes_obj)
	frase.set_classes_antes_pred(frase.classes_antes_verbo + frase.classes_antes_obj)
	frase.set_indices_pred(frase.indices_verbo + frase.indices_obj)

def set_elementos_extracao(dependencies_tags, pred_tags, dep_words, frase):
	"""
	Define as palavras que pertencem a cada elementoo frásico (sujeito, predicado e modificador de frase) da frase em português para a construção de regras.
	:param dependencies_tags: lista com as etiquetas de dependencia da frase dadas pelo SpaCy
	:param pred_tags: lista com as etiquetas morfossintáticas da frase dadas pelo Freeling
	:param dep_words: lista com as palavras da frase
	:param frase: objeto de uma das classes Frase_pt ou Frase_input que guarda informações sobre a frase em português
	:return:
	"""

	estrutura, indice_verbo, indice_subj = estrutura_sintatica_frase(dependencies_tags, pred_tags, dep_words, frase)



	for i, d in enumerate(dependencies_tags):

		if d == "nsubj":
			frase.append_analise_sintatica(dep_words[i], "ARG_EXT")

		if indice_subj!=-1:
			if d == "advmod" and i < indice_verbo and i < indice_subj:  # estamos perante um modificador de frase
				frase.append_analise_sintatica(dep_words[i], "")

			if d == "advmod" and i < indice_verbo and i > indice_subj:  # estamos perante um modificador de grupo verbal
				frase.append_analise_sintatica(dep_words[i], "ARG_INT")

			if d == "advmod" and i > indice_verbo and i > indice_subj:  # estamos perante um modificador do grupo verbal, portanto faz parte do obj
				frase.append_analise_sintatica(dep_words[i], "ARG_INT")

		else:
			if d == "advmod" and i < indice_verbo:  # estamos perante um modificador de frase
				frase.append_analise_sintatica(dep_words[i], "")

			if d == "advmod" and i > indice_verbo:  # estamos perante um modificador de grupo verbal
				frase.append_analise_sintatica(dep_words[i], "ARG_INT")

		if d == "obj" or d == "iobj":
			frase.append_analise_sintatica(dep_words[i], "ARG_INT")

		if d == "obl":  # estamos perante um modificador do grupo verbal ou complemento oblíquo
			frase.append_analise_sintatica(dep_words[i], "ARG_INT")

		if d == "ROOT" and "cop" not in dependencies_tags:
			frase.append_analise_sintatica(dep_words[i], "v")

		if d == "ROOT" and "cop" in dependencies_tags:
			frase.append_analise_sintatica(dep_words[i], "ARG_INT")

		if d == "cop" and "ROOT" in dependencies_tags:
			frase.append_analise_sintatica(dep_words[i], "v_cop")


	return estrutura