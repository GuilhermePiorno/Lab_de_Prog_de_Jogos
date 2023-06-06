import os


class SaveFile:
    def __init__(self, path):
        self.path = path
        self.Master_vol = 50
        self.BGM_vol = 50
        self.SFX_vol = 50

    def read_save_data(self):
        """
        Loads save if it exists and returns 1.
        returns 0 in case save is not found.
        :return:
        """
        if os.path.exists(self.path):
            data = []
            with open(self.path, mode='r',
                      encoding='utf-8') as fin:  # Le o save em arquivo e passa para memória.
                for linha in fin:
                    aux = linha.rstrip('\n')  # retorna uma lista sem os \n
                    aux = list(map(float, aux.split()))  # aplica float em todos elementos.
                    data.append(aux)

                    # Linha 0 => [master_vol, bgm_vol, sfx_vol]
            self.Master_Vol = data[0][0]
            self.BGM_Vol = data[0][1]
            self.SFX_Vol = data[0][2]
            print("Loaded Save Data.")
            return True
        else:
            print("No save detected, using default values.")
            return False

    def write_save_data(self, data):
        with open('./EatThis/savegame.txt', mode='w', encoding='utf-8') as fout:  # Preenche um save inicial em arquivo.
            for linha in range(1):
                fout.write(f'{self.Master_Vol} {self.BGM_Vol} {self.SFX_Vol}')
                fout.write('\n')
