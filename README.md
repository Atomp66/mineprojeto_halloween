# Projeto de Tratamento e Análise de Dados: Festa em Cena

## 1. Descrição do Projeto

### O Problema da Festa em Cena
A **Festa em Cena** é uma rede fictícia de produtos de Halloween que comercializa fantasias e acessórios através de três canais de venda: **Mercado**, **Loja física** e **Web**. Antes de utilizar a base de dados em análises estratégicas ou modelos de Machine Learning, a equipe identificou inconsistências operacionais no registro de dados, tais como categorias vazias, caracteres especiais e pontuações indevidas em textos, preços e quantidades inválidos e inconsistências no preenchimento de datas.

### Objetivo do Programa
O objetivo do programa desenvolvido em Python (sem utilização de bibliotecas externas como Pandas ou Numpy) é realizar a ingestão, limpeza, padronização e validação do histórico de pedidos contido no arquivo `halloween_vendas.csv`. O script analisa 1.500 registros e gera relatórios de consistência para apoiar tomadas de decisão sobre canais e sazonalidade.

### Estrutura do Dado (CSV)
* **Significado de 1 Linha:** Cada linha da base representa um pedido individual contendo um único tipo de produto (que pode incluir uma ou mais unidades adquiridas).

### Significado de 4 Colunas da Base:
1. `categoria`: Classificação do produto comercializado (ex.: fantasias, acessórios).
2. `quantidade`: Quantidade de unidades compradas no pedido.
3. `preco_unitario`: Valor em reais ($R\$) cobrado por cada unidade do produto.
4. `canal_venda`: Canal onde a venda foi realizada (`Mercado`, `Loja física` ou `Web`).

---

## 2. Regras de Tratamento Adotadas

### Regras para Textos (`categoria` e `canal_venda`)
* **Categorias:** Aplicação de `.strip()` para remoção de espaços nas extremidades, `.lower()` para padronização em minúsculas e Expressão Regular (`re.sub(r'[^a-z\s]', '', texto)`) para remover pontuações e símbolos. Registros vazios ou que resultaram em texto vazio após a limpeza foram preenchidos como `"sem categoria"`.
* **Canais de Venda:** Mapeamento do texto para padronizar as entradas em três rótulos oficiais: `"Mercado"`, `"Loja física"` e `"Web"`.

### Regras para Valores Numéricos (`quantidade` e `preco_unitario`)
* **Quantidade:** Deve ser um número inteiro estritamente maior que zero ($>0$).
* **Preço Unitário:** Deve ser um número preenchido e não negativo ($\ge 0$).
* **Importante:** Registros com inconsistências numéricas foram apenas contabilizados e separados para auditabilidade, preservando os dados originais sem invenção ou imputação artificial de valores.

### Regras para Datas (`data_venda` e `data_entrega`)
* **Data de Venda:** Convertida de texto para objeto temporal via `datetime.strptime()` no formato `%Y-%m-%d %H:%M:%S`. Extração do ano-mês (`%Y-%m`) para análise temporal e exibição formatada no padrão brasileiro (`DD/MM/AAAA`). Datas inválidas foram contabilizadas sem interromper o processamento nem substituir pela data atual.
* **Data de Entrega:** Utilizada para teste de hipótese operacional sem alteração ou criação artificial de datas.

---

## 3. Guia de Execução

### Requisitos e Arquivos Necessários
Para executar o projeto, você precisa ter o Python instalado e os seguintes arquivos na mesma pasta raiz: 
    halloween_vendas.csv    # Base de dados original
    main.py                 # Script de processamento em Python puro 