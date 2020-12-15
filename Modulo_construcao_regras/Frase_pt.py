class Frase_pt:
	#informações com as dependências da frase em português e das classes gramaticais.

	def __init__(self, frase_pt= ""):
		self.frase_pt = frase_pt
		self.lemmas = {}
		self.classes_gramaticais = {}
		self.analise_sintatica = {}


	def append_classes_gramaticais(self, glosa, classe):
		self.classes_gramaticais[glosa] = classe

	def append_analise_sintatica(self, glosa, classe):
		self.analise_sintatica[glosa] = classe

	def append_lemmas(self, glosa, lemma):
		self.lemmas[glosa] = lemma

	def converter_classes_gramaticais(self):
		for k,v in self.classes_gramaticais.items():
			if v.startswith( 'V'):
				self.classes_gramaticais[k]="V"
			if v.startswith( 'N'):
				self.classes_gramaticais[k]="N"
			if v.startswith( 'AQ') or v.startswith( 'AO'):
				self.classes_gramaticais[k]="ADJ"
			if v.startswith( 'R'):
				self.classes_gramaticais[k]="ADV"
			if v.startswith( 'C'):
				self.classes_gramaticais[k]="CONJ"
			if v.startswith( 'Z'):
				self.classes_gramaticais[k]="NUM"
			if v.startswith( 'I'):
				self.classes_gramaticais[k]="INT"
			if v.startswith( 'P'):
				self.classes_gramaticais[k]="PRO"
			if v.startswith( 'D'):
				self.classes_gramaticais[k]="DET"