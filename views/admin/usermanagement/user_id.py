""" Search"""
import pygame
from pygame.locals import *
import time
import os
import config 
import elements
import views
import services
import data_example



class User_Id:
    """Create a single-window app with multiple scenes."""

    def __init__(self, editstage):
        """Initialize pygame and the application."""
        pygame.init() # Initialize the pygame
        pygame.display.init()  # Initialize the display module
        self.screen = pygame.display.set_mode(config.screensize, config.flags) # Set mode of screen
        self.screen.fill(Color('white')) # Set background color of screen
        self.running = True 
        self.next_button = False # Set default avtivation status of next button
        self.previous_button = False # Set default avtivation status of previous button
        self.index = 0 # Set default index value of listview page
        self.product_data = ""
        self.message = False # Set default status of output message1
        self.message2 = False # Set default status of output message2
        self.editstage = editstage
        if self.editstage:
            self.caption = 'Edit user id'
            self.title = 'EDIT USER ID'
        else:
            self.caption = 'Add user id'
            self.title = 'ADD USER ID'

        self.shortcuts = {
            (K_x, KMOD_LMETA): 'print("cmd+X")',
            (K_x, KMOD_LALT): 'print("alt+X")',
            (K_x, KMOD_LCTRL): 'home.App().run()',
            (K_x, KMOD_LMETA + KMOD_LSHIFT): 'print("cmd+shift+X")',
            (K_x, KMOD_LMETA + KMOD_LALT): 'print("cmd+alt+X")',
            (K_x, KMOD_LMETA + KMOD_LALT + KMOD_LSHIFT): 'print("cmd+alt+shift+X")',
        }

        self.click = {
            # Click next button
            (8, 8): 'self.next_click()',
            (9, 8): 'self.next_click()',
            (10, 8): 'self.next_click()',
            (8, 9): 'self.next_click()',
            (9, 9): 'self.next_click()',
            (10, 9): 'self.next_click()',
            # Click cancel button
            (8, 10): 'self.cancel_click()',
            (9, 10): 'self.cancel_click()',
            (10, 10): 'self.cancel_click()',
        }

    def do_shortcut(self, event):
        """Find the the key/mod combination in the dictionary and execute the cmd."""
        k = event.key
        m = event.mod
        if (k, m) in self.shortcuts:
            exec(self.shortcuts[k, m])

    def do_click(self, x, y):
        """Find the mouse positionm in the gird and execute the event."""
        column_click = x // (config.bwidth + config.margin)
        row_click = y // (config.bheight + config.margin)
        if (column_click, row_click) in self.click:
            exec(self.click[column_click, row_click])

    def next_click(self):
        if self.userid_value != '':
            if self.editstage:
                if not services.selectpersonbyid(self.userid_value)[0]:
                    views.user_data.user_data['user_id'] = self.userid_value
                    views.User_Name(True).run()
                    pygame.quit()
                else:
                    if self.userid_value == views.user_data.old_id:
                        views.user_data.user_data['user_id'] = self.userid_value
                        views.User_Name(True).run()
                        pygame.quit()
                    else:
                        self.userid_input.update('*')
                        self.message = False
                        self.message2 = True
                        print("This user id is already")
            else:
                if not services.selectpersonbyid(self.userid_value)[0]:
                    views.user_data.user_data['user_id'] = self.userid_value
                    views.User_Name(False).run()
                    pygame.quit()
                else:
                    self.userid_input.update('*')
                    self.message = False
                    self.message2 = True
                    print("This user id is already")
        else:
            self.message2 = False
            self.message = True
            print("Please enter user id")

    def cancel_click(self):
        if self.editstage:
            views.user_data.userdata_reset()
            views.user_data.list_reset()
            views.User_Edit().run()
            pygame.quit()
        else:
            views.user_data.user_data['user_id'] = ''
            views.User_Management().run()
            pygame.quit()

    def run(self):
        """Initialize Caption and Valiable."""
        pygame.display.set_caption(self.caption + config.VERSION)
        self.userid_input = elements.InputBox_Userid(1, 3, 10, 1, views.user_data.user_data['user_id'], app = (self.screen), active = True, numpad_active = True)
        print("User_datt :", views.user_data.user_data)
        """Run the main event loop."""
        while self.running:
            self.number = 1
            self.screen.fill(Color('white'))      
            """Initialize user interface."""
            for row in range(12):
                y = (config.margin + config.bheight) * row + config.margin
                for column in range(12):
                    x = (config.margin + config.bwidth) * column + config.margin
                    position = ((config.margin + config.bwidth) * column + (config.bwidth / 2.1), (config.margin + config.bheight) * row + (config.bheight / 3.5) - 5)
                    position2 = ((config.margin + config.bwidth) * column + (config.bwidth / 2.1), (config.margin + config.bheight) * row + (config.bheight / 3.5) - 5)
                    position3 = ((config.margin + config.bwidth) * column + (config.bwidth / 2.1) + 10, (config.margin + config.bheight) * row + (config.bheight / 3.5) + 30)
                    position4 = ((config.margin + config.bwidth) * column + (config.bwidth / 2.1) + 10, (config.margin + config.bheight) * row + (config.bheight / 3.5) - 5)
                    if row == 0 and column == 0:
                        elements.Title(self.title, pos=(400, 67), app=(self.screen)).draw()
                        elements.Header_Table('MESSAGE', 1, 4, app=(self.screen)).draw()
                        elements.Rectangle(1, 5, 7, 4, app=(self.screen)).draw()
                        elements.Header_Table('OUTPUT', 1, 9, app=(self.screen)).draw()
                        elements.Rectangle(1, 10, 7, 1, app=(self.screen)).draw()
                        if self.editstage:
                            elements.Header_Table("  •  Please edit user id.", 1, 5, app=(self.screen)).draw()
                            elements.Header_Table("  •  If you don't want to edit, Please press next.", 1, 6, app=(self.screen)).draw()
                        else:
                            elements.Header_Table('  •  Please enter user id.', 1, 5, app=(self.screen)).draw()
                        if self.message:
                            elements.Output_Message("  •  Please enter user id.", 1, 10, app=(self.screen)).draw()
                        if self.message2:
                            elements.Output_Message("  •  This user id is already.", 1, 10, app=(self.screen)).draw()
                        self.userid_input.draw()                  
                    """Initialize Numpad."""
                    if row >= 4 and row <= 7 and column >= 8 and column <= 10:
                        if row == 7 and column == 8:
                            elements.Button(self.screen, config.light_blue, x, y, config.bwidth, config.bheight).Rect()
                            elements.Number('*', position, app=(self.screen)).draw()
                        elif row == 7 and column == 9:
                            elements.Button(self.screen, config.blue, x, y, config.bwidth, config.bheight).Rect()
                            elements.Number(str(0), position, app=(self.screen)).draw()
                        elif row == 7 and column == 10:
                            elements.Button(self.screen, config.light_blue, x, y, config.bwidth, config.bheight).Rect()
                            elements.Number('#', position, app=(self.screen)).draw()
                        else:
                            elements.Button(self.screen, config.blue, x, y, config.bwidth, config.bheight).Rect()
                            elements.Number(str(self.number), position, app=(self.screen)).draw()
                        self.number += 1
                    if row == 8 and column == 8:
                        elements.Button(self.screen, config.green, x, y, config.bwidth + 214, config.bheight + 67).Rect()
                        elements.Text_Button_Medium('      NEXT', position3, app=(self.screen)).draw()
                    if row == 10 and column == 8:
                        elements.Button(self.screen, config.red, x, y, config.bwidth + 214, config.bheight).Rect()
                        elements.Text_Button_Medium('    CANCEL', position4, app=(self.screen)).draw()
                   

            for event in pygame.event.get():
                self.userid_value = self.userid_input.handle_event(event)
                if event.type == KEYDOWN:
                    self.do_shortcut(event)
                if event.type == QUIT:
                    self.running = False
                if event.type == MOUSEBUTTONDOWN or event.type == FINGERDOWN:
                    # self.do_click(event)
                    if event.type == FINGERDOWN:
                        x = event.x * config.width
                        y = event.y * config.height
                        self.do_click(x, y)
                    else:
                        x, y = event.pos
                        self.do_click(x, y)
            
            pygame.display.update()
            pygame.display.flip()
        pygame.quit()