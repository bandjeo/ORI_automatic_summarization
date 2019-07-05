import os
import codecs

directory_path = 'data'

def process_file(file_name):
    f = codecs.open(file_name, encoding='utf-8')
    text = f.read()
    articles = text.split('[[')[1:]
    for article in articles:
        try:
            article_name, article_text = article.split(']]')
            af = codecs.open(directory_path + '\\articles\\' + article_name + '.txt', 'w', "utf-8-sig")
            af.write(article_text)
            af.close()
        except:
            continue
    f.close()



if __name__ == '__main__':
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            process_file(directory_path + '\\' + filename)