import os
import sys

if __name__ == "__main__" and __package__ is None:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if base_dir not in sys.path:
        sys.path.insert(0, base_dir)

from src.graph import Graph
from src.depth_first_paths import DepthFirstPaths
from src.breadth_first_paths import BreadthFirstPaths
from utils.queue import Queue

# Mapeamento: índice <-> sigla do estado
ESTADOS = ["AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE"]
NOMES = {
    "MA": "Maranhão",
    "PI": "Piauí",
    "CE": "Ceará",
    "RN": "Rio Grande do Norte",
    "PB": "Paraíba",
    "PE": "Pernambuco",
    "AL": "Alagoas",
    "SE": "Sergipe",
    "BA": "Bahia",
}
SIGLA_PARA_ID = {sigla: i for i, sigla in enumerate(ESTADOS)}


def carregar_grafo(caminho):
    """Carrega o grafo a partir do arquivo no formato algs4."""
    with open(caminho) as f:
        V = int(f.readline().strip())
        E = int(f.readline().strip())
        g = Graph(V)
        for _ in range(E):
            v, w = f.readline().strip().split()
            g.add_edge(int(v), int(w))
    return g


def ordem_visita_dfs(grafo, s):
    """Retorna a ordem em que a DFS visita os vértices."""
    marked = [False] * grafo.V
    ordem = []

    def dfs(v):
        marked[v] = True
        ordem.append(v)
        for w in grafo.adj[v]:
            if not marked[w]:
                dfs(w)

    dfs(s)
    return ordem


def ordem_visita_bfs(grafo, s):
    """Retorna a ordem em que a BFS visita os vértices."""
    marked = [False] * grafo.V
    ordem = []
    q = Queue()

    marked[s] = True
    q.enqueue(s)
    while not q.is_empty():
        v = q.dequeue()
        ordem.append(v)
        for w in grafo.adj[v]:
            if not marked[w]:
                marked[w] = True
                q.enqueue(w)

    return ordem


def formatar_caminho(path):
    """Converte iterable de índices em string com siglas separadas por seta."""
    return " -> ".join(ESTADOS[v] for v in path)


def formatar_ordem(order):
    """Converte lista de índices em string com siglas separadas por vírgula."""
    return ", ".join(ESTADOS[v] for v in order)


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    arquivo = os.path.join(base_dir, "dados", "nordeste.txt")
    grafo = carregar_grafo(arquivo)

    print("=" * 60)
    print("  GRAFO DOS ESTADOS DO NORDESTE DO BRASIL")
    print("  Resolução de Problemas com Grafos - Trabalho Prático 1")
    print("=" * 60)
    print()
    print("Estados disponíveis:", ", ".join(ESTADOS))
    print()

    try:
        origem = input("Digite o estado de ORIGEM (sigla, ex: CE): ").strip().upper()
        destino = input("Digite o estado de DESTINO (sigla, ex: BA): ").strip().upper()
    except EOFError:
        print("Erro: entrada não fornecida.")
        sys.exit(1)

    if origem not in SIGLA_PARA_ID or destino not in SIGLA_PARA_ID:
        print("Erro: sigla inválida. Use uma das seguintes:", ", ".join(ESTADOS))
        sys.exit(1)

    id_origem = SIGLA_PARA_ID[origem]
    id_destino = SIGLA_PARA_ID[destino]

    dfs = DepthFirstPaths(grafo, id_origem)
    bfs = BreadthFirstPaths(grafo, id_origem)

    print()
    print("-" * 60)

    # 1. Conectividade
    print(f"\n1) É possível ir de {origem} até {destino} por fronteiras terrestres?")
    if dfs.has_path_to(id_destino):
        print(f"   SIM, é possível ir de {origem} ({NOMES[origem]}) até {destino} ({NOMES[destino]}).")
    else:
        print(f"   NÃO, não é possível ir de {origem} até {destino}.")

    # 2. Caminho DFS
    print(f"\n2) Caminho encontrado pela DFS de {origem} até {destino}:")
    caminho_dfs = dfs.path_to(id_destino)
    if caminho_dfs:
        print(f"   {formatar_caminho(caminho_dfs)}")
    else:
        print("   Nenhum caminho encontrado.")

    # 3. Caminho BFS
    print(f"\n3) Caminho encontrado pela BFS de {origem} até {destino}:")
    caminho_bfs = bfs.path_to(id_destino)
    if caminho_bfs:
        print(f"   {formatar_caminho(caminho_bfs)}")
    else:
        print("   Nenhum caminho encontrado.")

    # 4. Estados alcançáveis
    print(f"\n4) Quantos estados são alcançáveis a partir de {origem}?")
    print(f"   {sum(1 for m in dfs.marked if m)} estado(s) alcançável(is) a partir de {origem}.")

    # 5. Ordem de visita DFS
    print(f"\n5) Ordem de visita da DFS a partir de {origem}:")
    print(f"   {formatar_ordem(ordem_visita_dfs(grafo, id_origem))}")

    # 6. Ordem de visita BFS
    print(f"\n6) Ordem de visita da BFS a partir de {origem}:")
    print(f"   {formatar_ordem(ordem_visita_bfs(grafo, id_origem))}")

    print()
    print("-" * 60)
    print("Fim da execução.")


if __name__ == "__main__":
    main()