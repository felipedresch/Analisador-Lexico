# Analisador Léxico - Linguagem C++

![Python](https://img.shields.io/badge/Python-3.12%2B-blue)

Um analisador léxico simples em Python que reconhece comandos básicos da linguagem C++. Este projeto foi desenvolvido como parte de um estudo sobre análise léxica e serve como 
uma introdução ao processamento de linguagens formais.

## Funcionalidades

- Reconhecimento de variáveis (identificadores), operadores e estruturas de controle básicas da linguagem C++.
- Suporte limitado a um subconjunto da linguagem C++.
- Saída dos tokens reconhecidos no formato desejado.

## Requisitos

- Python 3.12.4 ou superior.

## Especificação Léxica da Linguagem
Descreve os tokens e padrões de formatação

| Token | Padrão de Formatação |
|-----|--------------------|
| Identificador | letra(letra+dígito)* |
| Número real | dígito⁺.dígito∗ |
| Número inteiro | dígito⁺ |
| String | “(letra + dígito + simbolo)∗” |
| Operador matemático| ‘+’ + ‘-’ + ‘*’ + ‘/’ + ‘+=’ + ‘-=’|
| Operador de Atribuição | ‘=’ |
| Operador de Comparação | ‘==’ |
| Palavra reservada | 'main()' + 'int' + 'bool' + 'for' + 'if' + 'else' + 'double' + 'string' + 'return' |
| Caractere Especial | '+' + '-' + '*' + '/' + '(', ')' + '<' + '>' + '=' + ':' + ';' + '{' + '}' |
| Operador lógico | 'true' + 'false' |

<!--| Palavra Reservada | letra(letra⁺) + letra(letra⁺) ‘(’ ‘)’ | -->



