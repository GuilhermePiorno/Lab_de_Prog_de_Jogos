import os


class SaveFile:
    def __init__(self, path):
        self.path = path
        # SOM
        self._Master_vol = 0.5
        self._BGM_vol = 50
        self._SFX_vol = 50
        self.Master_vol = self._Master_vol
        self.BGM_vol = self._BGM_vol
        self.SFX_vol = self._SFX_vol
        # Upgrades Permanentes
        self._has_shoes = 0
        self.has_shoes = self._has_shoes
        # Upgrades Temporários
        self._grip_factor = 1
        self.grip_factor = self._grip_factor
        self._has_bomb_ability = 0
        self.has_bomb_ability = self._has_bomb_ability
        self._max_bombs = 1
        self.max_bombs = self._max_bombs
        self._bomb_range_upgrade = 0
        self.bomb_range_upgrade = self._bomb_range_upgrade
        self.speed_upgrade = 0
        self._has_fireball_ability = 0
        self.has_fireball_ability = self._has_fireball_ability
        self._fireball_ammo = 0
        self.fireball_ammo = self._fireball_ammo
        self._fireball_mult_spd = 1
        self.fireball_mult_spd = self._fireball_mult_spd
        self._vuln_res = 0
        self.vuln_res = self._vuln_res
        # Uso entre fases
        self._stage_no = 1
        self.stage_no = self._stage_no
        self._credits = 0
        self.credits = self._credits

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
            # Linha 1 => [has_shoes]
            self.has_shoes = data[1][0]
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
            fout.write(f'{+self.has_shoes} \n')     # +var faz com que True retorne 1 e False retorne 0
        print("Game was saved.")

    def reset_save_data(self):
        """
        Loads default values into memory.

        :return:
        """
        self.Master_vol = self._Master_vol
        self.BGM_vol = self._BGM_vol
        self.SFX_vol = self._SFX_vol
        self.has_shoes = self._has_shoes

