# Exemplo de abertura de arquivo para escrita e escrita de três linhas.
fout = open('exemplo_de_saida.txt', mode='w', encoding='utf-8')
try:
    fout.write('Um texto qualquer\n')
    fout.write('Outro texto qualquer\n')
    linha = 'Mais uma linha'
    fout.write(f'{linha}\n')  # Equivale a print(linha)
finally:
    fout.close()


# Exemplo equivalente ao de cima, porém utilizando with-as no lugar de try-finally-close.
with open('exemplo_de_saida.txt', mode='w', encoding='utf-8') as fout:
    fout.write('Um texto qualquer\n')
    fout.write('Outro texto qualquer\n')
    linha = 'Mais uma linha'
    fout.write(f'{linha}\n')  # Equivale a print(linha)
