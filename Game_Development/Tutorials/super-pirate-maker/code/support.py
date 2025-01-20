import pygame
from os import walk

"""
接受一个参数path，表示文件夹的路径。函数使用os.walk()方法遍历指定路径下的所有文件和子文件夹
"""
def import_folder(path):
	surface_list = []

	for folder_name, sub_folders, img_files in walk(path):
		for image_name in img_files:
			full_path = path + '/' + image_name
			image_surf = pygame.image.load(full_path).convert_alpha()
			surface_list.append(image_surf)
	return surface_list


"""
import_folder_dict函数与import_folder函数类似，但它返回一个字典，其中每个图像的文件名（不包括扩展名）用作键，对应的surface对象用作值
"""
def import_folder_dict(path):
	surface_dict = {}

	for folder_name, sub_folders, img_files in walk(path):
		for image_name in img_files:
			full_path = path + '/' + image_name
			image_surf = pygame.image.load(full_path).convert_alpha()
			surface_dict[image_name.split('.')[0]] = image_surf
			
	return surface_dict