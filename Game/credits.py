from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sound import *

def play_credits(screen_width, screen_height, save):
    janela = Window(screen_width, screen_height)
    janela.set_title("Credits")
    teclado = janela.get_keyboard()
    credits_song = Sound("Assets/Music/Pac-Man_You_Had_Me_at_Yellow_OC_ReMix.ogg")
    credits_song.set_volume(save.BGM_vol * save.Master_vol)
    credits_song.play()

    esc_pressed = False
    credits_clock = 0

    medium_font = pygame.font.Font('Assets/Fonts/MinimalPixel v2.ttf', 30)
    small_font = pygame.font.Font('Assets/Fonts/MinimalPixel v2.ttf', 20)


    thanks_list = [['Sound Effects',
                   'InterFace SFX Pack 1  by  ObsydianX',
                   'INTERFACE BLEEPS  by  Bleeoop',
                   '8 bit - 16 bit sound effects pack  by  JDWasabi'],
                   ['Sprites',
                    'Cryo\'s Mini GUI by PaperHatLizard',
                    'Shikashi\'s Fantasy Icons Pack by cheekyinkling',
                    'HylianAngel from The Spriters Resource',
                    'Phongpon from The Spriters Resource',
                    '2D Spaceships from MSGDI'
                    'Cockpit by vectorpouch on freepik'],
                   ['Font',
                    'MinimalPixel Font by Mounir Tohami'],
                   ['Music',
                    'Bortcle - ReMix:Pac-Man \"You Had Me at Yellow\"',
                    'Dubmood - FLCTR4 (feat. Zabutom)',
                    'Kenet & Rez - Unreal Super Hero 3',
                    'Ben Prunty - Lanius',
                    'Rainbowdragoneyes - The Arcane Golem',
                    'Rainbowdragoneyes - The Bat Matriarch',
                    'Toby Fox - Once Upon a Time']
                   ]
    us = [
        ['Programmers',
         'Guilherme Y. H. Piorno',
         'Mauricio P. Davis'],
        ['Lead creator of unfinished git branches',
         'Guilherme Y. H. Piorno'],
        ['Lead \"But what if we make it using Classes instead?\"',
         'Mauricio P. Davis']
    ]

    final_credit = 'Thank you for playing!'


    credits_speed = 25
    pull_text = janela.height
    while True:
        janela.set_background_color('black')
        dt = janela.delta_time()
        if dt > 0.1:
            dt = 0
        credits_clock += dt


        if not teclado.key_pressed("ESC") and esc_pressed:
            credits_song.stop()
            return
        if teclado.key_pressed("ESC"):
            esc_pressed = True

        delay = 2

        if credits_clock > delay:
            pull_text -= credits_speed*dt
            # print(pull_text)
            spacing = [0, 300, 700, 900]
            for blk in range(len(thanks_list)):
                block = [medium_font.render(thanks_list[blk][0], True, 'blue')]
                for i in range(1, len(thanks_list[blk])):
                    block.append(medium_font.render(thanks_list[blk][i], True, 'white'))

                for i in range(0, len(block)):
                    pos_x = 0.5 * (janela.width - block[i].get_width())
                    pos_y = spacing[blk] + pull_text  +  50 * i
                    janela.screen.blit(block[i], (pos_x, pos_y))


            if pull_text <= -1388:
                pull_text = -1388

            other_spacing = [600, 800, 950]
            for blk in range(len(us)):
                block = [medium_font.render(us[blk][0], True, 'blue')]
                for i in range(1, len(us[blk])):
                    block.append(medium_font.render(us[blk][i], True, 'white'))

                for i in range(0, len(block)):
                    pos_x = 0.5 * (janela.width - block[i].get_width())
                    pos_y = other_spacing[blk] + spacing[-1] + pull_text  +  50 * i
                    janela.screen.blit(block[i], (pos_x, pos_y))


            final_credit_surface = medium_font.render(final_credit, True, 'red')
            fpos_x = 0.5 * (janela.width - final_credit_surface.get_width())
            fpos_y = spacing[-1] + pull_text  + 1100
            janela.screen.blit(final_credit_surface, (fpos_x, fpos_y))


        janela.update()
