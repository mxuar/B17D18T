# !/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import pinyin
import jieba
import string
import re
import re
from gensim.models import word2vec 
import jieba

model=word2vec.Word2Vec.load('model/old_data1.model')
PUNCTUATION_LIST = string.punctuation
PUNCTUATION_LIST += "。，？：；｛｝［］‘“”《》／！％……（）"

vocab=model.wv.vocab

cn_dict=[]
with open('data/cn_dict.txt') as f:
    for word in f:
        cn_dict.append(word.strip())

        
def getCandidate(phrase,index,sentence_cut):
    
    start=max(index-3,0)
    end=min(index+3,len(sentence_cut))
    
    
    splits     = [(phrase[:i], phrase[i:])  for i in range(len(phrase) + 1)]
    #deletes    = [L + R[1:]                 for L, R in splits if R]
    deletes=[]
    transposes = [L + R[1] + R[0] + R[2:]   for L, R in splits if len(R)>1]
    
    replaces=[]
    candidates=[]
    py_phrase=pinyin.get(phrase,delimiter='', format='strip')
    for i,item in enumerate(list(phrase)):
        for word in vocab.keys():
            if item in list(word):
                py_word=pinyin.get(word,delimiter='', format='strip')
                if edit(py_phrase,py_word)<2:
                    replaces.append(word)
        

    inserts    = [L + c + R for L, R in splits for c in cn_dict]
    
    candidates=set(deletes + transposes + replaces + inserts)
    
    candidates=[x for x in candidates if x in vocab]
    
    scores={}
    for can_item in candidates:
        scores.update({can_item:0})
    sum_count=0
    for item in candidates:
        #print(item,vocab[item].count)
        sum_count+=vocab[item].count
    for item in candidates:
        scores[item]=vocab[item].count/sum_count*5
    
    for can in candidates:
        sentence_cut[index]=can
        score=model.score([sentence_cut[start:end]])
        if edit(py_phrase,pinyin.get(can,delimiter='', format='strip'))==0:
            scores[can]+=5
        scores[can]+=score
        
    max_word=''
    max_score=-900
    for k,v in scores.items():
        if (v>max_score):
            max_score=v
            max_word=k
    #print(candidates)
    return candidates,max_word


def edit(str1, str2):
    
    matrix = [[i+j for j in range(len(str2) + 1)] for i in range(len(str1) + 1)]


    for i in range(1,len(str1)+1):
        for j in range(1,len(str2)+1):
            if str1[i-1] == str2[j-1]:
                d = 0
            else:
                d = 1
            matrix[i][j] = min(matrix[i-1][j]+1,matrix[i][j-1]+1,matrix[i-1][j-1]+d)


    return matrix[len(str1)][len(str2)]
  

def corrector(error_sentence):
    jieba_cut = jieba.cut( error_sentence, cut_all=False)
    seg_list = " ".join(jieba_cut).split(' ')

    corrected_sentence = ""


    for index,phrase in enumerate(seg_list):
        if phrase not in PUNCTUATION_LIST:
            if phrase not in vocab or vocab[phrase].count<100:
                can,word = getCandidate(phrase,index,seg_list)
                seg_list[index]=word
#             elif vocab[phrase].count<10:
#                 can,word = getCandidate(phrase,index,seg_list)
#                 seg_list[index]=word        

    return ''.join(seg_list)



def main():

    err2 = ('杭洲是浙江的城市')
    correct_sent = corrector( err2 )
    print( "original sentence:" + err2  + "\ncorrected sentence:" + correct_sent)
    print('')
    err3 = ('这历到底是人间天棠还是地狱！')
    correct_sent = corrector( err3 )
    print( "original sentence:" + err3  + "\ncorrected sentence:" + correct_sent)
    print('')
    err9 = ('机奇学习！')
    correct_sent = corrector( err9 )
    print( "original sentence:" + err9  + "\ncorrected sentence:" + correct_sent)
    
    

    
    
if __name__=="__main__":
    main()

