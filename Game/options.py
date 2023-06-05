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

    # SFX init.
    sfx_select = Sound('Assets/SFX/Select_0.wav')
    sfx_select.set_volume(50)
    sfx_confirm = Sound('Assets/SFX/Confirm_0.wav')
    sfx_confirm.set_volume(50)
    sfx_cancel = Sound('Assets/SFX/Cancel_0.wav')
    sfx_cancel.set_volume(50)

    # Text init.
    font = pygame.font.Font('Assets/Fonts/MinimalPixel v2.ttf', 30)


    options_items = ["Back", "Volume", "Credits"]
    options_items = [
                        ["Back", "Volume", "Credits"],
                        ["Back", "Master Volume", "BGM Volume", "SFX Volume"],
                        ["Back"]
                    ]

    options_item_text = []
    nav_level = 0
    longest_word = 0
    longest_word_ind = 0
    # for i in range(len(options_items)):
    #     txt = font.render(options_items[nav_level][i], True, 'white')
    #     options_item_text.append(txt)
    #     if len(options_items[nav_level][i]) > longest_word:
    #         longest_word = len(options_items[nav_level][i])
    #         longest_word_ind = i


    # options_volume = ["Master Volume", "BGM Volume", "SFX Volume"]

    # System Variables.
    options_output = 20 # Por equanto apenas o volume, no futuro mais coisas.
    last_input = "return"
    button_state = True
    in_options = True
    option_item_select = 0
    # select = a[select].index('Back')


    while in_options:

        if not button_state:
            if teclado.key_pressed("down"):
                button_state = True
                last_input = "down"
                sfx_select.play()
                option_item_select = (option_item_select + 1) % len(options_items[nav_level])
            if teclado.key_pressed("up"):
                button_state = True
                last_input = "up"
                sfx_select.play()
                option_item_select = (option_item_select - 1) % len(options_items[nav_level])
            if teclado.key_pressed("return"):
                button_state = True
                last_input = "return"
                sfx_confirm.play()
                if options_items[nav_level][option_item_select] == "Back":
                    print("Back selected")
                    if nav_level > 0:
                        # volta nav_level para a "coluna" da opção, como 'back' está sempre na coluna zero. nav_level = 0
                        nav_level = options_items[nav_level].index(options_items[nav_level][option_item_select])
                    else:
                        return options_output
                if options_items[nav_level][option_item_select] == "Volume":
                    # nav_level recebe a "coluna" da opção, como 'volume' é o segundo item da lista, nav_level = 1.
                    nav_level = options_items[nav_level].index(options_items[nav_level][option_item_select])
                    # print(nav_level)
                    option_item_select = 0  # retorna cursor para a primeira opção
                    print("Volume selected")
                if options_items[nav_level][option_item_select] == "Credits":
                    # nav_level recebe a "coluna" da opção, como 'Credits' é o terceiro item da lista, nav_level = 2.
                    nav_level = options_items[nav_level].index(options_items[nav_level][option_item_select])
                    option_item_select = 0  # retorna cursor para a primeira opção
                    print("Credits selected")
            if teclado.key_pressed("ESC"):
                button_state = True
                last_input = "esc"
                sfx_cancel.play()
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

        # renderiza todas as opções da lista option_item_text
        for i in range(len(options_item_text)):
            janela.screen.blit(options_item_text[i], ((janela.width - options_item_text[longest_word_ind].get_width())/ 2, 200 + 50 * i))

        moldura.draw()
        janela.update()


