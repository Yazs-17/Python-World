# coding:UTF-8

import sys
sys.path.insert(0, "../")

import aiml

#os.chdir('./res/alice')
k = aiml.Kernel()
k.learn("cn-startup.xml")
#k.respond('LOAD ALICE')
#k.respond("load alice")
k.respond("load aiml cn")

while True:
	print(k.respond(input(">>")))
