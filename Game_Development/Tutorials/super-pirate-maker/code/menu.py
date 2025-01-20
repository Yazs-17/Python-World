import pygame
from settings import *
from pygame.image import load

"""
Menu的类，用于创建游戏中的菜单界面
"""
class Menu:
	def __init__(self):
		# display_surface属性表示要显示菜单的表面对象
		self.display_surface = pygame.display.get_surface()
		self.create_data()
		self.create_buttons()

	"""
	于创建菜单所需的数据，将每个菜单按钮的图像加载到self.menu_surfs字典中
	"""
	def create_data(self):
		self.menu_surfs = {}
		for key, value in EDITOR_DATA.items():
			if value['menu']:
				if not value['menu'] in self.menu_surfs:
					self.menu_surfs[value['menu']] = [(key,load(value['menu_surf']))]
				else:
					self.menu_surfs[value['menu']].append((key,load(value['menu_surf'])))

	"""
	用于创建菜单中的按钮，通过定义按钮的矩形区域和加载相应的图像，并添加到self.buttons精灵组中。
	"""
	def create_buttons(self):
		
		# menu area
		size = 180
		margin = 6
		topleft = (WINDOW_WIDTH - size - margin,WINDOW_HEIGHT - size - margin)
		self.rect = pygame.Rect(topleft,(size,size))

		# button areas
		generic_button_rect = pygame.Rect(self.rect.topleft, (self.rect.width / 2, self.rect.height / 2))
		button_margin = 5
		self.tile_button_rect = generic_button_rect.copy().inflate(-button_margin,-button_margin)
		self.coin_button_rect = generic_button_rect.move(self.rect.height / 2,0).inflate(-button_margin,-button_margin)
		self.enemy_button_rect = generic_button_rect.move(self.rect.height / 2,self.rect.width / 2).inflate(-button_margin,-button_margin)
		self.palm_button_rect = generic_button_rect.move(0,self.rect.width / 2).inflate(-button_margin,-button_margin)

		# create the buttons
		self.buttons = pygame.sprite.Group()
		Button(self.tile_button_rect, self.buttons, self.menu_surfs['terrain'])
		Button(self.coin_button_rect, self.buttons, self.menu_surfs['coin'])
		Button(self.enemy_button_rect, self.buttons, self.menu_surfs['enemy'])
		Button(self.palm_button_rect, self.buttons, self.menu_surfs['palm fg'], self.menu_surfs['palm bg'])

	"""
	用于处理点击事件，根据鼠标点击的位置和按钮的状态进行响应
	"""
	def click(self, mouse_pos, mouse_button):
		for sprite in self.buttons:
			if sprite.rect.collidepoint(mouse_pos):
				if mouse_button[1]: # middle mouse click
					if sprite.items['alt']:
						sprite.main_active = not sprite.main_active 
				if mouse_button[2]: # right click
					sprite.switch()
				return sprite.get_id()

	"""
	用于在菜单界面上高亮显示当前选中的按钮指示器。根据按钮所属的菜单类型，绘制对应的矩形框来高亮显示
	"""
	def highlight_indicator(self, index):
		if EDITOR_DATA[index]['menu'] == 'terrain':
			pygame.draw.rect(self.display_surface, BUTTON_LINE_COLOR, self.tile_button_rect.inflate(4,4),5,4)
		if EDITOR_DATA[index]['menu'] == 'coin':
			pygame.draw.rect(self.display_surface, BUTTON_LINE_COLOR, self.coin_button_rect.inflate(4,4),5,4)
		if EDITOR_DATA[index]['menu'] == 'enemy':
			pygame.draw.rect(self.display_surface, BUTTON_LINE_COLOR, self.enemy_button_rect.inflate(4,4),5,4)
		if EDITOR_DATA[index]['menu'] in ('palm bg', 'palm fg'):
			pygame.draw.rect(self.display_surface, BUTTON_LINE_COLOR, self.palm_button_rect.inflate(4,4),5,4)

	"""
	显示整个菜单界面。先更新按钮的状态，然后将按钮绘制到display_surface表面上，最后调用highlight_indicator方法来高亮显示当前选中的按钮指示器
	"""
	def display(self, index):
		self.buttons.update()
		self.buttons.draw(self.display_surface)
		self.highlight_indicator(index)

"""
Button的类，用于创建游戏中的按钮对象
"""
class Button(pygame.sprite.Sprite):

	"""
	创建了一个精灵对象。初始化了一些属性和变量，包括按钮的图像、矩形区域、按钮的状态和索引等
	"""
	def __init__(self, rect, group, items, items_alt = None):
		super().__init__(group)
		self.image = pygame.Surface(rect.size)
		self.rect = rect

		# items 
		self.items = {'main': items, 'alt': items_alt}
		self.index = 0
		self.main_active = True

	"""
	获取按钮对应的ID值，根据当前按钮状态和索引来确定返回的ID
	"""
	def get_id(self):
		return self.items['main' if self.main_active else 'alt'][self.index][0]

	"""
	用于切换按钮的状态和索引值。每次调用该方法，索引值加1，并根据索引是否越界来更新索引值
	"""
	def switch(self):
		self.index += 1
		self.index = 0 if self.index >= len(self.items['main' if self.main_active else 'alt']) else self.index

	def update(self):
		self.image.fill(BUTTON_BG_COLOR)
		surf = self.items['main' if self.main_active else 'alt'][self.index][1]
		rect = surf.get_rect(center = (self.rect.width / 2, self.rect.height / 2))
		self.image.blit(surf, rect)