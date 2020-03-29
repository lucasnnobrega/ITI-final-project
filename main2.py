import compressor
import descompressor
import argparse
from constantes import *


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Código para cadeira de ITI')
    parser.add_argument(
        'mode', type=str, help='Modo da função main: "encoder" para codificar;\
                                 "decoder" para decodificar.')
    parser.add_argument(
        'input_file_name', type=str, help='Nome do arquivo')

    parser.add_argument(
        'bit_length', type=str, choices=[str(i) for i in range(9, 17)], help='Modo da função main: "encoder" para codificar;\
                                 "decoder" para decodificar.')

    args = parser.parse_args()

    if args.mode == "encoder":
        print(GREEN, "Encoder mode chosen", RESET, sep="")
        compressor.main(args.input_file_name, int(args.bit_length))
    elif args.mode == "decoder":
        print(GREEN, "Decoder mode chosen", RESET, sep="")
        descompressor.main(args.input_file_name, int(args.bit_length))
