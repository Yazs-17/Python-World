import pygame
from pygame.math import Vector2 as vector

from settings import *
from timer import Timer

from random import choice, randint

"""
通用的角色类，包含了角色的基本属性和方法
"""
class Generic(pygame.sprite.Sprite):
	def __init__(self, pos, surf, group, z = LEVEL_LAYERS['main']):
		super().__init__(group)
		self.image = surf
		self.rect = self.image.get_rect(topleft = pos)
		self.z = z

"""
游戏中的方块角色，继承自Generic类
"""
class Block(Generic):
	def __init__(self, pos, size, group):
		surf = pygame.Surface(size)
		super().__init__(pos, surf, group)

"""
游戏中的云朵角色
"""
class Cloud(Generic):
	def __init__(self, pos, surf, group, left_limit):
		super().__init__(pos, surf, group, LEVEL_LAYERS['clouds'])
		self.left_limit = left_limit

		# movement
		self.pos = vector(self.rect.topleft)
		self.speed = randint(20,30)

	def update(self, dt):
		self.pos.x -= self.speed * dt
		self.rect.x = round(self.pos.x)
		if self.rect.x <= self.left_limit:
			self.kill()


"""
游戏中的动画对象角色，继承自Generic类，具有动画效果。
"""

# simple animated objects
class Animated(Generic):
	def __init__(self, assets, pos, group, z = LEVEL_LAYERS['main']):
		self.animation_frames = assets
		self.frame_index = 0
		super().__init__(pos, self.animation_frames[self.frame_index], group, z)

	def animate(self, dt):
		self.frame_index += ANIMATION_SPEED * dt
		self.frame_index = 0 if self.frame_index >= len(self.animation_frames) else self.frame_index
		self.image = self.animation_frames[int(self.frame_index)]

	def update(self, dt):
		self.animate(dt)

"""
碰撞
"""
class Particle(Animated):
	def __init__(self, assets, pos, group):
		super().__init__(assets, pos, group)
		self.rect = self.image.get_rect(center = pos)

	def animate(self, dt):
		self.frame_index += ANIMATION_SPEED * dt
		if self.frame_index < len(self.animation_frames):
			self.image = self.animation_frames[int(self.frame_index)]
		else:
			self.kill()

"""
金币
"""
class Coin(Animated):
	def __init__(self, coin_type, assets, pos, group):
		super().__init__(assets, pos, group)
		self.rect = self.image.get_rect(center = pos)
		self.coin_type = coin_type


# enemies
"""
尖刺
"""
class Spikes(Generic):
	def __init__(self, surf, pos, group):
		super().__init__(pos, surf, group)
		self.mask = pygame.mask.from_surface(self.image)

"""
牙齿敌人
"""
class Tooth(Generic):
	def __init__(self, assets, pos, group, collision_sprites):

		# general setup
		self.animation_frames = assets
		self.frame_index = 0
		self.orientation = 'right'
		surf = self.animation_frames[f'run_{self.orientation}'][self.frame_index]
		super().__init__(pos, surf, group)
		self.rect.bottom = self.rect.top + TILE_SIZE
		self.mask = pygame.mask.from_surface(self.image)

		# movement
		self.direction = vector(choice((1,-1)),0)
		self.orientation = 'left' if self.direction.x < 0 else 'right'
		self.pos = vector(self.rect.topleft)
		self.speed = 120
		self.collision_sprites = collision_sprites

		# destory tooth at the beginning if he is not on a floor
		if not [sprite for sprite in collision_sprites if sprite.rect.collidepoint(self.rect.midbottom + vector(0,10))]:
			self.kill()

	def animate(self, dt):
		current_animation = self.animation_frames[f'run_{self.orientation}']
		self.frame_index += ANIMATION_SPEED * dt
		self.frame_index = 0 if self.frame_index >= len(current_animation) else self.frame_index
		self.image = current_animation[int(self.frame_index)]
		self.mask = pygame.mask.from_surface(self.image)

	def move(self, dt):
		right_gap = self.rect.bottomright + vector(1,1)
		right_block = self.rect.midright + vector(1,0)
		left_gap = self.rect.bottomleft + vector(-1,1)
		left_block = self.rect.midleft + vector(-1,0)

		if self.direction.x > 0: # moving right
			# 1. no floor collision
			floor_sprites = [sprite for sprite in self.collision_sprites if sprite.rect.collidepoint(right_gap)]
			# 2. wall collision
			wall_sprites = [sprite for sprite in self.collision_sprites if sprite.rect.collidepoint(right_block)]
			if wall_sprites or not floor_sprites:
				self.direction.x *= -1
				self.orientation = 'left'

		# exercise
		if self.direction.x < 0:  
			if not [sprite for sprite in self.collision_sprites if sprite.rect.collidepoint(left_gap)] \
			or [sprite for sprite in self.collision_sprites if sprite.rect.collidepoint(left_block)]:
				self.direction.x *= -1
				self.orientation = 'right'

		self.pos.x += self.direction.x * self.speed * dt
		self.rect.x = round(self.pos.x)

	def update(self, dt):
		self.animate(dt)
		self.move(dt)

"""
贝壳敌人
"""
class Shell(Generic):
	def __init__(self, orientation, assets, pos, group, pearl_surf, damage_sprites):
		self.orientation = orientation
		self.animation_frames = assets.copy()
		if orientation == 'right':
			for key, value in self.animation_frames.items():
				self.animation_frames[key] = [pygame.transform.flip(surf,True,False) for surf in value]

		self.frame_index = 0
		self.status = 'idle'
		super().__init__(pos, self.animation_frames[self.status][self.frame_index], group)
		self.rect.bottom = self.rect.top + TILE_SIZE

		# pearl 
		self.pearl_surf = pearl_surf
		self.has_shot = False
		self.attack_cooldown = Timer(2000)
		self.damage_sprites = damage_sprites 

	def animate(self, dt):
		current_animation = self.animation_frames[self.status]
		self.frame_index += ANIMATION_SPEED * dt
		if self.frame_index >= len(current_animation):
			self.frame_index = 0
			if self.has_shot:
				self.attack_cooldown.activate()
				self.has_shot = False
		self.image = current_animation[int(self.frame_index)]

		if int(self.frame_index) == 2 and self.status == 'attack' and not self.has_shot:
			pearl_direction = vector(-1,0) if self.orientation == 'left' else vector(1,0)
			offset = (pearl_direction * 50) + vector(0,-10) if self.orientation == 'left' else (pearl_direction * 20) + vector(0,-10)
			Pearl(self.rect.center + offset, pearl_direction, self.pearl_surf, [self.groups()[0], self.damage_sprites])
			self.has_shot = True

	def get_status(self):
		if vector(self.player.rect.center).distance_to(vector(self.rect.center)) < 500 and not self.attack_cooldown.active:
			self.status = 'attack'
		else:
			self.status = 'idle'

	def update(self, dt):
		self.get_status()
		self.animate(dt)
		self.attack_cooldown.update()

class Pearl(Generic):
	def __init__(self, pos, direction, surf, group):
		super().__init__(pos, surf, group)
		self.mask = pygame.mask.from_surface(self.image)

		# movement 
		self.pos = vector(self.rect.topleft)
		self.direction = direction
		self.speed = 150

		# self destruct 
		self.timer = Timer(6000)
		self.timer.activate()

	def update(self, dt):
		# movement 
		self.pos.x += self.direction.x * self.speed * dt
		self.rect.x = round(self.pos.x)

		# timer 
		self.timer.update()
		if not self.timer.active:
			self.kill()

"""
Player的类，它表示游戏中的玩家角色,处理玩家的动画、移动、碰撞和更新
"""
class Player(Generic):
	def __init__(self, pos, assets, group, collision_sprites, jump_sound):
		
		# animation
		self.animation_frames = assets  # 存储用于动画的图像帧
		self.frame_index = 0  # 当前动画帧的索引
		self.status = 'idle' #玩家的状态（空闲、奔跑、跳跃、下落）
		self.orientation = 'right'
		surf = self.animation_frames[f'{self.status}_{self.orientation}'][self.frame_index]
		super().__init__(pos, surf, group)
		self.mask = pygame.mask.from_surface(self.image)
		# 设置血条
		self.life = 2

		# movement
		self.direction = vector()
		self.pos = vector(self.rect.center)
		self.speed = 300  # 玩家的移动速度
		self.gravity = 4  # 重力的强度
		self.on_floor = False  # 玩家是否在地面上

		# collision  碰撞
		self.collision_sprites = collision_sprites
		self.hitbox = self.rect.inflate(-50, 0)

		# timer 
		self.invul_timer = Timer(200)

		# sound
		self.jump_sound = jump_sound
		self.jump_sound.set_volume(0.2)

	"""
	受到伤害时的操作，使玩家向上移动并启动无敌计时器
	"""
	def damage(self):
		if not self.invul_timer.active:
			print('受伤')
			self.invul_timer.activate()
			self.direction.y -= 1.5
			self.life -= 1




	"""
	根据玩家的上下运动情况确定状态
	"""
	def get_status(self):
		if self.direction.y < 0:
			self.status = 'jump'
		elif self.direction.y > 1:
			self.status = 'fall'
		else:
			self.status = 'run' if self.direction.x != 0 else 'idle'

	"""
	根据当前状态和朝向播放适当的动画帧
	"""
	def animate(self, dt):
		current_animation = self.animation_frames[f'{self.status}_{self.orientation}']
		self.frame_index += ANIMATION_SPEED * dt
		self.frame_index = 0 if self.frame_index >= len(current_animation) else self.frame_index
		self.image = current_animation[int(self.frame_index)]
		self.mask = pygame.mask.from_surface(self.image)

		if self.invul_timer.active:
			surf = self.mask.to_surface()
			surf.set_colorkey('black')
			self.image = surf

	"""
	处理玩家输入，包括移动方向和跳跃动作
	"""
	def input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_RIGHT]:
			self.direction.x = 1
			self.orientation = 'right'
		elif keys[pygame.K_LEFT]:
			self.direction.x = -1
			self.orientation = 'left'
		else:
			self.direction.x = 0

		if keys[pygame.K_SPACE] and self.on_floor:
			self.direction.y = -2
			self.jump_sound.play()

	"""
	处理玩家的移动，包括水平和垂直移动，并进行碰撞检测
	"""
	def move(self, dt):
		
		# horizontal movement
		self.pos.x += self.direction.x * self.speed * dt
		self.hitbox.centerx = round(self.pos.x)
		self.rect.centerx = self.hitbox.centerx
		self.collision('horizontal')

		# vertical movement
		self.pos.y += self.direction.y * self.speed * dt
		self.hitbox.centery = round(self.pos.y)
		self.rect.centery = self.hitbox.centery
		self.collision('vertical')

	"""
	应用重力，使玩家向下移动
	"""
	def apply_gravity(self, dt):
		self.direction.y += self.gravity * dt
		self.rect.y += self.direction.y

	"""
	检查玩家是否在地面上
	"""
	def check_on_floor(self):
		floor_rect = pygame.Rect(self.hitbox.bottomleft, (self.hitbox.width, 2))
		floor_sprites = [sprite for sprite in self.collision_sprites if sprite.rect.colliderect(floor_rect)]
		self.on_floor = True if floor_sprites else False

	def collision(self, direction):
		for sprite in self.collision_sprites:
			if sprite.rect.colliderect(self.hitbox):
				if direction == 'horizontal':
					self.hitbox.right = sprite.rect.left if self.direction.x > 0 else self.hitbox.right
					self.hitbox.left = sprite.rect.right if self.direction.x < 0 else self.hitbox.left
					self.rect.centerx, self.pos.x = self.hitbox.centerx, self.hitbox.centerx
				else: # vertical
					self.hitbox.top = sprite.rect.bottom if self.direction.y < 0 else self.hitbox.top
					self.hitbox.bottom = sprite.rect.top if self.direction.y > 0 else self.hitbox.bottom
					self.rect.centery, self.pos.y = self.hitbox.centery, self.hitbox.centery
					self.direction.y = 0

	def update(self, dt):
		self.input()
		self.apply_gravity(dt)
		self.move(dt)
		self.check_on_floor()
		self.invul_timer.update()

		self.get_status()
		self.animate(dt)
