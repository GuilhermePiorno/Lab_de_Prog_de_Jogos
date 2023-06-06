from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sound import *

def open_options(screen_width, screen_height):
    janela = Window(1280, 720)
    teclado = janela.get_keyboard()

    # Assets init.
    background = GameImage('Assets/Sprites/Options/Options_Background.png')
    moldura = GameImage('Assets/Sprites/Options/moldura.png')
    moldura.set_position((janela.width - moldura.width)/2, (janela.height - moldura.height)/2)

    vol_bar_layer0 = GameImage("Assets/Sprites/Options/Soundbar_00.png")
    vol_bar_layer1 = GameImage("Assets/Sprites/Options/Soundbar_01.png")
    vol_bar_layer2 = GameImage("Assets/Sprites/Options/Soundbar_02.png")

    bar_posx = (janela.width - vol_bar_layer0.width)/2
    bar_posy = (janela.height - vol_bar_layer0.height)/2 - 50
    vol_bar_layer0.set_position(bar_posx, bar_posy)
    vol_bar_layer1.set_position(bar_posx, bar_posy)
    vol_bar_layer2.set_position(bar_posx, bar_posy)

    master_vol = 50
    bgm_vol = 50
    sfx_vol = 50


    # SFX init.
    sfx_select = Sound('Assets/SFX/Select_0.wav')
    sfx_select.set_volume(sfx_vol)
    sfx_confirm = Sound('Assets/SFX/Confirm_0.wav')
    sfx_confirm.set_volume(sfx_vol)
    sfx_cancel = Sound('Assets/SFX/Cancel_0.wav')
    sfx_cancel.set_volume(sfx_vol)

    # Text init.
    font = pygame.font.Font('Assets/Fonts/MinimalPixel v2.ttf', 30)


    options_items = [
                        ["Back", "Volume", "Credits"],
                        ["Back", "Master Volume", "BGM Volume", "SFX Volume"],
                        ["Back"]
                    ]

    nav_level = 0


    # System Variables.
    options_output = 20 # Por equanto apenas o volume, no futuro mais coisas.
    last_input = "return"
    button_state = True
    in_options = True
    option_item_select = 0
    controlling_master_volume = False
    controlling_SFX_volume = False
    controlling_BGM_volume = False



    while in_options:
        sfx_select.set_volume(sfx_vol)
        sfx_confirm.set_volume(sfx_vol)
        sfx_cancel.set_volume(sfx_vol)


        if not button_state:
            if teclado.key_pressed("down"):
                if controlling_master_volume or controlling_SFX_volume or controlling_BGM_volume:
                    button_state = True
                    last_input = "down"
                    sfx_select.play()
                    if controlling_master_volume:   # controle do volume "master"
                        master_vol -= 10
                        if master_vol < 0:
                            master_vol = 0
                    if controlling_BGM_volume:   # controle do volume "BGM"
                        bgm_vol -= 10
                        if bgm_vol < 0:
                            bgm_vol = 0
                    if controlling_SFX_volume:   # controle do volume "SFX"
                        sfx_vol -= 10
                        if sfx_vol < 0:
                            sfx_vol = 0
                else:
                    button_state = True
                    last_input = "down"
                    sfx_select.play()
                    option_item_select = (option_item_select + 1) % len(options_items[nav_level])
            if teclado.key_pressed("up"):
                if controlling_master_volume or controlling_SFX_volume or controlling_BGM_volume:
                    button_state = True
                    last_input = "up"
                    sfx_select.play()
                    if controlling_master_volume:  # controle do volume "master"
                        master_vol += 10
                        if master_vol > 100:
                            master_vol = 100
                    if controlling_BGM_volume:   # controle do volume "BGM"
                        bgm_vol += 10
                        if bgm_vol > 100:
                            bgm_vol = 100
                    if controlling_SFX_volume:   # controle do volume "SFX"
                        sfx_vol += 10
                        if sfx_vol > 100:
                            sfx_vol = 100
                else:
                    button_state = True
                    last_input = "up"
                    sfx_select.play()
                    option_item_select = (option_item_select - 1) % len(options_items[nav_level])
            if teclado.key_pressed("left"):
                if controlling_master_volume or controlling_SFX_volume or controlling_BGM_volume:
                    button_state = True
                    last_input = "left"
                    sfx_select.play()
                    if controlling_master_volume:  # controle do volume "master"
                        master_vol -= 1
                        if master_vol < 0:
                            master_vol = 0
                    if controlling_BGM_volume:   # controle do volume "BGM"
                        bgm_vol -= 1
                        if bgm_vol < 0:
                            bgm_vol = 0
                    if controlling_SFX_volume:   # controle do volume "SFX"
                        sfx_vol -= 1
                        if sfx_vol < 0:
                            sfx_vol = 0

            if teclado.key_pressed("right"):
                if controlling_master_volume or controlling_SFX_volume or controlling_BGM_volume:
                    button_state = True
                    last_input = "right"
                    sfx_select.play()
                    if controlling_master_volume:  # controle do volume "master"
                        master_vol += 1
                        if master_vol > 100:
                            master_vol = 100
                    if controlling_BGM_volume:   # controle do volume "BGM"
                        bgm_vol += 1
                        if bgm_vol > 100:
                            bgm_vol = 100
                    if controlling_SFX_volume:   # controle do volume "SFX"
                        sfx_vol += 1
                        if sfx_vol > 100:
                            sfx_vol = 100

            if teclado.key_pressed("return"):
                button_state = True
                last_input = "return"
                if options_items[nav_level][option_item_select] == "Back":
                    print("Back selected")
                    sfx_cancel.play()
                    if nav_level > 0:
                        # volta nav_level para a "coluna" da opção, como 'back' está sempre na coluna zero. nav_level = 0
                        nav_level = options_items[nav_level].index(options_items[nav_level][option_item_select])
                    else:
                        return options_output
                if options_items[nav_level][option_item_select] == "Volume":
                    sfx_confirm.play()
                    # nav_level recebe a "coluna" da opção, como 'volume' é o segundo item da lista, nav_level = 1.
                    nav_level = options_items[nav_level].index(options_items[nav_level][option_item_select])
                    option_item_select = 0  # retorna cursor para a primeira opção
                    print("Volume selected")
                if options_items[nav_level][option_item_select] == "Credits":
                    sfx_confirm.play()
                    # nav_level recebe a "coluna" da opção, como 'Credits' é o terceiro item da lista, nav_level = 2.
                    nav_level = options_items[nav_level].index(options_items[nav_level][option_item_select])
                    option_item_select = 0  # retorna cursor para a primeira opção
                    print("Credits selected")
                if options_items[nav_level][option_item_select] == "Master Volume":
                    sfx_confirm.play()
                    controlling_master_volume = not controlling_master_volume
                if options_items[nav_level][option_item_select] == "BGM Volume":
                    sfx_confirm.play()
                    controlling_BGM_volume = not controlling_BGM_volume
                if options_items[nav_level][option_item_select] == "SFX Volume":
                    sfx_confirm.play()
                    controlling_SFX_volume = not controlling_SFX_volume

            if teclado.key_pressed("ESC"):
                button_state = True
                last_input = "esc"
                sfx_cancel.play()
                if controlling_SFX_volume or controlling_master_volume or controlling_BGM_volume:
                    controlling_master_volume = controlling_SFX_volume = controlling_BGM_volume = False
                else:
                    if nav_level > 0:
                        option_item_select = 0  # retorna cursor para a primeira opção
                        nav_level = 0           # Volta ao inicio do options (pode ser feito porque nenhum menu tem mais de 1 de profundidade)
                    else:
                        return options_output

        if not teclado.key_pressed(last_input):
            button_state = False

        longest_word = 0
        longest_word_ind = 0
        # Item select highlight
        options_item_text = []
        # varre as opções de acordo com nav_level e armazena-as em na lista option_item_text.
        for i in range(len(options_items[nav_level])):
            if option_item_select == i:
                txt = font.render(options_items[nav_level][i], True, 'yellow')
            else:
                txt = font.render(options_items[nav_level][i], True, 'white')
            options_item_text.append(txt)
            # Armazena o maior tamanho de texto para centralização do menu.
            if len(options_items[nav_level][i]) > longest_word:
                longest_word = len(options_items[nav_level][i])
                longest_word_ind = i


        # Draws
        background.draw()
        if controlling_master_volume:
            for i in range(len(options_item_text)):
                space = 0
                if i >= 2:
                    space = 50
                janela.screen.blit(options_item_text[i],
                                   ((janela.width - options_item_text[longest_word_ind].get_width()) / 2,
                                    space + 200 + 50 * i))
            vol_bar_layer0.set_position(bar_posx, bar_posy)
            vol_bar_layer0.draw()
            vol_bar_layer1.set_position(bar_posx + 2.06 *  master_vol, bar_posy) # 0 a 206
            vol_bar_layer1.draw()
            vol_bar_layer2.set_position(bar_posx, bar_posy)
            vol_bar_layer2.draw()
        elif controlling_BGM_volume:
            for i in range(len(options_item_text)):
                space = 0
                if i >= 3:
                    space = 50
                janela.screen.blit(options_item_text[i],
                                   ((janela.width - options_item_text[longest_word_ind].get_width()) / 2,
                                    space + 200 + 50 * i))
            vol_bar_layer0.set_position(bar_posx, bar_posy + 50)
            vol_bar_layer0.draw()
            vol_bar_layer1.set_position(bar_posx + 2.06 * bgm_vol, bar_posy + 50)  # 0 a 206
            vol_bar_layer1.draw()
            vol_bar_layer2.set_position(bar_posx, bar_posy + 50)
            vol_bar_layer2.draw()

        elif controlling_SFX_volume:
            for i in range(len(options_item_text)):
                janela.screen.blit(options_item_text[i],
                                   ((janela.width - options_item_text[longest_word_ind].get_width()) / 2,
                                    200 + 50 * i))
            vol_bar_layer0.set_position(bar_posx, bar_posy + 100)
            vol_bar_layer0.draw()
            vol_bar_layer1.set_position(bar_posx + 2.06 * sfx_vol, bar_posy + 100)  # 0 a 206
            vol_bar_layer1.draw()
            vol_bar_layer2.set_position(bar_posx, bar_posy + 100)
            vol_bar_layer2.draw()
        else:
            # renderiza todas as opções da lista option_item_text
            for i in range(len(options_item_text)):
                janela.screen.blit(options_item_text[i],
                                   ((janela.width - options_item_text[longest_word_ind].get_width())/ 2,
                                    200 + 50 * i))

        moldura.draw()
        janela.update()


