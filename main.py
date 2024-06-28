from lexico import Lexico

"""
    @Authors: Felipe Dresch, Felipe Scherer, Eduardo Paim
"""


def main():
    escolha = input("Escolha o código a ser lido:\n"
                    "1 - Fibonnaci\n"
                    "2 - Multiplicacao\n"
                    "-> ")
    match escolha:
        case '1': Lexico("codigos/fibonnaci.txt")
        case '2': Lexico("codigos/multiplicacao.txt")


