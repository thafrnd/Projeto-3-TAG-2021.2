# Projeto 3 da disciplina Teoria e Aplicação de Grafos
# Universidade de Brasilia
# Departamento de Ciencia da Computacao
# Professor: Díbio Leandro Borges
# Aluna: Thaís Fernanda de Castro Garcia
# Matricula: 200043722

from random import shuffle
import copy
#usei de cinco classes para estruturar o projeto
#uma classe Grafo a qual é responsável por criar o grafo e suas estruturas
#uma classe No a qual é responsável por crias as funções para os Nós e algumas de suas estruturas
#uma classe Gerador_sudoku responsável por criar um jogo de sudoku valido, usando força bruta
#uma classe Quadro_sudoku responsável por criar o quadro de sudoku como uma matriz e montar o grafo
#uma classe Sudoku responsável por solucionar o jogo criado, usando o algortimo de coloração em grafos


#aplicação classica de classe para a criação de grafos e suas estruturas e metodos
#a classe ja possui as funções que posteriormente serão usadas na busca em profundidade e em largura para a criação de um jogo valido
class Grafo : 

    vertices_totais = 0 
    
    def __init__(self) : 
    
        self.nos_totais = dict()

    def cria_no(self, idx) : 
        if idx in self.nos_totais : 
            return None
        
        Grafo.vertices_totais += 1
        no = No(idx=idx)
        self.nos_totais[idx] = no
        return no


    def adiciona_vertice(self, src, dst, wt = 0) : 
        self.nos_totais[src].adiciona_vizinho(self.nos_totais[dst], wt)
        self.nos_totais[dst].adiciona_vizinho(self.nos_totais[src], wt)
    
    def eh_vizinho(self, u, v) : 
        if u >=1 and u <= 81 and v >=1 and v<= 81 and u !=v : 
            if v in self.nos_totais[u].get_conexao() : 
                return True
        return False

    def get_ids_totais(self) : 
        return self.nos_totais.keys()

#aplicação de uma classe Nó que cria alguns metódos que precisaremos usar posteriormente
class No : 
    
    def __init__(self, idx) :    
        self.id = idx
        self.conecta = dict()

    def adiciona_vizinho(self, vizinho , peso = 0) :
        if vizinho.id not in self.conecta.keys() :  
            self.conecta[vizinho.id] = peso

    def get_conexao(self) : 
        return self.conecta.keys()

    def get_id(self) : 
        return self.id
    
    
#classe responável por criar um jogo novo de Sudoku válido
#o jogo é criado preenchendo, com uso da busca em profundidade e em largura, todos os espaços com numeros 
#que não se repitam nem na coluna nem na linha
#depois os numeros são parcialmente removidos, gerando assim as lacunas que o jogador deve preencher
#dessa forma, é garantido que o jogo é válido
    
class Gerador_sudoku:
#inicializa as estruturas do jogo
    def __init__(self):
        self.contador = 0
        self.caminho = []
        self.jogo = [[0 for i in range(9)] for j in range(9)]
        self.gera_jogo()
        self.original = copy.deepcopy(self.jogo)

#cria e preenche a lista a qual corresponde ao jogo 9X9
    def gera_jogo(self):
        lista_sudoku=[]
        self.preenche_jogo(self.jogo)
        self.esvazia_jogo()
        for linha in self.jogo:
            lista_sudoku.append(linha)
        return lista_sudoku
    
#retorna se o numero ja foi usado na linha atual
    def ja_foi_usado_linha(self,jogo,linha,numero):
        if numero in jogo[linha]:
            return True
        return False
#retorna se o número ja foi usado na coluna atual
    def ja_foi_usado_coluna(self,jogo,coluna,numero):
        for i in range(9):
            if jogo[i][coluna] == numero:
                return True
        return False
    
#cada subjogo consiste em um quadrado 3x3
#retorna se o numero ja foi utilizado no subjogo atual
    def ja_foi_usado_subjogo(self,jogo,linha,coluna,numero):        
        sub_linha = (linha // 3) * 3
        sub_coluna = (coluna // 3)  * 3
        for i in range(sub_linha, (sub_linha + 3)): 
            for j in range(sub_coluna, (sub_coluna + 3)): 
                if jogo[i][j] == numero: 
                    return True
        return False
#usa das funções definidas acima para verificar se o numero pode ser usado em determinada posição
#retorna se ela é valida
    def posicao_valida(self,jogo,linha,coluna,numero):
        if self.ja_foi_usado_linha(jogo, linha,numero):
            return False
        elif self.ja_foi_usado_coluna(jogo,coluna,numero):
            return False
        elif self.ja_foi_usado_subjogo(jogo,linha,coluna,numero):
            return False
        return True
#itera para achar a proxima posição vazia
#uma posição vazi contém o número 0 nela
    def proxima_posição_vazia(self,jogo):
        for i in range(9):
            for j in range(9):
                if jogo[i][j] == 0:
                    return (i,j)
        return
#soluciona o jogo, se livra das posições igual a 0
    def soluciona(self, jogo):
        for i in range(0,81):
            linha=i//9
            coluna=i%9
            #verifica se a posição esta vazia
            if jogo[linha][coluna]==0:
                for number in range(1,10):
                    #verifica se o numero pode ser utilizado na posição 
                    if self.posicao_valida(jogo,linha,coluna,number):
                        jogo[linha][coluna]=number
                    #verifica se a posição precisa ser preenchida
                        if not self.proxima_posição_vazia(jogo):
                            self.contador+=1
                            break
                        else:
                            if self.soluciona(jogo):
                                return True
                break
        #caso contrario a posição é preenchida com 0
        jogo[linha][coluna]=0  
        return False
#responsável por preencher por completo, mesmo que com 0
    def preenche_jogo(self, jogo):
        possiveis_numeros = [1,2,3,4,5,6,7,8,9]
        for i in range(0,81):
            linha=i//9
            coluna=i%9
            #acha a proxima posição vazia
            if jogo[linha][coluna]==0:
                #se estiver vazia reposiciona os numeros
                shuffle(possiveis_numeros)
                #para cada um, antes de seguir, verifica se a posição é valida
                for numero in possiveis_numeros:
                    if self.posicao_valida(jogo,linha,coluna,numero):
                        self.caminho.append((numero,linha,coluna))
                        jogo[linha][coluna]=numero
                        #verifica se precisa ser preenchida
                        if not self.proxima_posição_vazia(jogo):
                            return True
                        else:
                            if self.preenche_jogo(jogo):
                                #se estiver cheio retorna True
                                return True
                break
        jogo[linha][coluna]=0  
        return False
#retorna as posições que já foram preenchidas no jogo
    def preenchidos(self,jogo):
        lista_preenchidos = []
        #itera sobre o jogo verificando se as posições estão preenchidas
        for i in range(len(jogo)):
            for j in range(len(jogo)):
                if jogo[i][j] != 0:
                    #reconhece então a posição como preenchida
                    lista_preenchidos.append((i,j))
        #reposiciona a lista
        shuffle(lista_preenchidos)
        return lista_preenchidos
#função que esvazia de forma estrategica o jogo que foi preenchido, para que o jogador possa o solucionar
#para que seja um jogo, no inicio deve conter pelo menos 17 posições preenchidas e ter apenas uma solução
    def esvazia_jogo(self):
        #cria uma lista com todas as posições que estão preenchidas
        lista_preenchidos = self.preenchidos(self.jogo)
        lista_preenchidos_contador = len(lista_preenchidos)
        loop = 3
        #verifica se possui pelo menos 17 posições preenchidas
        while loop > 0 and lista_preenchidos_contador >= 17:
            linha,coluna = lista_preenchidos.pop()
            lista_preenchidos_contador -= 1
            #salva qual é a posição para caso precise reverter
            posição_esvaziada = self.jogo[linha][coluna]
            self.jogo[linha][coluna]=0
            #gera uma copia do jogo pra que possa soluciona-la
            copia_do_jogo = copy.deepcopy(self.jogo)
            #cria um contador pras soluções
            self.contador=0      
            self.soluciona(copia_do_jogo)   
            #verifica se existe mais de uma solução, caso sim, reverte a posição que foi esvaziada 
            if self.contador!=1:
                self.jogo[linha][coluna]=posição_esvaziada
                lista_preenchidos_contador += 1
                loop -=1
        return self
#classe responsável por criar o quadro de sudoku como uma matriz e montar o grafo
class Quadro_sudoku :
    def __init__(self) :  
        self.grafo = Grafo() 
        self.linhas = 9
        self.colunas = 9
        self.total_de_posições = 81
        self.gera_grafo()
        self.conecta_vertices() 
        self.lista_ids = self.grafo.get_ids_totais() #cria uma lista com os ids
        
    def gera_grafo(self) : 
        for idx in range(1, self.total_de_posições+1) :
            _ = self.grafo.cria_no(idx)

    def conecta_vertices(self) : 
        matriz = self.gera_matriz()
        conexoes_matriz = dict()
        #itera sob as linhas e culnas de cada linha
        for linha in range(9) :
            for coluna in range(9) : 
                topo = matriz[linha][coluna] #topo vai ser usado pra identificar o nó
                connections = self.estruturação(matriz, linha, coluna)
                conexoes_matriz[topo] = connections
        self.conecta_entre_si(conexoes_matriz=conexoes_matriz)
        
    def conecta_entre_si(self, conexoes_matriz) : 
        for topo in conexoes_matriz.keys() :
            connections = conexoes_matriz[topo]
            for chave in connections :  #gera uma lista de todas as conexões
                for v in connections[chave] : 
                    self.grafo.adiciona_vertice(src=topo, dst=v)

 
    def estruturação(self, matriz, linhas, colunas) :
        connections = dict()
        linha = []
        coluna = []
        block = []

        # cria as linhas
        for c in range(colunas+1, 9) : 
            linha.append(matriz[linhas][c])
        
        connections["linhas"] = linha

        # cria as colunas 
        for r in range(linhas+1, 9):
            coluna.append(matriz[r][colunas])
        
        connections["colunas"] = coluna

        # cria os blocos 3X3
        if linhas%3 == 0 : 

            if colunas%3 == 0 :
                
                block.append(matriz[linhas+1][colunas+1])
                block.append(matriz[linhas+1][colunas+2])
                block.append(matriz[linhas+2][colunas+1])
                block.append(matriz[linhas+2][colunas+2])

            elif colunas%3 == 1 :
                
                block.append(matriz[linhas+1][colunas-1])
                block.append(matriz[linhas+1][colunas+1])
                block.append(matriz[linhas+2][colunas-1])
                block.append(matriz[linhas+2][colunas+1])
                
            elif colunas%3 == 2 :
                
                block.append(matriz[linhas+1][colunas-2])
                block.append(matriz[linhas+1][colunas-1])
                block.append(matriz[linhas+2][colunas-2])
                block.append(matriz[linhas+2][colunas-1])

        elif linhas%3 == 1 :
            
            if colunas%3 == 0 :
                
                block.append(matriz[linhas-1][colunas+1])
                block.append(matriz[linhas-1][colunas+2])
                block.append(matriz[linhas+1][colunas+1])
                block.append(matriz[linhas+1][colunas+2])

            elif colunas%3 == 1 :
                
                block.append(matriz[linhas-1][colunas-1])
                block.append(matriz[linhas-1][colunas+1])
                block.append(matriz[linhas+1][colunas-1])
                block.append(matriz[linhas+1][colunas+1])
                
            elif colunas%3 == 2 :
                
                block.append(matriz[linhas-1][colunas-2])
                block.append(matriz[linhas-1][colunas-1])
                block.append(matriz[linhas+1][colunas-2])
                block.append(matriz[linhas+1][colunas-1])

        elif linhas%3 == 2 :
            
            if colunas%3 == 0 :
                
                block.append(matriz[linhas-2][colunas+1])
                block.append(matriz[linhas-2][colunas+2])
                block.append(matriz[linhas-1][colunas+1])
                block.append(matriz[linhas-1][colunas+2])

            elif colunas%3 == 1 :
                
                block.append(matriz[linhas-2][colunas-1])
                block.append(matriz[linhas-2][colunas+1])
                block.append(matriz[linhas-1][colunas-1])
                block.append(matriz[linhas-1][colunas+1])
                
            elif colunas%3 == 2 :
                
                block.append(matriz[linhas-2][colunas-2])
                block.append(matriz[linhas-2][colunas-1])
                block.append(matriz[linhas-1][colunas-2])
                block.append(matriz[linhas-1][colunas-1])
        #conexões
        connections["blocks"] = block
        return connections
#gera uma matriz correspondente ao quadro do jogo
    def gera_matriz(self) : 
        matriz = [[0 for colunas in range(self.colunas)] 
        for linhas in range(self.linhas)]
        conta = 1
        for linhas in range(9) :
            for colunas in range(9):
                matriz[linhas][colunas] = conta
                conta+=1
        return matriz
#classe responsável por manipular o quadro gerado e aplicar o algoritmo de coloração para achar a solução do Sudoku
class Sudoku :
    
    def __init__(self) : 
        self.quadro = self.get_quadro()
        self.grafo_sudoku = Quadro_sudoku()
        #pega os ids das posições da matrix
        self.quadro_mapeado = self.get_matriz_mapeada() 

    def get_matriz_mapeada(self) : 
        matriz = [[0 for colunas in range(9)] 
        for linhas in range(9)]
        conta = 1
        for linhas in range(9) : 
            for colunas in range(9):
                matriz[linhas][colunas] = conta
                conta+=1
        return matriz
    
#usa das funções ja criadas pra gerar um novo jogo
    def get_quadro(self) : 
        novo_jogo = Gerador_sudoku()
        quadro= novo_jogo.gera_jogo()
        return quadro
#função que itera sobre a matriz criada pra exibir o quadro de jogo no formato usual
    def exibe_quadro(self) : 
        for i in range(len(self.quadro)) : 
            if i%3 == 0 and i != 0:
                print("  - - - - - - - - - - - - - - ")
            for j in range(len(self.quadro[i])) : 
                if j %3 == 0 : 
                    print(" |  ", end = "")
                if j == 8 :
                    print(self.quadro[i][j]," | ")
                else : 
                    print(f"{ self.quadro[i][j] } ", end="")
                       
        
#aqui já temos tudo que é necessário para poder comerçarmos a solucionar o jogo usando o algoritmo de coloração
#vamos usar 9 cores diferentes para colorir os vertices, dessa forma gantimos que nenhum dos vertices adjacentes possuam a mesma cor
#vamos de forma recursiva solucionar a posição de cada cor no quadro
#tentamos para cada iteração usar a cor c no no atual v usando a função pode_colorir para verificar se é possível ou não
#se for possivel chama a função colore_ap para o proximo vertice
#se não a iteração prossegue para a proxima cor
#caso qualquer uma das condicionais retorne True é quebrada a iteração

#inicializa as cores de cada id
    def inicializa_cores(self):
        #setadas são as cores que já estão definidas e não devem ser mudadas
        cor = [0] * (81+1)
        setadas = []
        #processo=[]
        
        #itera sobre o quadro e vai salvando os ids como idx e atualizando a cor 
        for linha in range(len(self.quadro)) : 
            for coluna in range(len(self.quadro[linha])) : 
                if self.quadro[linha][coluna] != 0 : 
                    idx = self.quadro_mapeado[linha][coluna]
                    #colore
                    cor[idx] = self.quadro[linha][coluna] 
                    setadas.append(idx)
        #self.exibe_quadro()
        #processo.append(self)
        return cor, setadas

#chama as funções inicializa_cores() e colore_ap() e retorna as cores
#recebe o jogo e passa os argumentos para a colore_ap()
    def colore (self, m =9) :
        cor, setadas = self.inicializa_cores()
        if self.colore_ap(m =m, cor=cor, v =1, setadas=setadas) is None :
            return False
        conta = 1
        for linha in range(9) :
            for coluna in range(9) :
                self.quadro[linha][coluna] = cor[conta]
                conta += 1
            if conta>=10:
                print("\n\n\n")
                self.exibe_quadro()
            
        return cor
#função recursiva onde se verifica se a cor atual pode ser usada no no atual    
    def colore_ap(self, m, cor, v, setadas) :
        if v == (81) +1  : 
            return True
        for c in range(1, m+1) : 
            if self.pode_colorir(v, cor, c, setadas) == True :
                cor[v] = c
                if self.colore_ap(m, cor, v+1, setadas) :
                    return True
            if v not in setadas : 
                cor[v] = 0
        return
    #função que verifica se a celula deve ser colorida ou não
    def pode_colorir(self, v, color, c, setadas) : 
        #self.exibe_quadro()
        if v in setadas and color[v] == c: 
            return True
        elif v in setadas : 
            return False

        for i in range(1, (81)+1) :
            if color[i] == c and self.grafo_sudoku.grafo.eh_vizinho(v, i) :
                return False
        return True


######################################################################################################################################### 
#executando as classes criadas
jogo_sudoku = Sudoku()
print("Jogo criado:")
print("\n")
jogo_sudoku.exibe_quadro()
print("\n\n\nSaídas intermediárias:") 
jogo_sudoku.colore(m=9)
print("\n\nSolução:")
print("\n")
jogo_sudoku.exibe_quadro()
