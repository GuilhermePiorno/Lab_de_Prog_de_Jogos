# #====================== Substituido por save me forma de classes para melhor leitura de código e utilização.
# # Save constants
# VOLUME_SETTINGS = 0  # [master_vol, bgm_vol, sfx_vol]
# MASTER_VOLUME = (0, 0)
# BGM_VOL = (0, 1)
# SFX_VOL = (0, 2)
# UPGRADE_VELOCIDADE = 1  # [nível do upgrade]
# UPGRADE_MEIA_VOLTA = 2  # [nível do upgrade]
# UPGRADE_STATE_CHANGE = 3  # [liga/desliga, cooldown]
# UPGRADE_TIRO = 4  # [liga/desliga]
# BULLET_TIME = 5  # [liga/desliga, duration
#
# def reset_save_data():
#     with open('./EatThis/savegame.txt', mode='w', encoding='utf-8') as fout:  # Preenche um save inicial em arquivo.
#         fout.write('50 50 50\n')
#     print("Save Data Reset.")
#
#
# def read_save_data():
#     data = []
#     with open('./EatThis/savegame.txt', mode='r',
#               encoding='utf-8') as fin:  # Le o save em arquivo e passa para memória.
#         for linha in fin:
#             aux = linha.rstrip('\n')  # retorna uma lista sem os \n
#             data.append(list(map(float, aux.split())))  # aplica float em todos elementos.
#     print("Loaded Save Data.")
#     return data
#
#
# def write_save_data(data):
#     with open('./EatThis/savegame.txt', mode='w', encoding='utf-8') as fout:  # Preenche um save inicial em arquivo.
#         for linha in range(len(data)):
#             for coluna in range(len(data[linha])):
#                 fout.write(f'{data[linha][coluna]} ')
#             fout.write('\n')
#
#
# def access(data, address):
#     return data[address[0]][address[1]]
