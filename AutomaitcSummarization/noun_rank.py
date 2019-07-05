from noun_graph import NounGraph
from nltk.tokenize import sent_tokenize, word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
import nltk
import math
import codecs

import spacy
import neuralcoref

# conversion rate
gamma = 0.1

# noun rank damping rate
damp = 0.9

noun_tags = ['NN', 'NNS', 'NNP', 'NNPS']
nlp = spacy.load('en')
neuralcoref.add_to_pipe(nlp)

def get_sentences(file_name):
    # open file
    f = codecs.open(file_name, encoding='utf-8')
    text = f.read()
    # get sentences as lists of words
    sentences = sent_tokenize(text)
    f.close()
    return sentences


# params: list of sentences
# returns: list of sentences with pronouns replaced with corresponding nouns
def resolve_pronouns(sentences):
    resolved = []
    for sentence in sentences:
        resolved.append(nlp(sentence)._.coref_resolved)
    return resolved


# params: list of sentences
# returns: list of sentences represented as a list of tagged words
# tagged word is a tuple (word, tag)
def tag_sentences(sentences):
    tagged = []
    stop_words = set(stopwords.words('english'))
    tokenizer = RegexpTokenizer(r'\w+')
    for sentence in sentences:
        tokens = tokenizer.tokenize(sentence)
        # remove stop words
        filtered_tokens = []
        for word in tokens:
            if word not in stop_words:
                filtered_tokens.append(word)
        tagged.append(nltk.pos_tag(filtered_tokens))
    return tagged


# params: list of tagged words (tuples)
# returns: connected weighted graph
def build_graph(sentences):
    g = NounGraph()
    for sentence in sentences:
        # keep a dictionary of key=position and value=noun for each noun we encountered in the sentence
        previous_nouns = {}
        word_counter = 0
        for word in sentence:
            # check if word is noun
            if word[1] not in noun_tags:
                continue
            # add the noun as a vertex if it doesn't exist
            if word[0] not in g.vert_dict.keys():
                g.add_vertex(word[0])
            # add edge between current noun and each previous noun
            for position, noun in previous_nouns.items():
                # don't add an edge to the noun itself (if there are multiple instances of the noun in the sentence)
                if noun == word[0]:
                    continue
                # weight is in reverse proportion to the distance between the nouns in the sentence
                g.add_edge(word[0], noun, 1/(word_counter - position))
            previous_nouns[word_counter] = word[0]
            word_counter += 1
    return g

# params: connected, weighted graph
# returns:
def extract_sentences(graph, tagged_sentences, original_sentences):
    # rank nouns
    for noun in graph.vert_dict.values():
        noun.rank = sum(noun.adjacent.values())

    # iterate over both sentence lists to get ranked sentences
    # list contains indexes of best ranked sentences
    ranked_senteces = []
    number_to_extract = int(len(original_sentences)*gamma)
    # repeat process of finding best rank sentence until desired number of sentences is extracted
    for i in range(number_to_extract):
        max_rank = 0
        best_sentence_index = 0
        for j in range(len(original_sentences)):
            # skip already ranked sentences
            if j in ranked_senteces:
                continue
            # calculate sentence rank
            sentence_rank = 0
            for word in tagged_sentences[j]:
                if word[1] in noun_tags:
                    sentence_rank += graph.vert_dict[word[0]].rank
            # take into account that longer sentences will have more nouns
            sentence_rank /= max(1, math.log2(1 + len(tagged_sentences[j])))
            # keep track of best ranked sentence
            if sentence_rank > max_rank:
                max_rank = sentence_rank
                best_sentence_index = j
        # add the best ranked sentence to extracted sentences
        ranked_senteces.append(best_sentence_index)
        # reduce the value of nouns in the extracted sentence by damp factor
        for word in tagged_sentences[best_sentence_index]:
            if word[1] in noun_tags:
                graph.vert_dict[word[0]].rank *= damp


    # sort sentences by position
    ranked_senteces.sort()

    # return only the original text of extracted sentences
    return list(original_sentences[idx] for idx in ranked_senteces)


# prints the extracted sentences as text
def print_summary(extracted_sentences):
    print('Number of sentences extracted: ' + str(len(extracted_sentences)))
    print('. '.join(extracted_sentences))


def noun_rank_summ(file_name):

    original_sentences = get_sentences(file_name)
    resovled_sentences = resolve_pronouns(original_sentences)
    tagged_sentences = tag_sentences(resovled_sentences)
    graph = build_graph(tagged_sentences)
    extracted_senteces = extract_sentences(graph, tagged_sentences, original_sentences)
    return extracted_senteces

if __name__ == '__main__':
    print_summary(noun_rank_summ('test.txt'))

