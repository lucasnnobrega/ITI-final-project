# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 14:34:05 2020

 

@author: aerci
"""

 

import random
import copy
import time

 

ascii_table = {} ### DICIONARIO

 

################ CRIANDO DICIONARIO INICIAL UM PARA AS 40 IMGAENS

for i in range(256):
    ascii_table[i] = bytes([ord(chr(i))])

 

dicionario = [copy.deepcopy(ascii_table) for _ in range(40)]
state = 0

 
#######  ABRINDO IMAGENS

def openImages():
    images= []
    for i in range(1,41):
        imagesTemp = []
        for j in range(1,11):
            with open("d:/Documentos/UFPB/P8/iti/proj final/orl_faces/s"+str(i)+"/"+str(j)+".pgm", "rb") as binary_file:
                    imagesTemp.append(bytearray(binary_file.read()))
        images.append(imagesTemp)   
        
    return images



###   BUSCAR ELEMENTO NO DICIONARIO    

def getKeysByValue(dictOfElements, valueToFind):    
    listOfItems = dictOfElements.items()
    for item  in listOfItems:
        if item[1] == valueToFind:
            return item[0]
    return  -1


###   DIVIDINDO ENTRE TREINO E TESTE
    
def divisao(images):
    treino = []
    testes = []

 

    for i in range(len(images)):
        index = random.choice(range(len(images[i])))
        treino.append(images[i].pop(index))
        testes.append(i)
    
    return treino, testes

 

###### TREINANDO IMAGENS
def treinarImagens(imagesTrain, i):
        state = 0   
        print("Treino K = "+ str(i))

 

        for category in range(len(imagesTrain)):
            print("Treinamento Pessoa :" +str(category+1))
            for person in range(len(imagesTrain[category])):
                Compressor(imagesTrain[category][person], i, dicionario[category])

 


###### FAZENDO A "CLASSIFICAÇÃO" DAS IMAGENS
                
def predict(images, label, k):        
    state = 1 
    
    predictions = []

 

    for person in range(len(images)):
        compressionRates = []
        print("Predict pessoa:"+str(person+1))
        for category in range(len(dicionario)):
            compressionRates.append(Compressor(images[person], k, dicionario[category]))                
        
        predictions.append(compressionRates.index(sorted(compressionRates)[0]))

 

    count = 0
    for i in range(len(label)):
        if label[i] == predictions[i]:
            count += 1    
    print("Acertou "+ str(count*100/len(label)) + "%" + " com K = " + str(k))

 

#############################################  COMPRESSOR    ##################################

 

def Compressor(image, K ,asciis_table):
    MAX = 2**K
    table_size = len(asciis_table)
    
    indice = []
    
    
    primeiro = True
    
    for pixel in image:
        if(primeiro):
            byte = bytes([ord(chr(pixel))])
            s = b''
    
        #VERIFICA SE O BYTE ANTERIOR + O BYTE ATUAL ESTÁ NO DICIONÁRIO
        index = getKeysByValue(asciis_table,s+byte)
        
        #SE SIM, ELE IRÁ SOMAR OS DOIS BYTES E LER UM NOVO BYTE
        if index != -1:
            s += byte
        #CASO CONTRÁRIO, ELE CODIFICA O BYTE ANTERIOR PARA A SAÍDA
        else:
            indice.append(getKeysByValue(asciis_table,s))
            #E SALVA O BYTE ANTERIOR + O BYTE ATUAL NO DICIONÁRIO, CASO O TAMANHO DO DICIONÁRIO PERMITA
            if table_size < MAX and state == 0:
                asciis_table[table_size] = s + byte
                table_size += 1
            #ATUALIZA O BYTE ANTERIOR COM O BYTE ATUAL
            s = byte
            
        byte = bytes([ord(chr(pixel))])
        
        primeiro = False
    
    return len(indice)
        

 

def main():
    for i in range(16,17):
        start_time = time.time()
        print("Carregar Imagens")
        images = openImages()
        train = copy.deepcopy(images)
        print("Dividir entre Treino e Teste")
        test, label = divisao(train)
        print("Treinar Modelo")
        treinarImagens(train, i)
        print("Prever Categoria de Imagens")
        predict(test,label,i)
        print("Fim")
        print("---K = "+str(i)+" %s segundos ---" % (time.time() - start_time))
    
    
if __name__ =="__main__":
    main()