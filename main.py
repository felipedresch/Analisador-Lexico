from lexico import Lexico

"""
    @Authors: Felipe Dresch, Felipe Scherer, Eduardo Paim
"""


def main():
    escolha = input("Escolha o código a ser lido:\n"
                    "1 - Código de sucesso\n"
                    "2 - Código de sucesso dois\n"
                    "3 - Código de falha\n"
                    "-> ")
    match escolha:
        case '1':
            analisador = Lexico("codigos/sucesso")
            analisador.print_tokens()
        case '2':
            analisador = Lexico("codigos/sucesso2")
            analisador.print_tokens()
        case '3':
            Lexico("codigos/erro")




if __name__ == '__main__':
    main()
