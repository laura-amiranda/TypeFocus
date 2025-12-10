import random
import pygame
import os
import json
from datetime import datetime
from palavras import (LISTA_PALAVRAS_PADRAO, PALAVRAS_POR_NIVEL, PALAVRAS_INGLES, PALABRAS_ESPANOL)
from utils import calcular_pontos
from crud import carregar_jogadores, salvar_jogadores, validar_nome, validar_idade

WIDTH, HEIGHT = 800, 800
BG = (18, 8, 28)
ACCENT = (106, 13, 173)
ACCENT_LIGHT = (181, 126, 220)
TEXT = (230, 230, 230)
TEXT_DIM = (150, 150, 150)
ERROR_COLOR = (220, 50, 50)
SUCCESS_COLOR = (50, 220, 100)

HISTORICO_ARQUIVO = "historico.json"

class Botao:
    def __init__(self, x, y, width, height, text, font, color=ACCENT, hover_color=ACCENT_LIGHT, text_color=TEXT):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.hovered = False
    
    def desenhar(self, screen):
        color = self.hover_color if self.hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, TEXT, self.rect, width=2, border_radius=10)
        
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
    
    def processar_evento(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

class CampoTexto:
    def __init__(self, x, y, width, height, font, placeholder="", max_length=30):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.placeholder = placeholder
        self.text = ""
        self.max_length = max_length
        self.active = False
        self.cursor_visible = True
        self.cursor_timer = 0
    
    def desenhar(self, screen):
        color = ACCENT_LIGHT if self.active else TEXT_DIM
        pygame.draw.rect(screen, BG, self.rect)
        pygame.draw.rect(screen, color, self.rect, width=2)
        
        display_text = self.text if self.text else self.placeholder
        text_color = TEXT if self.text else TEXT_DIM
        text_surf = self.font.render(display_text, True, text_color)
        screen.blit(text_surf, (self.rect.x + 10, self.rect.y + (self.rect.height - text_surf.get_height()) // 2))
        
        if self.active and self.cursor_visible and self.text:
            cursor_x = self.rect.x + 10 + self.font.size(self.text)[0]
            pygame.draw.line(screen, TEXT, (cursor_x, self.rect.y + 5), 
                           (cursor_x, self.rect.y + self.rect.height - 5), 2)
    
    def processar_evento(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                return 'submit'
            elif len(self.text) < self.max_length and event.unicode.isprintable():
                self.text += event.unicode
        return None
    
    def atualizar(self):
        self.cursor_timer += 1
        if self.cursor_timer >= 30:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0

class TypeFocusGUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('TypeFocus')
        self.clock = pygame.time.Clock()
        self.font_title = pygame.font.Font(None, 72)
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        self.font_tiny = pygame.font.Font(None, 18)
        self.assets_dir = os.path.join(os.path.dirname(__file__), 'assets')
        self.backgrounds = self.carregar_fundos()
        self.sounds = self.carregar_sons()
        self.state = 'menu'
        self.running = True
        self.current_player = None
        self.player_name = ""
        self.idioma = 'pt'
        self.nivel = 'padrao'
        self.palavra_atual = ""
        self.typed_text = ""
        self.start_time = 0
        self.streak = 0
        self.palavras_disponiveis = []
        self.ranking_sessao = []
        self.last_result = {}
        self.input_fields = {}
        self.buttons = {}
        self.error_message = ""
        self.scroll_offset = 0
        self.mascote_x = -100
        self.mascote_y = 0
        self.mascote_bounce = 0
        self.mascote_direction = 1
        self.mascote_frame = 1
        self.mascote_frame_timer = 0
        
    def carregar_fundos(self):
        bgs = {}
        bg_names = ['menu_bg', 'cadastro-idioma_bg', 'bg', 'result_bg']      
        for name in bg_names:
            for ext in ['.jpg', '.png', '.jpeg']:
                path = os.path.join(self.assets_dir, name + ext)
                if os.path.exists(path):
                    try:
                        bgs[name] = pygame.image.load(path)
                        break
                    except Exception:
                        pass       
        for i in range(1, 4):
            for ext in ['.png', '.jpg', '.jpeg']:
                frame_path = os.path.join(self.assets_dir, f'typebot_frame{i}' + ext)
                if os.path.exists(frame_path):
                    try:
                        bgs[f'typebot_frame{i}'] = pygame.image.load(frame_path)
                        break
                    except Exception:
                        pass  
        return bgs
    
    def carregar_sons(self):
        sounds = {}
        try:
            pygame.mixer.init()
            sound_names = ['countdown', 'countdown_final', 'countdown_continuous']
            for name in sound_names:
                for ext in ['.wav', '.ogg', '.mp3']:
                    path = os.path.join(self.assets_dir, name + ext)
                    if os.path.exists(path):
                        try:
                            sounds[name] = pygame.mixer.Sound(path)
                            break
                        except Exception:
                            pass
        except Exception:
            pass
        return sounds
    
    def desenhar_fundo(self, bg_name='menu_bg'):
        if bg_name in self.backgrounds:
            try:
                bg_surf = pygame.transform.smoothscale(self.backgrounds[bg_name], (WIDTH, HEIGHT))
                self.screen.blit(bg_surf, (0, 0))
            except Exception:
                self.screen.fill(BG)
        else:
            self.screen.fill(BG)
    
    def desenhar_titulo(self, y=80):
        title = self.font_title.render('TypeFocus', True, ACCENT)
        self.screen.blit(title, ((WIDTH - title.get_width()) // 2, y))
    
    def registrar_historico(self, registro):
        try:
            if os.path.exists(HISTORICO_ARQUIVO):
                with open(HISTORICO_ARQUIVO, 'r', encoding='utf-8') as f:
                    historico = json.load(f)
            else:
                historico = []
            
            historico.append(registro)
            
            with open(HISTORICO_ARQUIVO, 'w', encoding='utf-8') as f:
                json.dump(historico, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar histórico: {e}")
    
    def atualizar_estatisticas_jogador(self, nome, tempo):
        jogadores = carregar_jogadores()
        if nome in jogadores:
            p = jogadores[nome]
            p['partidas'] = p.get('partidas', 0) + 1
            p['total_tempo'] = p.get('total_tempo', 0.0) + tempo         
            bateu_recorde = False
            if (p.get('melhor_tempo') is None) or (tempo < p.get('melhor_tempo')):
                p['melhor_tempo'] = tempo
                bateu_recorde = True           
            jogadores[nome] = p
            salvar_jogadores(jogadores)
            return bateu_recorde, p
        return False, None
    
    def processar_estado_menu(self):
        self.desenhar_fundo('menu_bg')
        if 'menu' not in self.buttons:
            button_width = 300
            button_height = 50
            start_y = 200
            spacing = 70           
            menu_options = [
                ('play', 'Jogar'),
                ('edit', 'Editar Cadastro'),
                ('delete', 'Deletar Cadastro'),
                ('ranking_session', 'Ranking da Sessão'),
                ('ranking_history', 'Ranking Histórico'),
                ('exit', 'Sair')]           
            self.buttons['menu'] = {}
            for i, (key, text) in enumerate(menu_options):
                x = (WIDTH - button_width) // 2
                y = start_y + i * spacing
                self.buttons['menu'][key] = Botao(x, y, button_width, button_height, text, self.font_small)
        for btn in self.buttons['menu'].values():
            btn.desenhar(self.screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False         
            for key, btn in self.buttons['menu'].items():
                if btn.processar_evento(event):
                    if key == 'play':
                        self.state = 'login'
                        self.buttons.pop('menu', None)
                    elif key == 'edit':
                        self.state = 'edit_player'
                        self.buttons.pop('menu', None)
                    elif key == 'delete':
                        self.state = 'delete_player'
                        self.buttons.pop('menu', None)
                    elif key == 'ranking_session':
                        self.state = 'ranking_session'
                        self.buttons.pop('menu', None)
                    elif key == 'ranking_history':
                        self.state = 'ranking_history'
                        self.buttons.pop('menu', None)
                    elif key == 'exit':
                        self.running = False
    
    def processar_estado_login(self):
        self.desenhar_fundo('cadastro-idioma_bg')
        if 'login' not in self.input_fields:
            self.input_fields['login'] = {
                'nome': CampoTexto(200, 200, 400, 50, self.font_small, "Nome completo", 30),
                'idade': CampoTexto(200, 280, 400, 50, self.font_small, "Idade", 3),
                'tdah': CampoTexto(200, 360, 400, 50, self.font_small, "TDAH? (s/n)", 1)
            }    
            self.buttons['login'] = {
                'submit': Botao(250, 480, 150, 50, 'Entrar', self.font_small),
                'back': Botao(420, 480, 130, 50, 'Voltar', self.font_small)
            }
        labels = [
            ('Nome:', 200, 170),
            ('Idade:', 200, 250),
            ('TDAH:', 200, 330)
        ]
        for text, x, y in labels:
            surf = self.font_small.render(text, True, TEXT)
            self.screen.blit(surf, (x, y))
        for field in self.input_fields['login'].values():
            field.desenhar(self.screen)
            field.atualizar()
        for btn in self.buttons['login'].values():
            btn.desenhar(self.screen)
        if self.error_message:
            error_surf = self.font_tiny.render(self.error_message, True, ERROR_COLOR)
            self.screen.blit(error_surf, ((WIDTH - error_surf.get_width()) // 2, 440))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if 'login' in self.input_fields:
                for field in self.input_fields['login'].values():
                    if field.processar_evento(event) == 'submit':
                        self.processar_login()
            login_buttons = self.buttons.get('login', {})
            if login_buttons:
                if login_buttons.get('submit') and login_buttons['submit'].processar_evento(event):
                    self.processar_login()              
                if login_buttons.get('back') and login_buttons['back'].processar_evento(event):
                    self.state = 'menu'
                    self.input_fields.pop('login', None)
                    self.buttons.pop('login', None)
                    self.error_message = ""
    
    def processar_login(self):
        nome = self.input_fields['login']['nome'].text.strip().title()
        idade = self.input_fields['login']['idade'].text.strip()
        tdah = self.input_fields['login']['tdah'].text.strip().lower()
        if not nome:
            self.error_message = "Nome não pode ficar vazio"
            return       
        if not validar_nome(nome):
            self.error_message = "Nome deve conter apenas letras"
            return       
        jogadores = carregar_jogadores()
        if nome in jogadores:
            self.current_player = jogadores[nome]
            self.player_name = nome
            self.error_message = ""
            self.state = 'language_select'
            self.input_fields.pop('login', None)
            self.buttons.pop('login', None)
            return
        if not idade:
            self.error_message = "Digite a idade"
            return       
        if not validar_idade(idade):
            self.error_message = "Idade deve ser um número válido"
            return      
        if tdah not in ['s', 'n']:
            self.error_message = "Digite 's' para sim ou 'n' para não (TDAH)"
            return
        jogadores[nome] = {
            "nome": nome,
            "idade": int(idade),
            "tdah": True if tdah == "s" else False,
            "melhor_tempo": None,
            "partidas": 0,
            "total_tempo": 0.0
        }
        salvar_jogadores(jogadores)      
        self.current_player = jogadores[nome]
        self.player_name = nome
        self.error_message = ""
        self.state = 'language_select'
        self.input_fields.pop('login', None)
        self.buttons.pop('login', None)
    
    def processar_estado_selecao_idioma(self):
        self.desenhar_fundo('cadastro-idioma_bg')
        subtitle = self.font_medium.render('Escolha o idioma', True, TEXT)
        self.screen.blit(subtitle, ((WIDTH - subtitle.get_width()) // 2, 160))
        if 'language' not in self.buttons:
            button_width = 250
            button_height = 60
            start_y = 280
            spacing = 90          
            languages = [
                ('pt', 'Português'),
                ('en', 'English'),
                ('es', 'Español')
            ]           
            self.buttons['language'] = {}
            for i, (key, text) in enumerate(languages):
                x = (WIDTH - button_width) // 2
                y = start_y + i * spacing
                self.buttons['language'][key] = Botao(x, y, button_width, button_height, 
                                                       text, self.font_medium)
            self.buttons['language']['back'] = Botao(325, 650, 150, 50, 'Voltar', self.font_small)
        for btn in self.buttons['language'].values():
            btn.desenhar(self.screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False        
            for key, btn in self.buttons['language'].items():
                if btn.processar_evento(event):
                    if key in ['pt', 'en', 'es']:
                        self.idioma = key
                        self.state = 'difficulty_select'
                        self.buttons.pop('language', None)
                    elif key == 'back':
                        self.state = 'menu'
                        self.buttons.pop('language', None)
    
    def processar_estado_selecao_dificuldade(self):
        self.desenhar_fundo('cadastro-idioma_bg')
        subtitles = {
            'pt': 'Escolha a dificuldade',
            'en': 'Choose difficulty',
            'es': 'Elige la dificultad'
        }
        subtitle = self.font_medium.render(subtitles.get(self.idioma, subtitles['pt']), True, TEXT)
        self.screen.blit(subtitle, ((WIDTH - subtitle.get_width()) // 2, 160))
        if 'difficulty' not in self.buttons:
            button_width = 250
            button_height = 60
            start_y = 260
            spacing = 75         
            difficulties = [
                ('facil', {'pt': 'Fácil', 'en': 'Easy', 'es': 'Fácil'}),
                ('medio', {'pt': 'Médio', 'en': 'Medium', 'es': 'Medio'}),
                ('dificil', {'pt': 'Difícil', 'en': 'Hard', 'es': 'Difícil'}),
                ('padrao', {'pt': 'Padrão', 'en': 'Standard', 'es': 'Estándar'})
            ]         
            self.buttons['difficulty'] = {}
            for i, (key, texts) in enumerate(difficulties):
                x = (WIDTH - button_width) // 2
                y = start_y + i * spacing
                text = texts.get(self.idioma, texts['pt'])
                self.buttons['difficulty'][key] = Botao(x, y, button_width, button_height, 
                                                         text, self.font_small)
            self.buttons['difficulty']['back'] = Botao(325, 650, 150, 50, 'Voltar', self.font_small)
        for btn in self.buttons['difficulty'].values():
            btn.desenhar(self.screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False         
            for key, btn in self.buttons['difficulty'].items():
                if btn.processar_evento(event):
                    if key in ['facil', 'medio', 'dificil', 'padrao']:
                        self.nivel = key
                        self.preparar_jogo()
                        self.state = 'countdown'
                        self.buttons.pop('difficulty', None)
                    elif key == 'back':
                        self.state = 'language_select'
                        self.buttons.pop('difficulty', None)
    
    def preparar_jogo(self):
        if self.idioma == 'en':
            if self.nivel == 'padrao':
                self.palavras_disponiveis = []
                for words in PALAVRAS_INGLES.values():
                    self.palavras_disponiveis.extend(words)
            else:
                self.palavras_disponiveis = PALAVRAS_INGLES.get(self.nivel, []).copy()
        elif self.idioma == 'es':
            if self.nivel == 'padrao':
                self.palavras_disponiveis = []
                for words in PALABRAS_ESPANOL.values():
                    self.palavras_disponiveis.extend(words)
            else:
                self.palavras_disponiveis = PALABRAS_ESPANOL.get(self.nivel, []).copy()
        else:
            if self.nivel == 'padrao':
                self.palavras_disponiveis = LISTA_PALAVRAS_PADRAO.copy()
            else:
                self.palavras_disponiveis = PALAVRAS_POR_NIVEL.get(self.nivel, []).copy()
    
    def processar_estado_contagem(self):
        self.desenhar_fundo('bg')
        elapsed = pygame.time.get_ticks() - getattr(self, 'countdown_start', pygame.time.get_ticks())     
        if not hasattr(self, 'countdown_start'):
            self.countdown_start = pygame.time.get_ticks()
            self.countdown_stage = 3
            if 'countdown' in self.sounds:
                self.sounds['countdown'].play()     
        if elapsed > 700:
            self.countdown_stage -= 1
            self.countdown_start = pygame.time.get_ticks()        
            if self.countdown_stage > 0:
                if 'countdown' in self.sounds:
                    self.sounds['countdown'].play()
            elif self.countdown_stage == 0:
                if 'countdown_continuous' in self.sounds:
                    self.sounds['countdown_continuous'].play()
                elif 'countdown_final' in self.sounds:
                    self.sounds['countdown_final'].play()     
        if self.countdown_stage > 0:
            count_text = self.font_large.render(str(self.countdown_stage), True, ACCENT)
            self.screen.blit(count_text, ((WIDTH - count_text.get_width()) // 2, 
                                         (HEIGHT - count_text.get_height()) // 2))
        else:
            if not self.palavras_disponiveis:
                self.preparar_jogo()        
            if self.palavras_disponiveis:
                self.palavra_atual = random.choice(self.palavras_disponiveis)
                self.palavras_disponiveis.remove(self.palavra_atual)
            else:
                self.palavra_atual = "python"          
            self.typed_text = ""
            self.start_time = pygame.time.get_ticks()
            self.state = 'typing'
            delattr(self, 'countdown_start')
            delattr(self, 'countdown_stage')
    
    def processar_estado_digitacao(self):
        self.desenhar_fundo('bg')
        word_surf = self.font_large.render(self.palavra_atual, True, TEXT)
        self.screen.blit(word_surf, ((WIDTH - word_surf.get_width()) // 2, 200))
        typed_display = ""
        correct = True
        for i, char in enumerate(self.typed_text):
            if i < len(self.palavra_atual) and char.lower() == self.palavra_atual[i].lower():
                typed_display += char
            else:
                correct = False
                break      
        typed_color = SUCCESS_COLOR if correct else ERROR_COLOR
        typed_surf = self.font_medium.render(self.typed_text + '|', True, typed_color)
        self.screen.blit(typed_surf, ((WIDTH - typed_surf.get_width()) // 2, 300))
        elapsed = (pygame.time.get_ticks() - self.start_time) / 1000.0
        time_surf = self.font_small.render(f'Tempo: {elapsed:.1f}s', True, TEXT_DIM)
        self.screen.blit(time_surf, (50, 50))     
        streak_surf = self.font_small.render(f'Combo: {self.streak}', True, ACCENT_LIGHT)
        self.screen.blit(streak_surf, (WIDTH - 200, 50))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.typed_text = self.typed_text[:-1]
                elif event.key == pygame.K_ESCAPE:
                    self.state = 'menu'
                    self.typed_text = ""
                elif event.unicode and event.unicode.isprintable():
                    self.typed_text += event.unicode
                    if self.typed_text.lower() == self.palavra_atual.lower():
                        self.finalizar_rodada(elapsed, correct)
    
    def finalizar_rodada(self, tempo, sem_erros):
        bateu_recorde, jogador_info = self.atualizar_estatisticas_jogador(self.player_name, tempo)
        pontos = calcular_pontos(tempo, sem_erros=sem_erros, streak=self.streak, bateu_recorde=bateu_recorde)
        if sem_erros:
            self.streak += 1
        else:
            self.streak = 0
        self.ranking_sessao.append({
            "nome": self.player_name,
            "pontos": pontos,
            "palavra": self.palavra_atual,
            "tempo": tempo,
            "streak": self.streak
        })
        registro = {
            "nome": self.player_name,
            "idioma": "ingles" if self.idioma == 'en' else ("espanhol" if self.idioma == 'es' else "portugues"),
            "nivel": self.nivel,
            "palavra": self.palavra_atual,
            "tempo": tempo,
            "pontos": pontos,
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "streak": self.streak,
            "feedback": ""
        }
        self.registrar_historico(registro)
        self.last_result = {
            'tempo': tempo,
            'pontos': pontos,
            'streak': self.streak,
            'bateu_recorde': bateu_recorde,
            'palavra': self.palavra_atual
        }
        self.state = 'result'
        self.typed_text = ""
    
    def processar_estado_resultado(self):
        self.desenhar_fundo('bg')     
        if 'typebot_frame1' in self.backgrounds:
            import math
            self.mascote_x += 3 * self.mascote_direction
            self.mascote_bounce = abs(math.sin(pygame.time.get_ticks() * 0.01)) * 20         
            if self.mascote_x > WIDTH:
                self.mascote_x = -100         
            self.mascote_frame_timer += 1
            if self.mascote_frame_timer >= 10:
                self.mascote_frame = (self.mascote_frame % 3) + 1
                self.mascote_frame_timer = 0          
            mascote_img = self.backgrounds.get(f'typebot_frame{self.mascote_frame}')
            if mascote_img:
                mascote_scale = 120
                mascote_scaled = pygame.transform.smoothscale(mascote_img, (mascote_scale, mascote_scale))             
                if self.mascote_direction < 0:
                    mascote_scaled = pygame.transform.flip(mascote_scaled, True, False)             
                self.screen.blit(mascote_scaled, (int(self.mascote_x), int(HEIGHT - 130 - self.mascote_bounce)))     
        titles = {
            'pt': 'Resultado',
            'en': 'Result',
            'es': 'Resultado'
        }
        title = self.font_large.render(titles.get(self.idioma, titles['pt']), True, ACCENT)
        self.screen.blit(title, ((WIDTH - title.get_width()) // 2, 80))
        y = 180
        result_texts = [
            f"Palavra: {self.last_result.get('palavra', '')}",
            f"Tempo: {self.last_result.get('tempo', 0):.2f}s",
            f"Pontos: {self.last_result.get('pontos', 0)}",
            f"Combo: {self.last_result.get('streak', 0)}",
        ]   
        if self.last_result.get('bateu_recorde', False):
            result_texts.append(" NOVO RECORDE! ")
        
        tempo_total = self.last_result.get('tempo', 0)
        acertou = self.last_result.get('pontos', 0) > 0
        if acertou:
            if tempo_total < 2:
                msg = {"pt": "Reflexo incrível! Continue assim!", "en": "Lightning reflex! Keep it up!", "es": "¡Reflejo increíble! ¡Sigue así!"}
            elif tempo_total < 4:
                msg = {"pt": "Mandou bem, continue!", "en": "Nice! Keep going!", "es": "¡Buen trabajo! ¡Sigue así!"}
            elif tempo_total < 6:
                msg = {"pt": "Tá indo bem, mas pode ser mais rápido.", "en": "You're doing well, but you can be faster.", "es": "Vas bien, pero puedes ser más rápido."}
            else:
                msg = {"pt": "Concentre-se mais na próxima!", "en": "Focus more next time!", "es": "¡Concéntrate más la próxima vez!"}
            result_texts.append(msg.get(self.idioma, msg['pt']))
        else:
            msg_fail = {"pt": "Não desanime — tente novamente!", "en": "Don't give up — try again!", "es": "¡No te rindas — inténtalo de nuevo!"}
            result_texts.append(msg_fail.get(self.idioma, msg_fail['pt']))     
        for text in result_texts:
            surf = self.font_small.render(text, True, TEXT)
            self.screen.blit(surf, ((WIDTH - surf.get_width()) // 2, y))
            y += 40
        if 'result_feedback' not in self.input_fields:
            self.input_fields['result_feedback'] = CampoTexto(200, y + 20, 400, 40, 
            self.font_tiny, "Feedback (opcional)", 100)     
        feedback_label = self.font_tiny.render("Deixe um comentário:", True, TEXT_DIM)
        self.screen.blit(feedback_label, ((WIDTH - feedback_label.get_width()) // 2, y))     
        self.input_fields['result_feedback'].desenhar(self.screen)
        self.input_fields['result_feedback'].atualizar()
        if 'result' not in self.buttons:
            button_width = 180
            button_height = 45
            start_y = y + 100
            spacing = 55      
            options = [
                ('again', {'pt': 'Jogar Novamente', 'en': 'Play Again', 'es': 'Jugar de Nuevo'}),
                ('change_lang', {'pt': 'Mudar Idioma', 'en': 'Change Language', 'es': 'Cambiar Idioma'}),
                ('change_diff', {'pt': 'Mudar Nível', 'en': 'Change Level', 'es': 'Cambiar Nivel'}),
                ('menu', {'pt': 'Menu Principal', 'en': 'Main Menu', 'es': 'Menú Principal'})
            ]        
            self.buttons['result'] = {}
            for i, (key, texts) in enumerate(options):
                x = (WIDTH - button_width) // 2
                y_pos = start_y + i * spacing
                text = texts.get(self.idioma, texts['pt'])
                self.buttons['result'][key] = Botao(x, y_pos, button_width, button_height, 
                                                     text, self.font_tiny)
        for btn in self.buttons['result'].values():
            btn.desenhar(self.screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False          
            self.input_fields['result_feedback'].processar_evento(event)         
            for key, btn in self.buttons['result'].items():
                if btn.processar_evento(event):
                    feedback = self.input_fields['result_feedback'].text.strip()
                    if feedback:
                        try:
                            with open(HISTORICO_ARQUIVO, 'r', encoding='utf-8') as f:
                                historico = json.load(f)
                            if historico:
                                historico[-1]['feedback'] = feedback
                            with open(HISTORICO_ARQUIVO, 'w', encoding='utf-8') as f:
                                json.dump(historico, f, indent=4, ensure_ascii=False)
                        except Exception:
                            pass                
                    self.input_fields.pop('result_feedback', None)
                    self.buttons.pop('result', None)               
                    if key == 'again':
                        self.state = 'countdown'
                    elif key == 'change_lang':
                        self.state = 'language_select'
                    elif key == 'change_diff':
                        self.state = 'difficulty_select'
                    elif key == 'menu':
                        self.state = 'menu'
                        self.streak = 0
    
    def processar_estado_ranking_sessao(self):
        self.desenhar_fundo('bg')    
        title = self.font_large.render('Ranking da Sessão', True, ACCENT)
        self.screen.blit(title, ((WIDTH - title.get_width()) // 2, 50))   
        if not self.ranking_sessao:
            msg = self.font_small.render('Nenhum resultado ainda', True, TEXT_DIM)
            self.screen.blit(msg, ((WIDTH - msg.get_width()) // 2, 200))
        else:
            sorted_ranking = sorted(self.ranking_sessao, key=lambda x: x['pontos'], reverse=True)
            y = 130
            for i, entry in enumerate(sorted_ranking[:15], 1):
                text = f"{i}. {entry['nome']} - {entry['pontos']} pts ({entry['palavra']}, {entry.get('tempo', 0):.2f}s)"
                surf = self.font_tiny.render(text, True, TEXT)
                self.screen.blit(surf, (50, y))
                y += 35
        if 'ranking_session_back' not in self.buttons:
            self.buttons['ranking_session_back'] = Botao(325, 700, 150, 50, 'Voltar', self.font_small)    
        self.buttons['ranking_session_back'].desenhar(self.screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False         
            if self.buttons['ranking_session_back'].processar_evento(event):
                self.state = 'menu'
                self.buttons.pop('ranking_session_back', None)
    
    def processar_estado_ranking_historico(self):
        self.desenhar_fundo('bg') 
        title = self.font_large.render('Ranking Histórico', True, ACCENT)
        self.screen.blit(title, ((WIDTH - title.get_width()) // 2, 50))
        try:
            with open(HISTORICO_ARQUIVO, 'r', encoding='utf-8') as f:
                historico = json.load(f)
        except Exception:
            historico = [] 
        if not historico:
            msg = self.font_small.render('Nenhum histórico salvo', True, TEXT_DIM)
            self.screen.blit(msg, ((WIDTH - msg.get_width()) // 2, 200))
        else:
            melhor_por_jogador = {}
            for r in historico:
                nome = r.get('nome')
                pontos = r.get('pontos', 0)
                if nome not in melhor_por_jogador or pontos > melhor_por_jogador[nome]:
                    melhor_por_jogador[nome] = pontos           
            sorted_melhor = sorted(melhor_por_jogador.items(), key=lambda x: x[1], reverse=True)          
            y = 130
            for i, (nome, pts) in enumerate(sorted_melhor[:15], 1):
                text = f"{i}. {nome} - {pts} pts"
                surf = self.font_tiny.render(text, True, TEXT)
                self.screen.blit(surf, (50, y))
                y += 35
        if 'ranking_history_back' not in self.buttons:
            self.buttons['ranking_history_back'] = Botao(325, 700, 150, 50, 'Voltar', self.font_small)     
        self.buttons['ranking_history_back'].desenhar(self.screen)      
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False          
            if self.buttons['ranking_history_back'].processar_evento(event):
                self.state = 'menu'
                self.buttons.pop('ranking_history_back', None)
    
    def processar_estado_editar_jogador(self):
        self.desenhar_fundo('cadastro-idioma_bg')     
        subtitle = self.font_medium.render('Editar Cadastro', True, TEXT)
        self.screen.blit(subtitle, ((WIDTH - subtitle.get_width()) // 2, 80))
        if 'edit' not in self.input_fields:
            self.input_fields['edit'] = {
                'nome': CampoTexto(200, 180, 400, 50, self.font_small, "Nome do jogador", 30),
                'novo_nome': CampoTexto(200, 260, 400, 50, self.font_small, "Novo nome (opcional)", 30),
                'idade': CampoTexto(200, 340, 400, 50, self.font_small, "Nova idade (opcional)", 3),
                'tdah': CampoTexto(200, 420, 400, 50, self.font_small, "TDAH? s/n (opcional)", 1)
            }         
            self.buttons['edit'] = {
                'submit': Botao(250, 520, 150, 50, 'Salvar', self.font_small),
                'back': Botao(420, 520, 130, 50, 'Voltar', self.font_small)
            }
        labels = [
            ('Nome atual:', 200, 150),
            ('Novo nome:', 200, 230),
            ('Nova idade:', 200, 310),
            ('TDAH (s/n):', 200, 390)
        ]
        for text, x, y in labels:
            surf = self.font_small.render(text, True, TEXT)
            self.screen.blit(surf, (x, y))
        for field in self.input_fields['edit'].values():
            field.desenhar(self.screen)
            field.atualizar()
        for btn in self.buttons['edit'].values():
            btn.desenhar(self.screen)
        if self.error_message:
            color = SUCCESS_COLOR if 'sucesso' in self.error_message.lower() else ERROR_COLOR
            msg_surf = self.font_tiny.render(self.error_message, True, color)
            self.screen.blit(msg_surf, ((WIDTH - msg_surf.get_width()) // 2, 630))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False         
            if 'edit' in self.input_fields:
                for field in self.input_fields['edit'].values():
                    field.processar_evento(event)         
            edit_buttons = self.buttons.get('edit', {})
            if edit_buttons:
                if edit_buttons.get('submit') and edit_buttons['submit'].processar_evento(event):
                    self.processar_editar_jogador()             
                if edit_buttons.get('back') and edit_buttons['back'].processar_evento(event):
                    self.state = 'menu'
                    self.input_fields.pop('edit', None)
                    self.buttons.pop('edit', None)
                    self.error_message = ""
    
    def processar_editar_jogador(self):
        nome = self.input_fields['edit']['nome'].text.strip().title()
        novo_nome = self.input_fields['edit']['novo_nome'].text.strip().title()
        nova_idade = self.input_fields['edit']['idade'].text.strip()
        novo_tdah = self.input_fields['edit']['tdah'].text.strip().lower()     
        if not nome:
            self.error_message = "Digite o nome do jogador"
            return     
        jogadores = carregar_jogadores()      
        if nome not in jogadores:
            self.error_message = "Jogador não encontrado"
            return
        nome_final = nome
        if novo_nome and validar_nome(novo_nome):
            jogadores[novo_nome] = jogadores[nome].copy()
            jogadores[novo_nome]['nome'] = novo_nome
            if novo_nome != nome:
                del jogadores[nome]
            nome_final = novo_nome     
        if nova_idade and validar_idade(nova_idade):
            jogadores[nome_final]['idade'] = int(nova_idade)    
        if novo_tdah in ['s', 'n']:
            jogadores[nome_final]['tdah'] = (novo_tdah == 's')    
        salvar_jogadores(jogadores)
        self.error_message = "Cadastro atualizado com sucesso!"
    
    def processar_estado_deletar_jogador(self):
        self.desenhar_fundo('cadastro-idioma_bg')     
        subtitle = self.font_medium.render('Deletar Cadastro', True, ERROR_COLOR)
        self.screen.blit(subtitle, ((WIDTH - subtitle.get_width()) // 2, 80))
        warning = self.font_small.render('ATENÇÃO: Esta ação não pode ser desfeita!', True, ERROR_COLOR)
        self.screen.blit(warning, ((WIDTH - warning.get_width()) // 2, 140))
        if 'delete' not in self.input_fields:
            self.input_fields['delete'] = {
                'nome': CampoTexto(200, 220, 400, 50, self.font_small, "Nome do jogador", 30)
            }        
            self.buttons['delete'] = {
                'submit': Botao(250, 320, 150, 50, 'Deletar', self.font_small, ERROR_COLOR),
                'back': Botao(420, 320, 130, 50, 'Voltar', self.font_small)
            }
        label = self.font_small.render('Nome:', True, TEXT)
        self.screen.blit(label, (200, 190))
        self.input_fields['delete']['nome'].desenhar(self.screen)
        self.input_fields['delete']['nome'].atualizar()
        for btn in self.buttons['delete'].values():
            btn.desenhar(self.screen)
        if self.error_message:
            color = SUCCESS_COLOR if 'removido' in self.error_message.lower() else ERROR_COLOR
            msg_surf = self.font_tiny.render(self.error_message, True, color)
            self.screen.blit(msg_surf, ((WIDTH - msg_surf.get_width()) // 2, 400))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False          
            if 'delete' in self.input_fields:
                self.input_fields['delete']['nome'].processar_evento(event)         
            delete_buttons = self.buttons.get('delete', {})
            if delete_buttons:
                if delete_buttons.get('submit') and delete_buttons['submit'].processar_evento(event):
                    self.processar_deletar_jogador()               
                if delete_buttons.get('back') and delete_buttons['back'].processar_evento(event):
                    self.state = 'menu'
                    self.input_fields.pop('delete', None)
                    self.buttons.pop('delete', None)
                    self.error_message = ""
    
    def processar_deletar_jogador(self):
        nome = self.input_fields['delete']['nome'].text.strip().title()     
        if not nome:
            self.error_message = "Digite o nome do jogador"
            return      
        jogadores = carregar_jogadores()       
        if nome not in jogadores:
            self.error_message = "Jogador não encontrado"
            return      
        del jogadores[nome]
        salvar_jogadores(jogadores)
        self.error_message = f"Cadastro de {nome} removido com sucesso!"
        self.input_fields['delete']['nome'].text = ""
    
    def run(self):
        while self.running:
            if self.state == 'menu':
                self.processar_estado_menu()
            elif self.state == 'login':
                self.processar_estado_login()
            elif self.state == 'language_select':
                self.processar_estado_selecao_idioma()
            elif self.state == 'difficulty_select':
                self.processar_estado_selecao_dificuldade()
            elif self.state == 'countdown':
                self.processar_estado_contagem()
            elif self.state == 'typing':
                self.processar_estado_digitacao()
            elif self.state == 'result':
                self.processar_estado_resultado()
            elif self.state == 'ranking_session':
                self.processar_estado_ranking_sessao()
            elif self.state == 'ranking_history':
                self.processar_estado_ranking_historico()
            elif self.state == 'edit_player':
                self.processar_estado_editar_jogador()
            elif self.state == 'delete_player':
                self.processar_estado_deletar_jogador()           
            pygame.display.flip()
            self.clock.tick(60)       
        pygame.quit()

def main():
    app = TypeFocusGUI()
    app.run()

if __name__ == '__main__':
    main()