from nltk.corpus import wordnet as wn
from pyjarowinkler import distance
import re
from operator import itemgetter


def sets_syn(token):
    """
    Dadas palavras/gestos, retorna para cada uma/um um conjunto de sinónimos (synset).
    :param token: palavra/gesto
    :return: um dicionário com o token e o respetivo synset. ex: {'SÉCULO': ['century.n.01', 'century.n.01', 'era.n.01'], '17': [], 'TER': ['give_birth.v.01', 'have.v.12', 'suffer.v.02', 'own.v.01']}
    """

    dict_synsets = {}

    synsets_token = []
    for i in range(len(wn.synsets(token, lang='por'))):
        synsets_token.append(wn.synset(wn.synsets(token, lang='por')[i].name()))
    dict_synsets[token] = synsets_token  # temos um dicionário com os tokens e os respetivos synsets

    return dict_synsets


def synsets_similarity_values(palavra, token_pt, token_lgp):
    """
    Calcula a semelhança entre uma palavra e um gesto, tendo em conta a sua disposição na wordnet e semelhança entre os
    sinónimos dessas palavras e gestos.
    :param palavra: string com a palavra
    :param token_pt: string com o lema da palavra
    :param token_lgp: string com o lema do gesto
    :return: lista com os pares palavra-gesto alinhados, lista com os pares palavra-gesto não alinhados, lista com os pares palavra-gesto alinhados e a sua semelhança
    """
    valores_semelhanca = []
    sim_value = 0
    dict_synset_pt = sets_syn(token_pt)
    dict_synset_lgp = sets_syn(token_lgp)
    valores_semelhanca_jaro = []
    threshold_similarity = 0.90
    threshold_similarity_jaro = 0.80
    aligned_word = []
    not_aligned_word = []

    if len(list(dict_synset_pt.values())[0]) > 0 and len(list(dict_synset_lgp.values())[0]) > 0: #se os conjunto de sinónimos não é vazio
        for key_pt, s_pt in dict_synset_pt.items():
            for key_lgp, s_lgp in dict_synset_lgp.items():
                    for i in range(len(s_pt)): #quero saber a semelhança entre os sinónimos de cada palavra/glosa
                        for j in range(len(s_lgp)):
                            sim_value = s_pt[i].wup_similarity(s_lgp[j], simulate_root=False)

                            syn_token_pt = re.sub(r'\.\w\.\d+', '', s_pt[i].name())
                            syn_token_lgp = re.sub(r'\.\w\.\d+', '', s_lgp[j].name())

                            if sim_value!=None:
                                if sim_value >= threshold_similarity:
                                    valores_semelhanca.append((key_pt, key_lgp, syn_token_pt, syn_token_lgp, sim_value))

                                elif sim_value < threshold_similarity:
                                    sim = distance.get_jaro_distance(syn_token_pt, syn_token_lgp, winkler=True, scaling=0.1)
                                    valores_semelhanca_jaro.append((key_pt, key_lgp, syn_token_pt, syn_token_lgp, sim))

                            else:
                                sim_value = 0
                                sim = distance.get_jaro_distance(syn_token_pt, syn_token_lgp, winkler=True, scaling=0.1)
                                valores_semelhanca_jaro.append((key_pt, key_lgp, syn_token_pt, syn_token_lgp, sim))

        if len(valores_semelhanca)>0:
            sim_value = max(valores_semelhanca, key=itemgetter(4))[4]

        if sim_value >= threshold_similarity:
            aligned_word.append((palavra, key_pt, key_lgp, sim_value))

            return aligned_word, not_aligned_word, valores_semelhanca_jaro
        else: #entro no cálculo do jaro_distance entre os sinónimos de ambos synsets
            if len(valores_semelhanca_jaro)>0 and sim >= threshold_similarity_jaro:
                sim_value = max(valores_semelhanca_jaro, key=itemgetter(4))[4]
                aligned_word.append((palavra, key_pt, key_lgp, sim_value))
            if sim<threshold_similarity_jaro or len(valores_semelhanca_jaro)<0:
                not_aligned_word.append((key_pt,key_lgp))
            return aligned_word, not_aligned_word, valores_semelhanca_jaro

    else:
        not_aligned_word.append((token_pt, token_lgp))

    return aligned_word, not_aligned_word, valores_semelhanca_jaro




