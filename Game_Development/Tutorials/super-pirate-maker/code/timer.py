import pygame

"""
Timer的类的定义，用于实现计时器功能
"""
class Timer:
	def __init__(self, duration):
		self.duration = duration
		self.active = False
		self.start_time = 0

	def activate(self):
		self.active = True
		self.start_time = pygame.time.get_ticks()

	def deactivate(self):
		self.active = False
		self.start_time = 0

	def update(self):
		current_time = pygame.time.get_ticks()
		if current_time - self.start_time >= self.duration:
			self.deactivate()