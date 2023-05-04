# Exemplo de abertura de um arquivo para leitura e um para escrita, levando à cópia do conteúdo do primeiro para o segundo, linha a linha.
with open('exemplo_de_entrada.txt', mode='r', encoding='utf-8') as fin:
    with open('exemplo_de_saida.txt', mode='w', encoding='utf-8') as fout:
        linha = fin.readline()
        while linha != '':
            fout.write(linha)
            linha = fin.readline()


# Exemplo equivalente ao de cima, mas utilizando for para ler as linhas do arquivo uma a uma.
with open('exemplo_de_entrada.txt', mode='r', encoding='utf-8') as fin:
    with open('exemplo_de_saida.txt', mode='w', encoding='utf-8') as fout:
        for linha in fin:
            fout.write(linha)
