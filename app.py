# VARIÁVEIS GLOBAIS
tamanho = 7             # Tamanho do tabuleiro
computador = 'x'        # Simbolo para o computador (1)
humano = 'o'            # Simbolo do jogador humano (-1)
vazio = ' '             # Simbolo para espaço não jogado
player = -1             # Jogador atual (padrão: inicia com humano: -1)
infinito = 111000       # Valor infinito utilizado
depth = tamanho**2      # Profundidade inicial - Tabuleiro vazio
tabuleiro = [['x', 'o', 'o', 'x', 'o', ' ', ' '],
             ['x', 'x', 'o', 'x', 'x', ' ', 'x'],
             ['x', 'o', 'x', 'o', 'o', ' ', 'o'],
             ['o', 'o', 'o', 'o', 'x', ' ', 'x'],
             ['x', 'x', 'o', 'x', 'o', ' ', 'o'],
             ['x', 'o', 'x', 'o', 'x', ' ', 'x'],
             ['o', 'x', 'o', 'x', 'o', ' ', 'o']] # Tabuleiro 7x7

# Retorna 1 se player = X ou -1 para player = O e 0 caso contrário
def get_numero_jogador(player = ''):
    if player == computador:
        return 1
    elif player == humano:
        return -1
    return 0

# Retorna X se player = 1 ou O para player = -1 e '' caso contrário
def get_simbolo_jogador(player = 0):
    if player == 1:
        return computador
    elif player == -1:
        return humano
    return vazio

# Retorna 1 se X ganhou, -1 se 0 ganhou, 0 caso contrário.
def custo(tabuleiro):
    for i in range(tamanho): # Checagem das linhas e colunas
        if(tabuleiro[i][0] == tabuleiro[i][1] == tabuleiro[i][2] == tabuleiro[i][3] 
           == tabuleiro[i][4] == tabuleiro[i][5] == tabuleiro[i][6] != vazio):
            return get_numero_jogador(tabuleiro[i][0])
        if(tabuleiro[0][i] == tabuleiro[1][i] == tabuleiro[2][i] == tabuleiro[3][i] 
           == tabuleiro[4][i] == tabuleiro[5][i] == tabuleiro[6][i] != vazio):
            return get_numero_jogador(tabuleiro[0][i])

    if(tabuleiro[0][0] == tabuleiro[1][1] == tabuleiro[2][2] == tabuleiro[3][3] 
       == tabuleiro[4][4] == tabuleiro[5][5] == tabuleiro[6][6] != vazio):
        return get_numero_jogador(tabuleiro[0][0])
    if(tabuleiro[6][0] == tabuleiro[5][1] == tabuleiro[4][2]
       == tabuleiro[3][3] == tabuleiro[2][4] == tabuleiro[1][5] == tabuleiro[0][6] != vazio):
        return get_numero_jogador(tabuleiro[1][1])
    return 0

# Retorna o tabuleiro que resulta ao fazer a jogada i,j
def resultado(tabuleiro, acao):
    x, y = acao[0], acao[1]
    if tabuleiro[x][y] == vazio:
        tabuleiro[x][y] = get_simbolo_jogador(player)
        return tabuleiro
    else:
        print("Jogada não permitida! Campo já preenchido.")
        return None
    
# Retorna o ganhador, se houver
def ganhador(tabuleiro) -> str:
    r = get_simbolo_jogador(custo(tabuleiro))
    return r if r != vazio else "Empate"

# Retorna Verdadeiro se o jogo acabou, Falso caso contrário
def final(tabuleiro):
    if custo(tabuleiro) != 0 or len(acoes(tabuleiro)) == 0:
        return True
    return False

# Retorna todas as jogadas disponíveis
def acoes(tabuleiro):
    jogadas = []
    for i in range(tamanho):
        for j in range(tamanho):
            if tabuleiro[i][j] == vazio:
                jogadas.append([i,j])
    return jogadas

# Retorna a jogada ótima para o jogador atual
def minimax(tabuleiro, profundidade, p):

    if p == get_numero_jogador(computador): # Caso o player seja o computador
        best = [-1, -1, -infinito]     # Define a busca pelo valor máximo
    else:
        best = [-1, -1, +infinito]     # Define a busca pelo valor mínimo

    if profundidade == 0 or final(tabuleiro): # Caso folha da arvore de recursão
        score = custo(tabuleiro)
        return [-1, -1, score] # Retorna somente pontuação

    for acao in acoes(tabuleiro):
        x, y = acao[0], acao[1]
        tabuleiro[x][y] = get_simbolo_jogador(p)
        score = minimax(tabuleiro, profundidade - 1, -p)
        tabuleiro[x][y] = get_simbolo_jogador(0)
        score[0], score[1] = x, y

        if p == get_numero_jogador(computador):
            if score[2] > best[2]:
                best = score  # max value
        else:
            if score[2] < best[2]:
                best = score  # min value
    return best

# Desenha o tabuleiro
def desenhar_tabuleiro(tabuleiro, tamanho):
    for i in range(tamanho):
        print(tabuleiro[i][0] + " | " + tabuleiro[i][1] + " | " + tabuleiro[i][2] + " | " 
              + tabuleiro[i][3] + " | " + tabuleiro[i][4] + " | " + tabuleiro[i][5] + " | "
              + tabuleiro[i][6])
        if i < tamanho - 1:
            print("--"*13)

if __name__ == "__main__":

    while True:
        desenhar_tabuleiro(tabuleiro,tamanho)

        if final(tabuleiro): break

        if player == -1:
            x, y = input("Digite sua jogada: ").split()
            x = int(x)
            y = int(y)
            if (x < 7 and x >= 0) and (y < 7 and y >= 0) and tabuleiro[x][y] == vazio:
                tab = resultado(tabuleiro, [x, y])
                player = -player
                depth -= 1
            else:
                print("Jogada não permitida.")
        else:
            acao_computador = minimax(tabuleiro, depth, player)
            tabuleiro = resultado(tabuleiro, acao_computador)
            player = -player
            depth -= 1

    print("Vencedor: ", ganhador(tabuleiro))