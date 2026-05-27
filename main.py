import math
import sys

import pygame


LARGURA, ALTURA = 900, 520
FPS = 60
CHAO_Y = 430

BRANCO = (245, 246, 250)
PRETO = (30, 34, 40)
AZUL = (67, 134, 245)
AZUL_ESCURO = (35, 77, 153)
VERDE = (82, 196, 120)
AMARELO = (255, 212, 82)
LARANJA = (245, 139, 61)
VERMELHO = (231, 76, 60)
ROXO = (125, 92, 255)


def desenhar_texto(tela, fonte, texto, x, y, cor=PRETO):
    imagem = fonte.render(texto, True, cor)
    tela.blit(imagem, (x, y))


def criar_spritesheet_personagem():
    """Cria uma spritesheet 4x2: linha 0 corrida, linha 1 pulo."""
    largura_frame = 72
    altura_frame = 72
    sheet = pygame.Surface((largura_frame * 4, altura_frame * 2), pygame.SRCALPHA)

    for linha in range(2):
        for coluna in range(4):
            x = coluna * largura_frame
            y = linha * altura_frame
            frame = pygame.Surface((largura_frame, altura_frame), pygame.SRCALPHA)

            balanco = [0, -4, 0, 4][coluna]
            if linha == 0:
                corpo_y = 24
                perna_esq = (30, 52 + balanco)
                perna_dir = (45, 52 - balanco)
                braco_esq = (24, 35 - balanco)
                braco_dir = (49, 35 + balanco)
            else:
                corpo_y = 18 - abs(coluna - 1.5) * 2
                perna_esq = (31, 57)
                perna_dir = (45, 57)
                braco_esq = (20, 29)
                braco_dir = (53, 29)

            pygame.draw.ellipse(frame, AZUL_ESCURO, (25, corpo_y + 15, 24, 32))
            pygame.draw.circle(frame, AMARELO, (37, int(corpo_y) + 9), 12)
            pygame.draw.circle(frame, PRETO, (41, int(corpo_y) + 7), 2)
            pygame.draw.line(frame, AZUL_ESCURO, (29, int(corpo_y) + 26), braco_esq, 6)
            pygame.draw.line(frame, AZUL_ESCURO, (45, int(corpo_y) + 26), braco_dir, 6)
            pygame.draw.line(frame, PRETO, (32, int(corpo_y) + 43), perna_esq, 6)
            pygame.draw.line(frame, PRETO, (43, int(corpo_y) + 43), perna_dir, 6)
            pygame.draw.rect(frame, BRANCO, (22, 60, 31, 5), border_radius=3)

            sheet.blit(frame, (x, y))

    return sheet, largura_frame, altura_frame


def recortar_frames(sheet, largura_frame, altura_frame, linha, total):
    frames = []
    for coluna in range(total):
        area = pygame.Rect(
            coluna * largura_frame,
            linha * altura_frame,
            largura_frame,
            altura_frame,
        )
        frames.append(sheet.subsurface(area).copy())
    return frames


def criar_frames_moeda():
    frames = []
    for i in range(8):
        frame = pygame.Surface((70, 70), pygame.SRCALPHA)
        largura = max(8, int(50 * abs(math.cos(i * math.pi / 8))))
        pygame.draw.ellipse(frame, AMARELO, (35 - largura // 2, 8, largura, 54))
        pygame.draw.ellipse(frame, LARANJA, (35 - largura // 2, 8, largura, 54), 4)
        if largura > 22:
            pygame.draw.circle(frame, BRANCO, (29, 25), 4)
        frames.append(frame)
    return frames


def criar_frames_explosao():
    frames = []
    for i in range(9):
        frame = pygame.Surface((110, 110), pygame.SRCALPHA)
        raio = 10 + i * 5
        alpha = max(35, 230 - i * 22)
        cor = (*VERMELHO, alpha)
        pygame.draw.circle(frame, cor, (55, 55), raio)
        pygame.draw.circle(frame, (*LARANJA, alpha), (55, 55), max(4, raio - 12))
        pygame.draw.circle(frame, (*AMARELO, alpha), (55, 55), max(2, raio - 24))
        frames.append(frame)
    return frames


def frame_animacao(frames, indice, velocidade):
    return frames[(indice // velocidade) % len(frames)]


def desenhar_cenario(tela):
    tela.fill((220, 235, 247))
    pygame.draw.rect(tela, (176, 221, 177), (0, CHAO_Y, LARGURA, ALTURA - CHAO_Y))
    pygame.draw.rect(tela, (101, 153, 94), (0, CHAO_Y, LARGURA, 8))

    for x in range(0, LARGURA, 90):
        pygame.draw.line(tela, (120, 180, 112), (x, CHAO_Y + 18), (x + 35, CHAO_Y + 6), 3)


def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Atividade 11 - Animacoes no PyGame")
    relogio = pygame.time.Clock()
    fonte = pygame.font.SysFont("arial", 18)
    fonte_titulo = pygame.font.SysFont("arial", 24, bold=True)

    spritesheet, largura_frame, altura_frame = criar_spritesheet_personagem()
    frames_corrida = recortar_frames(spritesheet, largura_frame, altura_frame, 0, 4)
    frames_pulo = recortar_frames(spritesheet, largura_frame, altura_frame, 1, 4)
    frames_corrida_esquerda = [pygame.transform.flip(frame, True, False) for frame in frames_corrida]
    frames_pulo_esquerda = [pygame.transform.flip(frame, True, False) for frame in frames_pulo]

    frames_moeda = criar_frames_moeda()
    frames_explosao = criar_frames_explosao()

    jogador_x = 390
    jogador_y = CHAO_Y - altura_frame
    velocidade_x = 0
    velocidade_y = 0
    direcao = 1
    no_chao = True

    contador_constante = 0
    contador_corrida = 0
    contador_pulo = 0
    explosao_ativa = False
    contador_explosao = 0

    rodando = True
    while rodando:
        dt = relogio.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    rodando = False
                elif evento.key == pygame.K_SPACE and no_chao:
                    velocidade_y = -15
                    no_chao = False
                    contador_pulo = 0
                elif evento.key == pygame.K_e:
                    explosao_ativa = True
                    contador_explosao = 0
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                explosao_ativa = True
                contador_explosao = 0

        teclas = pygame.key.get_pressed()
        velocidade_x = 0

        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            velocidade_x = 5
            direcao = 1
            contador_corrida += 1
        elif teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            velocidade_x = -5
            direcao = -1
            contador_corrida += 1
        else:
            contador_corrida = 0

        jogador_x += velocidade_x
        jogador_x = max(10, min(LARGURA - largura_frame - 10, jogador_x))

        velocidade_y += 0.75
        jogador_y += velocidade_y
        if jogador_y >= CHAO_Y - altura_frame:
            jogador_y = CHAO_Y - altura_frame
            velocidade_y = 0
            no_chao = True

        contador_constante += 1
        if not no_chao:
            contador_pulo += 1

        if explosao_ativa:
            contador_explosao += 1
            if contador_explosao // 5 >= len(frames_explosao):
                explosao_ativa = False
                contador_explosao = 0

        if not no_chao:
            frames_atuais = frames_pulo if direcao == 1 else frames_pulo_esquerda
            frame_jogador = frame_animacao(frames_atuais, contador_pulo, 7)
        elif velocidade_x != 0:
            frames_atuais = frames_corrida if direcao == 1 else frames_corrida_esquerda
            frame_jogador = frame_animacao(frames_atuais, contador_corrida, 8)
        else:
            frame_jogador = frames_corrida[0] if direcao == 1 else frames_corrida_esquerda[0]

        desenhar_cenario(tela)

        moeda = frame_animacao(frames_moeda, contador_constante, 6)
        tela.blit(moeda, (75, 95))
        desenhar_texto(tela, fonte_titulo, "1) Animacao constante", 30, 35)
        desenhar_texto(tela, fonte, "A moeda gira sem precisar apertar nada.", 30, 65)

        tela.blit(frame_jogador, (jogador_x, jogador_y))
        desenhar_texto(tela, fonte_titulo, "2) Personagem por tecla segurada + EXTRA", 300, 35)
        desenhar_texto(tela, fonte, "Segure A/D ou setas para mover. Solte para parar. Espaco pula.", 300, 65)

        desenhar_texto(tela, fonte_titulo, "3) Animacao por evento", 610, 35)
        desenhar_texto(tela, fonte, "Clique ou pressione E uma vez.", 610, 65)

        pygame.draw.circle(tela, ROXO, (735, 330), 16)
        pygame.draw.rect(tela, ROXO, (719, 330, 32, 72), border_radius=8)
        pygame.draw.circle(tela, BRANCO, (741, 325), 3)

        if explosao_ativa:
            frame_explosao = frames_explosao[contador_explosao // 5]
            tela.blit(frame_explosao, (697, 260))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
