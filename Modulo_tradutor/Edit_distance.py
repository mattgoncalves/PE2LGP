class Edit_distance:
	"""
	Classe que guarda as informaçoes sobre a distancia do elemento frásico a cada regra.
	"""
	def __init__(self, distancia, regra_pt, regra_lgp, regra_pt_bij, regra_lgp_bij, tipo):
		self.distancia = distancia
		self.regra_pt = regra_pt
		self.regra_lgp = regra_lgp
		self.regra_pt_bij = regra_pt_bij
		self.regra_lgp_bij = regra_lgp_bij
		self.regra_pt_bij_tipo = []
		self.regra_lgp_bij_tipo = []
		self.regra_toda = []
		self.regra_toda_bij = []
		self.tipo = tipo

	def set_regra_toda(self, tipo):
		self.regra_toda = self.regra_pt + self.regra_lgp

	def set_regra_toda_bij(self, tipo):
		self.regra_toda_bij = self.regra_pt_bij + self.regra_lgp_bij

	def set_regra_pt_bij_tipo(self, tipo):
		self.regra_pt_bij_tipo = self.regra_pt_bij
		self.regra_pt_bij_tipo.append(tipo)

	def set_regra_lgp_bij_tipo(self, tipo):
		self.regra_lgp_bij_tipo = self.regra_lgp_bij
		self.regra_lgp_bij_tipo.append(tipo)


