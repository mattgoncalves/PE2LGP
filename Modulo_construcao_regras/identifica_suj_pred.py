"""
Os exemplos dados em cada função dizem respeito à frase "A Maria e o Luís comeram marisco".
"""
def filhos(indice, dependency_filhos):
	"""
	Devolve os indices dos filhos do nó dado como input (indice)
	:param indice: indice de um nó
	:param dependency_filhos: lista com sublistas que contêm os indices dos filhos, ex: [[], [0, 4], [], [], [2, 3], [1, 6, 7], [], []]
	:return: Lista com os indices filhos do nó dado (indice)
	"""
	return dependency_filhos[indice]


def procura_filhos(indice, dependency_filhos):
	"""
	Procura em largura os filhos de cada filho do nó raiz.
	:param indice: Indice raiz, para o exemplo, é o indice 5 (comeram)
	:param dependency_filhos: lista com sublistas que contêm os indices dos filhos, ex: [[], [0, 4], [], [], [2, 3], [1, 6, 7], [], []]
	:return: Lista com os filhos de cada nó, ex: para o filho com indice 1 do nó raiz, temos result=[1,0,4,2,3]
	"""
	result = []
	queue = [indice]

	while queue:
		current = queue[0]
		queue.remove(current)
		result += [current]
		queue += filhos(current, dependency_filhos)


	return result




def funcao_sintatica(filhos, dependency_pt):
	"""
	Aos filhos de um dado nó pai, atribui a mesma função sintática que o nó pai. O nó pai é sempre o indice que aparece em primeiro na lista
	"filhos".
	:param filhos: Lista com sublistas com os indices dos nós filhos de cada nó filho do nó raiz. Ex: [[1,0,4,2,3],[6],[7]]
	:param dependency_pt: lista com as relações de dependências do SpaCy, ex:[det, nsubj, cc, det, conj, root, obj,punct]
	:return: Lista com as funções sintáticas principais de cada palavra sem o elemento raiz. Ex: [nsubj, nsubj, nsubj, nsubj, nsubj, obj, punct]
	"""
	dependency_tags = []
	for f in filhos:
		for i in range(len(f)):
			dependency_tags.append(dependency_pt[f[0]])


	return dependency_tags


def identifica_elementos(dependency_pt, dependency_filhos):
	"""
	Identifica a que elemento frásico principal (sujeito, predicado, etc.) pertence cada palavra da frase em português de acordo
	com as relações de dependências entre as palavras.
	:param dependency_pt: lista com as dependências, ex:[det, nsubj, cc, det, conj, root, obj,punct]
	:param dependency_filhos: lista com sublistas que contêm os indices dos filhos, ex: [[], [0, 4], [], [], [2, 3], [1, 6, 7], [], []], para a frase "A Maria e o Luís comeram marisco"
	:return: Lista com as relações de dependências principais de cada palavra.
	Ex: Para a frase "A Maria e o Luís comeram marisco.", retorna [nsubj, nsubj, nsubj, nsubj, nsubj, root, obj, punct]
	"""

	ind = [i for i, x in enumerate(dependency_pt) if x == "ROOT"]
	ind_root_vazio = -1
	for i in ind:
		filhos_root = dependency_filhos[i]
		if not filhos_root:
			ind_root_vazio = i
			continue
		else:
			filhos_root = dependency_filhos[i]
			ind_root = i



	filhos = []
	for i in filhos_root:
		filhos.append(procura_filhos(i, dependency_filhos))

	dependency_tags = funcao_sintatica(filhos, dependency_pt)
	if ind_root_vazio!= -1:
		dependency_tags.insert(ind_root_vazio, "ROOT") #Adiciona elemento raiz
	dependency_tags.insert(ind_root, "ROOT")

	return dependency_tags
