# -*- coding: utf-8 -*-
import discord
from discord.channel import Channel, PrivateChannel
from urllib.parse import urlparse, urlencode
from time import sleep
from urllib.request import urlopen
import json as j
from math import floor, ceil
import subprocess as sp
import sys

cl = discord.Client()

CMD_PREFIX = "::"
APPID = "OxmjFTOolhIL3IKDpkQ2"

@cl.event
async def on_ready():
	print("Logged in as\n"+cl.user.name+"\n"+cl.user.id+"\n-----")

@cl.event
async def on_message(m):
	reply = m.channel
	if m.content.startswith(CMD_PREFIX) is True:
		cmd = m.content.split(" ")
		if cmd[1] == "":
			await cl.send_message(m.channel, m.author.mention+"\nError: 引数1は必須です。")
			return
		if cmd[2] == "":
			await cl.send_message(m.channel, m.author.mention+"\nError: 引数2は必須です。")
			return
		try:
			page = str(int(cmd[3]))
		except (IndexError, ValueError):
			page = "1"
		if cmd[0] == CMD_PREFIX+"search" or cmd[0] == CMD_PREFIX+"s":
			if cmd[1] == "free":
				type = "q"
				value = cmd[2]
			elif cmd[1] == "title":
				type = "title"
				value = cmd[2]
			elif cmd[1] == "author":
				type = "author"
				value = cmd[2]
			elif cmd[1] == "publisher":
				type = "publisher"
				value = cmd[2]
			elif cmd[1] == "isbn":
				type = "isbn"
				value = cmd[2]
			elif cmd[1] == "ncid":
				type = "ncid"
				value = cmd[2]
			else:
				await cl.send_message(m.channel, m.author.mention+"\nError: 引数2には「free」、「title」、「author」、「publisher」、「isbn」、「ncid」のみ指定できます。")
				return
			url = "http://ci.nii.ac.jp/books/opensearch/search?"
			url += urlencode({type: value})
			url += "&appid="+APPID
			url += "&format=json"
			url += "&p="+page
			try:
				pageint = int(page)
			except ValueError:
				await cl.send_message(m.channel, m.author.mention+"\nError: 引数3には数字のみ指定できます。")
				return
			with urlopen(url) as res:
				json = j.load(res)
			result1 = m.author.mention+"\n"
			result1 += "---"+json["@graph"][0]["title"]+"---\n"
			result1 += "ヒット数: "+json["@graph"][0]["opensearch:totalResults"]+"\n"
			result1 += "ページ: "+page+"/"+str(ceil(int(json["@graph"][0]["opensearch:totalResults"]) / 20))
			result1 += "\n----------"
			await cl.send_message(reply, result1)
			result1 = m.author.mention+"\n"
			try:
				for var in range(len(json["@graph"][0]["items"])):
					result1 += str(var + 1 + int(json["@graph"][0]["opensearch:startIndex"]))+"/"+json["@graph"][0]["opensearch:totalResults"]+"\n"
					result1 += "タイトル: "+json["@graph"][0]["items"][var]["title"]+"\n"
					try:
						result1 += "著者: "+json["@graph"][0]["items"][var]["dc:creator"]+"\n"
					except KeyError:
						result1 += "著者: ---\n"
					result1 += "出版社: "
					for pub in range(len(json["@graph"][0]["items"][var]["dc:publisher"])):
						result1 += "["+json["@graph"][0]["items"][var]["dc:publisher"][pub]+"]"
					result1 += "\n"
					try:
						result1 += "出版年: "+json["@graph"][0]["items"][var]["dc:date"]+"\n"
					except KeyError:
						result1 += "出版年: ----\n"
					result1 += "NCID: "+json["@graph"][0]["items"][var]["link"]["@id"].replace("http://ci.nii.ac.jp/ncid/", "")+"\n"
					result1 += "詳細: "+json["@graph"][0]["items"][var]["link"]["@id"]+"\n"
					result1 += "----------\n"
					await cl.send_message(reply, result1)
					result1 = m.author.mention+"\n"
				await cl.send_message(reply, m.author.mention+"\n--End of Results--")
			except KeyError:
				await cl.send_message(reply, m.author.mention+"\nNo Results found.")

cl.run("NDEyNDMyMDczNzQwMjU1MjMz.DWKK0w.-b4k_2PFpxuFliFD04oKxOq-TL4")