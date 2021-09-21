# instalar o pygame: pip install pygame
# importar as bibilotecas a baixo:
#Biblioteca da IA, comando para instalar: pip install neat.python
import pygame
import os
import random
import neat

#Definições da IA

ai_jogando = True
geracao = 0

# Definir Largura e Altura da tela

tela_largura = 500
tela_altura = 800

# Definir Imagens do jogo: Ex: imagem_cano:

# Sempre que quiser importar uma imagem do pygame usar o comando: pygame.image.load()
# Para importar imagens de outra pasta usar o comando: os.path.join ('nome da pasta' , 'nome do arquivo')
# Para aumentar a imagem em 2x, usar o comando: pygame.transform.scale2x. Vai servir para amplicar as imagens do jogo
# Repetir o Processo em todos os objetos, exceto nas imagens do passaro. Você deve importar as 3 imagens juntas.

imagem_Cano = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs' , 'pipe.png' )))
imagem_Chao = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs' , 'base.png' )))
imagem_background = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs' , 'bg.png' )))
imagens_Passaro = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs' , 'bird1.png' ))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs' , 'bird2.png' ))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs' , 'bird3.png' ))),
]

#Criação da Tabela de pontos
#Usar comando pygame.font.init() e pygame.font.Sysfont para definir o estilo e tamanho da fonte

pygame.font.init()
fonte_pontos = pygame.font.SysFont('arial', 40)


#Criação das Classes Necessárias

class Passaro:
    imgs = imagens_Passaro
    #Definir animações da rotação
    rotacao_maxima = 25
    velocidade_rotacao = 20
    tempo_animacao = 5

    #Definição do passaro

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_imagem = 0
        self.imagem = self.imgs[0]


    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        # calcular o deslocamento
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo

        # restringir o deslocamento
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2

        self.y += deslocamento

        # o angulo do passaro
        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.rotacao_maxima:
                self.angulo = self.rotacao_maxima
        else:
            if self.angulo > -90:
                self.angulo -= self.velocidade_rotacao

    # função desenhar
    def desenhar(self, tela):
        # definir qual imagem do passaro vai usar
        self.contagem_imagem += 1

        if self.contagem_imagem < self.tempo_animacao:
            self.imagem = self.imgs[0]
        elif self.contagem_imagem < self.tempo_animacao*2:
            self.imagem = self.imgs[1]
        elif self.contagem_imagem < self.tempo_animacao*3:
            self.imagem = self.imgs[2]
        elif self.contagem_imagem < self.tempo_animacao*4:
            self.imagem = self.imgs[1]
        elif self.contagem_imagem >= self.tempo_animacao*4 + 1:
            self.imagem = self.imgs[0]
            self.contagem_imagem = 0

        # se o passaro estiver caindo eu não vou bater a asa
        if self.angulo <= -80:
            self.imagem = self.imgs[1]
            self.contagem_imagem = self.tempo_animacao*2

        # desenhar a imagem
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        pos_centro_imagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=pos_centro_imagem)
        tela.blit(imagem_rotacionada, retangulo.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)

# Classificação do cano
class Cano:
    distancia = 200
    velocidade = 5

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.pos_top = 0
        self.pos_base = 0
        self.cano_top = pygame.transform.flip(imagem_Cano, False, True)
        self.cano_base = imagem_Cano
        self.passou = False
        self.definir_altura()

# Definir altura do cano

    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        self.pos_top = self.altura - self.cano_top.get_height()
        self.pos_base = self.altura + self.distancia

# Ajustar movimentação do cano

    def mover(self):
        self.x -= self.velocidade

# Desenho do cano

    def desenhar(self, tela):
        tela.blit(self.cano_top, (self.x, self.pos_top))
        tela.blit(self.cano_base, (self.x, self.pos_base))

# Colisão do passaro com o cano

    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        top_mask = pygame.mask.from_surface(self.cano_top)
        base_mask = pygame.mask.from_surface(self.cano_base)

        distancia_top = (self.x - passaro.x, self.pos_top - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        top_ponto = passaro_mask.overlap(top_mask, distancia_top)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)

        if base_ponto or top_ponto:
            return True
        else:
            return False

# Classificação do chão

class Chao:

    velocidade = 5
    largura = imagem_Chao.get_width()
    imagem = imagem_Chao

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.largura

# Movimentação do chão

    def mover(self):
        self.x1 -= self.velocidade
        self.x2 -= self.velocidade

        if self.x1 + self.largura < 0:
            self.x1 = self.x2 + self.largura
        if self.x2 + self.largura < 0:
            self.x2 = self.x1 + self.largura

# desenho do chão
    def desenhar(self, tela):
        tela.blit(self.imagem, (self.x1, self.y))
        tela.blit(self.imagem, (self.x2, self.y))

# Desenhar tela do jogo

def desenhar_tela(tela, passaros, canos, chao, pontos):
    tela.blit(imagem_background, (0, 0))
    for passaro in passaros:
        passaro.desenhar(tela)
    for cano in canos:
        cano.desenhar(tela)

    texto = fonte_pontos.render(f"Pontuação: {pontos}", 1, (255, 255, 255))
    tela.blit(texto, (tela_largura - 10 - texto.get_width(), 10))
    if ai_jogando:
        texto = fonte_pontos.render(f"Geração: {geracao}", 1, (255, 255, 255))
        tela.blit(texto, (10, 10))

    chao.desenhar(tela)
    pygame.display.update()

# Função para iniciar o jogo

def main(genomas, config):  #fitness function
    global geracao
    geracao += 1

    if ai_jogando:
    # criar vários passaros
        redes = []
        lista_genomas = []
        passaros = []
        for _, genoma in genomas:
            rede = neat.nn.FeedForwardNetwork.create(genoma, config)
            redes.append(rede)
            genoma.fitness = 0
            lista_genomas.append(genoma)
            passaros.append(Passaro(230, 350))
    else:
        passaros = [Passaro (230, 350)]
    chao = Chao(730)
    canos = [Cano(700)]
    tela = pygame.display.set_mode((tela_largura, tela_altura))
    pontos = 0
    relogio = pygame.time.Clock()

    rodando = True
    while rodando:
        relogio.tick(30)

        #Interação com o usuário

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
            if not ai_jogando:
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                        for passaro in passaros:
                            passaro.pular()

        indice_cano = 0
        if len(passaros) > 0:
            if len(canos) > 1 and passaros[0].x > (canos[0].x + canos[0].cano_top.get_width()):
                indice_cano = 1
        else:
            rodando = False
            break

        #mover as coisas
        for i, passaro in enumerate(passaros):
            passaro.mover()
            lista_genomas[i].fitness += 0.1
            output = redes[i].activate((passaro.y, abs(passaro.y - canos[indice_cano].altura), abs(passaro.y - canos[indice_cano].pos_base)))
            if output[0] > 0.5:
                passaro.pular()
        chao.mover()

#Interação do passaro ao bater no cano e contagem de pontos ao passar

        adicionar_cano = False
        remover_canos = []
        for cano in canos:
            for i, passaro in enumerate(passaros):
                if cano.colidir(passaro):
                    passaros.pop(i)
                    if ai_jogando:
                        lista_genomas[i].fitness -= 1
                        lista_genomas.pop(i)
                        redes.pop(i)
                if not cano.passou and passaro.x > cano.x:
                    cano.passou = True
                    adicionar_cano = True
            cano.mover()
            if cano.x + cano.cano_top.get_width() < 0:
                remover_canos.append(cano)

        if adicionar_cano:
            pontos += 1
            canos.append(Cano(600))
            for genoma in lista_genomas:
                genoma.fitness += 5
        for cano in remover_canos:
            canos.remove(cano)

        for i, passaro in enumerate(passaros):
            if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                passaros.pop(i)
                if ai_jogando:
                    lista_genomas.pop(i)
                    redes.pop(i)

        desenhar_tela(tela, passaros, canos, chao, pontos)


def rodar(caminho_config):
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                caminho_config)

    populacao = neat.Population(config)
    populacao.add_reporter(neat.StdOutReporter(True))
    populacao.add_reporter(neat.StatisticsReporter())

    if ai_jogando:
        populacao.run(main, 50)
    else:
        main(None, None)

if __name__ == '__main__':
    caminho = os.path.dirname(__file__)
    caminho_config = os.path.join(caminho, 'config.txt')
    rodar(caminho_config)








