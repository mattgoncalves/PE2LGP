# PE2LGP: traduzindo português para língua gestual portuguesa

PE2LGP é um sistema de tradução de texto em português europeu para língua gestual portuguesa.

## Descrição

O sistema de tradução divide-se em dois módulos. O primeiro módulo, construção de regras de tradução, consiste na extração de informações linguísticas do corpus de referência da língua gestual portuguesa e, a partir dessas informações, na criação de regras automáticas. O segundo módulo, tradução automática, consiste na tradução de texto em português europeu para língua gestual portuguesa (LGP), em que a frase em LGP é representada por uma sequência de glosas com marcadores que identificam as expressões faciais e palavras soletradas. Na base da tradução encontram-se as regras automáticas e regras manuais.



Disponibilizamos ainda o script para a avaliação automática do sistema de tradução, usando as medidas TER e BLEU.



## Requisitos

**Para correr o PE2LGP:**

1. Instalar Python 3


2. Instalar as bibliotecas do Python necessárias:

```bash
pip install -r requirements.txt
```

3. Instalar a biblioteca [Freeling 4.1](https://freeling-user-manual.readthedocs.io/en/v4.1/toc/)


4. Download do modelo pré-treinado do SpaCy para a análise de dependências:

```bash
python -m spacy download pt_core_news_sm
```


**Para correr o script de avaliação automática:**

1. Instalar Python 2

2. Instalar a biblioteca [pyter](https://pypi.org/project/pyter/):


```bash
pip2 install pyter
```


## Utilização (Ubuntu)

**Módulo de construção de regras automáticas**
```bash
cd Modulo_construcao_regras
python criacao_regras_automaticas.py ficheiro.html
```

`ficheiro.html` é o ficheiro html exportado do ELAN. Um exemplo deste ficheiro encontra-se em `/modulo_construcao_regras/Corpus/exemplo.html`


**Módulo de tradução automática**
```bash
cd Modulo_tradutor
python tradutor.py
```

**Avaliação automática**
```bash
cd Avaliacao
python aval_automatica.py corpus_teste.csv traducoes.csv
```

`corpus_teste.csv` é o ficheiro com o corpus de teste. O corpus de teste usado na avaliação do sistema encontra-se em `/Avaliacao/corpus_teste.csv`.

`traducoes.csv` é o ficheiro com as traduções das frases em português no corpus de teste do sistema de tradução automática. Este ficheiro encontra-se em `/Avaliacao/traducoes.csv`.


## Contactos

Desenvolvido por Matilde Gonçalves, matilde.do.carmo.lages.goncalves@tecnico.ulisboa.pt

