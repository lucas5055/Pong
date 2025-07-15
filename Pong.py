# Aqui puxa a biblioteca pygame e uns arquivos do sistema
import pygame
import sys
import random
# Inicialização
pygame.init()

# Definições de tela (Ainda preciso fazer com que a pessoa possa escolher a resolução)
LARGURA_TELA = 1280
ALTURA_TELA = 720

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0) # Fundo preto, mas o fundo do jogo é uma imagem (Isso ainda ta aqui pois eu quero fazer uma tela inicial antes de começar o jogo)

# Configuração da tela
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Pong")

# Carrega os frames do fundo
frames = []
for i in range(1, 1213):  # Ajuste o número de frames conforme necessário
    frame = pygame.image.load(f'Template\\frame_{i:03d}.png')
    frame = pygame.transform.scale(frame, (LARGURA_TELA, ALTURA_TELA))
    frames.append(frame)

frame_duration = 10
last_update = pygame.time.get_ticks()
frame_index = 0
direcao = 1

# Sons
try:
    pygame.mixer.init()
    backgroundmusic = pygame.mixer.Sound("Music\\Music 2.wav")
    backgroundmusic.play(-1)
    bonk = pygame.mixer.Sound("Music\\Bonk 2.wav")
    point_sound = pygame.mixer.Sound("Music\\Ponto 2.wav")
except pygame.error as e:
    print(f"Erro ao carregar ou reproduzir sons: {e}")
    backgroundmusic = None
    bonk = None
    point_sound = None

# Raquetes e bola
raquete_largura, raquete_altura = 10, 100
raquete1 = pygame.Rect(10, ALTURA_TELA // 2 - raquete_altura // 2, raquete_largura, raquete_altura) # Raquete da esquerda (Distancia da raquete para o fundo de tela, maximo que ela pode ir para cima e para baixo, posição onde ela aparece(aq so to incluindoo os numeros para lembrar))
raquete2 = pygame.Rect(LARGURA_TELA - 40, ALTURA_TELA // 2 - raquete_altura // 2, raquete_largura, raquete_altura)  #Msm coisa do comentario acima, mas na direita, valores maiores pq se usa "coordenadas" na tela pra definir a posição
# Bola
bola = pygame.Rect(LARGURA_TELA // 2 - 15, ALTURA_TELA // 2 - 15, 30, 30)

# Velocidades
velocidade_bola_x = 8
velocidade_bola_y = 8
velocidade_raq1 = 8
velocidade_ia = 10 

# Pontuação
pontos1 = 0
pontos2 = 0
# Precisão da IA
precisao_ia = 0.9  # Quanto mais próximo de 1, mais precisa a IA será
# Fonte do placar
fonte = pygame.font.Font(None, 74)

# Loop principal
while True:
    current_time = pygame.time.get_ticks()  # Atualiza o tempo aqui fora do for

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Movimento das raquetes
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_w] and raquete1.top > 0:
        raquete1.y -= velocidade_raq1
    if teclas[pygame.K_s] and raquete1.bottom < ALTURA_TELA:
        raquete1.y += velocidade_raq1
    if teclas[pygame.K_UP] and raquete2.top > 0:
        raquete2.y -= velocidade_ia
    if teclas[pygame.K_DOWN] and raquete2.bottom < ALTURA_TELA:
        raquete2.y += velocidade_ia

    # Move a bola
    bola.x += velocidade_bola_x
    bola.y += velocidade_bola_y

    # Colisão com as bordas
    if bola.top <= 0 or bola.bottom >= ALTURA_TELA:
        velocidade_bola_y = -velocidade_bola_y
        if bonk:
            bonk.play()

    # Pontuação
    if bola.left <= 0:
        pontos2 += 1
        if point_sound:
            point_sound.play()
        bola.x = LARGURA_TELA // 2 - 15
        bola.y = ALTURA_TELA // 2 - 15
        velocidade_bola_x = -velocidade_bola_x
        print(f"Pontos: Jogador 1: {pontos1} | Jogador 2: {pontos2}")
    elif bola.right >= LARGURA_TELA:
        pontos1 += 1
        if point_sound:
            point_sound.play()
            velocidade_bola_x = 8
            velocidade_bola_y = 8
            velocidade_raq1 = 8
            velocidade_ia = 10
        bola.x = LARGURA_TELA // 2 - 15
        bola.y = ALTURA_TELA // 2 - 15
        velocidade_bola_x = -velocidade_bola_x
        print(f"Pontos: Jogador 1: {pontos1} | Jogador 2: {pontos2}")

    # Colisão com as raquetes
    if bola.colliderect(raquete1) or bola.colliderect(raquete2):
        velocidade_bola_x = -velocidade_bola_x
        if bonk:
            bonk.play()
            velocidade_bola_x = velocidade_bola_x * 1.1  # Aumenta a velocidade da bola levemente
            velocidade_bola_y = velocidade_bola_y * 1.1  # Aumenta a velocidade da bola levemente
            velocidade_raq1 = velocidade_raq1 * 1.1  # Aumenta a velocidade da raquete levemente
            velocidade_ia = velocidade_ia * 1.1  # Aumenta a velocidade da IA levemente
    # Atualiza o frame do fundo
    while current_time - last_update > frame_duration:
        frame_index += direcao
        last_update += frame_duration

    # Inverte direção se chegar no fim ou começo
    if frame_index >= len(frames) - 1:
        frame_index = len(frames) - 1
        direcao *= -1
    elif frame_index <= 0:
        frame_index = 0
        direcao *= -1
    # Desenha tudo
    tela.blit(frames[frame_index], (0, 0))  # Fundo primeiro
    pygame.draw.rect(tela, BRANCO, raquete1)
    pygame.draw.rect(tela, BRANCO, raquete2)
    pygame.draw.ellipse(tela, BRANCO, bola)
    pygame.draw.aaline(tela, BRANCO, (LARGURA_TELA // 2, 0), (LARGURA_TELA // 2, ALTURA_TELA))

    # Placar
    texto1 = fonte.render(str(pontos1), True, BRANCO)
    texto2 = fonte.render(str(pontos2), True, BRANCO)
    tela.blit(texto1, (LARGURA_TELA // 4, 10))
    tela.blit(texto2, (LARGURA_TELA * 3 // 4, 10))
    
    
    # IA para a raquete1
    if bola.x < LARGURA_TELA // 2 and random.random() < precisao_ia:
        if raquete1.centery < bola.centery:
            raquete1.y += velocidade_ia
        elif raquete1.centery > bola.centery:
            raquete1.y -= velocidade_ia
        
    
    # Isso atualiza a tela e define o FPS
    clock = pygame.time.Clock()
    pygame.display.flip()
    clock.tick(60)
    
    # Encerra com P ou ESC
    if teclas[pygame.K_p] or teclas[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()