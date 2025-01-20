import pygame
from pygame.math import Vector2 as vector
from settings import *
from support import *

from pygame.image import load

from editor import Editor
from level import Level

from os import walk

class Main:
	def __init__(self):
		pygame.init()
		# 创建一个游戏窗口，并设置窗口的宽度和高度为WINDOW_WIDTH和WINDOW_HEIGHT
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		# 设置游戏名
		pygame.display.set_caption('Super Pirate Maker')
		# 创建一个时钟对象，用于控制游戏循环的帧率
		self.clock = pygame.time.Clock()
		# 调用imports()函数，用于导入游戏所需的其他模块或资源
		self.imports()

		# 分数
		self.score = 0

		# 首先进入编辑模式
		self.editor_active = True
		self.transition = Transition(self.toggle)
		self.editor = Editor(self.land_tiles, self.switch)

		# 创建了一个自定义的光标对象，使用pygame.cursors.Cursor()函数，传入一个图片路径来创建光标的图像
		surf = load('../graphics/cursors/mouse.png').convert_alpha()
		cursor = pygame.cursors.Cursor((0, 0), surf)
		pygame.mouse.set_cursor(cursor)

	"""
	导入游戏所需资源
	"""
	def imports(self):
		# terrain
		self.land_tiles = import_folder_dict('../graphics/terrain/land')
		self.water_bottom = load('../graphics/terrain/water/water_bottom.png').convert_alpha()
		self.water_top_animation = import_folder('../graphics/terrain/water/animation')

		# coins
		self.gold = import_folder('../graphics/items/gold')
		self.silver = import_folder('../graphics/items/silver')
		self.diamond = import_folder('../graphics/items/diamond')
		self.particle = import_folder('../graphics/items/particle')

		# palm trees
		self.palms = {folder: import_folder(f'../graphics/terrain/palm/{folder}') for folder in list(walk('../graphics/terrain/palm'))[0][1]}

		# enemies
		self.spikes = load('../graphics/enemies/spikes/spikes.png').convert_alpha()
		self.tooth = {folder: import_folder(f'../graphics/enemies/tooth/{folder}') for folder in list(walk('../graphics/enemies/tooth'))[0][1]}
		self.shell = {folder: import_folder(f'../graphics/enemies/shell_left/{folder}') for folder in list(walk('../graphics/enemies/shell_left/'))[0][1]}
		self.pearl = load('../graphics/enemies/pearl/pearl.png').convert_alpha()

		# player
		self.player_graphics = {folder: import_folder(f'../graphics/player/{folder}') for folder in list(walk('../graphics/player/'))[0][1]}

		# clouds
		self.clouds = import_folder('../graphics/clouds')

		# sounds
		self.level_sounds = {
			'coin': pygame.mixer.Sound('../audio/coin.wav'),
			'hit': pygame.mixer.Sound('../audio/hit.wav'),
			'jump': pygame.mixer.Sound('../audio/jump.wav'),
			'music': pygame.mixer.Sound('../audio/SuperHero.ogg'),
		}

	"""
	用于切换编辑器状态
	"""
	def toggle(self):
		print('进入toggle，切换游戏的模式状态')
		self.editor_active = not self.editor_active
		# 通过检查self.editor_active的值，判断是否需要启动编辑器音乐
		if self.editor_active:
			self.editor.editor_music.play()

	"""
	用于切换关卡
	"""
	def switch(self, grid = None):
		print('进入switch函数')
		# 将self.transition.active设置为True，表示切换过程正在进行中
		self.transition.active = True
		# 通过检查grid参数是否存在，来确定是否需要创建新的关卡。如果grid不为空，则表示需要创建新的关卡
		if grid:
			# 在创建关卡时，将所需的资源作为参数传递给Level类的构造函数，以便在关卡中使用这些资源。这些资源包括各种地块、物品、敌人和玩家的图像资源，以及音效资源
			self.level = Level(
				grid, 
				self.switch,{
					'land': self.land_tiles,
					'water bottom': self.water_bottom,
					'water top': self.water_top_animation,
					'gold': self.gold,
					'silver': self.silver,
					'diamond': self.diamond,
					'particle': self.particle,
					'palms': self.palms,
					'spikes': self.spikes,
					'tooth': self.tooth,
					'shell': self.shell,
					'player': self.player_graphics,
					'pearl': self.pearl,
					'clouds': self.clouds},
				self.level_sounds)

	def run(self):
		while True:
			dt = self.clock.tick() / 1000
			# 通过检查self.editor_active的值，决定是运行编辑器还是关卡
			if self.editor_active:
				self.editor.run(dt)

			else:
				self.level.run(dt)

			self.transition.display(dt)
			pygame.display.update()



"""
Transition的类的定义，用于实现游戏中的过渡效果
"""
class Transition:
	def __init__(self, toggle):
		# 使用pygame.display.get_surface()获取当前显示的游戏窗口
		self.display_surface = pygame.display.get_surface()
		self.toggle = toggle
		self.active = False

		self.border_width = 0
		self.direction = 1
		self.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
		self.radius = vector(self.center).magnitude()
		self.threshold = self.radius + 100

	"""
	用于在游戏窗口中绘制过渡效果
	"""
	def display(self, dt):
		if self.active:
			self.border_width += 1000 * dt * self.direction
			if self.border_width >= self.threshold:
				self.direction = -1
				self.toggle()
			
			if self.border_width < 0:
				self.active = False
				self.border_width = 0
				self.direction = 1
			pygame.draw.circle(self.display_surface, 'black',self.center, self.radius, int(self.border_width))




if __name__ == '__main__':
	main = Main()
	main.run() 