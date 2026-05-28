import pygame

pygame.init()
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Homem-Aranha - Barreiras e Pé no Chão!")
clock = pygame.time.Clock()

CHAO = 450


# fundo

sheet_aranha = pygame.image.load("222-2223326_spiderman-sprite-sheet-png-transparent-png.png").convert()
cor_fundo_falso = sheet_aranha.get_at((0, 0))
sheet_aranha.set_colorkey(cor_fundo_falso)


# quadros

w_frame = sheet_aranha.get_width() // 3
h_frame = 220 

frames_direita = []
frames_esquerda = []

# correndo(3 quadros)
for i in range(3):
    quadro = sheet_aranha.subsurface((i * w_frame, 0, w_frame, h_frame))
    quadro = pygame.transform.scale(quadro, (90, 90))
    frames_direita.append(quadro)
    frames_esquerda.append(pygame.transform.flip(quadro, True, False))

# parado
frame_parado = sheet_aranha.subsurface((0, 0, w_frame, h_frame))
frame_parado = pygame.transform.scale(frame_parado, (90, 90))

# pulo
frame_pulo = sheet_aranha.subsurface((w_frame, h_frame + 30, w_frame, h_frame - 30))
frame_pulo = pygame.transform.scale(frame_pulo, (90, 90))

# teia
h_total = sheet_aranha.get_height()
h_terceira_linha = h_total // 3
w_metade = sheet_aranha.get_width() // 2 

frame_teia_base = sheet_aranha.subsurface((0, h_total - h_terceira_linha, w_metade, h_terceira_linha))
frame_teia_dir = pygame.transform.scale(frame_teia_base, (130, 90))
frame_teia_esq = pygame.transform.flip(frame_teia_dir, True, False)


# variaveis

indice_aranha = 0
tempo_anim_aranha = 0
x_aranha = 100
y_aranha = CHAO - 10 
estado_aranha = "PARADO"
direcao_aranha = "DIREITA"

pulando = False
vel_y = 0

anim_constante_cor = (255, 0, 0)
tempo_anim_constante = 0


# LOOP PRINCIPAL

rodando = True
while rodando:
    tela.fill((200, 230, 255)) 
    pygame.draw.rect(tela, (50, 50, 50), (0, CHAO + 80, largura, altura)) 
    
    # eventos gerais
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            rodando = False
            
        # pulo
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_SPACE and not pulando:
                pulando = True
                vel_y = -16 

    # movimentacao
    keys = pygame.key.get_pressed()
    movendo_horizontal = False
    
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        x_aranha += 5
        direcao_aranha = "DIREITA"
        movendo_horizontal = True
    elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
        x_aranha -= 5
        direcao_aranha = "ESQUERDA"
        movendo_horizontal = True

    
    # barreira
    
    if x_aranha < 0: 
        x_aranha = 0 
        
    if x_aranha > largura - 90: 
        x_aranha = largura - 90 
    
    # pulo
    if pulando:
        y_aranha += vel_y
        vel_y += 1 
        
        if y_aranha >= CHAO - 10:
            y_aranha = CHAO - 10
            pulando = False

    # animacao
    if keys[pygame.K_e]: 
        estado_aranha = "TEIA" 
    elif pulando:
        estado_aranha = "PULANDO"
    elif movendo_horizontal:
        estado_aranha = "ANDANDO"
    else:
        estado_aranha = "PARADO"

    # frame
    tempo_anim_constante += 1
    if tempo_anim_constante >= 15:
        anim_constante_cor = (255, 255, 0) if anim_constante_cor == (255, 0, 0) else (255, 0, 0)
        tempo_anim_constante = 0

    if estado_aranha == "ANDANDO":
        tempo_anim_aranha += 1
        if tempo_anim_aranha >= 6: 
            indice_aranha = (indice_aranha + 1) % len(frames_direita)
            tempo_anim_aranha = 0
    else:
        indice_aranha = 0 

    # desenho
    pygame.draw.rect(tela, anim_constante_cor, (700, 100, 40, 40))
    
    # imagem
    if estado_aranha == "TEIA":
        img_atual = frame_teia_dir if direcao_aranha == "DIREITA" else frame_teia_esq
    elif estado_aranha == "PULANDO":
        img_atual = frame_pulo
    elif estado_aranha == "ANDANDO":
        img_atual = frames_direita[indice_aranha] if direcao_aranha == "DIREITA" else frames_esquerda[indice_aranha]
    else:
        img_atual = frame_parado

    # ajuste de posicoes finais
    pos_x_final = x_aranha
    pos_y_final = y_aranha
    
    if estado_aranha == "TEIA":
        
        pos_y_final += 26 
        if direcao_aranha == "ESQUERDA":
            pos_x_final -= 40 
            
    tela.blit(img_atual, (pos_x_final, pos_y_final))
    pygame.display.update()
    clock.tick(60)

pygame.quit()