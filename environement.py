import pygame
import balls
pygame.init()
clock = pygame.time.Clock()
WIDTH=900
HEIGHT=600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('BAll Physics')
done = False
balls.ball.SURFACE=screen
balls.ball.WIDTH=WIDTH
balls.ball.HEIGHT=HEIGHT
balls.ball.border="wall"
balls.ball.rpopulate(30)
mx=0
my=0
while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                        (mx,my)=pygame.mouse.get_pos()
                        if event.button== 1:#LEFT
                                balls.ball.checkpickup(mx,my)
                        if event.button==3:
                                balls.ball.checkforapplied(mx,my)
                if event.type == pygame.MOUSEBUTTONUP:
                        (mx,my)=pygame.mouse.get_pos()
                        if event.button==1:
                                balls.ball.putback()
                        if event.button==3:
                                balls.ball.checkforletgo(mx,my)
                if event.type == pygame.MOUSEMOTION:
                        (mx,my)=pygame.mouse.get_pos()
                        balls.ball.checkforcarried(mx,my)

        screen.fill((0,0,0))
        balls.ball.drawall(mx,my)
        clock.tick()
        pygame.display.set_caption("BALLS PHYSICS fps: "+ str(int(clock.get_fps())))
        pygame.display.flip()