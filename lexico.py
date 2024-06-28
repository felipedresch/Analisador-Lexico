from os import path
from tabulate import tabulate


class Lexico:
    """
        Analisador léxico parcial da linguagem C++ que recebe um arquivo de texto
        (codigo fonte) e classifica seu conteúdo em diferentes tokens.
    """

    def __init__(self, codigo_fonte):
        self.__pos_fita = 0
        self.__fita = []
        self.__num_linha = 1
        self.__tbl_simbolos = []
        self.__lexema = ''
        self.__fim_linha = '\n'
        self.__especiais = ['+', '-', '*', '/', '(', ')', '<', '>', '=', ':', ';', '{', '}']
        self.__codigo_fonte = codigo_fonte

        if path.exists(self.__codigo_fonte):
            self.__codigo = open(self.__codigo_fonte, 'r')
        else:
            raise FileNotFoundError(self.__codigo_fonte)

    def __avancar_fita(self):
        self.__pos_fita += 1

    def __get_pos_fita(self):
        # retorna a posição de leitura atual da fita
        return self.__pos_fita

    def __update_num_linha(self):
        self.__num_linha += 1

    def __get_caracter(self):
        if self.__pos_fita < len(self.__fita):
            self.__letra = self.__fita[self.__pos_fita]
            self.__avancar_fita()
            if self.__letra != self.__fim_linha or not self.__letra.isspace():
                self.__lexema += self.__letra
            return self.__letra
        else:
            return '\n'

    def __get_tbl_tokens(self):
        # Define a tabela de tokens
        for linha in self.__codigo:
            print(linha)
            self.__fita = list(linha)
            print(self.__fita)
            self.__q0()
            self.__update_num_linha()
            self.__pos_fita = 0
        self.__codigo.close()
        return self.__tbl_simbolos

    def __print_tokens(self):
        header = ['Token', 'Lexema', 'Linha', 'Coluna']
        print(tabulate(self.__get_tbl_tokens(), headers=header, tablefmt='fancy_grid'))

    def __q0(self):
        self.__caracter = self.__get_caracter()

        match self.__caracter:
            case 'i':
                print("Ir para o proximo estado")
                # self.__q1()
            case 'f':
                print("Ir para o proximo estado")
                # self.__q2()
            #  case ...
            case self.__caracter.isdigit():
                print()
                # self.__qx()
            case self.__caracter.isspace():
                self.__letra = ''
                self.__q0()
            case self.__fim_linha:
                pass
            case _:
                raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                                 f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")






