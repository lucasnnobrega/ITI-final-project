from datetime import datetime
import math
import os
import sys
from chardet import detect
import BitVector
from io import StringIO
from constantes import *

# get file encoding type


def get_encoding_type(file):
    with open(file, 'rb') as f:
        rawdata = f.read()
    return detect(rawdata)['encoding']


def calculateNumberOfPads(numberOfBits):
    numberOfBytes = numberOfBits / 8.0
    idealNumberOfBytes = (math.ceil(numberOfBytes/1.0) * 8)
    pad = (idealNumberOfBytes - numberOfBits)
    # print(pad)
    return pad


def getBestFormat(size):
    bytesFormats = {'B': 1, 'H': 2, 'I': 4, 'Q': 8}

    exponencialInt = math.ceil(math.log2(size)/1.0)

    numberOfBytes = math.ceil((exponencialInt/8.0)/1.0)

    for key in bytesFormats:
        if (numberOfBytes <= bytesFormats[key]):
            # print(key)
            return key, bytesFormats[key]


def Comprimir(fileName, k=9):
    if not os.path.exists(fileName):
        print(RED, "Arquivo Não Existe", RESET)
        sys.exit()

    data = open(fileName, 'rb').read()

    # time.sleep(10)
    resultComprm, size, txt = compress(data, k)

    print("Compressão Finalizada \nCriando Arquvios")
    createComprmFiles(resultComprm, size, fileName, k)


def createComprmFiles(comprm, size, fileName, k):
    formatB, value = getBestFormat(size)
    folderName = fileName.split(".")[0]
    fileExt = fileName.split(".")[1]

    if not os.path.exists(folderName):
        os.mkdir(folderName)

    print("Convertendo dec Para Bin")
    fp_write = StringIO()

    numberOfBits = 0
    for b in comprm:
        numberOfBits += k
        bv = BitVector.BitVector(intVal=b, size=k)
        bv.write_bits_to_fileobject(fp_write)
    print('Conversão Finalizada')

    print('Construindo Vetor de Bits')
    bv = BitVector.BitVector(bitstring=fp_write.getvalue())
    print('Construção Finalizada')

    print("Calculando Numero de Pads")
    pad = calculateNumberOfPads(numberOfBits)

    print("Adicionando Pads")
    bv.pad_from_right(pad)

    print("Escrevendo Bits Em Disco")
    with open(f"{folderName}/out_bl{k}.bin", 'wb') as f:
        bv.write_to_file(f)
        f.close()

    print("Escrevendo Atributos Necessários para Descompressão")
    with open(f"{folderName}/comprm_bl{k}.attr", 'w') as f:
        f.write(str(pad) + "\n" + fileExt + "\n" + str(k) + "\n")
        f.close()


def compress(uncompressed, k=9):

    if k < 9:
        print("K Inválido")
        sys.exit()

    # Tamanho inicial do dicionario
    dict_size = 256
    # Tamanho maximo do dicionario, com base no parametro K
    dict_max_lenght = int(math.pow(2, k))
    # Construindo o dicionario {"simbolo": index}
    dictionary = {chr(i): i for i in range(dict_size)}

    w = ""
    result = []

    for c in uncompressed:
        # Adicione um novo caractere a w
        new_string = w + chr(c)
        # Se new_string ja esta no dicionario, entao aumente o tamanho de new_string
        if new_string in dictionary:
            # colocando o valor em w para aumentar a quantidade de simbolos
            w = new_string
        # Se nao tiver, precisa adicionar pois esse simbolo sera usado
        else:
            # Adicione no final do result o valor de w para formar o arquivo final
            result.append(dictionary[w])

            # Adicionar a new_string ao dicionario, com valor = dict_size
            dictionary[new_string] = dict_size
            # Incrementar o valor do dicionario para que o prox a ser inserido tenha valor diferente
            dict_size += 1

            # Converter o valor encontrado para char
            w = chr(c)

            # Resetando a Janela deslizante, que eh equivalente ao comprimento do dicionario(2**K)
            if len(dictionary) == dict_max_lenght:
                # Reseta o dicionario
                dict_size = 256
                # se w estiver com algo, entao adicione no dicionario
                if w:
                    result.append(dictionary[w])
                w = ""
                # Limpe o dicionario
                dictionary.clear()
                # Reconstruindo o dicionario com as entradas padroes
                dictionary = {chr(i): i for i in range(dict_size)}

    # Verificando se nao restou nada no w
    if w:
        result.append(dictionary[w])

    return result, dict_max_lenght, uncompressed


def main(fileName, k=9):
    print('Começando a Compressão')
    #fileName = 'smallCorpus.txt'
    print("Começando Para " + fileName + " Com K igual " + str(k))
    Comprimir(fileName, k)
    print('Concluido')
    return 0


if __name__ == "__main__":
    main(9)
