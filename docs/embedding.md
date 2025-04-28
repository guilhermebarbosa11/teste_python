# Documentação: Processo de Embedding

## O que é Embedding?

Embedding é uma técnica de representação de dados (geralmente texto) em vetores numéricos densos de alta dimensão. Esses vetores capturam características semânticas e sintáticas do texto, permitindo comparações via distância ou similaridade.

## Aplicações Comuns

- **Busca Semântica**: encontrar documentos relevantes com base no significado, não apenas palavras-chave.
- **Classificação de Texto**: usar embeddings como features para modelos de machine learning.
- **Detecção de Similaridade**: medir similaridade entre sentenças ou parágrafos.
- **Clustering**: agrupar documentos ou tokens similares.

## APIs da OpenAI

- **Modelo**: `text-embedding-ada-002` é o mais comum para embeddings de texto.
- **Chamada**: `openai.Embedding.create(model, input)` retorna um vetor no campo `data[0].embedding`.

## Exemplo de Uso

```python
response = openai.Embedding.create(
    model="text-embedding-ada-002",
    input="Seu texto aqui"
)
vector = response.data[0].embedding