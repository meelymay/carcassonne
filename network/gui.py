import sys, os
import pygame
import pygame.locals

def load_tile_table(dir_name):
    images = []
    imgs = os.listdir(dir_name)
    for img in imgs:
        if 'jpg' in img:
            image = pygame.image.load(dir_name+'/'+img).convert()
            width, height = image.get_size()
            #images.append(image.subsurface((0,0,width, height)))
            images.append(image)
    tile_table = []
    i = 0
    for tile_x in range(5):
        line = []
        tile_table.append(line)
        for tile_y in range(5):
            image = images[i]
            line.append(image)
            i += 1
    return tile_table

if __name__=='__main__':
    pygame.init()
    width = 95
    height = 95
    screen = pygame.display.set_mode((5+95*5, 5+95*5))
    screen.fill((255, 255, 255))
    # table = load_tile_table("tiles")
    # for y in range(5):
    #     for x in range(5):
    #         screen.blit(table[x][y], (5+x*width, 5+y*height))

    pygame.display.flip()
    dir_name = 'tiles'
    for i in range(10):
        text = raw_input('which tile would you like to place where? ')

        parts = text.split()
        tile = parts[0]
        rotations = int(parts[1])
        x, y = [int(n) for n in parts[2:]]
        image = pygame.image.load(dir_name+'/'+tile+'.jpg').convert()
        print 'rotating by', rotations
        image = pygame.transform.rotate(image, -rotations*90.0)
        screen.blit(image, (5+x*width, 5+y*height))
        pygame.display.flip()
        
        if pygame.event.wait().type == pygame.locals.QUIT:
            sys.exit()
