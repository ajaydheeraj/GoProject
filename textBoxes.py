### text boxes that appear when a player is trying to undo a move, pass the turn
### or reset the game

import pygame
from static import *

# object for using text boxes
class TextBox(pygame.sprite.Sprite):
    bounds = (50, 200, 500, 200)
    
    def __init__(self, action):
        self.action = action
        text = "Are you sure you want to %s?" % action
        self.text = pygame.font.Font(None, 36).render(text, True, (0, 0, 0))
        
    def draw(self, screen):
        pygame.draw.rect(screen, Colors.WHITE, self.bounds)
        pygame.draw.rect(screen, Colors.BLACK, self.bounds, 5)
        screen.blit(self.text, (75, 225))
        BoolBox("Yes").draw(screen)
        BoolBox("No").draw(screen)
        
    def __repr__(self):
        return self.action
        
# object for clicking to remove dead stones text box, draws from TextBox super
class DeadStoneBox(TextBox):
    def __init__(self, action):
        super().__init__(action)
        self.text = pygame.font.Font(None, 36).render("Click to remove dead stones", True, (0, 0, 0))
        self.text2 = pygame.font.Font(None, 36).render("Press 'D' when done", True, (0, 0, 0))
        
    def draw(self, screen):
        pygame.draw.rect(screen, Colors.WHITE, self.bounds)
        pygame.draw.rect(screen, Colors.BLACK, self.bounds, 5)
        screen.blit(self.text, (75, 225))
        screen.blit(self.text2, (75, 275))
        BoolBox("OK").draw(screen)
        
# The box that appears when the game is over
class GameOverBox(pygame.sprite.Sprite):
    bounds = (50, 200, 500, 200)
    
    def __init__(self, p1score, p2score):
        if p1score > p2score:
            gameStats = ("Black", p1score, p2score)
        else:
            gameStats = ("White", p2score, p1score)
        self.text1 = pygame.font.Font(None, 36).render("GAME OVER!", True, (0, 0, 0))
        self.text2 = pygame.font.Font(None, 36).render("Winner is %s, %d to %d"%gameStats, True, (0, 0, 0))
        self.text3 = pygame.font.Font(None, 28).render("(Click anywhere to close this box)", True, (0, 0, 0))
        
    def draw(self, screen):
        pygame.draw.rect(screen, Colors.WHITE, self.bounds)
        pygame.draw.rect(screen, Colors.BLACK, self.bounds, 5)
        screen.blit(self.text1, (75, 225))
        screen.blit(self.text2, (75, 275))
        screen.blit(self.text3, (75, 325))
      
# the "yes" and "no" buttons on one such text box
class BoolBox(pygame.sprite.Sprite):
    def __init__(self, boolean):
        self.text = pygame.font.Font(None, 36).render(boolean, True, (0, 0, 0))
        if boolean == "Yes" or boolean == "OK":
            self.bounds = GoConstants.YESBOXBOUNDS
            self.textPos = (100, 337)
        elif boolean == "No":
            self.bounds = GoConstants.NOBOXBOUNDS
            self.textPos = (405, 337)
        
    def draw(self, screen):
        pygame.draw.rect(screen, Colors.BLACK, self.bounds, 3)
        screen.blit(self.text, self.textPos)
        
# the "play" button on the start screen
class PlayButton(pygame.sprite.Sprite):
    bounds = (200, 250, 200, 50)
    
    def __init__(self):
        self.text = pygame.font.Font(None, 36).render("PLAY", True, (0, 0, 0))
        self.textPos = (270, 263)
        
    def draw(self, screen):
        pygame.draw.rect(screen, Colors.WHITE, self.bounds)
        pygame.draw.rect(screen, Colors.BLACK, self.bounds, 5)
        screen.blit(self.text, self.textPos)
        
# the "instructions" button on the start screen
class InstructionsButton(pygame.sprite.Sprite):
    bounds = (200, 325, 200, 50)
    
    def __init__(self):
        self.text = pygame.font.Font(None, 36).render("INSTRUCTIONS", True, (0, 0, 0))
        self.textPos = (205, 338)
        
    def draw(self, screen):
        pygame.draw.rect(screen, Colors.WHITE, self.bounds)
        pygame.draw.rect(screen, Colors.BLACK, self.bounds, 5)
        screen.blit(self.text, self.textPos)
        
# the title box on the start screen
class TitleBox(pygame.sprite.Sprite):
    bounds = (100, 50, 400, 75)
    
    def __init__(self):
        self.text = pygame.font.Font(None, 50).render("Go Game", True, (0, 0, 0))
        self.textPos = (230, 75)
        
    def draw(self, screen):
        pygame.draw.rect(screen, Colors.WHITE, self.bounds)
        pygame.draw.rect(screen, Colors.BLACK, self.bounds, 5)
        screen.blit(self.text, self.textPos)