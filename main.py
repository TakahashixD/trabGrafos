from random import randint, random
import collections
import math
import time

class Vertice:
    def __init__(self, num, d, cor, pai, rank, chave, visitado):
        self.num = num
        self.d = d
        self.adj = []
        self.cor = cor
        self.pai = pai
        self.rank = rank
        self.chave = chave
        self.visitado = visitado

    def __repr__(self):
        return f"vertice: {self.num}"

class Grafo:
    def __init__(self, n):
        list = []
        for i in range(n):
            v = Vertice(i, -1, -1, -1, -1, -1, -1)
            list.append(v)
        self.lista = list
        self.aresta = []

    #adiciona vários vértices ao grafo
    def addLista(self, u, listav):
        for i in range(len(listav)):
            self.lista[u].adj.append(self.lista[listav[i]])

    #adiciona somente um vértice ao grafo
    def addListaund(self, u, v):
        self.lista[u].adj.append(self.lista[v])

    #adiciona aresta ao grafo
    def addaresta(self, u, v, peso):
        self.aresta.append((u, v, peso))
    

# A função bfs tem como entrada um grafo e um vertice pertencente a esse grafo
def bfs(grafo, s):
    for v in grafo.lista:
        v.d = -1
        v.cor = "branco"
        v.pai = -1
    s.d = 0
    s.cor = "cinza"
    s.pai = -1
    fila = collections.deque()
    fila.append(s)
    while fila:
        u = fila.popleft()
        for v in u.adj:
            if v.cor == "branco":
                v.cor = "cinza"
                v.pai = u
                v.d = u.d + 1
                fila.append(v)
        u.cor = "preto"


# A funcao diameter tem como entrada uma arvore T e retorna o diametro dessa arvore
def diameter(T):
    s = T.lista[randint(0, (len(T.lista) - 1))]
    bfs(T, s)
    maior = 0
    for i in T.lista:
        if i.d > maior:
            maior = i.d
            a = T.lista[i.num]
    bfs(T, a)
    distancia = 0
    for i in T.lista:
        if i.d > distancia:
            distancia = i.d
    return distancia

# Função random_tree_walk tem como entrada um número n, que é o tamanho do grafo e retorna
# uma árvore aleatória como resultado
def random_tree_random_walk(n):
    g = Grafo(n)
    for u in g.lista:
        u.cor = "branco"
    u = g.lista[randint(0, (len(g.lista) - 1))]
    u.cor = "preto"
    arestas = 0
    while arestas < n-1:
        v = g.lista[randint(0, (len(g.lista) - 1))]
        if v.cor == "branco":
            g.addLista(u.num, [v.num])
            g.addLista(v.num, [u.num])
            v.cor = "preto"
            arestas = arestas + 1
        u = v
    return g

#A funcao Make_Set tem como entrada um vertice 'x' e cria um componente para cada vertice
def Make_Set(x):
    x.pai = x
    x.rank = 0

#A funcao Union tem como entrada 2 vertices 'x' e 'y' e faz a união 
# entre os componentes os quais eles pertencem
def Union(x, y):
    Link(Find_Set(x), Find_Set(y))

#A funcao Link tem como entrada 2 vertices 'x' e 'y' e faz a ligação entre os componentes
def Link(x, y):
    if x.rank > y.rank:
        y.pai = x
    else:
        x.pai = y
        if x.rank == y.rank:
            y.rank = y.rank + 1

#A funcao Find_set tem como entrada o vertice 'x' 
# e retorna o indentificador do conjunto ao qual ele pertence
def Find_Set(x):
    if x != x.pai:
        x.pai = Find_Set(x.pai)
    return x.pai

#Funcao `MST_kruskal` recebe um grafo completo `g` e retorna uma arvore de peso minimo
def MST_Kruskal(g):
    A = Grafo(len(g.lista))
    for u in g.lista:
        Make_Set(u)
    g.aresta.sort(key = lambda aresta: aresta[2])
    for e in g.aresta:
        if Find_Set(g.lista[e[0]]) != Find_Set(g.lista[e[1]]):
            Union(g.lista[e[0]], g.lista[e[1]])
            A.addListaund(e[0], e[1])
            A.addListaund(e[1], e[0])
            A.addaresta(e[0], e[1], e[2])
    return A

#Funcao que gera um grafo completo
def grafo_completo(n):
    g = Grafo(n)
    for v in g.lista:
        for i in range(n):
            if v.num != i:
                g.addListaund(v.num, i)
    return g

#Funcao random tree kruskal recebe um numero `n` que representa o tamanho do grafo completo a
# a ser gereado e retorna um grafo construido apartir das arestas da árvore produzida pelo MST_Kruskal
def Random_tree_kruskal(n):
    g = grafo_completo(n)
    for v in g.lista:
        for u in v.adj:
            if v.num < u.num:
                x = random()
                g.addaresta(v.num, u.num, x)
    return MST_Kruskal(g)

#A função extract_min recebe como parametro uma lista vetores 'Q' e retorna o vertice de menor chave
def extract_min(Q):
    menor = math.inf
    for v in Q:
        if v.chave < menor and v.visitado == -1:
            menor = v.chave
            menorvertice = v
    menorvertice.visitado = 1
    return menorvertice

#Funcao `MST_Prim` recebe um grafo completo `g`, uma matriz de pesos 'W'
# e um vertice 'r' que retorna uma arvore de peso minimo    
def MST_Prim(g, W, r):
    for v in g.lista:
        v.chave = math.inf
        v.pai = -1
        v.visistado = -1
    r.chave = 0
    Q = g.lista
    i = 0
    while i < len(g.lista):
        u = extract_min(Q)
        for v in g.lista[u.num].adj:
            if v.chave > W[u.num][v.num] and v.visitado == -1:
                v.chave = W[u.num][v.num]
                v.pai = u
        i += 1
    arvore = Grafo(len(g.lista))
    for v in g.lista:
        if v.pai != -1:
            arvore.addListaund(v.num, v.pai.num)
            arvore.addListaund(v.pai.num, v.num)
    return arvore

#Funcao random tree Prim recebe um numero `n` que representa o tamanho do grafo completo a
# a ser gereado e retorna um grafo construido apartir dos vertices da árvore produzida pelo MST_Prim
def Random_tree_Prim(n):
    W = []
    g = grafo_completo(n)
    for i in range(n):
        linha = []
        for j in range(n):
            linha.append(0)
        W.append(linha)

    for i in range(n):
        for j in range(n):
            if j > i:
                break
            x = random()
            W[i][j] = x
            W[j][i] = x

    r = g.lista[0]
    return MST_Prim(g, W, r)


# Criando os grafos "g" e "gr"
g = Grafo(8)
g.addLista(0, [1, 4])
g.addLista(1, [0, 5])
g.addLista(2, [3, 6])
g.addLista(3, [2])
g.addLista(4, [0])
g.addLista(5, [1, 6])
g.addLista(6, [2, 5, 7])
g.addLista(7, [6])

gr = Grafo(4)
gr.addLista(0, [2, 3])
gr.addLista(1, [3])
gr.addLista(2, [0])
gr.addLista(3, [0, 1])


# Testando a função bfs para os grafos "g" e "gr"
bfs(g, g.lista[1])
assert g.lista[0].d == 1
assert g.lista[1].d == 0
assert g.lista[2].d == 3
assert g.lista[3].d == 4
assert g.lista[4].d == 2
assert g.lista[5].d == 1
assert g.lista[6].d == 2
assert g.lista[7].d == 3

bfs(gr, gr.lista[0])
assert gr.lista[0].d == 0
assert gr.lista[1].d == 2
assert gr.lista[2].d == 1
assert gr.lista[3].d == 1


# Testando a função diameter para os grafos "g" e "gr"
assert diameter(g) == 6
assert diameter(gr) == 3

#Testando a função grafo_completo com tamanho 5
g = grafo_completo(5)
assert g.lista[0].adj == [g.lista[1], g.lista[2], g.lista[3], g.lista[4]]
assert g.lista[1].adj == [g.lista[0], g.lista[2], g.lista[3], g.lista[4]]
assert g.lista[2].adj == [g.lista[0], g.lista[1], g.lista[3], g.lista[4]]
assert g.lista[3].adj == [g.lista[0], g.lista[1], g.lista[2], g.lista[4]]
assert g.lista[4].adj == [g.lista[0], g.lista[1], g.lista[2], g.lista[3]]

#Criando grafo 'graf' para testar o MST_Kruskal e MST_Prim
graf = Grafo(5)
graf.addLista(0, [1, 2, 3])
graf.addLista(1, [0, 4])
graf.addLista(2, [0, 3])
graf.addLista(3, [0, 2, 4])
graf.addLista(4, [1, 3])

graf.addaresta(0, 1, 5)
graf.addaresta(0, 2, 1)
graf.addaresta(0, 3, 3)
graf.addaresta(1, 4, 1)
graf.addaresta(2, 3, 4)
graf.addaresta(3, 4, 2)

#Testando o MST_Kruskal 
g = MST_Kruskal(graf)
#Calcular o peso do grafo 'g'
peso = 0
for e in g.aresta:
    peso = e[2] + peso
assert peso == 7

#Vertices para testes das funções a seguir
a = Vertice(0, -1, -1, -1, -1, -1, -1)
b = Vertice(1, -1, -1, -1, -1, -1, -1)
c = Vertice(2, -1, -1, -1, -1, -1, -1)
d = Vertice(3, -1, -1, -1, -1, -1, -1)
e = Vertice(4, -1, -1, -1, -1, -1, -1)
f = Vertice(5, -1, -1, -1, -1, -1, -1)
g = Vertice(6, -1, -1, -1, -1, -1, -1)

#Testando função Make_Set
Make_Set(a)
Make_Set(b)
Make_Set(c)
Make_Set(d)
Make_Set(e)
Make_Set(f)
Make_Set(g)
assert a.pai == a
assert a.rank == 0
assert b.pai == b
assert b.rank == 0
assert c.pai == c
assert c.rank == 0

#Testando função Find_Set
assert Find_Set(a) == a
assert Find_Set(b) == b
assert Find_Set(c) == c 

#Testando função Union
Union(a, b)
Union(b, c)
assert Find_Set(a) == Find_Set(c)
assert Find_Set(a) == Find_Set(b)
assert Find_Set(a) != Find_Set(d)

#Testando função Link
Link(e, f)
Link(f, g)
assert Find_Set(e) == Find_Set(f)
assert Find_Set(e) == Find_Set(g)
assert Find_Set(e) != Find_Set(a)

#Testando função extract_min

#Criando vetices para testar o extract_min
v1 = Vertice(0, -1, -1, -1, -1, 12, -1)
v2 = Vertice(1, -1, -1, -1, -1, 5, -1)
v3 = Vertice(2, -1, -1, -1, -1, 65, -1)
v4 = Vertice(3, -1, -1, -1, -1, 3, -1)
v5 = Vertice(4, -1, -1, -1, -1, 125, -1)
v6 = Vertice(5, -1, -1, -1, -1, 1, -1)
v7 = Vertice(6, -1, -1, -1, -1, 7546, -1)
v8 = Vertice(7, -1, -1, -1, -1, 97, -1)

lista1 = [v1, v2, v3, v4, v5]
lista2 = [v1, v7, v3, v6, v8]
lista3 = [v3, v2, v7, v8, v5]
lista4 = [v3, v5, v7, v8, v1]

assert extract_min(lista1) == v4
assert extract_min(lista2) == v6
assert extract_min(lista3) == v2
assert extract_min(lista4) == v1


# #Testando a função random_tree_random_walk
# for n in [250, 500, 750, 1000, 1250, 1500, 1750, 2000]:
#     soma = 0
#     for _ in range(500):
#         soma += diameter(random_tree_walk(n))
#     media = soma/500
#     print(media)

# #Testando a função random_tree_random_kruskal
# for n in [250, 500, 750, 1000, 1250, 1500, 1750, 2000]:
#     soma = 0
#     inicial = time.time()
#     for _ in range(500):
#         soma += diameter(Random_tree_kruskal(n))
#     media = soma/500
#     print(media)
#     fim = time.time()
#     print(fim - inicial)

# #Testando a função random_tree_random_Prim
# for n in [250, 500, 750, 1000, 1250, 1500, 1750, 2000]:
#     soma = 0
#     inicial = time.time()
#     for _ in range(500):
#         soma += diameter(Random_tree_Prim(n))
#     media = soma/500
#     print(media)
#     fim = time.time()
#     print(fim - inicial)
