""" Product request (Add))"""
import pygame
from pygame.locals import *
import time
import os
import config 
import elements
import views
import services

class product_list():
    section = ""
    qrcode = ""
    item_number = ""
    product_name = ""
    part_number = ""
    part_name = ""
    drawing_number = ""
    locker_number = ""
    quantity = ""
    other = ""
    drawer = ""
    cavity = ""

class Request_Add:
    """Create a single-window app with multiple scenes."""
    def __init__(self):
        """Initialize pygame and the application."""
        pygame.init() # Initialize the pygame
        pygame.display.init()  # Initialize the display module
        self.screen = pygame.display.set_mode(config.screensize, config.flags) # Set mode of screen
        self.screen.fill(Color('white')) # Set background color of screen
        self.running = True 
        self.message = False # Set default status of output message1
        self.message2 = False # Set default status of output message2
        self.message3 = False # Set default status of output message3
        self.message4 = False # Set default status of output message4
        self.message5 = False # Set default status of output message5
        self.message6 = False # Set default status of output message6
        views.request_data.inbox_active[0] = True # Set default input box activation
        views.request_data.inbox_active[1] = False # Set default input box activation
        self.index = 0 # Set default index value of listview page
        self.data = ''
        self.product_data = views.request_data.request_list
        self.product_list = product_list()
        self.shortcuts = {
            (K_x, KMOD_LMETA): 'print("cmd+X")',
            (K_x, KMOD_LALT): 'print("alt+X")',
            (K_x, KMOD_LCTRL): 'home.App().run()',
            (K_x, KMOD_LMETA + KMOD_LSHIFT): 'print("cmd+shift+X")',
            (K_x, KMOD_LMETA + KMOD_LALT): 'print("cmd+alt+X")',
            (K_x, KMOD_LMETA + KMOD_LALT + KMOD_LSHIFT): 'print("cmd+alt+shift+X")',
        }
        self.click = {
            # Click search button
            (8, 3): 'self.search_click()',
            (9, 3): 'self.search_click()',
            (10, 3): 'self.search_click()',
            # Click add button
            (8, 8): 'self.add()',
            (9, 8): 'self.add()',
            (10, 8): 'self.add()',
            (8, 9): 'self.add()',
            (9, 9): 'self.add()',
            (10, 9): 'self.add()',
            # Click cancel button
            (8, 10): 'self.cancel()',
            (9, 10): 'self.cancel()',
            (10, 10): 'self.cancel()',
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

    def add(self):
        if self.data != '':
            if int(self.data[1][0][0][9]) > 0:
                if self.quantity_value != "":
                    if int(self.quantity_value) <= int(self.product_list.quantity):
                        if int(self.quantity_value) > 0:
                            self.drawers = services.getproduct_drawer(self.data[1][0][0][2])
                            self.product_list.section = self.data[1][0][0][1]
                            self.product_list.qrcode = self.data[1][0][0][2]
                            self.product_list.item_number = self.data[1][0][0][3]
                            self.product_list.product_name = self.data[1][0][0][4]
                            self.product_list.part_number = self.data[1][0][0][5]
                            self.product_list.part_name = self.data[1][0][0][6]
                            self.product_list.drawing_number = self.data[1][0][0][7]
                            self.product_list.locker_number = services.getproductlocker_string(self.data[1][0][0][2])
                            self.product_list.quantity = str(self.quantity_value)
                            self.product_list.other = self.data[1][0][0][10]
                            self.product_list.drawer = self.drawers[3] 
                            self.product_list.cavity = self.drawers[4]
                            views.request_data.list_reset()
                            views.request_data.list_check_add(False)
                            views.request_data.add(self.product_list)
                            views.Request().run(); pygame.quit()
                        else:
                            self.message = False
                            self.message2 = False 
                            self.message3 = False 
                            self.message4 = True 
                            self.message5 = False
                            self.message6 = False
                            print("Please enter the quantity more than 0")
                    else:
                        self.message = False
                        self.message2 = False 
                        self.message3 = True 
                        self.message4 = False 
                        self.message5 = False
                        self.message6 = False
                        print("Please enter less quantity in stock")
                else:
                    self.message = False
                    self.message2 = True 
                    self.message3 = False 
                    self.message4 = False 
                    self.message5 = False
                    self.message6 = False
                    print("Please enter the quantity do you request")
            else: 
                self.message = False
                self.message2 = False 
                self.message3 = False 
                self.message4 = False 
                self.message5 = True
                self.message6 = False
                print("No product quantity in stock")
        else:
            self.message = True
            self.message2 = False 
            self.message3 = False 
            self.message4 = False 
            self.message5 = False
            self.message6 = False
            self.product_list.product_name = self.search_value
            print("Product request is invalid")

    def search_click(self):
        self.data = services.selectproductbysearch(self.search_value.replace("\r", ""))
        if self.data[0]:
            self.drawers = services.getproduct_drawer(self.data[1][0][0][2])
            self.product_list.section = self.data[1][0][0][1]
            self.product_list.qrcode = self.data[1][0][0][2]
            self.product_list.item_number = self.data[1][0][0][3]
            self.product_list.product_name = (self.data[1][0][0][4])
            self.product_list.part_number = self.data[1][0][0][5]
            self.product_list.part_name = self.data[1][0][0][6]
            self.product_list.drawing_number = self.data[1][0][0][7]
            self.product_list.locker_number = services.getproductlocker_string(self.data[1][0][0][2])
            self.product_list.quantity = str(self.data[1][0][0][9])
            self.product_list.other = self.data[1][0][0][10]
            self.product_list.drawer = self.drawers[3] 
            self.product_list.cavity = self.drawers[4]
            views.request_data.list_reset()
            views.request_data.list_add(self.product_list)
            views.request_data.inbox_active[0] = False # Set default input box activation
            views.request_data.inbox_active[1] = True # Set default input box activation
            #self.search_input.update('*')
            if int(self.data[1][0][0][9]) < 1:
                self.message = False
                self.message2 = False 
                self.message3 = False 
                self.message4 = False 
                self.message5 = True
                self.message6 = False
                print("No product quantity in stock")
        else:
            views.request_data.list_reset()
            self.search_input.update('*')
            self.quantity_input.update('*')
            self.message = False
            self.message2 = False 
            self.message3 = False 
            self.message4 = False 
            self.message5 = False
            self.message6 = True
            print("don't have product in your request")

    def cancel(self):
        views.Request().run()
        pygame.quit()
       

    def run(self):
        """Initialize Caption and Valiable."""
        pygame.display.set_caption('Add product requestion' + config.VERSION)
        self.search_input = elements.InputBox_2(1, 3, 7, 1, app = (self.screen), active = views.request_data.inbox_active[0], numpad_active = True)
        self.quantity_input = elements.InputBox_2(1, 8, 7, 1, app = (self.screen), active = views.request_data.inbox_active[1], numpad_active = True)
        """Run the main event loop."""
        while self.running:
            self.number = 1
            self.screen.fill(Color('white'))
            self.search_input.active = views.request_data.inbox_active[0]
            self.quantity_input.active = views.request_data.inbox_active[1]
            self.productadd_listview = elements.Productadd_Listview(1, 5, 7, 2, app=(self.screen),data = self.product_data, index = self.index)
            """Initialize user interface."""
            for row in range(12):
                y = (config.margin + config.bheight) * row + config.margin
                row_click = row
                for column in range(12):
                    x = (config.margin + config.bwidth) * column + config.margin
                    column_click = column
                    position = ((config.margin + config.bwidth) * column + (config.bwidth / 2.1), (config.margin + config.bheight) * row + (config.bheight / 3.5) - 5)
                    position2 = ((config.margin + config.bwidth) * column + (config.bwidth / 2.1), (config.margin + config.bheight) * row + (config.bheight / 3.5) + 30)
                    if row == 0 and column == 0:
                        elements.Title('ADD PRODUCT REQUEST', pos=(230, 67), app=(self.screen)).draw()
                        elements.Header_Table('No.', 1, 4, app=(self.screen)).draw()
                        elements.Header_Table('Product name', 1.5, 4, app=(self.screen)).draw()
                        elements.Header_Table('Part no.', 3.2, 4, app=(self.screen)).draw()
                        elements.Header_Table('Part name', 4.2, 4, app=(self.screen)).draw()
                        elements.Header_Table('Draw no.', 5.6, 4, app=(self.screen)).draw()
                        elements.Header_Table('QTY.', 6.8, 4, app=(self.screen)).draw()
                        elements.Header_Table('Locker', 7.4, 4, app=(self.screen)).draw()
                        elements.Header_Table('Quantity Requesition', 1, 7, app=(self.screen)).draw()
                        elements.Header_Table('OUTPUT', 1, 9, app=(self.screen)).draw()
                        elements.Rectangle(1, 10, 7, 1, app=(self.screen)).draw()
                        if self.message:
                            elements.Output_Message("  •  Product request is invalid.", 1, 10, app=(self.screen)).draw()
                        if self.message2:
                            elements.Output_Message("  •  Please enter the quantity do you request.", 1, 10, app=(self.screen)).draw()
                        if self.message3:
                            elements.Output_Message("  •  Please enter less quantity in stock.", 1, 10, app=(self.screen)).draw()
                        if self.message4:
                            elements.Output_Message("  •  Please enter the quantity more than 0.", 1, 10, app=(self.screen)).draw()
                        if self.message5:
                            elements.Output_Message("  •  No product quantity in stock.", 1, 10, app=(self.screen)).draw()
                        if self.message6:
                            elements.Output_Message("  •  Don't have product in your request.", 1, 10, app=(self.screen)).draw()
                        self.search_input.draw()
                        self.quantity_input.draw()  
                        self.productadd_listview.draw()                     
                    if row == 3 and column == 8:
                        elements.Button(self.screen, config.green, x, y, config.bwidth + 214, config.bheight).Rect()
                        elements.Text_Button_Medium('     SEARCH', position, app=(self.screen)).draw()
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
                        elements.Text_Button_Medium('        ADD', position2, app=(self.screen)).draw()
                    if row == 10 and column == 8:
                        elements.Button(self.screen, config.red, x, y, config.bwidth + 214, config.bheight).Rect()
                        elements.Text_Button_Medium('     CANCEL', position, app=(self.screen)).draw()                 

            for event in pygame.event.get():
                self.search_value = self.search_input.handle_event(event, 1)
                self.quantity_value = self.quantity_input.handle_event(event, 2)
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        self.search_click()
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