# Exemplo de abertura de arquivo para leitura e leitura de uma linha.
fin = open('exemplo_de_entrada.txt', mode='r', encoding='utf-8')
try:
    linha = fin.readline().rstrip('\n')  # Equivale a input(), só que no arquivo fin
    print(linha)
finally:
    fin.close()

with open('exemplo_de_entrada.txt', mode='r', encoding='utf-8') as fin:
    linha = fin.readline().rstrip('\n')  # Equivale a input(), só que no arquivo fin
    print(linha)


# Exemplo de abertura de arquivo para leitura e leitura de todas as linhas até chegar no final do arquivo.
fin = open('exemplo_de_entrada.txt', mode='r', encoding='utf-8')
try:
    linha = fin.readline()
    while linha != '':
        linha = linha.rstrip('\n')
        print(f'Linha atual = {linha}')
        linha = fin.readline()
finally:
    fin.close()
