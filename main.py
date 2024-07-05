from lexico import Lexico

"""
    @Authors: Felipe Dresch, Felipe Scherer, Eduardo Paim
"""


def main():
    escolha = input("Escolha o código a ser lido:\n"
                    "1 - Código de sucesso\n"
                    "2 - Código com erro\n"
                    "3 - if e int\n"
                    "-> ")
    match escolha:
        case '1':
            Lexico("codigos/sucesso")
        case '2':
            Lexico("codigos/erro")
        case '3':
            analisador = Lexico("codigos/if")
            analisador.print_tokens()


if __name__ == '__main__':
    main()
