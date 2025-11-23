# stf-app-clustering-documents

Este projeto tem como objetivo analisar e agrupar documentos jurídicos do STF utilizando técnicas de **clustering** e **Processamento de Linguagem Natural (NLP)**. Foi utilizado o **BERTopic** para identificar tópicos recorrentes nos documentos e tentar classificar a categoria majoritária, denominada como "outros".  

Além disso, aplicou-se **Few-Shot Learning** para treinar o ChatGPT a se comportar como um assistente jurídico e gerar análises no formato **FIRAC** (Facts, Issues, Rules, Analysis, Conclusion).

## Estrutura do projeto

- `client.py`: aplicação em **Streamlit** que executa os passos implementados no notebook `trabalho.ipynb`.  
- `transform_data.py`: realiza o pré-processamento e tratamento dos textos antes de enviá-los aos modelos.

## Bases utilizadas

A base principal é a **Victor** da **UNB**, que contém documentos jurídicos do STF.

Também foram criados arquivos auxiliares para o pré-processamento:

- `stopwords_br.txt`: stopwords da língua portuguesa.  
- `stopwords_juridicas.txt`: stopwords específicas do contexto jurídico.  
- `topicos_comuns.txt`: termos e tópicos recorrentes nos documentos.

## Como utilizar

1. Instale as dependências:

```bash
pip install -r requirements.txt
```

2. Execute a aplicação:

```bash
streamlit run client.py
```