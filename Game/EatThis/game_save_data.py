def reset_save_data():
    with open('./EatThis/savegame.txt', mode='w', encoding='utf-8') as fout:  # Preenche um save inicial em arquivo.
        fout.write('1\n')
        fout.write('0\n')
        fout.write('0 9999\n')
        fout.write('0\n')
        fout.write('0 0\n')
    print("Save Data Reset.")

def read_save_data():
    data = []
    with open('./EatThis/savegame.txt', mode='r',
              encoding='utf-8') as fin:  # Le o save em arquivo e passa para memória.
        for linha in fin:
            aux = linha.rstrip('\n')  # retorna uma lista sem os \n
            data.append(list(map(float, aux.split())))  # aplica float em todos elementos.
    print("Loaded Save Data.")
    return data

def write_save_data(data):
    with open('./EatThis/savegame.txt', mode='w', encoding='utf-8') as fout:  # Preenche um save inicial em arquivo.
        for linha in range(len(data)):
            for coluna in range(len(data[linha])):
                fout.write(f'{data[linha][coluna]} ')
            fout.write('\n')