import os


class SaveFile:
    def __init__(self, path):
        self.path = path
        # Variáveis internas para armazenar valores padrão de inicialização. (usado para restar save)
        self._Master_vol = 0.5
        self._BGM_vol = 50
        self._SFX_vol = 50
        self.Master_vol = self._Master_vol
        self.BGM_vol = self._BGM_vol
        self.SFX_vol = self._SFX_vol

    def read_save_from_file(self):
        """
        Loads data from file to memory.
        Returns True if the save game is present on path, False if it's not.

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
            self.Master_vol = data[0][0]
            self.BGM_vol = data[0][1]
            self.SFX_vol = data[0][2]
            # Linha 1 => ??
            print("Loaded Save Data.")
            return True
        else:
            print("No save detected, using default values.")
            return False

    def write_save_to_file(self):
        """
        Writes data from memory into the file.
        :return:
        """
        with open('./EatThis/savegame.txt', mode='w', encoding='utf-8') as fout:
            fout.write(f'{self.Master_vol} {self.BGM_vol} {self.SFX_vol} \n')
        print("Game was saved.")

    def reset_save_data(self):
        """
        Loads default values into memory.

        :return:
        """
        self.Master_vol = self._Master_vol
        self.BGM_vol = self._BGM_vol
        self.SFX_vol = self._SFX_vol
