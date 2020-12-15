class Frase_input:
	"""
	Classe que guarda as informações sobre a frase em português dada ao tradutor.
	"""

	def __init__(self, frase):
		self.frase = frase
		self.estrutura = ""
		self.dep_tags = []
		self.frase_sem_det = []

		self.traducao = []
		self.palavras_compostas = {}
		self.palavras = []
		self.tipo = []
		self.classes = []
		self.classes_sem_tipo = []
		self.classes_antes = []

		self.indices_obj = []
		self.indices_suj = []
		self.indices_verbo = []
		self.indices_outros = []
		self.indices_pred = []

		self.lemmas_sem_det = []
		self.lemma_verdade_sem_det = []
		self.frase_sem_det_lemma_verd = []

		self.classes_suj = []
		self.classes_pred = []
		self.classes_obj = []
		self.classes_verbo = []
		self.classes_outro = []

		self.classes_antes_suj = []
		self.classes_antes_pred = []
		self.classes_antes_obj = []
		self.classes_antes_outro = []
		self.classes_antes_verbo = []

		self.classes_suj_sem_tipo = []
		self.classes_pred_sem_tipo = []
		self.classes_obj_sem_tipo = []
		self.classes_verbo_sem_tipo = []
		self.classes_outro_sem_tipo = []
		self.dep = []
		self.indx_suj = []
		self.indx_obj = []
		self.indx_verbo = []
		self.indx_outros = []
		self.indx_tipo = []
		self.regra_escolhida = []
		self.ind_regra_escolhida = 0

		self.traducao_regras_pred = []
		self.traducao_regras_suj = []
		self.traducao_regras_obj= []
		self.traducao_regras_outro = []
		self.traducao_regras_verbo = []

	def set_estrutura(self, est):
		self.estrutura = est

	def set_traducao_regras_pred(self, lista):
		self.traducao_regras_pred = lista

	def set_traducao_regras_obj(self, lista):
		self.traducao_regras_obj= lista

	def set_traducao_regras_suj(self, lista):
		self.traducao_regras_suj = lista

	def set_traducao_regras_outro(self, lista):
		self.traducao_regras_outro = lista

	def set_traducao_regras_verbo(self, lista):
		self.traducao_regras_verbo = lista

	def set_palavras(self, valor):
		self.palavras = valor

	def set_dep_tags(self,valor):
		self.dep_tags = valor

	def set_palavras_compostas(self, valor_antes, valor_depois):
		self.palavras_compostas[valor_depois] = valor_antes

	def set_tipo(self, valor):
		self.tipo = valor

	def set_lemmas_sem_det(self, valor):
		self.lemmas_sem_det = valor

	def set_lemma_verdade_sem_det(self, valor):
		self.lemma_verdade_sem_det = valor

	def set_frase_sem_det(self, palavra, lemma, classe):
		for p in range(len(palavra)):
			self.frase_sem_det.append((palavra[p], lemma[p], classe[p]))

	def update_frase_sem_det(self, lista):
		self.frase_sem_det.append(lista)

	def reset_frase_sem_det(self):
		self.frase_sem_det = []

	def set_frase_sem_det_lemmas_verd(self, palavra, lemma, classe):
		for p in range(len(palavra)):
			self.frase_sem_det_lemma_verd.append((palavra[p], lemma[p], classe[p]))

	def set_classes(self, valor):
		self.classes = valor

	def set_classes_antes(self, valor):
		self.classes_antes = valor

	def set_traducao(self, a, b, c):
		self.traducao = a + b + c

	def set_classes_antes_suj(self, palavra, valor):
		self.classes_antes_suj.append((palavra, valor))
	def set_classes_antes_obj(self, palavra, valor):
		self.classes_antes_obj.append((palavra, valor))
	def set_classes_antes_outro(self, palavra, valor):
		self.classes_antes_outro.append((palavra, valor))
	def set_classes_antes_v(self, palavra, valor):
		self.classes_antes_verbo.append((palavra, valor))

	def set_classes_sem_tipo(self, valor):
		self.classes_sem_tipo.append(valor)

	def set_classes_v(self, valor):
		self.classes_verbo.append(valor)

	def set_classes_suj(self, valor):
		self.classes_suj.append(valor)

	def set_classes_obj(self, valor):
		self.classes_obj.append(valor)

	def set_indices_suj(self, valor):
		self.indices_suj.append(valor)

	def set_indices_verbo(self, valor):
		self.indices_verbo.append(valor)

	def set_indices_obj(self, valor):
		self.indices_obj.append(valor)

	def set_indices_outros(self, valor):
		self.indices_outros.append(valor)

	def set_indices_pred(self, valor):
		self.indices_pred = valor

	def set_classes_outros(self, valor):
		self.classes_outro.append(valor)


	def set_classes_antes_pred(self, v):
		self.classes_antes_pred = v

	def set_classes_pred(self, v):
		self.classes_pred =v

	def set_classes_v_sem_tipo(self, valor):
		self.classes_verbo_sem_tipo.append(valor)

	def set_classes_suj_sem_tipo(self, valor):
		self.classes_suj_sem_tipo.append(valor)

	def set_classes_obj_sem_tipo(self, valor):
		self.classes_obj_sem_tipo.append(valor)

	def set_classes_outros_sem_tipo(self, valor):
		self.classes_outro_sem_tipo.append(valor)

	def set_classes_pred_sem_tipo(self):
		self.classes_pred_sem_tipo = self.classes_verbo_sem_tipo + self.classes_obj_sem_tipo

	def set_indx_tipo(self, valor):
		self.indx_tipo.append(valor)

	def set_tipo(self, valor):
		self.tipo.append(valor)

	def set_dep(self, valor):
		self.dep.append(valor)

	def set_regra_escolhida(self, valor):
		self.regra_escolhida = valor

	def set_ind_regra_escolhida(self, valor):
		self.ind_regra_escolhida = valor






