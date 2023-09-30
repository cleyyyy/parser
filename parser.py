#Trabalho de compiladores 2.
#Alunos: Cleydison V. Dourado, Leandro, Erick.
#Professor: Eduardo.

import keyboard
import os

# Tokens de teste
'''tokens = [
    "class", "id", "{", "public", "static", "void", "main", "(", "String", "[", "]", "id", ")", "{",
    "System.out.println", "(", "new", "id", "(", ")", ".", "id", "(", "num", ")", ")", ";", "}","}", "$"
]'''


# Inicialização de variáveis globais
current_token = None
next_token = None
index = 0

# Função para obter os próximos tokens da lista
def get_next_token():
    global current_token, index, next_token
    tam = len(tokens)
    if index < tam:
        index = index + 1
        current_token = tokens[index-1]
        if index < tam:
            next_token = tokens[index]

# Função para verificar se o token atual corresponde ao esperado e avançar para os próximos tokens
def match(expected_token):
    if current_token == expected_token:
        get_next_token()
    else:
        raise Exception(f"Erro de análise: Esperado '{expected_token}', encontrado '{current_token}'")

# Função para análisar a regra PROG
def PROG():
    isMainDeClasse()
    while current_token == "class":
        isClasse()
    match("$")

# Função para análisar a regra isMainDeClasse
def isMainDeClasse():
    match("class")
    match("id")
    match("{")
    match("public")
    match("static")
    match("void")
    match("main")
    match("(")
    match("String")
    match("[")
    match("]")
    match("id")
    match(")")
    match("{")
    CMD()
    match("}")
    match("}")

#Função para análisar a regra isClasse
def isClasse():
    match("class")
    match("id")
    if current_token == "extends":
        match("extends")
        match("id")

    match("{")

    while current_token in ["int","boolean","id"]:
        VAR()

    while current_token == "public":
        isDeclaracaoMetodo()

    match("}")

#Função para análisar a regra  VAR
def VAR():
    tipo()
    match("id")
    match(";")

#Função para análisar a regra isDeclaracaoMetodo
def isDeclaracaoMetodo():
    match("public")
    tipo()
    match("id")
    match("(")

    if current_token in ["int","boolean","id"]:
        isParametro()

    match(")")
    match("{")

    while current_token in ["int", "boolean", "id"]:
        VAR()

    while current_token in ["if", "{", "while","System.out.println","id"]:
        CMD()

    match("return")
    EXP()
    match(";")
    match("}")

#Função para análisar a regra isParametro
def isParametro():
    tipo()
    match("id")
    while current_token == ",":
        match(",")
        tipo()
        match("id")

#Função para análisar a regra tipo
def tipo():
    if current_token == "int":
        match("int")
        if current_token == "[":
            match("[")
            match("]")
    elif current_token == "boolean":
        match("boolean")
    elif current_token == "id":
        match("id")

# Função para análisar a regra CMD
def CMD():
    if current_token == "{":
        match("{")
        while current_token in ["if", "{", "while", "System.out.println", "id"]:
            CMD()
        match("}")
    elif current_token == "if":
        match("if")
        match("(")
        EXP()
        match(")")
        CMD()
        if current_token == "else":
            match("else")
            CMD()
    elif current_token == "while":
        match("while")
        match("(")
        EXP()
        match(")")
        CMD()
    elif current_token == "System.out.println":
        match("System.out.println")
        match("(")
        EXP()
        match(")")
        match(";")
    elif current_token == "id":
        match("id")
        if current_token == "=":
            match("=")
            EXP()
            match(";")
        elif current_token == "[":
            match("[")
            EXP()
            match("]")
            match("=")
            EXP()
            match(";")

# Função para análisar a regra EXP
def EXP():
    isSubtracao()
    if current_token == "&&":
        match("&&")
        EXP()

# Função para análisar a regra isSubtracao
def isSubtracao():
    isAdicao()
    if current_token in {"<", "==", "!="}:
        match(current_token)
        isAdicao()

# Função para análisar a regra isAdicao
def isAdicao():
    isMultiplicacao()
    if current_token in {"+", "-"}:
        match(current_token)
        isMultiplicacao()

# Função para análisar a regra isMultiplicacao
def isMultiplicacao():
    isAtribuicao()
    if current_token in {"*", "/"}:
        match(current_token)
        isAtribuicao()

# Função para análisar a regra isAtribuicao
def isAtribuicao():
    if current_token == "new":
        if next_token == "int":
            match("new")
            match("int")
            match("[")
            EXP()
            match("]")
        elif next_token == "id":
            isInstanciaDeClasse()
    elif current_token == "!":
        match("!")
        isAtribuicao()
    elif current_token == "-":
        match("-")
        isAtribuicao()
    elif current_token == "true":
        match("true")
    elif current_token == "false":
        match("false")
    elif current_token == "num":
        match("num")
    else:
        isInstanciaDeClasse()


#Função para análisar a regra isInstanciaDeClasse
def isInstanciaDeClasse():
    if current_token == "new":
        if next_token == "int":
            isAtribuicao()
        else:
            match("new")
            match("id")
            match("(")
            match(")")
    elif current_token == "id":
       match("id")
    elif current_token == "this":
        match("this")
    elif current_token == "(":
        match("(")
        EXP()
        match(")")

    if current_token == ".":
        if next_token == "id":
            match(".")
            match("id")
        elif next_token == "length":
            match(".")
            match("length")
        elif next_token == "[":
            match(".")
            match("[")
            EXP()
            match("]")

    while current_token in ["id", "this", "new", "("]:
        isInstanciaDeClasse()
# Função para análisar a regra EXPS
def EXPS():
    EXP()
    while current_token == ",":
        match(",")
        EXP()


#Inicio do programa.
if __name__:
    #Lendo o arquivo de tokens
    print("Trabalho de Compiladores 2")
    print("Alunos: Cleydison Vieira Dourado, Erick Vinicius, Leandro klein.")
    print()
    # Leitura do arquivo e Definição dos tokens
    try:
        with open('resultado.txt', 'r') as file:
            tokens = []
            for line in file:
                data = line.split()
                if data[0].replace("[", "").replace(",", "") == "Palavra":
                    tokens.append(data[2].replace("]", "").replace(",", ""))

                elif data[0].replace("[", "").replace(",", "") == "Numeral":
                    tokens.append("num")

                elif data[0].replace("[", "").replace(",", "") == "Identificador":
                    tokens.append("id")

                else:
                    if data[1].replace(",", "") == "]]":
                        tokens.append("]")
                    else:
                        tokens.append(data[1].replace(",", "").replace("]", ""))
            tokens.append("$")

            try:
                get_next_token()
                PROG()
                print("Análise síntatica realizada com sucesso!")
            except Exception as er:
                print("Erro de análise síntatica.")
                print(er)

    except:

        print("Escreva o nome/patch onde o arquivo TXT encontra-se. Ex: Exemplo.txt ou C:\Documentos\Trabalho\Exemplo.txt")
        file_name = input("Arquivo: ")

        # Definição dos tokens
        try:
            with open(file_name,'r') as file:
                tokens = []
                for line in file:
                    data = line.split()
                    if data[0].replace("[", "").replace(",", "") == "Palavra":
                        tokens.append(data[2].replace("]", "").replace(",", ""))

                    elif data[0].replace("[", "").replace(",", "") == "Numeral":
                        tokens.append("num")

                    elif data[0].replace("[", "").replace(",", "") == "Identificador":
                        tokens.append("id")

                    else:
                        if data[1].replace(",", "") == "]]":
                            tokens.append("]")
                        else:
                            tokens.append(data[1].replace(",", "").replace("]", ""))
                tokens.append("$")

                try:
                    get_next_token()
                    PROG()
                    print("Análise síntatica realizada com sucesso!")
                except Exception as er:
                    print("Erro de análise síntatica.")
                    print(er)

        except Exception as Erro:
            print("Caminho ou arquivo invalido, tente novamente.")
            print(Erro)

    print()
    print("\033[1;32m Pressione qualquer tecla para terminar o programa!")

    while True:
        if keyboard.read_key():
            break
