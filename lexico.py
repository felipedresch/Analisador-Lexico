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
        """
            Busca o próximo símbolo da fita e o adiciona ao lexema caso este símbolo não seja um espaço ou
            uma quebra de linha.
            :return: O próximo símbolo da fita
        """
        if self.__pos_fita < len(self.__fita):
            self.__letra = self.__fita[self.__pos_fita]
            self.__avancar_fita()
            if self.__letra is None:
                self.__letra = ' '
            if self.__letra != self.__fim_linha or not self.__letra.isspace():
                self.__lexema += self.__letra
            return self.__letra

    def __get_tbl_tokens(self):
        """
        O loop do código acontece aqui, pegando linha por linha e mandando para o estado q0 sempre em cada linha.
        Ao final, tem-se a tabela de símbolos.
        :return: A tabela de tokens/símbolos montada durante a execução do programa
        """
        for linha in self.__codigo:
            self.__fita = list(linha)
            # Aqui o programa 'começa'. Do q0 ele vai para vários outros estados até encontrar o fim da linha e
            # voltar para este lugar e repetir o processo para as demais linhas
            self.__q0()

            self.__update_num_linha()
            self.__pos_fita = 0
        self.__codigo.close()
        return self.__tbl_simbolos

    def print_tokens(self):
        header = ['Token', 'Lexema', 'Linha', 'Coluna']
        print(tabulate(self.__get_tbl_tokens(), headers=header, tablefmt='fancy_grid'))

    def __leu_espaco_reconhecedor(self, token: str):
        """
            Quando um estado reconhecedor lê um espaço. Significa que ainda há mais símbolos para ler na
            linha atual.
            :param token: str -> O token reconhecido.
        """
        self.__tbl_simbolos.append([token, self.__lexema, self.__num_linha, self.__pos_fita - len(self.__lexema)])
        self.__lexema = ''

    def __leu_fim_linha(self, token: str):
        """
            Usado em estados reconhecedores. Encontra um \n após o reconhecimento de um símbolo.
            :param token: str -> o token encontrado.
        """
        self.__tbl_simbolos.append([token, self.__lexema, self.__num_linha, self.__pos_fita - len(self.__lexema)])
        self.__lexema = ''

    def __leu_especial(self, token: str):
        """
            Usado em estados reconhecedores. Deve-se retornar a posição da fita de leitura e descartar o
            símbolo especial lido.
            :param token: str -> O token reconhecido.
        """
        self.__lexema = self.__lexema[:len(self.__lexema) - 1]
        self.__tbl_simbolos.append([token, self.__lexema, self.__num_linha, self.__pos_fita - len(self.__lexema)])
        self.__lexema = ''
        self.__pos_fita -= 1

    # IMPORTANTE!! Os espaços são lidos como uma string vazia assim -> '' e os fins de linha são lidos como None!

    def __q0(self):
        self.__caracter = self.__get_caracter()

        if self.__caracter is None:
            pass
        elif self.__caracter == '' or self.__caracter.isspace():
            self.__lexema = ''
            self.__q0()
        elif self.__caracter == 'i':
            self.__q1()
        elif self.__caracter == '+':
            self.__q6()
        elif self.__caracter == '*':
            self.__q8()
        elif self.__caracter == '/':
            self.__q10()
        elif self.__caracter == 'f':
            self.__q13()
        elif self.__caracter == 'e':
            self.__q14()
        elif self.__caracter == ';':
            self.__q16()
        elif self.__caracter == '-':
            self.__q18()
        elif self.__caracter == '%':
            self.__q20()
        elif self.__caracter == '=':
            self.__q21()
        elif self.__caracter == '<':
            self.__q24()
        elif self.__caracter == '>':
            self.__q25()
        elif self.__caracter == '(':
            self.__q29()
        elif self.__caracter == ')':
            self.__q30()
        elif self.__caracter == '{':
            self.__q17()
        elif self.__caracter == '}':
            self.__q17()
        elif self.__caracter == 'b':
            self.__q33()
        elif self.__caracter == 'd':
            self.__q37()
        elif self.__caracter == 'm':
            self.__q43()
        elif self.__caracter.isdigit():
            self.__q50()
        elif self.__caracter == 'r':
            self.__q52()
        elif self.__caracter == 't':
            self.__q62()
        elif self.__caracter == 's':
            self.__q65()
        elif self.__caracter.islower():
            self.__q11()
        elif self.__caracter == '"':
            self.__q64()
        elif self.__fim_linha:
            pass
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q1(self):
        """
            Estados intermediários (que não reconecem nenhum símbolo) só precisam ter a lógica de reconhecer
            o seu símbolo, dígitos e espaços. Fim de linha e especiais não precisa.
        :return:
        """
        self.__caracter = self.__get_caracter()

        if self.__caracter is None:
            pass
        elif self.__caracter == 'f':
            self.__q2()
        elif self.__caracter == 'n':
            self.__q31()
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        elif self.__caracter == '' or self.__caracter.isspace():
            self.__q11()
        elif self.__fim_linha:
            pass
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q2(self):
        """
        Reconhece o lexema 'if' e define o que fazer caso o próximo item a ser lido for um espaço,
        uma quebra de linha ou um caracter especial.
        """
        self.__caracter = self.__get_caracter()

        if self.__caracter is None or self.__caracter.isspace() or self.__caracter == '':  # verificar
            self.__leu_espaco_reconhecedor("palavra reservada")
            self.__q0()
        elif self.__caracter == self.__fim_linha:
            self.__leu_fim_linha("palavra reservada")
        elif self.__caracter in self.__especiais:
            self.__leu_especial("palavra reservada")
            self.__q0()
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q3(self):
        """
            Estados intermediários (que não reconecem nenhum símbolo) só precisam ter a lógica de reconhecer
            o seu símbolo, dígitos e espaços. Fim de linha e especiais não precisa.
        :return:
        """
        self.__caracter = self.__get_caracter()

        if self.__caracter is None:
            pass
        elif self.__caracter == 'e':
            self.__q4()
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        elif self.__caracter == '':
            self.__q0()
        elif self.__fim_linha:
            pass
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q4(self):
        """
        Reconhece o lexema 'else' e define o que fazer caso o próximo item a ser lido for um espaço,
        uma quebra de linha ou um caracter especial.
        """
        self.__caracter = self.__get_caracter()

        if self.__caracter is None or self.__caracter.isspace() or self.__caracter == '':  # verificar
            self.__leu_espaco_reconhecedor("palavra reservada")
            self.__q0()
        elif self.__caracter == self.__fim_linha:
            self.__leu_fim_linha("palavra reservada")
        elif self.__caracter in self.__especiais:
            self.__leu_especial("palavra reservada")
            self.__q0()
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q5(self):
        """
            Estados intermediários (que não reconecem nenhum símbolo) só precisam ter a lógica de reconhecer
            o seu símbolo, dígitos e espaços. Fim de linha e especiais não precisa.
        """
        self.__caracter = self.__get_caracter()

        if self.__caracter is None:
            pass
        elif self.__caracter == 's':
            self.__q3()
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        elif self.__caracter == '':
            self.__q0()
        elif self.__fim_linha:
            pass
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q6(self):
        self.__caracter = self.__get_caracter()
        if self.__caracter is None:
            pass
        elif self.__caracter == '+':
            self.__q9()
        elif self.__caracter == '=':
            self.__q26()
        elif self.__caracter.isspace() or self.__caracter == '':  # verificar
            self.__leu_especial("operador matemático344")
            self.__q0()
        elif self.__caracter == self.__fim_linha:
            self.__leu_fim_linha("operador matemático345")
        elif self.__caracter in self.__especiais:
            self.__leu_especial("operador matemático349")
            self.__q0()
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        elif self.__caracter == '':
            self.__q0()
        elif self.__fim_linha:
            pass
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q7(self):
        """
        Reconhece o lexema 'for' e define o que fazer caso o próximo item a ser lido for um espaço,
        uma quebra de linha ou um caracter especial.
        """
        self.__caracter = self.__get_caracter()

        if self.__caracter is None:
            pass
        elif self.__caracter is None or self.__caracter.isspace() or self.__caracter == '':  # verificar
            self.__leu_espaco_reconhecedor("palavra reservada")
            self.__q0()
        elif self.__caracter == self.__fim_linha:
            self.__leu_fim_linha("palavra reservada")
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q8(self):
        self.__caracter = self.__get_caracter()

        if self.__caracter is None or self.__caracter.isspace() or self.__caracter == '':  # verificar
            self.__leu_espaco_reconhecedor("operador matemático")
            self.__q0()
        elif self.__caracter == self.__fim_linha:
            self.__leu_fim_linha("operador matemático")
        elif self.__caracter in self.__especiais:
            self.__leu_especial("operador matemático")
            self.__q0()
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q9(self):
        self.__caracter = self.__get_caracter()

        if self.__caracter == self.__fim_linha:
            self.__leu_fim_linha("operador matemático34")
        elif self.__caracter.islower():
            self.__leu_especial("operador matemático1")
            self.__q11()
        elif self.__caracter in self.__especiais:
            self.__leu_especial("operador matemático2")
            self.__q0()
        elif self.__caracter is None or self.__caracter.isspace() or self.__caracter == '':
            self.__leu_especial("operador matemático3")
            self.__q0()
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q10(self):
        self.__caracter = self.__get_caracter()

        if self.__caracter is None or self.__caracter.isspace() or self.__caracter == '':  # verificar
            self.__leu_espaco_reconhecedor("operador matemático")
            self.__q0()
        elif self.__caracter == self.__fim_linha:
            self.__leu_fim_linha("operador matemático")
        elif self.__caracter in self.__especiais:
            self.__leu_especial("operador matemático")
            self.__q0()
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        elif self.__caracter == '':
            self.__q0()
        elif self.__fim_linha:
            pass
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q11(self):
        """
        Será o estado de destino sempre que o analisador encontrar, no meio de uma palavra que até
        aquele momento tem potencial para ser aceita, um número ou uma letra que não foi explicitamente
        definida no autômato.
        É também o destino, a partir de q0, caso seja lido uma letra minuscula.
        Este é um estado reconhecedor de variáveis/identificadores.
        """
        self.__caracter = self.__get_caracter()

        while self.__caracter is not None and (self.__caracter.islower() or self.__caracter.isdigit()):
            self.__caracter = self.__get_caracter()

        if self.__caracter is None:
            pass
        elif self.__caracter.isspace() or self.__caracter == '':
            self.__leu_espaco_reconhecedor("identificador")
            self.__q0()
        elif self.__caracter == self.__fim_linha:
            self.__leu_fim_linha("identificador")
        elif self.__caracter in self.__especiais:
            self.__leu_especial("identificador")
            self.__q0()
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q12(self):
        """
        Faz parte do reconhecimento do for, se encontrar o R vai pro q7, se não vai pro q11 pq é variavel
        """
        self.__caracter = self.__get_caracter()

        if self.__caracter is None:
            pass
        elif self.__caracter == 'r':
            self.__q7()
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q13(self):
        self.__caracter = self.__get_caracter()

        if self.__caracter is None:
            pass
        elif self.__caracter == 'o':
            self.__q12()
        elif self.__caracter == 'a':
            self.__q58()
        elif self.__caracter != 'o':
            self.__q11()
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q14(self):
        """
            Estados intermediários (que não reconecem nenhum símbolo) só precisam ter a lógica de reconhecer
            o seu símbolo, dígitos e espaços. Fim de linha e especiais não precisa.
        """
        self.__caracter = self.__get_caracter()

        if self.__caracter is None:
            pass
        elif self.__caracter == 'l':
            self.__q5()
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        elif self.__caracter == '':
            self.__q0()
        elif self.__fim_linha:
            pass
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q16(self):
        self.__caracter = self.__get_caracter()

        if self.__caracter is None:
            self.__leu_fim_linha("caractere especial")
        elif self.__caracter == '' or self.__caracter.isspace():
            self.__leu_espaco_reconhecedor("caractere especial")
            self.__q0()
        elif self.__caracter in self.__especiais:
            self.__q0()
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q17(self):
        self.__caracter = self.__get_caracter()

        if self.__caracter is None:
            pass
        elif self.__caracter == '' or self.__caracter.isspace():
            self.__leu_espaco_reconhecedor("caractere especial")
            self.__q0()
        elif self.__caracter in self.__especiais:
            self.__q0()
        elif self.__caracter == self.__fim_linha:
            self.__leu_fim_linha("caractere especial")
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__leu_especial("caracter especial")
            self.__q0()
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q18(self):
        self.__caracter = self.__get_caracter()

        if self.__caracter is None or self.__caracter.isspace() or self.__caracter == '':  # verificar
            self.__leu_espaco_reconhecedor("operador matemático")
            self.__q0()
        elif self.__caracter == self.__fim_linha:
            self.__leu_fim_linha("operador matemático")
        elif self.__caracter in self.__especiais:
            self.__leu_especial("operador matemático")
            self.__q0()
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q19(self):
        self.__caracter = self.__get_caracter()

        if self.__caracter is None:
            self.__leu_fim_linha("caractere especial")
        elif self.__caracter == '' or self.__caracter.isspace():
            self.__leu_espaco_reconhecedor("caractere especial")
            self.__q0()
        elif self.__caracter in self.__especiais:
            self.__q0()
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q20(self):
        self.__caracter = self.__get_caracter()

        if self.__caracter is None or self.__caracter.isspace() or self.__caracter == '':  # verificar
            self.__leu_espaco_reconhecedor("operador matemático")
            self.__q0()
        elif self.__caracter == self.__fim_linha:
            self.__leu_fim_linha("operador matemático")
        elif self.__caracter in self.__especiais:
            self.__leu_especial("operador matemático")
            self.__q0()
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q21(self):
        self.__caracter = self.__get_caracter()

        if self.__caracter == '=':
            self.__q22()
        elif self.__caracter is None or self.__caracter.isspace() or self.__caracter == '':  # verificar
            self.__leu_espaco_reconhecedor("operador de atribuição")
            self.__q0()
        elif self.__caracter == self.__fim_linha:
            self.__leu_fim_linha("operador de atribuição")
        elif self.__caracter in self.__especiais:
            self.__leu_especial("operador de atribuição")
            self.__q0()
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        elif self.__caracter == '':
            self.__q0()
        elif self.__fim_linha:
            pass
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q22(self):
        self.__caracter = self.__get_caracter()

        if self.__caracter is None or self.__caracter.isspace() or self.__caracter == '':
            self.__leu_espaco_reconhecedor("operador de comparação")
            self.__q0()
        elif self.__caracter == self.__fim_linha:
            self.__leu_fim_linha("operador de comparação")
        elif self.__caracter in self.__especiais:
            self.__leu_especial("operador de comparação")
            self.__q0()
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q24(self):
        self.__caracter = self.__get_caracter()
        if self.__caracter == '=':
            self.__q27()
        elif self.__caracter is None or self.__caracter.isspace() or self.__caracter == '':  # verificar
            self.__leu_espaco_reconhecedor("operador de comparação")
            self.__q0()
        elif self.__caracter == self.__fim_linha:
            self.__leu_fim_linha("operador de comparação")
        elif self.__caracter in self.__especiais:
            self.__leu_especial("operador de comparação")
            self.__q0()
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        elif self.__caracter == '':
            self.__q0()
        elif self.__fim_linha:
            pass
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q25(self):
        self.__caracter = self.__get_caracter()
        if self.__caracter == '=':
            self.__q27()
        elif self.__caracter is None or self.__caracter.isspace() or self.__caracter == '':  # verificar
            self.__leu_espaco_reconhecedor("operador de comparação")
            self.__q0()
        elif self.__caracter == self.__fim_linha:
            self.__leu_fim_linha("operador de comparação")
        elif self.__caracter in self.__especiais:
            self.__leu_especial("operador de comparação")
            self.__q0()
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        elif self.__caracter == '':
            self.__q0()
        elif self.__fim_linha:
            pass
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q26(self):
        self.__caracter = self.__get_caracter()

        if self.__caracter is None or self.__caracter.isspace() or self.__caracter == '':
            self.__leu_espaco_reconhecedor("operador matemático")
            self.__q0()
        elif self.__caracter == self.__fim_linha:
            self.__leu_fim_linha("operador matemático")
        elif self.__caracter in self.__especiais:
            self.__leu_especial("operador matemático")
            self.__q0()
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q27(self):
        self.__caracter = self.__get_caracter()

        if self.__caracter is None or self.__caracter.isspace() or self.__caracter == '':
            self.__leu_espaco_reconhecedor("operador de comparação")
            self.__q0()
        elif self.__caracter == self.__fim_linha:
            self.__leu_fim_linha("operador de comparação")
        elif self.__caracter in self.__especiais:
            self.__leu_especial("operador de comparação")
            self.__q0()
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q29(self):
        self.__caracter = self.__get_caracter()

        if self.__caracter is None:
            pass
        elif self.__caracter == '' or self.__caracter.isspace():
            self.__leu_espaco_reconhecedor("caractere especial")
            self.__q0()
        elif self.__caracter in self.__especiais:
            self.__lexema = self.__lexema[:len(self.__lexema) - 1]
            self.__leu_espaco_reconhecedor("caractere especial")
            self.__pos_fita -= 1
            self.__q0()
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__lexema = self.__lexema[:len(self.__lexema) - 1]
            self.__leu_espaco_reconhecedor("caractere especial")
            self.__pos_fita -= 1
            self.__q0()
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q30(self):
        self.__caracter = self.__get_caracter()

        if self.__caracter is None:
            self.__leu_fim_linha("caractere especial")
        elif self.__caracter == '' or self.__caracter.isspace():
            self.__leu_espaco_reconhecedor("caractere especial")
            self.__q0()
        elif self.__caracter in self.__especiais:
            self.__leu_especial("caractere especial")
            self.__q0()
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q31(self):
        self.__caracter = self.__get_caracter()

        if self.__caracter == 't':  # Reconhece o lexema 'int'
            self.__q32()
        elif self.__caracter.islower() or self.__caracter.isdigit():
            self.__q11()
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q32(self):
        """
        Reconhece o token 'int' e define o que fazer depois disso.
        A lógica dos estados reconhecedores é sempre a mesma, muda apenas os estados de destino.
        """
        self.__caracter = self.__get_caracter()

        if self.__caracter is None:
            self.__leu_fim_linha("palavra reservada")
        elif self.__caracter == '' or self.__caracter.isspace():
            self.__leu_espaco_reconhecedor("palavra reservada")
            self.__q0()
        elif self.__caracter in self.__especiais:
            self.__leu_especial("palavra reservada")
            self.__q0()
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q33(self):
        """
            Estados intermediários (que não reconecem nenhum símbolo) só precisam ter a lógica de reconhecer
            o seu símbolo, dígitos e espaços. Fim de linha e especiais não precisa.
        :return:
        """
        self.__caracter = self.__get_caracter()

        if self.__caracter is None:
            pass
        elif self.__caracter == 'o':
            self.__q34()
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        elif self.__caracter == '':
            self.__q0()
        elif self.__fim_linha:
            pass
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q34(self):
        """
             Estados intermediários (que não reconecem nenhum símbolo) só precisam ter a lógica de reconhecer
             o seu símbolo, dígitos e espaços. Fim de linha e especiais não precisa.
         :return:
         """
        self.__caracter = self.__get_caracter()

        if self.__caracter is None:
            pass
        elif self.__caracter == 'o':
            self.__q35()
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        elif self.__caracter == '':
            self.__q0()
        elif self.__fim_linha:
            pass
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q35(self):
        """
              Estados intermediários (que não reconecem nenhum símbolo) só precisam ter a lógica de reconhecer
              o seu símbolo, dígitos e espaços. Fim de linha e especiais não precisa.
          :return:
          """
        self.__caracter = self.__get_caracter()

        if self.__caracter is None:
            pass
        elif self.__caracter == 'l':
            self.__q36()
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        elif self.__caracter == '':
            self.__q0()
        elif self.__fim_linha:
            pass
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q36(self):
        """
        Reconhece o token 'bool' e define o que fazer depois disso.
        A lógica dos estados reconhecedores é sempre a mesma, muda apenas os estados de destino.
        """
        self.__caracter = self.__get_caracter()

        if self.__caracter is None:
            self.__leu_fim_linha("palavra reservada")
        elif self.__caracter == '' or self.__caracter.isspace():
            self.__leu_espaco_reconhecedor("palavra reservada")
            self.__q0()
        elif self.__caracter in self.__especiais:
            self.__leu_especial("palavra reservada")
            self.__q0()
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q37(self):
        """
            Estados intermediários (que não reconecem nenhum símbolo) só precisam ter a lógica de reconhecer
            o seu símbolo, dígitos e espaços. Fim de linha e especiais não precisa.
        :return:
        """
        self.__caracter = self.__get_caracter()

        if self.__caracter is None:
            pass
        elif self.__caracter == 'o':
            self.__q38()
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        elif self.__caracter == '':
            self.__q0()
        elif self.__fim_linha:
            pass
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q38(self):
        """
            Estados intermediários (que não reconecem nenhum símbolo) só precisam ter a lógica de reconhecer
            o seu símbolo, dígitos e espaços. Fim de linha e especiais não precisa.
        :return:
        """
        self.__caracter = self.__get_caracter()

        if self.__caracter is None:
            pass
        elif self.__caracter == 'u':
            self.__q39()
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        elif self.__caracter == '':
            self.__q0()
        elif self.__fim_linha:
            pass
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q39(self):
        """
            Estados intermediários (que não reconecem nenhum símbolo) só precisam ter a lógica de reconhecer
            o seu símbolo, dígitos e espaços. Fim de linha e especiais não precisa.
        :return:
        """
        self.__caracter = self.__get_caracter()

        if self.__caracter is None:
            pass
        elif self.__caracter == 'b':
            self.__q40()
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        elif self.__caracter == '':
            self.__q0()
        elif self.__fim_linha:
            pass
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q40(self):
        """
            Estados intermediários (que não reconecem nenhum símbolo) só precisam ter a lógica de reconhecer
            o seu símbolo, dígitos e espaços. Fim de linha e especiais não precisa.
        :return:
        """
        self.__caracter = self.__get_caracter()

        if self.__caracter is None:
            pass
        elif self.__caracter == 'l':
            self.__q41()
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        elif self.__caracter == '':
            self.__q0()
        elif self.__fim_linha:
            pass
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q41(self):
        """
            Estados intermediários (que não reconecem nenhum símbolo) só precisam ter a lógica de reconhecer
            o seu símbolo, dígitos e espaços. Fim de linha e especiais não precisa.
        :return:
        """
        self.__caracter = self.__get_caracter()

        if self.__caracter is None:
            pass
        elif self.__caracter == 'e':
            self.__q42()
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        elif self.__caracter == '':
            self.__q0()
        elif self.__fim_linha:
            pass
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q42(self):
        """
        Reconhece o lexema 'double' e define o que fazer caso o próximo item a ser lido for um espaço,
        uma quebra de linha ou um caracter especial.
        """
        self.__caracter = self.__get_caracter()

        if self.__caracter is None or self.__caracter.isspace() or self.__caracter == '':  # verificar
            self.__leu_espaco_reconhecedor("palavra reservada")
            self.__q0()
        elif self.__caracter == self.__fim_linha:
            self.__leu_fim_linha("palavra reservada")
        elif self.__caracter in self.__especiais:
            self.__leu_especial("palavra reservada")
            self.__q0()
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q43(self):
        """
        :return:
        """
        self.__caracter = self.__get_caracter()

        if self.__caracter is None:
            pass
        elif self.__caracter == 'a':
            self.__q44()
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        elif self.__caracter == '':
            self.__q0()
        elif self.__fim_linha:
            pass
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q44(self):
        """
        :return:
        """
        self.__caracter = self.__get_caracter()

        if self.__caracter is None:
            pass
        elif self.__caracter == 'i':
            self.__q45()
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        elif self.__caracter == '':
            self.__q0()
        elif self.__fim_linha:
            pass
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q45(self):
        """
        :return:
        """
        self.__caracter = self.__get_caracter()

        if self.__caracter is None:
            pass
        elif self.__caracter == 'n':
            self.__q46()
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        elif self.__caracter == '':
            self.__q0()
        elif self.__fim_linha:
            pass
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q46(self):
        self.__caracter = self.__get_caracter()

        if self.__caracter is None:
            pass
        elif self.__caracter == '(':
            self.__q47()
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        elif self.__caracter == '':
            self.__q0()
        elif self.__fim_linha:
            pass
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q47(self):
        self.__caracter = self.__get_caracter()

        if self.__caracter == ')':  # Reconhece o lexema 'main()'
            self.__q48()
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q48(self):
        self.__caracter = self.__get_caracter()

        if self.__caracter is None:
            self.__leu_fim_linha("palavra reservada")
        elif self.__caracter == '' or self.__caracter.isspace():
            self.__leu_espaco_reconhecedor("palavra reservada")
            self.__q0()
        elif self.__caracter in self.__especiais:
            self.__leu_especial("palavra reservada")
            self.__q0()
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q50(self):
        self.__caracter = self.__get_caracter()

        while self.__caracter is not None and (self.__caracter in '0123456789'):
            self.__caracter = self.__get_caracter()

        if self.__caracter is None or self.__caracter.isspace() or self.__caracter == '':  # verificar
            self.__leu_espaco_reconhecedor("número inteiro")
            self.__q0()
        elif self.__caracter == '.':
            self.__q51()
        elif self.__caracter == self.__fim_linha:
            self.__leu_fim_linha("número inteiro")
        elif self.__caracter in self.__especiais:
            self.__leu_especial("número inteiro")
            self.__q0()
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q51(self):
        self.__caracter = self.__get_caracter()

        while self.__caracter is not None and (self.__caracter in '0123456789'):
            self.__caracter = self.__get_caracter()

        if self.__caracter is None or self.__caracter.isspace() or self.__caracter == '':  # verificar
            self.__leu_espaco_reconhecedor("número real")
            self.__q0()
        elif self.__caracter == self.__fim_linha:
            self.__leu_fim_linha("número real")
        elif self.__caracter in self.__especiais:
            self.__leu_especial("número real")
            self.__q0()
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q52(self):
        """
           Verifica se o caractere é um 'e', para formar a palavra reservada 'return', se não for
           apenas toma outro caminho
         """
        self.__caracter = self.__get_caracter()

        if self.__caracter is None:
            pass
        elif self.__caracter == 'e':
            self.__q53()
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        elif self.__caracter == '':
            self.__q0()
        elif self.__fim_linha:
            pass
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q53(self):
        """
           Verifica se o caractere é um 't', para formar a palavra reservada 'return', se não for
           apenas toma outro caminho
         """
        self.__caracter = self.__get_caracter()

        if self.__caracter is None:
            pass
        elif self.__caracter == 't':
            self.__q54()
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        elif self.__caracter == '':
            self.__q0()
        elif self.__fim_linha:
            pass
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q54(self):
        """
           Verifica se o caractere é um 'u', para formar a palavra reservada 'return', se não for
           apenas toma outro caminho
         """
        self.__caracter = self.__get_caracter()

        if self.__caracter is None:
            pass
        elif self.__caracter == 'u':
            self.__q55()
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        elif self.__caracter == '':
            self.__q0()
        elif self.__fim_linha:
            pass
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q55(self):
        """
           Verifica se o caractere é um 'r', para formar a palavra reservada 'return', se não for
           apenas toma outro caminho
         """
        self.__caracter = self.__get_caracter()

        if self.__caracter is None:
            pass
        elif self.__caracter == 'r':
            self.__q56()
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        elif self.__caracter == '':
            self.__q0()
        elif self.__fim_linha:
            pass
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q56(self):
        """
           Verifica se o caractere é um 'n', para formar a palavra reservada 'return', se não for
           apenas toma outro caminho
         """
        self.__caracter = self.__get_caracter()

        if self.__caracter == 'n':  # Reconhece o lexema 'return'
            self.__q57()
        elif self.__caracter.islower() or self.__caracter.isdigit():
            self.__q11()
        elif self.__caracter == '':
            self.__q0()
        elif self.__caracter == self.__fim_linha:
            pass
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q57(self):
        """
            Identifica a palavra reservada 'return'
         """

        self.__caracter = self.__get_caracter()

        if self.__caracter is None:
            self.__leu_fim_linha("palavra reservada")
        elif self.__caracter == '' or self.__caracter.isspace():
            self.__leu_espaco_reconhecedor("palavra reservada")
            self.__q0()
        elif self.__caracter in self.__especiais:
            self.__leu_especial("palavra reservada")
            self.__q0()
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q58(self):
        """
           Verifica se o caractere é um 'l', para formar a palavra reservada 'false', se não for
           apenas toma outro caminho
         """

        self.__caracter = self.__get_caracter()

        if self.__caracter is None:
            pass
        elif self.__caracter == 'l':
            self.__q59()
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        elif self.__caracter == '':
            self.__q0()
        elif self.__fim_linha:
            pass
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q59(self):
        """
           Verifica se o caractere é um 's', para formar a palavra reservada 'false', se não for
           apenas toma outro caminho
         :return:
         """

        self.__caracter = self.__get_caracter()

        if self.__caracter is None:
            pass
        elif self.__caracter == 's':
            self.__q60()
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        elif self.__caracter == '':
            self.__q0()
        elif self.__fim_linha:
            pass
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q60(self):
        """
          Verifica se o caractere é um 'e', para formar a palavra reservada 'false' ou 'true', se não for
          apenas toma outro caminho
        :return:
        """
        self.__caracter = self.__get_caracter()

        if self.__caracter == 'e':  # Reconhece o lexema 'false'
            self.__q61()
        elif self.__caracter.islower() or self.__caracter.isdigit():
            self.__q11()
        elif self.__caracter == '':
            self.__q0()
        elif self.__caracter == self.__fim_linha:
            pass
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q61(self):
        """
          Identifica a palavra reservada 'false'
        :return:
        """
        self.__caracter = self.__get_caracter()

        if self.__caracter is None:
            self.__leu_fim_linha("operador lógico")
        elif self.__caracter == '' or self.__caracter.isspace():
            self.__leu_espaco_reconhecedor("operador lógico")
            self.__q0()
        elif self.__caracter in self.__especiais:
            self.__leu_especial("operador lógico")
            self.__q0()
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q62(self):
        """
          Verifica se o caractere é um 'r', para formar a palavra reservada 'true', se não for
          apenas toma outro caminho
        :return:
        """

        self.__caracter = self.__get_caracter()

        if self.__caracter is None:
            pass
        elif self.__caracter == 'r':
            self.__q63()
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        elif self.__caracter == '':
            self.__q0()
        elif self.__fim_linha:
            pass
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q63(self):
        """
          Verifica se o caractere é um 'u', para formar a palavra reservada 'true', se não for
          apenas toma outro caminho
        """
        self.__caracter = self.__get_caracter()

        if self.__caracter is None:
            pass
        elif self.__caracter == 'u':
            self.__q60()
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        elif self.__caracter == '':
            self.__q0()
        elif self.__fim_linha:
            pass
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q64(self):
        """
        Lê uma string
        """
        self.__caracter = self.__get_caracter()

        while self.__caracter is not None and not self.__caracter == '"':
            self.__caracter = self.__get_caracter()

        if self.__caracter == '"':
            self.__caracter = self.__get_caracter()

        if self.__caracter is None:
            pass
        elif self.__caracter == '"':
            self.__caracter = self.__get_caracter()
        elif self.__caracter.isspace() or self.__caracter == '':
            self.__leu_espaco_reconhecedor("string")
            self.__q0()
        elif self.__caracter == self.__fim_linha:
            self.__leu_fim_linha("string")
        elif self.__caracter in self.__especiais:
            self.__leu_especial("string")
            self.__q0()
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q65(self):
        # 't' de 'string'
        self.__caracter = self.__get_caracter()

        if self.__caracter is None:
            pass
        elif self.__caracter == 't':
            self.__q66()
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        elif self.__caracter == '':
            self.__q0()
        elif self.__fim_linha:
            pass
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q66(self):
        # 'r' de 'string'
        self.__caracter = self.__get_caracter()

        if self.__caracter is None:
            pass
        elif self.__caracter == 'r':
            self.__q67()
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        elif self.__caracter == '':
            self.__q0()
        elif self.__fim_linha:
            pass
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q67(self):
        # 'i' de 'string'
        self.__caracter = self.__get_caracter()

        if self.__caracter is None:
            pass
        elif self.__caracter == 'i':
            self.__q68()
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        elif self.__caracter == '':
            self.__q0()
        elif self.__fim_linha:
            pass
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q68(self):
        # 'n' de 'string'
        self.__caracter = self.__get_caracter()

        if self.__caracter is None:
            pass
        elif self.__caracter == 'n':
            self.__q69()
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        elif self.__caracter == '':
            self.__q0()
        elif self.__fim_linha:
            pass
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q69(self):
        # 'g' de 'string'
        self.__caracter = self.__get_caracter()

        if self.__caracter is None:
            pass
        elif self.__caracter == 'g':
            self.__q70()
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        elif self.__caracter == '':
            self.__q0()
        elif self.__fim_linha:
            pass
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")

    def __q70(self):
        # reconhece a palavra reservada string
        self.__caracter = self.__get_caracter()

        if self.__caracter is None:
            pass
        elif self.__caracter.isdigit() or self.__caracter.islower():
            self.__q11()
        elif self.__caracter == '' or self.__caracter.isspace():
            self.__leu_espaco_reconhecedor("palavra reservada")
            self.__q0()
        elif self.__fim_linha:
            self.__leu_fim_linha("palavra reservada")
        else:
            raise ValueError(f"Erro léxico encontrado na linha {self.__num_linha} "
                             f"e coluna {self.__pos_fita} para o caracter {self.__caracter}")
