import heapq # импортирую для работ с кучами


from typing import List, Tuple

class Vertex:
    _id_counter: int = 0

    def __init__(self) -> None:
        self._links = []  # список связей с другими вершинами
        self.id: int = Vertex._id_counter
        Vertex._id_counter += 1

    @property
    def links(self) -> List:
        return self._links

    def __lt__(self, other: "Vertex") -> bool:
        return self.id < other.id  # сравнение по уникальному id


class Link:
    def __init__(self, v1: Vertex, v2: Vertex, dist: int = 1) -> None:
        self._v1: Vertex = v1
        self._v2: Vertex = v2
        self._dist: int = dist  # длина связи

    @property
    def v1(self) -> Vertex:
        return self._v1

    @property
    def v2(self) -> Vertex:
        return self._v2

    @property
    def dist(self) -> int:
        return self._dist

    @dist.setter
    def dist(self, value: int) -> None:
        self._dist = value


class LinkedGraph:
    def __init__(self) -> None:
        self._links: List[Link] = []  # список связей
        self._vertex: List[Vertex] = []  # список вершин

    def add_vertex(self, v: Vertex) -> None:
        if v not in self._vertex:
            self._vertex.append(v)

    def add_link(self, link: Link) -> None:
        # проверяем наличие связи (v1, v2) или (v2, v1)
        if not any(
            (link.v1 == l.v1 and link.v2 == l.v2)
            or (link.v1 == l.v2 and link.v2 == l.v1)
            for l in self._links
        ):
            self._links.append(link)
            # автоматически добавляем вершины связи, если их нет в списке _vertex
            self.add_vertex(link.v1)
            self.add_vertex(link.v2)

    def find_path(
        self, start_v: Vertex, stop_v: Vertex
    ) -> Tuple[List[Vertex], List[Link]]:
        # реализация алгоритма Дейкстры для поиска кратчайшего пути

        # 1) инициализация
        distances = {
            v: float("inf") for v in self._vertex
        }  # словарь где ключи - вершины графа, а значения - бесконечность (нужно по алгоритму)
        distances[start_v] = 0  # изначальное расстояние(0)
        previous_vertices = {
            v: None for v in self._vertex
        }  # хранит предшествующие вершины для восстановления пути (пригодится по алгоритму)

        # 2) очередь с приоритетами для вершин
        priority_queue = [
            (0, start_v)
        ]  # используется для извлечения вершины с минимальным расстоянием
        heapq.heapify(priority_queue)  # преобразуем список в кучу

        # 3) основной цикл
        # извлекается вершина с минимальным расстоянием
        while priority_queue:
            current_distance, current_vertex = heapq.heappop(
                priority_queue
            )  # это функция, которая извлекает и возвращает наименьший элемент из кучи heap
            # если текущее расстояние больше, чем уже найденное, пропускаем
            if current_distance > distances[current_vertex]:
                continue

            # 4) обработка соседних вершин
            for link in self._links:
                if link.v1 == current_vertex:
                    neighbor = link.v2
                elif link.v2 == current_vertex:
                    neighbor = link.v1
                else:
                    continue

                new_distance = distances[current_vertex] + link.dist

                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous_vertices[neighbor] = current_vertex
                    heapq.heappush(priority_queue, (new_distance, neighbor))

        # 5) восстановление пути
        path = []
        current_vertex = stop_v
        while current_vertex is not None:
            path.append(current_vertex)
            current_vertex = previous_vertices[current_vertex]
        path = path[::-1]

        # 6) сбор связей этого пути
        path_links = []
        for i in range(len(path) - 1):
            v1 = path[i]
            v2 = path[i + 1]
            for link in self._links:
                if (link.v1 == v1 and link.v2 == v2) or (
                    link.v1 == v2 and link.v2 == v1
                ):
                    path_links.append(link)
                    break

        return path, path_links


class Station(Vertex):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name: str = name

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name


class LinkMetro(Link):
    def __init__(self, v1: Vertex, v2: Vertex, dist: int) -> None:
        super().__init__(v1, v2)
        self._dist: int = dist

    @property
    def dist(self) -> int:
        return self._dist

    @dist.setter
    def dist(self, value: int) -> None:
        self._dist = value


# проверка
map2 = LinkedGraph()
v1 = Vertex()
v2 = Vertex()
v3 = Vertex()
v4 = Vertex()
v5 = Vertex()
map2.add_link(Link(v1, v2))
map2.add_link(Link(v2, v3))
map2.add_link(Link(v2, v4))
map2.add_link(Link(v3, v4))
map2.add_link(Link(v4, v5))
assert len(map2._links) == 5, "неверное число связей в списке _links класса LinkedGraph"
assert len(map2._vertex) == 5, "неверное число вершин в списке _vertex класса LinkedGraph"
map2.add_link(Link(v2, v1))
assert len(map2._links) == 5, "метод add_link() добавил связь Link(v2, v1), хотя уже имеется связь Link(v1, v2)"
path = map2.find_path(v1, v5)
s = sum([x.dist for x in path[1]])
assert s == 3, "неверная суммарная длина маршрута, возможно, некорректно работает объект-свойство dist"
assert issubclass(Station, Vertex) and issubclass(LinkMetro, Link), "класс Station должен наследоваться от класса Vertex, а класс LinkMetro от класса Link"
map2 = LinkedGraph()
v1 = Station("1")
v2 = Station("2")
v3 = Station("3")
v4 = Station("4")
v5 = Station("5")
map2.add_link(LinkMetro(v1, v2, 1))
map2.add_link(LinkMetro(v2, v3, 2))
map2.add_link(LinkMetro(v2, v4, 7))
map2.add_link(LinkMetro(v3, v4, 3))
map2.add_link(LinkMetro(v4, v5, 1))
assert len(map2._links) == 5, "неверное число связей в списке _links класса LinkedGraph"
assert len(map2._vertex) == 5, "неверное число вершин в списке _vertex класса LinkedGraph"
path = map2.find_path(v1, v5)
assert str(path[0]) == '[1, 2, 3, 4, 5]', path[0]
s = sum([x.dist for x in path[1]])
assert s == 7, "неверная суммарная длина маршрута для карты метро"
