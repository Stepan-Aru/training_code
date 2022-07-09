from math import inf


class Vertex:
    def __init__(self):
        self._links = []

    @property
    def links(self):
        return self._links

    def add_link(self, link):
        if len(list(
                filter(lambda x: x._v1 in (link._v1, link._v2) and x._v2 in (link._v1, link._v2), self._links))) == 0:
            self._links.append(link)

    @property
    def linked_v(self):
        res = []
        for link in self.links:
            v = link.v1 if link.v1 != self else link.v2
            res.append((v, link._dist))
        return res


class Link:
    def __init__(self, v1, v2):
        self._v1 = v1
        self._v2 = v2
        self._dist = 1

    @property
    def v1(self):
        return self._v1

    @v1.setter
    def v1(self, val):
        self._v1 = val

    @property
    def v2(self):
        return self._v2

    @v2.setter
    def v2(self, val):
        self._v2 = val

    @property
    def dist(self):
        return self._dist

    @dist.setter
    def dist(self, val):
        self._dist = val


class LinkedGraph:
    def __init__(self):
        self._links = []
        self._vertex = []

    def add_vertex(self, v):
        if v not in self._vertex:
            self._vertex.append(v)

    def add_link(self, link):
        if len(list(
                filter(lambda x: x.v1 in (link.v1, link.v2) and x.v2 in (link.v1, link.v2), self._links))) == 0:
            self._links.append(link)
            for v in (link.v1, link.v2):
                self.add_vertex(v)
                v.add_link(link)

    def get_links(self, path):
        res = []
        for i in range(len(path) - 1):
            for link in self._links:
                if path[i] in (link.v1, link.v2) and path[i + 1] in (link.v1, link.v2):
                    res.append(link)
        return res

    def find_path(self, start_v, stop_v):
        vertex_lst = self._vertex
        vertex_lst[0], vertex_lst[vertex_lst.index(start_v)] = vertex_lst[vertex_lst.index(start_v)], vertex_lst[0]
        vertex_dict = {key: val for key, val in enumerate(self._vertex)}

        def arg_min(T, S):
            amin = -1
            m = inf  # максимальное значение
            for i, t in enumerate(T):
                if t < m and i not in S:
                    m = t
                    amin = i

            return amin

        N = len(vertex_lst)  # число вершин в графе
        D = [[inf for _ in range(N)] for _ in range(N)]
        for key, vert in vertex_dict.items():
            D[key][key] = 0
            for v in vert.linked_v:
                D[key][vertex_lst.index(v[0])] = v[1]

        T = [inf] * N
        S = {0}  # просмотренные вершины
        v = 0
        T[v] = 0
        M = [0] * N

        while len(S) < N:
            for j, dw in enumerate(D[v]):
                if self._vertex[j] not in S:  # если вершина еще не просмотрена
                    w = T[v] + dw
                    if w < T[j]:
                        T[j] = w
                        M[j] = v

            v = arg_min(T, S)
            if v >= 0:
                S.add(v)

        start = self._vertex.index(start_v)
        end = self._vertex.index(stop_v)
        P = [end]
        while end != start:
            end = M[P[-1]]
            P.append(end)
        P.reverse()
        res_path = [self._vertex[i] for i in P]
        return res_path, self.get_links(res_path)


class Station(Vertex):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class LinkMetro(Link):
    def __init__(self, v1, v2, dist):
        super().__init__(v1, v2)
        self._dist = dist

    def __str__(self):
        return f'{self.v1} - {self.v2}'

    def __repr__(self):
        return f'{self.v1} - {self.v2}'


map_metro = LinkedGraph()
v1 = Station("Сретенский бульвар")
v2 = Station("Тургеневская")
v3 = Station("Чистые пруды")
v4 = Station("Лубянка")
v5 = Station("Кузнецкий мост")
v6 = Station("Китай-город 1")
v7 = Station("Китай-город 2")

map_metro.add_link(LinkMetro(v1, v2, 1))
map_metro.add_link(LinkMetro(v2, v3, 1))
map_metro.add_link(LinkMetro(v1, v3, 1))

map_metro.add_link(LinkMetro(v4, v5, 1))
map_metro.add_link(LinkMetro(v6, v7, 1))

map_metro.add_link(LinkMetro(v2, v7, 5))
map_metro.add_link(LinkMetro(v3, v4, 3))
map_metro.add_link(LinkMetro(v5, v6, 3))


path = map_metro.find_path(v1, v6)  # от сретенского бульвара до китай-город 1
print(path)
