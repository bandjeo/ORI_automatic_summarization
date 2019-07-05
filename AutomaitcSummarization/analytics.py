from noun_rank import noun_rank_summ
from text_rank import text_rank_summ, print_summary, text_rank_summ_ucs
from nltk import RegexpTokenizer
import os
import time
import codecs

def count_vocabulary(sentences):
    tokenizer = RegexpTokenizer(r'\w+')
    return len(set(tokenizer.tokenize(' '.join(sentences))))

def file_vocab_size(file_name):
    f = codecs.open(file_name,  encoding='utf-8')
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(f.read())
    return len(set(tokens))

def analyze_method(method):
    total_time = 0
    file_counter = 0
    total_extracted = 0
    total_vocab = 0
    for file_name in os.listdir('data\\articles'):
        if file_name.endswith('.txt'):
            start_time = time.time()
            extracted = method('data\\articles\\' + file_name)
            end_time = time.time()
            timedelta = end_time - start_time
            total_time += timedelta
            file_counter += 1
            total_extracted += len(extracted)
            vocab = count_vocabulary(extracted)/file_vocab_size('data\\articles\\' + file_name)
            total_vocab += vocab

            print("File: " + file_name + " summarized in " + str(timedelta) +
                  ";  number of sentences: " + str(len(extracted)) + ";  vocabulary retained: " + str(vocab * 100) + "%")


    avg_time = total_time/file_counter
    avg_extracted = total_extracted/file_counter
    avg_vocab = total_vocab/file_counter
    return avg_time, avg_extracted, avg_vocab



if __name__ == '__main__':
    print("***TEXT RANK***")
    text_rank_results = analyze_method(text_rank_summ)
    print("\n\n***TEXT RANK UCS***")
    text_rank_ucs_results = analyze_method(text_rank_summ_ucs)
    print("\n\n***NOUN RANK***")
    noun_rank_results = analyze_method(noun_rank_summ)


    print("\n\n")
    format_text = "{:20}|{:20}|{:40}|{:35}"

    print(format_text.format('Method', ' Average Time [s]',
                        ' Average Number of extracted sentences', ' Average fraction of vocabulary'))
    print("="*130)

    print(format_text.format('Text Rank', text_rank_results[0],
                              text_rank_results[1], text_rank_results[2]))

    print(format_text.format('Text Rank UCS', text_rank_ucs_results[0],
                              text_rank_ucs_results[1], text_rank_ucs_results[2]))

    print(format_text.format('Noun Rank', noun_rank_results[0],
                              noun_rank_results[1], noun_rank_results[2]))




