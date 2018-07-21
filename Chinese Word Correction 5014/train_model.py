#trainning CBOW model based on corpus
import re

seg_text_name='data/wiki_seg.txt'

lines=[]
with open(seg_text_name,'r') as f:
    for line in f:
        lines.append(line.strip().split())
        

def filterEnglish(x):
    if re.match("[a-zA-Z0-9|]+",x):
        return False
    else:
        return True
        
def delEnglish(sentences):
    for i,line in enumerate(sentences):
        line=[x for x in line if filterEnglish(x)]
        sentences[i]=line[:]
    return sentences

sentences=delEnglish(lines)


from gensim.models import word2vec                 

model = word2vec.Word2Vec(sentences,sg=0,size=100,window=5,hs=1,min_count=5,max_vocab_size=None,workers=4) 

model.save('model/my.model')