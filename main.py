import csv  # Importa o modulo nativo do Python para ler arquivos CSV
import re   # Importa o modulo nativo para limpar caracteres especiais com expressoes regulares
from datetime import datetime  # Importa a classe para tratar datas e horas

# Variavel global que armazena o nome do arquivo referente aos dados
dados_csv = 'halloween_vendas.csv'


# BLOCO 1: DEFINICAO DAS FUNCOES

def ler_e_inspecionar_csv(caminho_arquivo):
    # Cria uma lista vazia para armazenar cada pedido lido do arquivo
    pedidos = []
    # Abre o arquivo CSV em modo de leitura ('r') com codificacao UTF-8
    with open(caminho_arquivo, 'r', encoding='utf-8') as dados:
        # csv.DictReader le cada linha transformando as colunas em chaves de dicionario
        leitor = csv.DictReader(dados)
        # Percorre linha por linha dentro do leitor de CSV
        for linha in leitor:
            # Adiciona a linha (dicionario) dentro da lista principal de pedidos
            pedidos.append(linha)
    # Devolve a lista completa de pedidos para quem chamou a funcao
    return pedidos


def limpar_e_padronizar_strings(pedidos):
    # Contador para registrar quantas categorias estavam vazias e foram preenchidas
    qtd_categorias_vazias_preenchidas = 0
    # Contador para registrar quantas categorias existentes foram corrigidas
    qtd_categorias_alteradas = 0
    # Lista para guardar ate 3 exemplos de alteracao do tipo antes e depois
    exemplos_alteracao = []
    
    # Percorre cada dicionario de pedido presente na lista
    for pedido in pedidos:
        # Extrai os textos originais das colunas categoria e canal_venda
        cat_original = pedido['categoria']
        canal_original = pedido['canal_venda']
        
        # 1. LIMPEZA E PADRONIZACAO DA CATEGORIA
        # Verifica se o campo categoria esta vazio ou contem apenas espacos
        if not cat_original or cat_original.strip() == '':
            # Preenche a categoria vazia com o texto padrao sem categoria
            cat_limpa = "sem categoria"
            # Incrementa o contador de categorias vazias preenchidas
            qtd_categorias_vazias_preenchidas += 1
        else:
            # Remove espacos nas pontas e converte todas as letras para minusculas
            texto = cat_original.strip().lower()
            # Usa re.sub para remover tudo que nao for letra de 'a' a 'z' ou espaco
            cat_limpa = re.sub(r'[^a-z\s]', '', texto).strip()
            
            # Se a string ficou vazia apos a remocao de simbolos e pontuacoes
            if cat_limpa == '':
                # Atribui o valor padrao sem categoria
                cat_limpa = "sem categoria"
                # Incrementa o contador de categorias vazias preenchidas
                qtd_categorias_vazias_preenchidas += 1
            # Se o texto limpo ficou diferente do texto original recebido
            elif cat_limpa != cat_original:
                # Incrementa o contador de categorias corrigidas
                qtd_categorias_alteradas += 1
                # Armazena ate 3 exemplos de comparacao para exibicao
                if len(exemplos_alteracao) < 3:
                    exemplos_alteracao.append({'antes': cat_original, 'depois': cat_limpa})
        
        # Sobreve o valor tratado de volta na chave categoria do pedido
        pedido['categoria'] = cat_limpa
        
        # 2. PADRONIZACAO DO CANAL DE VENDA
        # Normaliza o texto removendo espacos e convertendo para minusculas
        canal_normalizado = canal_original.strip().lower() if canal_original else ''
        # Se tiver a palavra mercad atribui a string oficial Mercado
        if 'mercad' in canal_normalizado:
            pedido['canal_venda'] = 'Mercado'
        # Se tiver loja ou fisica atribui a string oficial Loja fisica
        elif 'loja' in canal_normalizado or 'física' in canal_normalizado or 'fisica' in canal_normalizado:
            pedido['canal_venda'] = 'Loja física'
        # Se tiver web ou site atribui a string oficial Web
        elif 'web' in canal_normalizado or 'site' in canal_normalizado:
            pedido['canal_venda'] = 'Web'
        else:
            # Atribui Desconhecido caso venha um canal nao catalogado
            pedido['canal_venda'] = 'Desconhecido'

    # Cria o dicionario com as metricas apuradas na Sprint 2
    resumo_sprint2 = {
        'categorias_vazias_preenchidas': qtd_categorias_vazias_preenchidas,
        'categorias_nao_vazias_alteradas': qtd_categorias_alteradas,
        'exemplos': exemplos_alteracao
    }
    # Retorna os pedidos modificados e o resumo da Sprint 2
    return pedidos, resumo_sprint2


def validar_dados_numericos(pedidos):
    # Contador de erros encontrados no campo quantidade
    erros_quantidade = 0
    # Contador de erros encontrados no campo preco_unitario
    erros_preco = 0
    # Contador de pedidos unicos afetados por pelo menos um erro numerico
    pedidos_afetados = 0
    
    # Percorre a lista de pedidos para validar os campos numericos
    for pedido in pedidos:
        # Variavel de controle para evitar somar o mesmo pedido duas vezes
        tem_erro = False
        
        # Remove espacos em branco da string de quantidade
        qtd_texto = pedido['quantidade'].strip()
        # Se nao for numero inteiro positivo (.isdigit) ou for igual a '0'
        if not qtd_texto.isdigit() or qtd_texto == '0':
            # Incrementa a contagem de erros de quantidade
            erros_quantidade += 1
            # Marca que este pedido especifico possui inconsistencia
            tem_erro = True
            
        # Remove espacos em branco da string de preco_unitario
        preco_texto = pedido['preco_unitario'].strip()
        # Se o preco estiver em branco ou comecar com sinal de menos '-'
        if preco_texto == '' or preco_texto.startswith('-'):
            # Incrementa a contagem de erros de preco
            erros_preco += 1
            # Marca que este pedido especifico possui inconsistencia
            tem_erro = True
            
        # Se o pedido possui erro na quantidade ou no preco incrementa a contagem unica
        if tem_erro:
            pedidos_afetados += 1

    # Guarda o resumo com os totais de erros numericos da Sprint 3
    resumo_sprint3 = {
        'erros_quantidade': erros_quantidade,
        'erros_preco': erros_preco,
        'pedidos_afetados': pedidos_afetados
    }
    # Retorna o dicionario de resumo da Sprint 3
    return resumo_sprint3


def analisar_datas_e_regras_negocio(pedidos):
    # Contadores para validar a analise de entrega e status do pedido
    pedidos_sem_entrega = 0
    sem_entrega_cancelados = 0
    sem_entrega_outros_status = 0
    exemplos_contraexemplos = []
    
    # Contador de datas de venda invalidas ou ausentes
    datas_venda_invalidas = 0
    # Dicionarios para acumular a contagem de pedidos por canal e ano-mes
    contagem_por_canal = {}
    contagem_por_ano_mes = {}
    
    # Percorre cada registro da base para processar datas e regras
    for pedido in pedidos:
        # Extrai e limpa os campos de data de entrega, status e data de venda
        data_entrega = pedido['data_entrega'].strip()
        status = pedido['status_pedido'].strip()
        data_venda = pedido['data_venda'].strip()
        
        # 1. INVESTIGACAO DA HIPOTESE DE ENTREGA
        # Verifica se o campo data_entrega esta sem preenchimento
        if not data_entrega:
            # Incrementa a contagem total de pedidos sem data de entrega
            pedidos_sem_entrega += 1
            # Se o status for Cancelado confirma o comportamento esperado
            if status.lower() == 'cancelado':
                sem_entrega_cancelados += 1
            else:
                # Se nao for Cancelado representa um contraexemplo da hipotese
                sem_entrega_outros_status += 1
                # Guarda ate 3 exemplos de pedidos nao entregues que nao foram cancelados
                if len(exemplos_contraexemplos) < 3:
                    exemplos_contraexemplos.append(pedido)
                    
        # 2. CONTAGEM POR CANAL DE VENDA
        # Pega o canal padronizado do registro
        canal = pedido['canal_venda']
        # Soma +1 para o canal no dicionario de contagem
        contagem_por_canal[canal] = contagem_por_canal.get(canal, 0) + 1
        
        # 3. FORMATACAO DE DATA DE VENDA E CONTAGEM POR ANO-MES
        # Bloco de tentativa para converter a string em objeto datetime
        try:
            # strptime converte o texto no formato ISO de data e hora
            dt_obj = datetime.strptime(data_venda, "%Y-%m-%d %H:%M:%S")
            # Extrai o ano como numero inteiro
            ano = dt_obj.year
            # Extrai o mes como numero inteiro
            mes = dt_obj.month
            # Extrai o dia como numero inteiro
            dia = dt_obj.dia if hasattr(dt_obj, 'dia') else dt_obj.day
            # Extrai a hora como numero inteiro
            hora = dt_obj.hour
            # strftime gera a formatacao brasileira em texto para apresentacao
            data_formatada_br = dt_obj.strftime("%d/%m/%Y")
            
            # Monta a chave no formato YYYY-MM para evitar misturar anos
            chave_ano_mes = f"{ano}-{mes:02d}"
            # Soma +1 no dicionario para aquele ano e mes especifico
            contagem_por_ano_mes[chave_ano_mes] = contagem_por_ano_mes.get(chave_ano_mes, 0) + 1
        except ValueError:
            # Caso a data de venda venha invalida ou vazia incrementa o contador de erros
            datas_venda_invalidas += 1

    # Resumo estatistico completo exigido na Sprint 4
    resumo_sprint4 = {
        'pedidos_sem_entrega': pedidos_sem_entrega,
        'sem_entrega_cancelados': sem_entrega_cancelados,
        'sem_entrega_outros_status': sem_entrega_outros_status,
        'exemplos_contraexemplos': exemplos_contraexemplos,
        'datas_venda_invalidas': datas_venda_invalidas,
        'contagem_por_canal': contagem_por_canal,
        'contagem_por_ano_mes': dict(sorted(contagem_por_ano_mes.items()))
    }
    # Retorna o dicionario de resultados da Sprint 4
    return resumo_sprint4



# BLOCO 2: EXECUCAO SEQUENCIAL DO PROJETO

# Executa a ingestao dos dados do arquivo CSV na Sprint 1
meus_pedidos = ler_e_inspecionar_csv(dados_csv)

# Executa o tratamento e padronizacao das strings na Sprint 2
pedidos_limpos, resumo_strings = limpar_e_padronizar_strings(meus_pedidos)

# Executa a validacao dos dados numericos e nulos na Sprint 3
resumo_numerico = validar_dados_numericos(pedidos_limpos)

# Executa a analise temporal e regras de negocio na Sprint 4
resumo_sprint4 = analisar_datas_e_regras_negocio(pedidos_limpos)


# BLOCO 3: EXIBICAO DO RELATORIO FINAL NO TERMINAL

print ("RELATORIO CONSOLIDADO DO PROJETO")


print("\n--- SPRINT 1: INGESTÃO DE DADOS ---")
print(f"Total de registros lidos no CSV: {len(meus_pedidos)}")

print("\n--- SPRINT 2: LIMPEZA DE TEXTOS ---")
print(f"Categorias vazias preenchidas: {resumo_strings['categorias_vazias_preenchidas']}")
print(f"Categorias corrigidas: {resumo_strings['categorias_nao_vazias_alteradas']}")

print("\n--- SPRINT 3: VALIDAÇÃO NUMÉRICA ---")
print(f"Erros de Quantidade (<= 0 ou invalida): {resumo_numerico['erros_quantidade']}")
print(f"Erros de Preco Unitario (< 0 ou ausente): {resumo_numerico['erros_preco']}")
print(f"Total de Pedidos Afetados (Sem sobreposicao): {resumo_numerico['pedidos_afetados']}")

print("\n--- SPRINT 4: REGRAS DE NEGÓCIO E DATAS ---")
print(f"Total de pedidos sem data de entrega: {resumo_sprint4['pedidos_sem_entrega']}")
print(f"  - Sem entrega e Cancelados: {resumo_sprint4['sem_entrega_cancelados']}")
print(f"  - Sem entrega com OUTROS status (Contraexemplos): {resumo_sprint4['sem_entrega_outros_status']}")
print(f"Datas de venda invalidas ou ausentes: {resumo_sprint4['datas_venda_invalidas']}")

print("\n--- CONTAGEM DE PEDIDOS POR CANAL ---")
for canal, qtd in resumo_sprint4['contagem_por_canal'].items():
    print(f"  - {canal}: {qtd} pedidos")

print("\n--- CONTAGEM DE PEDIDOS POR ANO-MÊS ---")
for ano_mes, qtd in resumo_sprint4['contagem_por_ano_mes'].items():
    print(f"  - {ano_mes}: {qtd} pedidos")

