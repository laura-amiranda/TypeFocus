import random
import pygame
import os
from palavras import LISTA_PALAVRAS_PADRAO
from utils import calcular_pontos

WIDTH, HEIGHT = 360, 360
BG = (18, 8, 28)
ACCENT = (181, 126, 220)
TEXT = (230, 230, 230)


def run_pygame():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('TypeFocus - Quick')
    clock = pygame.time.Clock()

    try:
        font_ui = pygame.font.Font(None, 20)
        font_count = pygame.font.Font(None, 108) 
        font_word = pygame.font.Font(None, 44)    
        font_result = pygame.font.Font(None, 28)  
    except Exception:
        font_ui = pygame.font.SysFont('arial', 18)
        font_count = pygame.font.SysFont('arial', 100)
        font_word = pygame.font.SysFont('arial', 40)
        font_result = pygame.font.SysFont('arial', 26)

    ASSETS_DIR = os.path.join(os.path.dirname(__file__), 'assets')
    menu_bg = None
    bg = None
    result_bg = None
    try:
        for suffix in ('.png', '.jpg', '.jpeg'):
            p = os.path.join(ASSETS_DIR, f'menu_bg{suffix}')
            if os.path.exists(p):
                menu_bg = pygame.image.load(p)
                break
        if menu_bg is None and os.path.isdir(ASSETS_DIR):
            for fname in os.listdir(ASSETS_DIR):
                if fname.lower().startswith('menu_bg'):
                    menu_bg = pygame.image.load(os.path.join(ASSETS_DIR, fname))
                    break

        for suffix in ('.png', '.jpg', '.jpeg'):
            p = os.path.join(ASSETS_DIR, f'bg{suffix}')
            if os.path.exists(p):
                bg = pygame.image.load(p)
                break
        if bg is None and os.path.isdir(ASSETS_DIR):
            for fname in os.listdir(ASSETS_DIR):
                if fname.lower().startswith('bg') and not fname.lower().startswith('bg_'):
                    bg = pygame.image.load(os.path.join(ASSETS_DIR, fname))
                    break

        for suffix in ('.png', '.jpg', '.jpeg'):
            p = os.path.join(ASSETS_DIR, f'result_bg{suffix}')
            if os.path.exists(p):
                result_bg = pygame.image.load(p)
                break
        if result_bg is None and os.path.isdir(ASSETS_DIR):
            for fname in os.listdir(ASSETS_DIR):
                if fname.lower().startswith('result_bg'):
                    result_bg = pygame.image.load(os.path.join(ASSETS_DIR, fname))
                    break
    except Exception:
        menu_bg = menu_bg or None
        bg = bg or None
        result_bg = result_bg or None

    bg = None
    result_bg = None
    try:
        for name in ('bg.png', 'bg.jpg', 'bg.jpeg'):
            p = os.path.join(ASSETS_DIR, name)
            if os.path.exists(p):
                bg = pygame.image.load(p)
                break
        for name in ('result_bg.png', 'result_bg.jpg', 'result_bg.jpeg'):
            p = os.path.join(ASSETS_DIR, name)
            if os.path.exists(p):
                result_bg = pygame.image.load(p)
                break
        if bg is None and os.path.isdir(ASSETS_DIR):
            for fname in os.listdir(ASSETS_DIR):
                if fname.lower().startswith('bg') and not fname.lower().startswith('bg_'):
                    bg = pygame.image.load(os.path.join(ASSETS_DIR, fname))
                    break
        if result_bg is None and os.path.isdir(ASSETS_DIR):
            for fname in os.listdir(ASSETS_DIR):
                if fname.lower().startswith('result_bg'):
                    result_bg = pygame.image.load(os.path.join(ASSETS_DIR, fname))
                    break
    except Exception:
        bg = bg or None
        result_bg = result_bg or None
    countdown_snd = None
    countdown_final_snd = None
    countdown_continuous_snd = None
    try:
        pygame.mixer.init()
        if os.path.isdir(ASSETS_DIR):
            for fname in os.listdir(ASSETS_DIR):
                low = fname.lower()
                if low.startswith('countdown') and low.rsplit('.', 1)[-1] in ('wav', 'ogg', 'mp3'):
                    try:
                        countdown_snd = pygame.mixer.Sound(os.path.join(ASSETS_DIR, fname))
                        break
                    except Exception:
                        countdown_snd = None
            if countdown_snd is None:
                for fname in os.listdir(ASSETS_DIR):
                    if fname.lower().startswith('countdown'):
                        try:
                            countdown_snd = pygame.mixer.Sound(os.path.join(ASSETS_DIR, fname))
                            break
                        except Exception:
                            continue
            for fname in os.listdir(ASSETS_DIR):
                if fname.lower().startswith('countdown_final') and fname.lower().rsplit('.', 1)[-1] in ('wav', 'ogg', 'mp3'):
                    try:
                        countdown_final_snd = pygame.mixer.Sound(os.path.join(ASSETS_DIR, fname))
                        break
                    except Exception:
                        countdown_final_snd = None
            if countdown_final_snd is None:
                for fname in os.listdir(ASSETS_DIR):
                    if fname.lower().startswith('countdown_final'):
                        try:
                            countdown_final_snd = pygame.mixer.Sound(os.path.join(ASSETS_DIR, fname))
                            break
                        except Exception:
                            continue
            for fname in os.listdir(ASSETS_DIR):
                if fname.lower().startswith('countdown_continuous') and fname.lower().rsplit('.', 1)[-1] in ('wav', 'ogg', 'mp3'):
                    try:
                        countdown_continuous_snd = pygame.mixer.Sound(os.path.join(ASSETS_DIR, fname))
                        break
                    except Exception:
                        countdown_continuous_snd = None
            if countdown_continuous_snd is None:
                for fname in os.listdir(ASSETS_DIR):
                    if fname.lower().startswith('countdown_continuous'):
                        try:
                            countdown_continuous_snd = pygame.mixer.Sound(os.path.join(ASSETS_DIR, fname))
                            break
                        except Exception:
                            continue
    except Exception:
        countdown_snd = None
        countdown_final_snd = None

    state = 'menu'
    typed = ''

    EXTRA_PALAVRAS = [
        'python', 'teclado', 'foco', 'rapido', 'janela', 'cores', 'musica', 'vento', 'mar', 'lua', 'sol',
        'estrela', 'nuvem', 'floresta', 'montanha', 'rio', 'cachoeira', 'deserto', 'oceano', 'ilha', 'praia',
        'cidade', 'cidadezinha', 'vila', 'casa', 'apartamento', 'predio', 'rua', 'avenida', 'parque', 'jardim',
        'flor', 'arvore', 'folha', 'raiz', 'fruta', 'legume', 'comida', 'bebida', 'livro', 'caneta', 'lapis',
        'papel', 'mesa', 'cadeira', 'computador', 'celular', 'monitor', 'janelaesquerda', 'telhado', 'balanco',
        'telefone', 'relógio', 'estante', 'armario', 'tapete', 'copo', 'garfo', 'colher', 'cadeirinha'
    ]
    pool = list(LISTA_PALAVRAS_PADRAO) + EXTRA_PALAVRAS
    remaining = pool.copy()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if state == 'menu' and event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    state = 'countdown'
                elif state == 'typing':
                    if event.key == pygame.K_BACKSPACE:
                        typed = typed[:-1]
                    elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        pass
                    else:
                        if event.unicode:
                            typed += event.unicode
                elif state == 'result_wait' and event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):

                    state = 'menu'
                    typed = ''
                    palavra = ''

        screen.fill(BG)
        if state == 'menu':
            if menu_bg:
                try:
                    menu_surf = pygame.transform.smoothscale(menu_bg, (WIDTH, HEIGHT))
                    screen.blit(menu_surf, (0, 0))
                except Exception:
                    screen.fill(BG)
            else:
                screen.fill(BG)

            title = font_word.render(' ', True, ACCENT)
            instr = font_ui.render('Pressione Enter para jogar', True, TEXT)
            screen.blit(title, ((WIDTH - title.get_width()) // 2, 80))
            screen.blit(instr, ((WIDTH - instr.get_width()) // 2, 150))
        elif state == 'countdown':

            for n in (3, 2, 1):
                if bg:
                    try:
                        bgs = pygame.transform.smoothscale(bg, (WIDTH, HEIGHT))
                        screen.blit(bgs, (0, 0))
                    except Exception:
                        screen.fill(BG)
                else:
                    screen.fill(BG)

                txt = font_count.render(str(n), True, ACCENT)
                screen.blit(txt, ((WIDTH - txt.get_width()) // 2,
                                   (HEIGHT - txt.get_height()) // 2))
                try:
                    if countdown_snd:
                        countdown_snd.play()
                except Exception:
                    pass
                pygame.display.flip()
                pygame.time.delay(700)
            try:
                if countdown_continuous_snd:
                    countdown_continuous_snd.play()
                    pygame.time.delay(1200)
                elif countdown_final_snd:
                    countdown_final_snd.play()
                    pygame.time.delay(700)
                elif countdown_snd:
                    countdown_snd.play()
                    pygame.time.delay(200)
                    countdown_snd.play()
                    pygame.time.delay(500)
            except Exception:
                pass

            if not remaining:
                remaining = pool.copy()
            palavra = random.choice(remaining)
            try:
                remaining.remove(palavra)
            except ValueError:
                pass
            typed = ''
            start_ms = pygame.time.get_ticks()
            state = 'typing'

        elif state == 'typing':

            if bg:
                try:
                    bgs = pygame.transform.smoothscale(bg, (WIDTH, HEIGHT))
                    screen.blit(bgs, (0, 0))
                except Exception:
                    screen.fill(BG)
            else:
                screen.fill(BG)

            palavra_surf = font_word.render(palavra, True, TEXT)
            screen.blit(palavra_surf, ((WIDTH - palavra_surf.get_width()) // 2, 60))
            typed_surf = font_ui.render(
                typed + ('|' if (pygame.time.get_ticks() // 400) % 2 == 0 else ''),
                True,
                (200, 200, 200),
            )
            screen.blit(typed_surf, ((WIDTH - typed_surf.get_width()) // 2, 140))


            if typed.strip().lower() == palavra.lower() and typed != '':
                elapsed = (pygame.time.get_ticks() - start_ms) / 1000.0
                pontos = calcular_pontos(elapsed, sem_erros=True, streak=0, bateu_recorde=False)

                result_display = f'Boa! {pontos} pts, em {elapsed:.2f}s'
                state = 'result_wait'

        elif state == 'result_wait':
            if result_bg:
                try:
                    rbs = pygame.transform.smoothscale(result_bg, (WIDTH, HEIGHT))
                    screen.blit(rbs, (0, 0))
                except Exception:
                    screen.fill(BG)
            else:
                screen.fill(BG)

            res = font_result.render(result_display, True, ACCENT)
            hint = font_ui.render('Pressione Enter para retornar', True, TEXT)
            screen.blit(res, ((WIDTH - res.get_width()) // 2, (HEIGHT - res.get_height()) // 2 - 10))
            screen.blit(hint, ((WIDTH - hint.get_width()) // 2, (HEIGHT - res.get_height()) // 2 + 30))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == '__main__':
    run_pygame()
