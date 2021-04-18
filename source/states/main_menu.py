from .. import tools
from .. import constants as C
from .. import setup
from ..components import info
import time
import pygame
import win32api,win32con # pip install pywin32




white = (255,255,255)
black = (0,0,0)
btn_d_color = (206, 154, 120)
btn_p_color = (190, 140, 110)
class Menu(tools.State):
    def __init__(self):
        super(Menu, self).__init__()
        game_info = {
            C.COIN_TOTAL: 0,
            C.SCORE: 0,
            C.LIVES: 3,
            C.TOP_SCORE: 0,
            C.CURRENT_TIME: 0.,
            C.LEVEL_NUM: 1,
            C.PLAYER_NAME: C.MARIO,
            C.POWERUP_LEVEL: C.SMALL
        }
        self.startup(0.0, game_info)
        self.textFont = pygame.font.Font("freesansbold.ttf", 25) #创建一个文本文件对象
        self.mutex = False # 设置一个按键的flag

        with open('resources/text/flag', 'r') as f:
            text = f.readline(10)
            if text == "mutex":
                self.mutex = True


    def startup(self, current_time, game_info):

        self.start_time = current_time
        self.next = C.LOAD_SCREEN
        self.game_info = game_info
        self.overhead_info = info.Info(self.game_info, C.MAIN_MENU)

        self.setup_background()
        self.setup_player()
        self.setup_cursor()

    def setup_background(self):
        self.background = setup.GRAPHICS['level_1']
        self.background_rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(self.background_rect.width * C.BG_MULTIPLIER),
                                                                   int(self.background_rect.height * C.BG_MULTIPLIER)))
        self.viewport = setup.SCREEN.get_rect()
        self.image_dict = {}
        image = tools.get_image(setup.GRAPHICS['title_screen'], 1, 60, 176, 88, (255, 0, 220), C.SIZE_MULTIPLIER) # 紫色
        rect = image.get_rect()
        rect.x, rect.y = (170, 100)
        self.image_dict['GAME_NAME_BOX'] = (image, rect)

    def setup_player(self):
        self.player_list = []
        player_rect_info = [(178, 32, 12, 16), (178, 128, 12, 16)] # 两只马里奥的位置
        for rect_info in player_rect_info:
            image = tools.get_image(setup.GRAPHICS['mario_bros'], *rect_info, (0, 0, 0), C.PLAYER_MULTIPLIER)
            rect = image.get_rect() #获取图片的大小区域
            rect.x, rect.bottom = 110, C.GROUND_HEIGHT #设置位置
            self.player_list.append((image, rect))
        self.player_index = 0

    def setup_cursor(self):
        self.cursor = pygame.sprite.Sprite()
        self.cursor.image = tools.get_image(setup.GRAPHICS['item_objects'], 24, 160, 8, 8, (0, 0, 0), 3)
        rect = self.cursor.image.get_rect()
        rect.x, rect.y = (220, 358)
        self.cursor.rect = rect
        self.cursor.state = C.PLAYER1

     #设置一个显示文本对象
    def text_objects(self, text, font, color):
        textSurface = font.render(text, True, color)
        return textSurface, textSurface.get_rect()

    #开关声音的按键
    def setup_mute_button(self, surface):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if self.mutex == False:#非静音状态
            textSurf, textRect = self.text_objects("MUSIC ON", self.textFont, white) #设置显示的文字
            textRect.center = (715, C.GROUND_HEIGHT - 100)
            # pygame.draw.rect(surface, btn_d_color, textRect)
            surface.blit(textSurf, textRect)
            if textRect[0] + textRect[2] > mouse[0] > textRect[0] and \
                textRect[1] + textRect[3] > mouse[1] > textRect[1]: #判断鼠标点击的范围
                if click[0] == 1: # 鼠标按下
                    time.sleep(0.2) #消抖
                    self.mutex = True #静音
                    with open('resources/text/flag', 'w') as f: #写入文件，记录状态
                        f.write("mutex")

        elif self.mutex == True: #静音状态
            textSurf, textRect = self.text_objects("MUSIC OFF", self.textFont, white)
            textRect.center = (720, C.GROUND_HEIGHT - 100)
            surface.blit(textSurf, textRect)
            if textRect[0] + textRect[2] > mouse[0] > textRect[0] and \
                    textRect[1] + textRect[3] > mouse[1] > textRect[1]:
                if click[0] == 1:
                    time.sleep(0.2)
                    self.mutex = False
                    with open('resources/text/flag', 'w') as f:
                        f.write("unmutex")

    # 显示游戏规则的信息的Button
    def setup_play_info_button(self, surface): #添加游玩信息
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        textSurf, textRect = self.text_objects("INFO", self.textFont, white)
        textRect.center = (680, C.GROUND_HEIGHT - 150)
        surface.blit(textSurf, textRect)
        if textRect[0] + textRect[2] > mouse[0] > textRect[0] and \
            textRect[1] + textRect[3] > mouse[1] > textRect[1]:
            if click[0] == 1: # 鼠标按下
                time.sleep(0.2)
                self.display_label()

    def display_label(self):  #弹窗显示游戏规则
        title_msg = "The rules of the game"
        win32api.MessageBox(0, title_msg, "Rules") # 使用弹窗规则


    def update(self, surface, keys, current_time):
        self.current_time = current_time
        self.game_info[C.CURRENT_TIME] = self.current_time
        self.player_image = self.player_list[self.player_index][0]
        self.player_rect = self.player_list[self.player_index][1]
        self.update_cursor(keys)
        self.overhead_info.update(self.game_info)

        surface.blit(self.background, self.viewport)
        self.setup_mute_button(surface)
        self.setup_play_info_button(surface)
        surface.blit(self.image_dict['GAME_NAME_BOX'][0], self.image_dict['GAME_NAME_BOX'][1])
        surface.blit(self.player_image, self.player_rect)
        surface.blit(self.cursor.image, self.cursor.rect)
        self.overhead_info.draw(surface)

    def update_cursor(self, keys):
        if self.cursor.state == C.PLAYER1:
            self.cursor.rect.y = 358
            if keys[pygame.K_DOWN]:
                self.cursor.state = C.PLAYER2
                self.player_index = 1
                self.game_info[C.PLAYER_NAME] = C.LUIGI
        elif self.cursor.state == C.PLAYER2:
            self.cursor.rect.y = 403
            if keys[pygame.K_UP]:
                self.cursor.state = C.PLAYER1
                self.player_index = 0
                self.game_info[C.PLAYER_NAME] = C.MARIO
        if keys[pygame.K_RETURN]:
            self.reset_game_info()
            self.finished = True

    def reset_game_info(self):
        reset_info = {
            C.COIN_TOTAL: 0,
            C.SCORE: 0,
            C.LIVES: 3,
            C.CURRENT_TIME: 0.,
            C.LEVEL_NUM: 1,
            C.POWERUP_LEVEL: C.SMALL
        }
        self.game_info.update(reset_info)