from random import randint


class Vertice:
    def __init__(self, num, d, cor, pai):
        self.num = num
        self.d = d
        self.adj = []
        self.cor = cor
        self.pai = pai

class Grafo:
    def __init__(self, n):
        list = []
        for i in range(n):
            v = Vertice(i, -1, -1, -1)
            list.append(v)
        self.lista = list

    def addLista(self, u, list):
        for i in range(len(list)):
            self.lista[u].adj.append(self.lista[list[i]])

#A função bfs tem como entrada um grafo e um vertice pertencente a esse grafo
def bfs(grafo, s):
    for v in grafo.lista:
        v.d = -1
        v.cor = "branco"
        v.pai = -1
    s.d = 0
    s.cor = "cinza"
    s.pai = -1
    fila = []
    fila.append(s)
    while fila != []:
        u = fila.pop(0)
        for v in u.adj:
            if v.cor == "branco":
                v.cor = "cinza"
                v.pai = u.num
                v.d = u.d + 1
                fila.append(v)
        u.cor = "preto"

#A funcao diameter tem como entrada uma arvore T e retorna o diametro dessa arvore 
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
    
g  = Grafo(8)
g.addLista(0, [1, 4])
g.addLista(1, [0, 5])
g.addLista(2, [3, 6])
g.addLista(3, [2])
g.addLista(4, [0])
g.addLista(5, [1, 6])
g.addLista(6, [2, 5, 7])
g.addLista(7, [6])


gr= Grafo(4)
gr.addLista(0, [2, 3])
gr.addLista(1, [3])
gr.addLista(2, [0])
gr.addLista(3, [0, 1])



#testando a função bfs para os grafos "g" e "gr"
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

# testando a função diameter para os grafos "g" e "gr"
assert diameter(g) == 6
assert diameter(gr) == 3

    
# #A função mostrar tem como entrada um grafo g e mostra todos os elementos de cada vértice desse grafo
#função auxiliar
# def mostrar(g):
#     for v in g.lista:
#         print("Vertice: ",v.num,"| Valor: ", v.d,"| Cor: ", v.cor, "| Pai: ", v.pai)
#     print("\n")