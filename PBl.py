"""
================================================================================
DECLARAÇÃO DE AUTORIA E INTEGRIDADE ACADÊMICA
================================================================================
Este código foi desenvolvido para a disciplina EXA854 - MI ALGORITMOS (2026.2)
da Universidade Estadual de Feira de Santana (UEFS).
Problema 2: Gincana dos Ateliês - O Duelo na Estação de Jogos da Pocket.

Autor: Gabriele Franco Nascimento
Data: 30 de Outubro de 2026
================================================================================
"""

import random

CONFIGS_BANCADA = {
    '1': {
        'nome': 'Bancada de Ensaio',
        'dimensao': 6,
        'pecas': [
            ('Armadura', 3, 1, 'R'),
            ('Capa', 2, 2, 'C'),
            ('Elmo', 1, 2, 'E')
        ]
    },
    '2': {
        'nome': 'Bancada de Montagem',
        'dimensao': 8,
        'pecas': [
            ('Par de Asas', 4, 1, 'A'),
            ('Armadura', 3, 1, 'R'),
            ('Capa', 2, 2, 'C'),
            ('Elmo', 1, 2, 'E')
        ]
    },
    '3': {
        'nome': 'Bancada de Véspera',
        'dimensao': 10,
        'pecas': [
            ('Par de Asas', 4, 1, 'A'),
            ('Armadura', 3, 2, 'R'),
            ('Capa', 2, 3, 'C'),
            ('Elmo', 1, 4, 'E')
        ]
    }
}

SIMBOLO_VAZIO = '.'
SIMBOLO_ACERTO = 'X'
SIMBOLO_ERRO = 'o'
MAX_OLHO_CLINICO = 3

def criar_matriz(dimensao, valor_inicial=SIMBOLO_VAZIO):
    """
    Cria uma matriz (lista de listas) com a dimensão informada.
    """
    matriz = []
    for _ in range(dimensao):
        linha = []
        for _ in range(dimensao):
            linha.append(valor_inicial)
        matriz.append(linha)
    return matriz


def criar_estrutura_pecas(config_bancada):
    """
    Gera a lista de dicionários de peças com IDs únicos para rastreamento individual.
    """
    lista_pecas = []
    id_contador = 1
    for nome, tamanho, quantidade, simbolo in config_bancada['pecas']:
        for i in range(1, quantidade + 1):
            lista_pecas.append({
                'id': f"{simbolo}{id_contador}",
                'nome': f"{nome} #{i}" if quantidade > 1 else nome,
                'tipo': nome,
                'tamanho': tamanho,
                'simbolo': simbolo,
                'casas': [],           
                'casas_atingidas': [] 
            })
            id_contador += 1
    return lista_pecas

def validar_posicionamento(matriz_real, dimensao, linha, coluna, tamanho, orientacao):
    """
    Valida se uma peça cabe na matriz e não se sobrepõe a peças já existentes.
    
    Explicação Técnica:
    Itera por TODAS as casas que a peça ocuparia sequencialmente (horizontal ou vertical).
    Se qualquer casa ultrapassar a dimensão N ou colidir com um símbolo diferente de VAZIO,
    a função rejeita o posicionamento informando a causa específica.
    """
    casas_ocupadas = []
    
    for k in range(tamanho):
        r = linha + (k if orientacao == 'V' else 0)
        c = coluna + (k if orientacao == 'H' else 0)
        
        # Checagem de Limites da Bancada
        if r < 0 or r >= dimensao or c < 0 or c >= dimensao:
            return False, "A peça ultrapassa os limites da bancada.", []
            
        # Checagem de Sobreposição de Peças
        if matriz_real[r][c] != SIMBOLO_VAZIO:
            return False, f"A posição ({r + 1}, {c + 1}) já está ocupada por outra peça.", []
            
        casas_ocupadas.append((r, c))
        
    return True, "Posição válida.", casas_ocupadas


def posicionar_peca_na_matriz(matriz_real, peca, casas_ocupadas):
    """
    Escreve a peça na matriz real e atualiza a estrutura da peça.
    """
    peca['casas'] = casas_ocupadas
    for r, c in casas_ocupadas:
        matriz_real[r][c] = peca['id']


def posicionar_pecas_automatico(matriz_real, dimensao, lista_pecas):
    """
    Posiciona aleatoriamente todas as peças da lista sem sobreposições.
    """
    for peca in lista_pecas:
        posicionado = False
        while not posicionado:
            linha = random.randint(0, dimensao - 1)
            coluna = random.randint(0, dimensao - 1)
            orientacao = random.choice(['H', 'V'])
            
            valido, _, casas = validar_posicionamento(
                matriz_real, dimensao, linha, coluna, peca['tamanho'], orientacao
            )
            if valido:
                posicionar_peca_na_matriz(matriz_real, peca, casas)
                posicionado = True


def posicionar_pecas_jogador(matriz_real, dimensao, lista_pecas):
    """
    Interface para o jogador posicionar manualmente suas peças com opção de modo automático.
    """
    print("\n--- POSICIONAMENTO DAS PEÇAS ---")
    print("Deseja posicionar suas peças manualmente ou automaticamente?")
    print("1 - Manualmente")
    print("2 - Automático (Aleatório)")
    
    opcao = ler_opcao_valida(["1", "2"], "Escolha o modo de posicionamento (1 ou 2): ")
    
    if opcao == "2":
        posicionar_pecas_automatico(matriz_real, dimensao, lista_pecas)
        print("\nSuas peças foram posicionadas automaticamente com sucesso!")
        return

    for peca in lista_pecas:
        posicionado = False
        while not posicionado:
            exibir_bancada_com_legendas(matriz_real, None, dimensao, titulo="SUA BANCADA (EM CONSTRUÇÃO)")
            print(f"\nPosicionando: {peca['nome']} (Tamanho: {peca['tamanho']} casa(s))")
            
            try:
                linha_input = input(f"Informe a linha inicial (1 a {dimensao}): ").strip()
                coluna_input = input(f"Informe a coluna inicial (1 a {dimensao}): ").strip()
                
                linha = int(linha_input) - 1
                coluna = int(coluna_input) - 1
                
                if peca['tamanho'] > 1:
                    orientacao = input("Informe a orientação (H - Horizontal / V - Vertical): ").strip().upper()
                    if orientacao not in ['H', 'V']:
                        print("Erro: Orientação inválida! Use apenas 'H' ou 'V'.")
                        continue
                else:
                    orientacao = 'H'
                    
                valido, motivo, casas = validar_posicionamento(
                    matriz_real, dimensao, linha, coluna, peca['tamanho'], orientacao
                )
                
                if valido:
                    posicionar_peca_na_matriz(matriz_real, peca, casas)
                    posicionado = True
                    print(f"-> {peca['nome']} posicionada com sucesso!")
                else:
                    print(f"Recusado: {motivo} Tente novamente.")
                    
            except ValueError:
                print("Erro de Entrada: Digite números inteiros válidos para linha e coluna.")
            except IndexError:
                print("Erro de Posição: Coordenadas fora dos limites da matriz.")


def exibir_bancada_com_legendas(matriz_jogador_real, matriz_totem_rastreio, dimensao, titulo=""):
    """
    Exibe visualmente as bancadas com cabeçalhos numerados e legendas legíveis.
    """
    if titulo:
        print(f"\n==================== {titulo} ====================")
        
    headers = "    " + " ".join(f"{c+1:2d}" for c in range(dimensao))
    separator = "   +" + "---" * dimensao + "+"
    
    if matriz_totem_rastreio is not None:
        print("\n--- BANCADA DO TOTEM (SUAS JOGADAS) ---")
        print(headers)
        print(separator)
        for r in range(dimensao):
            linha_str = f"{r+1:2d} |"
            for c in range(dimensao):
                cell = matriz_totem_rastreio[r][c]
                linha_str += f" {cell} "
            linha_str += "|"
            print(linha_str)
        print(separator)

    if matriz_jogador_real is not None:
        print("\n--- SUA BANCADA (SUAS PEÇAS & ATAQUES DO TOTEM) ---")
        print(headers)
        print(separator)
        for r in range(dimensao):
            linha_str = f"{r+1:2d} |"
            for c in range(dimensao):
                cell = matriz_jogador_real[r][c]
                if cell not in [SIMBOLO_VAZIO, SIMBOLO_ACERTO, SIMBOLO_ERRO]:
                    simbolo_exibicao = cell
                else:
                    simbolo_exibicao = cell
                linha_str += f" {simbolo_exibicao} "
            linha_str += "|"
            print(linha_str)
        print(separator)
        
    print("\nLEGENDA: [.] Não Cantada / Vazio  |  [X] Acerto  |  [o] Erro")
    print("PEÇAS:   [A] Asas (4) | [R] Armadura (3) | [C] Capa (2) | [E] Elmo (1)")


def executar_olho_clinico(matriz_totem_real, dimensao, usos_restantes):
    """
    Executa a habilidade Olho Clínico: conta peças em uma submatriz 3x3 sem revelar posições.
    
    Explicação Técnica:
    Calcula os limites inferior e superior do quadrado 3x3 centrado na célula (linha, coluna).
    Utiliza max(0, r-1) e min(dimensao-1, r+1) para tratamento seguro de cantos e bordas.
    """
    if usos_restantes <= 0:
        print("\n[Olho Clínico] Você já esgotou todos os usos permitidos nesta partida!")
        return False, 0
        
    print(f"\n--- OLHO CLÍNICO (Usos restantes: {usos_restantes}) ---")
    try:
        r_in = int(input(f"Informe a linha central do quadrado 3x3 (1 a {dimensao}): ")) - 1
        c_in = int(input(f"Informe a coluna central do quadrado 3x3 (1 a {dimensao}): ")) - 1
        
        if r_in < 0 or r_in >= dimensao or c_in < 0 or c_in >= dimensao:
            print("[Olho Clínico] Coordenada fora da bancada. Operação cancelada.")
            return False, 0
            
        r_min = max(0, r_in - 1)
        r_max = min(dimensao - 1, r_in + 1)
        c_min = max(0, c_in - 1)
        c_max = min(dimensao - 1, c_in + 1)
        
        contagem = 0
        for r in range(r_min, r_max + 1):
            for c in range(c_min, c_max + 1):
                if matriz_totem_real[r][c] != SIMBOLO_VAZIO:
                    contagem += 1
                    
        print(f"\n[Olho Clínico] O radar indica que existem {contagem} casa(s) ocupada(s) por peças na região 3x3 apontada!")
        return True, contagem
        
    except ValueError:
        print("[Olho Clínico] Entrada inválida. Digite apenas números inteiros.")
        return False, 0


def verificar_peca_completada(pecas_alvo, linha, coluna):
    """
    Registra acerto na estrutura da peça e verifica se todas as suas casas foram descobertas.
    """
    for peca in pecas_alvo:
        if (linha, coluna) in peca['casas']:
            if (linha, coluna) not in peca['casas_atingidas']:
                peca['casas_atingidas'].append((linha, coluna))
                
            if len(peca['casas_atingidas']) == peca['tamanho']:
                return peca['nome']
    return None


def resolver_jogada(linha, coluna, matriz_alvo_real, matriz_alvo_rastreio, pecas_alvo):
    """
    Processa um tiro no tabuleiro adversário.
    
    Retorna:
        tuple: (sucesso_valido, acertou, peca_completada_nome)
    """
    # Validação de casas repetidas
    if matriz_alvo_rastreio[linha][coluna] in [SIMBOLO_ACERTO, SIMBOLO_ERRO]:
        return False, False, None
        
    conteudo = matriz_alvo_real[linha][coluna]
    
    if conteudo != SIMBOLO_VAZIO:
        matriz_alvo_rastreio[linha][coluna] = SIMBOLO_ACERTO
        peca_completada = verificar_peca_completada(pecas_alvo, linha, coluna)
        return True, True, peca_completada
    else:
        matriz_alvo_rastreio[linha][coluna] = SIMBOLO_ERRO
        return True, False, None


def jogada_totem_novato(dimensao, matriz_jogador_rastreio):
    """
    IA Novato: Escolhe aleatoriamente uma casa ainda não cantada.
    """
    casas_disponiveis = [
        (r, c) for r in range(dimensao) for c in range(dimensao)
        if matriz_jogador_rastreio[r][c] not in [SIMBOLO_ACERTO, SIMBOLO_ERRO]
    ]
    return random.choice(casas_disponiveis)


def jogada_totem_veterano(dimensao, matriz_jogador_rastreio, estado_ia):
    """
    IA Veterano: Joga aleatoriamente até acertar. Após um acerto, foca nas vizinhas.
    """
    while estado_ia['vizinhos_pendentes']:
        r, c = estado_ia['vizinhos_pendentes'].pop(0)
        if 0 <= r < dimensao and 0 <= c < dimensao:
            if matriz_jogador_rastreio[r][c] not in [SIMBOLO_ACERTO, SIMBOLO_ERRO]:
                return (r, c)
                
    return jogada_totem_novato(dimensao, matriz_jogador_rastreio)


def adicionar_vizinhos_ia(r, c, dimensao, matriz_jogador_rastreio, estado_ia):
    """
    Adiciona vizinhos orthogonais (N, S, L, O) válidos para a busca da IA Veterano.
    """
    direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in direcoes:
        nr, nc = r + dr, c + dc
        if 0 <= nr < dimensao and 0 <= nc < dimensao:
            if matriz_jogador_rastreio[nr][nc] not in [SIMBOLO_ACERTO, SIMBOLO_ERRO]:
                if (nr, nc) not in estado_ia['vizinhos_pendentes']:
                    estado_ia['vizinhos_pendentes'].append((nr, nc))

def executar_partida(config_bancada, modo_ia_escolhido):
    """
    Gerencia o loop principal de uma partida entre o Jogador e o Totem.
    """
    dimensao = config_bancada['dimensao']
    
    # Inicialização das Bancadas (Listas de Listas)
    matriz_jogador_real = criar_matriz(dimensao)
    matriz_jogador_rastreio = criar_matriz(dimensao)
    matriz_totem_real = criar_matriz(dimensao)
    matriz_totem_rastreio = criar_matriz(dimensao)
    
    # Inicialização das Peças
    pecas_jogador = criar_estrutura_pecas(config_bancada)
    pecas_totem = criar_estrutura_pecas(config_bancada)
    
    # Posicionamento Inicial
    posicionar_pecas_automatico(matriz_totem_real, dimensao, pecas_totem)
    posicionar_pecas_jogador(matriz_jogador_real, dimensao, pecas_jogador)
    
    # Variáveis de Estado da Partida
    rodada = 1
    pontuacao = 0
    usos_olho = MAX_OLHO_CLINICO
    casas_cantadas_jogador = 0
    acertos_jogador = 0
    erros_jogador = 0
    pecas_completadas_jogador = 0
    pecas_completadas_totem = 0
    
    total_pecas = len(pecas_jogador)
    estado_ia = {'vizinhos_pendentes': []}
    
    desistência = False
    vencedor = None
    
    print("\n==================================================")
    print("          A PARTIDA COMEÇOU! BOA SORTE!          ")
    print("==================================================")
    
    while vencedor is None and not desistência:
        exibir_bancada_com_legendas(
            matriz_jogador_real, matriz_totem_rastreio, dimensao, 
            titulo=f"RODADA {rodada} | Pontuação: {pontuacao} pts"
        )
        
        # --- TURNO DO JOGADOR ---
        turno_jogador_concluido = False
        while not turno_jogador_concluido:
            print("\nSUA VEZ DE JOGAR:")
            print("1 - Cantar uma casa")
            print("2 - Usar Olho Clínico")
            print("3 - Desistir da partida")
            
            op = ler_opcao_valida(["1", "2", "3"], "Escolha sua ação (1, 2 ou 3): ")
            
            if op == "3":
                conf = input("Tem certeza que deseja desistir? (S/N): ").strip().upper()
                if conf == 'S':
                    desistência = True
                    turno_jogador_concluido = True
                    break
                else:
                    continue
                    
            elif op == "2":
                usou, _ = executar_olho_clinico(matriz_totem_real, dimensao, usos_olho)
                if usou:
                    usos_olho -= 1
                    pontuacao = max(0, pontuacao - 30)
                continue
                
            elif op == "1":
                try:
                    r_in = input(f"Informe a linha do tiro (1 a {dimensao}): ").strip()
                    c_in = input(f"Informe a coluna do tiro (1 a {dimensao}): ").strip()
                    
                    r = int(r_in) - 1
                    c = int(c_in) - 1
                    
                    if r < 0 or r >= dimensao or c < 0 or c >= dimensao:
                        print("Erro: Posição fora dos limites da bancada! Tente novamente.")
                        continue
                        
                    valido, acertou, peca_destruida = resolver_jogada(
                        r, c, matriz_totem_real, matriz_totem_rastreio, pecas_totem
                    )
                    
                    if not valido:
                        print("Aviso: Essa casa já foi cantada anteriormente! Sua vez não foi gasta.")
                        continue
                        
                    casas_cantadas_jogador += 1
                    turno_jogador_concluido = True
                    
                    if acertou:
                        acertos_jogador += 1
                        pontuacao += 10
                        print(f"\n-> FOGO! Você ACERTOU uma peça do Totem na posição ({r+1}, {c+1})! (+10 pts)")
                        if peca_destruida:
                            pecas_completadas_jogador += 1
                            pontuacao += 50
                            print(f"-> EXCELENTE! Você COMPLETOU a peça: {peca_destruida}! (+50 pts bônus)")
                    else:
                        erros_jogador += 1
                        pontuacao = max(0, pontuacao - 5)
                        print(f"\n-> ÁGUA! Nenhuma peça encontrada na posição ({r+1}, {c+1}). (-5 pts)")
                        
                except ValueError:
                    print("Erro de Entrada: Digite números inteiros válidos para linha e coluna.")
                except IndexError:
                    print("Erro de Limite: Coordenada fora do intervalo permitido.")

        # Verificação de Vitória do Jogador
        if pecas_completadas_jogador == total_pecas:
            vencedor = "Jogador"
            pontuacao += 200
            print("\n PARABÉNS! VOCÊ DESCOBRIU TODAS AS PEÇAS DO TOTEM E VENCEU! (+200 pts)")
            break

        if desistência:
            print("\nVocê desistiu da partida.")
            vencedor = "Totem (Desistência)"
            break

        # --- TURNO DO TOTEM ---
        print("\n--------------------------------------------------")
        print("TURNO DO TOTEM:")
        if modo_ia_escolhido == "Novato":
            r_totem, c_totem = jogada_totem_novato(dimensao, matriz_jogador_rastreio)
        else:
            r_totem, c_totem = jogada_totem_veterano(dimensao, matriz_jogador_rastreio, estado_ia)
            
        valido, acertou_totem, peca_destruida_totem = resolver_jogada(
            r_totem, c_totem, matriz_jogador_real, matriz_jogador_rastreio, pecas_jogador
        )
        
        if acertou_totem:
            print(f"-> O Totem atacou a posição ({r_totem+1}, {c_totem+1}) e ACERTOU uma de suas peças!")
            if modo_ia_escolhido == "Veterano":
                adicionar_vizinhos_ia(r_totem, c_totem, dimensao, matriz_jogador_rastreio, estado_ia)
            if peca_destruida_totem:
                pecas_completadas_totem += 1
                print(f"-> ATENÇÃO! O Totem completou a sua peça: {peca_destruida_totem}!")
                if modo_ia_escolhido == "Veterano":
                    estado_ia['vizinhos_pendentes'] = []
        else:
            print(f"-> O Totem atacou a posição ({r_totem+1}, {c_totem+1}) e deu ÁGUA.")
            
        if pecas_completadas_totem == total_pecas:
            vencedor = "Totem"
            print("\n O Totem descobriu todas as suas peças primeiro. Você perdeu esta partida.")
            break

        rodada += 1
    aproveitamento = (acertos_jogador / casas_cantadas_jogador * 100) if casas_cantadas_jogador > 0 else 0.0
    
    dados_partida = {
        'bancada': config_bancada['nome'],
        'modo_ia': modo_ia_escolhido,
        'resultado': "Vitória" if vencedor == "Jogador" else ("Desistência" if desistência else "Derrota"),
        'rodadas': rodada,
        'casas_cantadas': casas_cantadas_jogador,
        'acertos': acertos_jogador,
        'erros': erros_jogador,
        'aproveitamento': aproveitamento,
        'pecas_jogador_completadas': pecas_completadas_jogador,
        'pecas_totem_completadas': pecas_completadas_totem,
        'usos_olho': MAX_OLHO_CLINICO - usos_olho,
        'pontuacao': pontuacao
    }
    
    exibir_resumo_partida(dados_partida, matriz_totem_real, dimensao)
    return dados_partida


def exibir_resumo_partida(dados, matriz_totem_real, dimensao):
    """
    Exibe o relatório de fechamento da partida e revela o tabuleiro completo do Totem.
    """
    print("\n==================================================")
    print("               RESUMO DA PARTIDA                  ")
    print("==================================================")
    print(f"Resultado Final: {dados['resultado']}")
    print(f"Bancada Escolhida: {dados['bancada']}")
    print(f"Nível do Adversário: {dados['modo_ia']}")
    print(f"Total de Rodadas: {dados['rodadas']}")
    print(f"Casas Cantadas: {dados['casas_cantadas']}")
    print(f"Acertos: {dados['acertos']}")
    print(f"Erros: {dados['erros']}")
    print(f"Aproveitamento:   {dados['aproveitamento']:.1f}%")
    print(f"Peças Completadas (Você):  {dados['pecas_jogador_completadas']}")
    print(f"Peças Completadas (Totem): {dados['pecas_totem_completadas']}")
    print(f"Usos do Olho Clínico:  {dados['usos_olho']}")
    print(f"PONTUAÇÃO FINAL:   {dados['pontuacao']} pontos")
    print("==================================================")
    
    print("\n--- REVELAÇÃO DA BANCADA DO TOTEM (POSIÇÕES ESCONDIDAS) ---")
    headers = "    " + " ".join(f"{c+1:2d}" for c in range(dimensao))
    separator = "   +" + "---" * dimensao + "+"
    print(headers)
    print(separator)
    for r in range(dimensao):
        linha_str = f"{r+1:2d} |"
        for c in range(dimensao):
            cell = matriz_totem_real[r][c]
            simb = cell if cell != SIMBOLO_VAZIO else '.'
            linha_str += f" {simb} "
        linha_str += "|"
        print(linha_str)
    print(separator)
    input("\nPressione ENTER para voltar ao menu principal...")

def atualizar_placar(placar_do_dia, dados_partida):
    """
    Adiciona os dados de uma partida concluída ao placar do dia.
    """
    registro = [
        dados_partida['pontuacao'],
        dados_partida['resultado'],
        dados_partida['bancada'],
        dados_partida['modo_ia'],
        dados_partida['rodadas'],
        f"{dados_partida['aproveitamento']:.1f}%"
    ]
    placar_do_dia.append(registro)


def exibir_placar_do_dia(placar_do_dia):
    """
    Ordena e exibe o placar do dia em ordem decrescente de pontuação.
    """
    print("\n==========================================================================")
    print("                         PLACAR DO DIA (RANKING)                          ")
    print("==========================================================================")
    
    if not placar_do_dia:
        print("Nenhuma partida foi registrada no placar até o momento.")
        print("==========================================================================")
        input("\nPressione ENTER para voltar ao menu...")
        return

    placar_ordenado = sorted(placar_do_dia, key=lambda item: item, reverse=True)

    print(f"{'POS':<4} | {'PONTOS':<8} | {'RESULTADO':<12} | {'BANCADA':<20} | {'IA':<9} | {'RODADAS'}")
    print("-" * 74)
    
    for idx, reg in enumerate(placar_ordenado, 1):
        pontos, res, bancada, ia, rodadas, _ = reg
        print(f"{idx:<4} | {pontos:<8} | {res:<12} | {bancada:<20} | {ia:<9} | {rodadas}")
        
    print("==========================================================================")
    input("\nPressione ENTER para voltar ao menu...")


# ==============================================================================
# MENU E UTILITÁRIOS DE ENTRADA ROBUSTA
# ==============================================================================

def ler_opcao_valida(opcoes_validas, mensagem):
    """
    Trata exceções e valida escolhas de menu do jogador.
    """
    while True:
        try:
            opcao = input(mensagem).strip()
            if opcao in opcoes_validas:
                return opcao
            print(f"Opção inválida! Escolha entre: {', '.join(opcoes_validas)}")
        except Exception as e:
            print(f"Erro de leitura: {e}. Tente novamente.")


def exibir_regras():
    """
    Apresenta as regras do jogo e instruções aos novos visitantes.
    """
    print("\n==========================================================================")
    print("                   REGRAS DA GINCANA DOS ATELIÊS                          ")
    print("==========================================================================")
    print("1. OBJETIVO: Descobrir todas as peças escondidas na bancada do Totem antes")
    print("   que ele descubra todas as suas peças no ateliê.")
    print("2. BANCADAS:")
    print("   - Ensaio (6x6): 5 Peças (Armadura, 2 Capas, 2 Elmos)")
    print("   - Montagem (8x8): 6 Peças (Asas, Armadura, 2 Capas, 2 Elmos)")
    print("   - Véspera (10x10): 10 Peças (Asas, 2 Armaduras, 3 Capas, 4 Elmos)")
    print("3. PONTUAÇÃO:")
    print("   - Casa com peça encontrada: +10 pontos")
    print("   - Casa vazia cantada (Água): -5 pontos")
    print("   - Peça completada/destruída: +50 pontos bônus")
    print("   - Uso do Olho Clínico:       -30 pontos")
    print("   - Vitória na partida:        +200 pontos bônus")
    print("   - Mínimo de pontuação:       0 pontos (sem saldo negativo)")
    print("4. RECURSO OLHO CLÍNICO:")
    print("   - Permite consultar quantas casas ocupadas existem numa área 3x3")
    print("   - Limite de 3 usos por partida.")
    print("==========================================================================")
    input("\nPressione ENTER para continuar...")


def menu_principal():
    """
    Loop do menu do sistema contínuo do Totem.
    """
    placar_do_dia = []
    primeira_execucao = True
    
    while True:
        if primeira_execucao:
            exibir_regras()
            primeira_execucao = False
            
        print("\n==================================================")
        print("     TOTEM GAME-CON POCKET - GINCANA DOS ATELIÊS  ")
        print("==================================================")
        print("1 - Iniciar Nova Partida")
        print("2 - Ver Placar do Dia (Ranking)")
        print("3 - Instruções e Regras do Jogo")
        print("4 - Sair do Sistema (Exclusivo Organização)")
        
        opcao = ler_opcao_valida(["1", "2", "3", "4"], "Escolha uma opção (1-4): ")
        
        if opcao == "1":
            print("\n--- ESCOLHA A BANCADA ---")
            print("1 - Bancada de Ensaio (6 x 6)")
            print("2 - Bancada de Montagem (8 x 8)")
            print("3 - Bancada de Véspera (10 x 10)")
            bancada_op = ler_opcao_valida(["1", "2", "3"], "Selecione a bancada (1-3): ")
            config_bancada = CONFIGS_BANCADA[bancada_op]
            
            print("\n--- ESCOLHA O NÍVEL DO ADVERSÁRIO (TOTEM) ---")
            print("1 - Novato (Jogadas totalmente aleatórias)")
            print("2 - Veterano (Insiste nas casas vizinhas ao acertar)")
            ia_op = ler_opcao_valida(["1", "2"], "Selecione o nível (1 ou 2): ")
            modo_ia = "Novato" if ia_op == "1" else "Veterano"
            
            dados = executar_partida(config_bancada, modo_ia)
            atualizar_placar(placar_do_dia, dados)
            
        elif opcao == "2":
            exibir_placar_do_dia(placar_do_dia)
            
        elif opcao == "3":
            exibir_regras()
            
        elif opcao == "4":
            print("\nEncerrando a sessão do Totem...")
            break
if __name__ == "__main__":
    menu_principal()
