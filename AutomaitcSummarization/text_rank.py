from graph import Graph, Vertex
from nltk.tokenize import sent_tokenize, word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
from priority_queue import PriorityQueue
import math
import codecs

# rank difference convergence threshold
delta = 0.00001
# conversion rate
gamma = 0.1
# damping factor
damp = 0.85

# params: file name
# returns: list of sentences in the file
def get_sentences(file_name):
    # open file
    f = codecs.open(file_name, encoding='utf-8')
    text = f.read()
    # get sentences as lists of words
    sentences = sent_tokenize(text)
    f.close()
    return sentences


# params: list of sentences
# returns: unconnected graph with vertices representing sentences
def initialize_graph(sentences):
    g = Graph()
    pos_counter = 0
    tokenizer = RegexpTokenizer(r'\w+')
    stop_words = set(stopwords.words('english'))
    for s in sentences:
        # transform sentence to list of words
        s = tokenizer.tokenize(s)
        # remove stop words
        words_filtered = []
        for w in s:
            if w not in stop_words:
                words_filtered.append(w)
        # create vertex in graph
        g.add_vertex(words_filtered, pos_counter)
        pos_counter += 1

    return g

# params: 2 sentences
# output: number of common words
def get_matching_words(s1, s2):
    return len(set(s1).intersection(s2))


# params: 2 vertices
# returns: numeric value representing the similarity between the sentences
# in the vertices
def similarity(v1, v2):
    return get_matching_words(v1.sentence, v2.sentence) / \
           (math.log2(2 + len(v1.sentence)) + math.log2(2 + len(v2.sentence)))


# params: unconnected graph
# returns: connected graph with an edge between each pair of sentences with common words
# edge is weighted using similarity function
def create_edges(graph):
    # for each vertex check all other vertices
    for p1, v1 in graph.vert_dict.items():
        for p2, v2 in graph.vert_dict.items():
            # skip same vertex
            if p1 <= p2: continue
            # get number of matching words
            matching = get_matching_words(v1.sentence, v2.sentence)
            # if there are matching words, add an egde
            if matching > 0:
                # add edge with cost = similarity
                graph.add_edge(v1, v2, 1 + similarity(v1, v2))
    return graph

# params: unconnected graph
# returns: connected graph with edge between each pair of sentences with common words
# and edges between sentences next to each other
def create_egdes_shortest_path(graph):
    max_distance = len(graph.vert_dict)
    # for each vertex check all other vertices
    for p1, v1 in graph.vert_dict.items():
        for p2, v2 in graph.vert_dict.items():
            # skip same vertex
            if p1 >= p2 or p2 - p1 > max_distance: continue
            # check if sentences is next sentence
            if p2 - p1 == 1:
                graph.add_edge(v1, v2, 1 + similarity(v1, v2))
            else:
                # get number of matching words
                matching = get_matching_words(v1.sentence, v2.sentence)
                # if there are matching words, add an egde
                if matching > 0:
                    # add edge with cost = similarity
                    graph.add_edge(v1, v2, 1 + similarity(v1, v2))
    return graph

# params: connected unranked graph
# returns: ranked graph
def weighted_page_rank(graph):
    # iterate ranking algorithm until convergence of all ranks
    done = False
    while not done:
        done = True
        # assign a new rank to each vertex
        for v1 in graph.vert_dict.values():
            old_rank = v1.rank
            total_rank = 0
            for v2, weight in v1.adjacent.items():
                total_rank += weight * v2.rank / sum(v2.adjacent.values())
            # check if convergence criteria is met for this vertex
            if abs(old_rank - total_rank) > delta:
                done = False
            v1.rank = total_rank

    return graph


# params: ranked graph
# returns: list of top ranked sentences
def extract_sentences(graph, original_sentences):
    v_list = list(graph.vert_dict.values())
    v_list.sort(key=lambda x: x.rank, reverse=True)
    number_to_extract = int(len(graph.vert_dict)*gamma)
    v_list = v_list[0:number_to_extract]
    v_list.sort(key=lambda x: x.position)
    sentences = list(original_sentences[v.position] for v in v_list)
    return sentences

# params: ranked graph
# returns: list of top ranked sentences connecting the first and the last sentence
def extract_sentences_ucs(graph, original_sentences):
    # uniform cost search
    pk = PriorityQueue()
    # (vertex, parent, accumulated cost)
    start = (graph.vert_dict[0], None, 0)
    end_position = len(graph.vert_dict) - 1
    pk.insert(start, start[2])
    visited = [start[0].position]
    current = None
    # finding path to last sentence
    while not pk.isEmpty():
        current = pk.pop().data
        visited.append(current[0].position)

        if current[0].position == end_position:
            break

        for v, weigth in current[0].adjacent.items():
            if v.position <= current[0].position:
                continue
            if v.position not in visited:
                cost = current[2] + abs(v.position - current[0].position)/(weigth * v.rank)
                pk.insert((v, current, cost), cost)

    # building path
    path = []
    while current is not None:
        path.append(current[0])
        current = current[1]

    path.reverse()
    sentences = list(original_sentences[v.position] for v in path)
    return sentences



# prints the extracted sentences as text
def print_summary(extracted_sentences):
    print('Number of sentences extracted: ' + str(len(extracted_sentences)))
    print('. '.join(extracted_sentences))


def text_rank_summ(file_name):
    original_sentences = get_sentences(file_name)
    g = initialize_graph(original_sentences)
    g = create_edges(g)
    g = weighted_page_rank(g)
    extracted_sentences = extract_sentences(g, original_sentences)
    return extracted_sentences


def text_rank_summ_ucs(file_name):
    original_sentences = get_sentences(file_name)
    g = initialize_graph(original_sentences)
    g = create_egdes_shortest_path(g)
    g = weighted_page_rank(g)
    extracted_sentences = extract_sentences_ucs(g, original_sentences)
    return extracted_sentences


if __name__ == '__main__':
    print("\n*** TEXT RANK ***")
    print_summary(text_rank_summ('test.txt'))
    print("\n*************************************************************************************************************\n*** TEXT RANK WITH UCS ***")
    print_summary(text_rank_summ_ucs('test.txt'))




