class NounVertex:
    def __init__(self, noun):
        self.noun = noun
        self.rank = 0
        self.adjacent = {} # key = vertex, value = weight

    def __str__(self):
        return str(self.noun) + ' adjacent: ' + str([x.id for x in self.adjacent])

    def add_neighbor(self, neighbor, weight=0):
        if neighbor.noun in self.adjacent.keys():
            self.adjacent[neighbor] += weight
        else:
            self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent.keys()

    def get_noun(self):
        return self.noun

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

class NounGraph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0


    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, noun):
        self.num_vertices = self.num_vertices + 1
        new_vertex = NounVertex(noun)
        self.vert_dict[noun] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_edge(self, frm, to, weight=0):
        self.vert_dict[frm].add_neighbor(self.vert_dict[to], weight)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], weight)

    def get_vertices(self):
        return self.vert_dict.keys()
