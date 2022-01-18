import discord

import time

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

#setting
font_name = "HGRGY.TTC"

def create(content):
	size = (765, 1265)
	text = [s[-1] for s in content.split(",")]
	#text_size = 910-len(text)*210
	text_size = 350
	if len(text)==2:
		text_size = 500
	elif len(text)==1:
		text_size = 800

	base_image_path = "base.png"
	base_img = Image.open(base_image_path).copy()
	img = base_img.resize(size=size, resample=Image.ANTIALIAS)

	font = ImageFont.truetype(font_name,text_size)
	draw = ImageDraw.Draw(img)
	textsize = draw.textsize("\n".join(list(text)), font=font)
	pos = ((size[0]-textsize[0])//2,(size[1]*1.1-textsize[1])//2)
	acolors = {
		"red": (231,30,48),
		"black": (0,0,0),
		"blue": (79, 145, 223),
		"green": (0,134,53),
	}
	for data in content.split(","):
		if len(data)==2 and data[0] in ["g","r","b"]:
			if data[0]=="g":
				color = acolors["green"]
			elif data[0]=="r":
				color = acolors["red"]
			elif data[0]=="b":
				color = acolors["blue"]
		else:
			color = acolors["black"]
		c = data[-1]
		draw = ImageDraw.Draw(img)
		textsize = draw.textsize(c, font=font)
		#print(pos)
		cp = (pos[0], pos[1])
		print("color is",color)
		draw.text(cp, c, fill=color, font=font)
		#draw.text(cp, c, fill=(231,30,48), font=font)
		pos = (pos[0], pos[1]+textsize[1])

	file_path = "data/"+str(int(time.time()))+".png"
	img.save(file_path)
	#img.show()
	return file_path

def req(content):
	if len(content.split(","))>3:
		return "3文字までです",405
	else:
		try:
			return create(content),200
		except Exception as e:
			print(e)
			return "正しく入力してください",500

client = discord.Client()


#res,status = req("テ,rス,gト")

@client.event
async def on_ready():
	print("ready")

@client.event
async def on_message(message):
	if message.author!=client.user:
		prefix = "!mj "
		if message.content == prefix+"[]":
			res,status = "base.png",200
			if status!=200:
				await message.channel.send(res)
			else:
				await message.channel.send(file=discord.File(res))
		elif message.content.startswith(prefix):
			content = message.content[len(prefix):]
			res,status = req(content)
			if status!=200:
				await message.channel.send(res)
			else:
				await message.channel.send(file=discord.File(res))

with open("discord_token.txt") as f:
	token = f.read()

client.run(token)
