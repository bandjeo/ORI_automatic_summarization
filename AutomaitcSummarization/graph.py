class Vertex:
    def __init__(self, sentence, position):
        self.sentence = sentence
        self.position = position
        self.rank = 100
        self.adjacent = {} # key = vertex, value = weight

    def __str__(self):
        return str(self.position) + ' adjacent: ' + str([x.id for x in self.adjacent])

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent.keys()

    def get_position(self):
        return self.position

    def get_sentence(self):
        return self.sentence

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, sentence, position):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(sentence, position)
        self.vert_dict[position] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_edge(self, frm, to, weight=0):
        self.vert_dict[frm.position].add_neighbor(self.vert_dict[to.position], weight)
        self.vert_dict[to.position].add_neighbor(self.vert_dict[frm.position], weight)

    def get_vertices(self):
        return self.vert_dict.keys()
