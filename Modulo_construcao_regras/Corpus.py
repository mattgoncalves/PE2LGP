class Info_Corpus:
	"""
	Classe das informações extraídas do corpus.
	"""

	def __init__(self):
		self.frase_pt = ""
		self.frase_lgp = ""
		self.tipo_frase = ""
		self.classes_gramaticais = {}
		self.analise_sintatica = {}
		self.lemmas = {}

	def set_frase_pt(self, frase_pt):
		self.frase_pt = frase_pt

	def get_frase_pt(self):
		return self.frase_pt

	def append_frase_lgp(self, text):
		self.frase_lgp += text if self.frase_lgp == "" else " "+text

	def append_classes_gramaticais(self, glosa, classe):
		self.classes_gramaticais[glosa] = classe

	def append_analise_sintatica(self, glosa, classe):
		self.analise_sintatica[glosa] = classe

	def append_lemmas(self, glosa, lemma):
		self.lemmas[glosa] = lemma

	def append_tipo_frase(self, tipo):
		self.tipo_frase = tipo

	def get_tipo_frase(self):
		return self.tipo_frase


