import pygame
import math
import random
pygame.init()
pygame.display.init()
pygame.font.init()
screen = pygame.display.set_mode((450,450))
running = True
lost = False

pygame.display.set_caption("MineSweeper")

mine_colors = {
    0: (192, 192, 192),  # Gray for 0 mines
    1: (10, 120, 235),       # Blue for 1 mine
    2: (0, 195, 120),       # Green for 2 mines
    3: (188, 7, 89),       # Red for 3 mines
    4: (0, 30, 128),       # Dark Blue for 4 mines
    5: (128, 0, 0),       # Dark Red for 5 mines
    6: (0, 128, 128),     # Teal for 6 mines
    7: (0, 0, 0),         # Black for 7 mines
    8: (128, 128, 128)    # Light Gray for 8 mines
}



class Vec2():
    def __init__(self,pos):
        self.x = pos[0]
        self.y = pos[1]
        self.position = pos
        self.mag = self.get_len()

    def get_len(self):
        len = math.sqrt(self.x**2+self.y**2)

        if len == 0:
            return 0.1

        return len

    def normalise_self(self):
        self.x, self.y = self.x / self.mag, self.y / self.mag

    def normalise(self):
        return Vec2((self.x / self.mag, self.y / self.mag))

    def update(self,x,y):
        self.x = x
        self.y = y
        self.position = (x,y)
        self.mag = self.get_len()

    def __add__(self, vec2_2):
        return Vec2((self.x + vec2_2.x, self.y+vec2_2.y))

    def __sub__(self, vec2_2):
        return Vec2((self.x - vec2_2.x, self.y-vec2_2.y))

    def __mul__(self, n):
        return Vec2((self.x*n, self.y*n))

    def increment(self,vec):
        self.update(self.x + vec.x, self.y + vec.y)

    def decrement(self,vec):
        self.update(self.x - vec.x, self.y - vec.y)

    def __neg__(self):
        return Vec2((-self.x, -self.y))

    def __abs__(self):
        return Vec2((abs(self.x), abs(self.y)))

tileSize = 30
recentPressBool = True
font = pygame.font.Font("Poppins-Regular.ttf", int(tileSize/2))
TitleFont = pygame.font.Font("Poppins-Regular.ttf", 70)
class sweeperTile():
    def __init__(self, pos):
        self.pos = pos
        self.worldPos = pos*tileSize
        self.rect = pygame.Rect(self.worldPos.x, self.worldPos.y, tileSize, tileSize)
        self.uncover = False
        self.haveFlag = False
        self.startNode = False
        self.isMine = False
        self.nearMines = 0
        self.mines = []

    def draw(self, offset, screen):
        pygame.draw.rect(screen, (27, 228, 179), self.rect.move(offset.x, offset.y))
        mousePos = pygame.mouse.get_pos()
        if mousePos[0]//tileSize == self.pos.x+offset.x and mousePos[1]//tileSize == self.pos.y+offset.y and not self.uncover:
            pygame.draw.rect(screen, (21, 174, 136), pygame.Rect(self.worldPos.x + 5, self.worldPos.y + 5, tileSize - 10, tileSize - 10))
        else:
            if self.uncover:

                pygame.draw.rect(screen, (104, 230, 230),pygame.Rect(self.worldPos.x + 5, self.worldPos.y + 5, tileSize - 10, tileSize - 10))
            else:
                pygame.draw.rect(screen, (23, 200, 156),pygame.Rect(self.worldPos.x + 5, self.worldPos.y + 5, tileSize - 10, tileSize - 10))

        if self.haveFlag:
            pygame.draw.rect(screen, (245, 208, 109), pygame.Rect(self.worldPos.x + 5, self.worldPos.y + 5, tileSize - 10, tileSize - 10))

        if self.uncover:
            if self.isMine:
                pygame.draw.rect(screen, (188, 7, 89),pygame.Rect(self.worldPos.x + 5, self.worldPos.y + 5, tileSize - 10, tileSize - 10))
            else:
                if self.nearMines > 0:
                    color = mine_colors[self.nearMines]
                    text = font.render(str(self.nearMines), 1, color)
                    size = Vec2(text.get_size())

                    screen.blit(text,(self.worldPos+(Vec2((tileSize, tileSize)) - size)*0.5).position)
        else:
            if self.startNode:
                pygame.draw.rect(screen, (188, 7, 89), pygame.Rect(self.worldPos.x + 5, self.worldPos.y + 5, tileSize - 10, tileSize - 10))


class minesweeperBoard():
    def __init__(self, pos):
        self.pos = pos
        self.size = Vec2((15,15))
        self.numberOfMines = int(self.size.x*self.size.y*0.2)
        self.recentPressBool = False
        self.Tiles = self.init_Tiles(self.size)

    def get1dPos(self, pos):
        return int(pos.y*self.size.x+pos.x)

    def isPossible(self, pos):
        if pos.x >= 0 and pos.x < self.size.x:
            if pos.y >= 0 and pos.y < self.size.y:
                return True
        return False

    def get_surroundingTiles(self, tiles, pos):
        for x in range(-1,2):
            for y in range(-1,2):
                evalPos = Vec2((pos.x+x, pos.y+y))
                if self.isPossible(evalPos):
                    address = self.get1dPos(evalPos)
                    tiles[address].nearMines += 1
                    tiles[address].mines.append(pos)


    def init_Tiles(self, size):
        tiles = []

        for y in range(size.y):
            for x in range(size.x):
                tiles.append(sweeperTile(Vec2((x,y))))

        for i in range(self.numberOfMines):
            x_pos = random.randint(0,self.size.x-1)
            y_pos = random.randint(0,self.size.y-1)

            minePos = Vec2((x_pos, y_pos))

            address = self.get1dPos(minePos)

            while tiles[address].isMine:
                x_pos = random.randint(0, self.size.x - 1)
                y_pos = random.randint(0, self.size.y - 1)

                minePos = Vec2((x_pos, y_pos))

                address = self.get1dPos(minePos)

            tiles[address].isMine = True


            self.get_surroundingTiles(tiles, minePos)


        for tile in tiles:
            if tile.nearMines == 0:
                tile.startNode = True

                break

        return tiles

    def drawTiles(self,screen):
        for tile in self.Tiles:
            tile.draw(self.pos, screen)

    def BFSThing(self, tile):

        for x in range(-1,2):
            for y in range(-1,2):
                evalPos = Vec2((tile.pos.x+x, tile.pos.y+y))
                if self.isPossible(evalPos):
                    address = self.get1dPos(evalPos)
                    nearbyTile = self.Tiles[address]
                    if not nearbyTile.uncover and not nearbyTile.isMine:
                        if nearbyTile.nearMines == 0:
                            nearbyTile.uncover = True
                            self.BFSThing(nearbyTile)
                        else:
                            if tile.nearMines == 0:
                                nearbyTile.uncover = True

    def update(self):
        mousePos = pygame.mouse.get_pos()
        nearestTile = Vec2((mousePos[0]//tileSize, mousePos[1]//tileSize))
        global lost
        if self.isPossible(nearestTile):
            tile = self.Tiles[self.get1dPos(nearestTile)]
            if pygame.mouse.get_pressed()[2]:
                if not tile.uncover and not self.recentPressBool:
                    tile.haveFlag = not tile.haveFlag
                self.recentPressBool = True
            else:
                self.recentPressBool = False



            if pygame.mouse.get_pressed()[0]:
                if not tile.haveFlag:
                    if tile.isMine:

                        lost = True

                    else:
                        tile.uncover = True
                        self.BFSThing(tile)








board = minesweeperBoard(Vec2((0,0)))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.display.quit()
            pygame.quit()

    screen.fill((255, 255, 255))

    # sweeperTile1.draw(Vec2((0,0)), screen)
    keys = pygame.key.get_pressed()



    if not lost:
        board.update()
    board.drawTiles(screen)

    if lost:
        for tile in board.Tiles:
            if tile.isMine:
                tile.uncover = True
                text = TitleFont.render("You Lost lol", 1, (0,0,0))
                text2 = font.render("right click to play again", 1, (0,0,0))
                screen.blit(text,((board.size*tileSize-Vec2(text.get_size()))*0.5+Vec2((0,-30))).position)
                screen.blit(text2,((board.size*tileSize-Vec2(text2.get_size()))*0.5+Vec2((0,20))).position)

                if pygame.mouse.get_pressed()[2]:
                    board = minesweeperBoard(Vec2((0,0)))
                    lost = False

    if keys[pygame.K_w]:
        for tile in board.Tiles:
            if tile.isMine == False:
                tile.uncover = True

    win = True
    for tile in board.Tiles:
        if not tile.isMine and not tile.uncover:
            win = False
            break


    if win:
        text = TitleFont.render("Get a life lol", 1, (0, 0, 0))
        text2 = font.render("right click to play again", 1, (0, 0, 0))
        screen.blit(text, ((board.size * tileSize - Vec2(text.get_size())) * 0.5 + Vec2((0, -30))).position)
        screen.blit(text2, ((board.size * tileSize - Vec2(text2.get_size())) * 0.5 + Vec2((0, 20))).position)
        if pygame.mouse.get_pressed()[2]:
            board = minesweeperBoard(Vec2((0, 0)))
            win = False

    pygame.display.flip()