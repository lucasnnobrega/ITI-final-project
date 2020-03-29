# -*- coding: utf-8 -*-

from datetime import datetime
import os
import sys
import math
from io import StringIO
from chardet import detect
import BitVector

# get file encoding type


def get_encoding_type(file):
    with open(file, 'rb') as f:
        rawdata = f.read()
    return detect(rawdata)['encoding']


def decompress(compressed, k):
    """Decompress a list of output ks to a string."""

    # Build the dictionary.
    dict_size = 256
    dict_max_lenght = int(math.pow(2, k))
    dictionary = dict((i, chr(i)) for i in range(dict_size))
    # in Python 3: dictionary = {i: chr(i) for i in range(dict_size)}

    w = chr(compressed.pop(0))
    result = []
    # Converte w para ascii e coloca no resultado
    result.append(ord(w))
    # dicionario foi resetado flag (janela)
    dictReseted = False
    compressed_iter = iter(compressed)

    for k in compressed_iter:

        # Se o dicionario foi resetado
        if dictReseted:
            w = chr(k)
            result.append(ord(w))
            dictReseted = False
            continue

        # Se k estiver no dicionario
        if k in dictionary:
            entry = dictionary[k]
        # Se nao estiver no dicionario
        elif k == dict_size:
            entry = w + w[0]
        else:
            raise ValueError('Bad compressed k: %s' % k)

        for item in entry:
            result.append(ord(item))

        dictionary[dict_size] = w + entry[0]
        dict_size += 1
        w = entry

        # Resetando dicionario para implementar a janela deslizante
        if len(dictionary) == dict_max_lenght:
            dict_size = 256
            entry = ""
            dictionary.clear()
            dictReseted = True
            dictionary = dict((i, chr(i)) for i in range(dict_size))
    return result


def Descomprimir(folder, k):
    if not os.path.exists(folder):
        print("Pasta Não Existe")
        sys.exit()

    comprmFile = f'{folder}/out_bl{k}.bin'
    attrFile = f'{folder}/comprm_bl{k}.attr'

    if not os.path.exists(attrFile):
        print("Arquivo de Atributos Não Encontrado")
        sys.exit()
    if not os.path.exists(comprmFile):
        print("Arquivo Comprimido Não Encontrado")
        sys.exit()
    print("Obtendo Atributos")
    pad = ''
    fileExt = ""
    with open(attrFile, 'r') as f:
        pad = f.readline()
        pad = int(pad.replace("\n", ""))
        fileExt = f.readline()
        fileExt = fileExt.replace("\n", "")
        kLenght = f.readline()
        k = int(kLenght.replace("\n", ""))
    print("Começando Para " + folder + "." +
          fileExt + " Com K igual " + str(k))

    print("Lendo Arquivo de Compressão")
    fp_read = StringIO()
    bitVector_instance = BitVector.BitVector(filename=comprmFile)
    while(bitVector_instance.more_to_read):
        bitVector_instance_read = bitVector_instance.read_bits_from_file(8)
        bitVector_instance_read.write_bits_to_fileobject(fp_read)

    print("Retirando o pad")
    bitVector_instance = BitVector.BitVector(bitstring=fp_read.getvalue())

    # Se pad for diferente de zero
    if pad != 0:
        # Remova do final do vetor de bits os bits inuteis necessarios para
        # criar o arquivo com o padrao correto
        bitsInString = str(bitVector_instance)[:-pad]
    else:
        bitsInString = str(bitVector_instance)
    # time.sleep(10000)
    print("Obtendo Conjunto de Bits")
    bytesData = [bitsInString[i:i+k] for i in range(0, len(bitsInString), k)]
    # wrap(bitsInString, K)
    result = []

    print("Convertendo Bits para Dec")
    for item in bytesData:
        bitVector_instance = BitVector.BitVector(bitstring=item)
        result.append(bitVector_instance.int_val())

    print("Descomprimindo")
    desResult = decompress(result, k)
    desFileName = f"{folder}/{folder}_bl{k}.{fileExt}"

    print("Salvando Resultado")
    if 'txt' in fileExt:
        with open(desFileName, 'wb') as f:
            for c in desResult:
                f.write(c.to_bytes(1, 'little'))

    if 'mp4' in fileExt:
        with open(desFileName, 'wb') as f:
            for c in desResult:
                f.write(c.to_bytes(1, 'little'))

    if 'pgm' in fileExt:
        with open(desFileName, 'wb') as f:
            for c in desResult:
                f.write(c.to_bytes(1, 'little'))


def main(fileName, k):
    print("Iniciando Processo de Descompressão")
    Descomprimir(fileName.split('.')[0], k)
    return 0


if __name__ == "__main__":
    main("smallCorpus.txt", 9)
