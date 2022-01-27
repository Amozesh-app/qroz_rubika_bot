import asyncio
import base64
import concurrent.futures
import datetime
import glob
import json
import math
import os
import pathlib
import random
import sys
import time
from json import dumps, loads
from random import randint
import re
from re import findall
import requests
import urllib3
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from requests import post
from googletrans import Translator
import io
from PIL import Image , ImageFont, ImageDraw 
import arabic_reshaper
from bidi.algorithm import get_display
from mutagen.mp3 import MP3
from gtts import gTTS
from threading import Thread
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
#lisence by bahman ahmadi this classes
#this classes opened sourse and free
class encryption:
    def __init__(self, auth):
        self.key = bytearray(self.secret(auth), "UTF-8")
        self.iv = bytearray.fromhex('00000000000000000000000000000000')

    def replaceCharAt(self, e, t, i):
        return e[0:t] + i + e[t + len(i):]

    def secret(self, e):
        t = e[0:8]
        i = e[8:16]
        n = e[16:24] + t + e[24:32] + i
        s = 0
        while s < len(n):
            e = n[s]
            if e >= '0' and e <= '9':
                t = chr((ord(e[0]) - ord('0') + 5) % 10 + ord('0'))
                n = self.replaceCharAt(n, s, t)
            else:
                t = chr((ord(e[0]) - ord('a') + 9) % 26 + ord('a'))
                n = self.replaceCharAt(n, s, t)
            s += 1
        return n

    def encrypt(self, text):
        raw = pad(text.encode('UTF-8'), AES.block_size)
        aes = AES.new(self.key, AES.MODE_CBC, self.iv)
        enc = aes.encrypt(raw)
        result = base64.b64encode(enc).decode('UTF-8')
        return result

    def decrypt(self, text):
        aes = AES.new(self.key, AES.MODE_CBC, self.iv)
        dec = aes.decrypt(base64.urlsafe_b64decode(text.encode('UTF-8')))
        result = unpad(dec, AES.block_size).decode('UTF-8')
        return result

class Bot:
	def __init__(self, auth):
		self.auth = auth
		self.enc = encryption(auth)
		
	def sendMessage(self, chat_id, text, message_id=None):
		if message_id == None:
			t = False
			while t == False:
				try:
					p = post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
						"method":"sendMessage",
						"input":{
							"object_guid":chat_id,
							"rnd":f"{randint(100000,900000)}",
							"text":text,
							"reply_to_message_id":message_id
						},
						"client":{
							"app_name":"Main",
							"app_version":"3.2.1",
							"platform":"Web",
							"package":"web.rubika.ir",
							"lang_code":"fa"
						}
					}))},url="https://messengerg2c17.iranlms.ir/")
					p = loads(self.enc.decrypt(p.json()["data_enc"]))
					t = True
				except:
					t = False
			return p
		else:
			t = False
			while t == False:
				try:
					p = post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
						"method":"sendMessage",
						"input":{
							"object_guid":chat_id,
							"rnd":f"{randint(100000,900000)}",
							"text":text,
							"reply_to_message_id":message_id
						},
						"client":{
							"app_name":"Main",
							"app_version":"3.2.1",
							"platform":"Web",
							"package":"web.rubika.ir",
							"lang_code":"fa"
						}
					}))},url="https://messengerg2c17.iranlms.ir/")
					p = loads(self.enc.decrypt(p.json()["data_enc"]))
					t = True
				except:
					t = False
			return p
	
	def deleteMessages(self, chat_id, message_ids):
		return post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"deleteMessages",
			"input":{
				"object_guid":chat_id,
				"message_ids":message_ids,
				"type":"Global"
			},
			"client":{
				"app_name":"Main",
				"app_version":"3.2.1",
				"platform":"Web",
				"package":"web.rubika.ir",
				"lang_code":"fa"
			}
		}))},url="https://messengerg2c66.iranlms.ir/")

	def requestFile(self, name, size , mime):
		o = ''
		while str(o) != '<Response [200]>':
			o = post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
				"method":"requestSendFile",
				"input":{
					"file_name":name,
					"size":size,
					"mime":mime
				},
				"client":{
					"app_name":"Main",
					"app_version":"3.2.1",
					"platform":"Web",
					"package":"web.rubika.ir",
					"lang_code":"fa"
				}
			}))},url="https://messengerg2c66.iranlms.ir/")
			try:
				k = loads(self.enc.decrypt(o.json()["data_enc"]))
				if k['status'] != 'OK' or k['status_det'] != 'OK':
					o = '502'
			except:
				o = '502'
		return k['data']

	def fileUpload(self, bytef ,hash_send ,file_id ,url):		
		if len(bytef) <= 131072:
			h = {
				'auth':self.auth,
				'chunk-size':str(len(bytef)),
				'file-id':str(file_id),
				'access-hash-send':hash_send,
				'total-part':str(1),
				'part-number':str(1)
			}
			t = False
			while t == False:
				try:
					j = post(data=bytef,url=url,headers=h).text
					j = loads(j)['data']['access_hash_rec']
					t = True
				except:
					t = False
			
			return j
		else:
			t = len(bytef) / 131072
			t += 1
			t = random._floor(t)
			for i in range(1,t+1):
				if i != t:
					k = i - 1
					k = k * 131072
					t2 = False
					while t2 == False:
						try:
							o = post(data=bytef[k:k + 131072],url=url,headers={
								'auth':self.auth,
								'chunk-size':str(131072),
								'file-id':file_id,
								'access-hash-send':hash_send,
								'total-part':str(t),
								'part-number':str(i)
							}).text
							o = loads(o)['data']
							t2 = True
						except:
							t2 = False
					j = k + 131072
					j = round(j / 1024)
					j2 = round(len(bytef) / 1024)
					print(str(j) + 'kb / ' + str(j2) + ' kb')                
				else:
					k = i - 1
					k = k * 131072
					t2 = False
					while t2 == False:
						try:
							p = post(data=bytef[k:],url=url,headers={
								'auth':self.auth,
								'chunk-size':str(len(bytef[k:])),
								'file-id':file_id,
								'access-hash-send':hash_send,
								'total-part':str(t),
								'part-number':str(i)
							}).text
							p = loads(p)['data']['access_hash_rec']
							t2 = True
						except:
							t2 = False
					j2 = round(len(bytef) / 1024)
					print(str(j2) + 'kb / ' + str(j2) + ' kb') 
					return p

	def sendFile(self, chat_id, file_id , mime , dc_id, access_hash_rec, file_name, size, text=None, message_id=None):
			if text == None:
				if message_id == None:
					t = False
					while t == False:
						try:
							p = loads(self.enc.decrypt(loads(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
								"method":"sendMessage",
								"input":{
									"object_guid":chat_id,
									"rnd":f"{randint(100000,900000)}",
									"file_inline":{
										"dc_id":str(dc_id),
										"file_id":str(file_id),
										"type":"File",
										"file_name":file_name,
										"size":size,
										"mime":mime,
										"access_hash_rec":access_hash_rec
									}
								},
								"client":{
									"app_name":"Main",
									"app_version":"3.2.1",
									"platform":"Web",
									"package":"web.rubika.ir",
									"lang_code":"fa"
								}
							}))},url="https://messengerg2c17.iranlms.ir/").text)['data_enc']))
							t = True
						except:
							t = False
					return p
				else:
					return loads(self.enc.decrypt(loads(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
						"method":"sendMessage",
						"input":{
							"object_guid":chat_id,
							"rnd":f"{randint(100000,900000)}",
							"reply_to_message_id":message_id,
							"file_inline":{
								"dc_id":str(dc_id),
								"file_id":str(file_id),
								"type":"File",
								"file_name":file_name,
								"size":size,
								"mime":mime,
								"access_hash_rec":access_hash_rec
							}
						},
						"client":{
							"app_name":"Main",
							"app_version":"3.2.1",
							"platform":"Web",
							"package":"web.rubika.ir",
							"lang_code":"fa"
						}
					}))},url="https://messengerg2c17.iranlms.ir/").text)['data_enc']))    
			else:
				if message_id == None:
					return loads(self.enc.decrypt(loads(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
						"method":"sendMessage",
						"input":{
							"object_guid":chat_id,
							"rnd":f"{randint(100000,900000)}",
							"text":text,
							"file_inline":{
								"dc_id":str(dc_id),
								"file_id":str(file_id),
								"type":"File",
								"file_name":file_name,
								"size":size,
								"mime":mime,
								"access_hash_rec":access_hash_rec
							}
						},
						"client":{
							"app_name":"Main",
							"app_version":"3.2.1",
							"platform":"Web",
							"package":"web.rubika.ir",
							"lang_code":"fa"
						}
					}))},url="https://messengerg2c17.iranlms.ir/").text)['data_enc']))
				else:
					return loads(self.enc.decrypt(loads(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
						"method":"sendMessage",
						"input":{
							"object_guid":chat_id,
							"rnd":f"{randint(100000,900000)}",
							"text":text,
							"reply_to_message_id":message_id,
							"file_inline":{
								"dc_id":str(dc_id),
								"file_id":str(file_id),
								"type":"File",
								"file_name":file_name,
								"size":size,
								"mime":mime,
								"access_hash_rec":access_hash_rec
							}
						},
						"client":{
							"app_name":"Main",
							"app_version":"3.2.1",
							"platform":"Web",
							"package":"web.rubika.ir",
							"lang_code":"fa"
						}
					}))},url="https://messengerg2c17.iranlms.ir/").text)['data_enc'])) 

	def sendImage(self, chat_id, file_id , mime , dc_id, access_hash_rec, file_name,  size, thumb_inline , width , height, text=None, message_id=None):
			if text == None:
				if message_id == None:
					t = False
					while t == False:
						try:
							p = loads(self.enc.decrypt(loads(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
								"method":"sendMessage",
								"input":{
									"object_guid":chat_id,
									"rnd":f"{randint(100000,900000)}",
									"file_inline":{
										"dc_id":str(dc_id),
										"file_id":str(file_id),
										"type":"Image",
										"file_name":file_name,
										"size":size,
										"mime":mime,
										"access_hash_rec":access_hash_rec,
										'thumb_inline':thumb_inline,
										'width':width,
										'height':height
									}
								},
								"client":{
									"app_name":"Main",
									"app_version":"3.2.1",
									"platform":"Web",
									"package":"web.rubika.ir",
									"lang_code":"fa"
								}
							}))},url="https://messengerg2c17.iranlms.ir/").text)['data_enc']))
							t = True
						except:
							t = False
					return p
				else:
					return loads(self.enc.decrypt(loads(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
						"method":"sendMessage",
						"input":{
							"object_guid":chat_id,
							"rnd":f"{randint(100000,900000)}",
							"reply_to_message_id":message_id,
							"file_inline":{
								"dc_id":str(dc_id),
								"file_id":str(file_id),
								"type":"Image",
								"file_name":file_name,
								"size":size,
								"mime":mime,
								"access_hash_rec":access_hash_rec,
								'thumb_inline':thumb_inline,
								'width':width,
								'height':height
							}
						},
						"client":{
							"app_name":"Main",
							"app_version":"3.2.1",
							"platform":"Web",
							"package":"web.rubika.ir",
							"lang_code":"fa"
						}
					}))},url="https://messengerg2c17.iranlms.ir/").text)['data_enc']))    
			else:
				if message_id == None:
					return loads(self.enc.decrypt(loads(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
						"method":"sendMessage",
						"input":{
							"object_guid":chat_id,
							"rnd":f"{randint(100000,900000)}",
							"text":text,
							"file_inline":{
								"dc_id":str(dc_id),
								"file_id":str(file_id),
								"type":"Image",
								"file_name":file_name,
								"size":size,
								"mime":mime,
								"access_hash_rec":access_hash_rec,
								'thumb_inline':thumb_inline,
								'width':width,
								'height':height
							}
						},
						"client":{
							"app_name":"Main",
							"app_version":"3.2.1",
							"platform":"Web",
							"package":"web.rubika.ir",
							"lang_code":"fa"
						}
					}))},url="https://messengerg2c17.iranlms.ir/").text)['data_enc']))
				else:
					return loads(self.enc.decrypt(loads(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
						"method":"sendMessage",
						"input":{
							"object_guid":chat_id,
							"rnd":f"{randint(100000,900000)}",
							"text":text,
							"reply_to_message_id":message_id,
							"file_inline":{
								"dc_id":str(dc_id),
								"file_id":str(file_id),
								"type":"Image",
								"file_name":file_name,
								"size":size,
								"mime":mime,
								"access_hash_rec":access_hash_rec,
								'thumb_inline':thumb_inline,
								'width':width,
								'height':height
							}
						},
						"client":{
							"app_name":"Main",
							"app_version":"3.2.1",
							"platform":"Web",
							"package":"web.rubika.ir",
							"lang_code":"fa"
						}
					}))},url="https://messengerg2c17.iranlms.ir/").text)['data_enc'])) 

	def sendVoice(self, chat_id, file_id , mime , dc_id, access_hash_rec, file_name,  size, duration, text=None, message_id=None):
			if text == None:
				if message_id == None:
					t = False
					while t == False:
						try:
							p = loads(self.enc.decrypt(loads(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
								"method":"sendMessage",
								"input":{
									"object_guid":chat_id,
									"rnd":f"{randint(100000,900000)}",
									"file_inline":{
										"dc_id":str(dc_id),
										"file_id":str(file_id),
										"type":"Voice",
										"file_name":file_name,
										"size":size,
										"mime":mime,
										"access_hash_rec":access_hash_rec,
										'time':duration,
									}
								},
								"client":{
									"app_name":"Main",
									"app_version":"3.2.1",
									"platform":"Web",
									"package":"web.rubika.ir",
									"lang_code":"fa"
								}
							}))},url="https://messengerg2c17.iranlms.ir/").text)['data_enc']))
							t = True
						except:
							t = False
					return p
				else:
					return loads(self.enc.decrypt(loads(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
						"method":"sendMessage",
						"input":{
							"object_guid":chat_id,
							"rnd":f"{randint(100000,900000)}",
							"reply_to_message_id":message_id,
							"file_inline":{
								"dc_id":str(dc_id),
								"file_id":str(file_id),
								"type":"Voice",
								"file_name":file_name,
								"size":size,
								"mime":mime,
								"access_hash_rec":access_hash_rec,
								'time':duration,
							}
						},
						"client":{
							"app_name":"Main",
							"app_version":"3.2.1",
							"platform":"Web",
							"package":"web.rubika.ir",
							"lang_code":"fa"
						}
					}))},url="https://messengerg2c17.iranlms.ir/").text)['data_enc']))    
			else:
				if message_id == None:
					return loads(self.enc.decrypt(loads(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
						"method":"sendMessage",
						"input":{
							"object_guid":chat_id,
							"rnd":f"{randint(100000,900000)}",
							"text":text,
							"file_inline":{
								"dc_id":str(dc_id),
								"file_id":str(file_id),
								"type":"Voice",
								"file_name":file_name,
								"size":size,
								"mime":mime,
								"access_hash_rec":access_hash_rec,
								'time':duration,
							}
						},
						"client":{
							"app_name":"Main",
							"app_version":"3.2.1",
							"platform":"Web",
							"package":"web.rubika.ir",
							"lang_code":"fa"
						}
					}))},url="https://messengerg2c17.iranlms.ir/").text)['data_enc']))
				else:
					return loads(self.enc.decrypt(loads(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
						"method":"sendMessage",
						"input":{
							"object_guid":chat_id,
							"rnd":f"{randint(100000,900000)}",
							"text":text,
							"reply_to_message_id":message_id,
							"file_inline":{
								"dc_id":str(dc_id),
								"file_id":str(file_id),
								"type":"Voice",
								"file_name":file_name,
								"size":size,
								"mime":mime,
								"access_hash_rec":access_hash_rec,
								'time':duration,
							}
						},
						"client":{
							"app_name":"Main",
							"app_version":"3.2.1",
							"platform":"Web",
							"package":"web.rubika.ir",
							"lang_code":"fa"
						}
					}))},url="https://messengerg2c17.iranlms.ir/").text)['data_enc'])) 

	def getUserInfo(self, chat_id):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"getUserInfo",
			"input":{
				"user_guid":chat_id
			},
			"client":{
				"app_name":"Main",
				"app_version":"3.2.1",
				"platform":"Web",
				"package":"web.rubika.ir",
				"lang_code":"fa"
			}
		}))},url="https://messengerg2c37.iranlms.ir/").json()["data_enc"]))
	
	def getMessages(self, chat_id,min_id):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"getMessagesInterval",
			"input":{
				"object_guid":chat_id,
				"middle_message_id":min_id
			},
			"client":{
				"app_name":"Main",
				"app_version":"3.2.1",
				"platform":"Web",
				"package":"web.rubika.ir",
				"lang_code":"fa"
			}
		}))},url="https://messengerg2c67.iranlms.ir/").json().get("data_enc"))).get("data").get("messages")
		
	def getInfoByUsername(self, username):
		''' username should be without @ '''
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"getObjectByUsername",
			"input":{
				"username":username
			},
			"client":{
				"app_name":"Main",
				"app_version":"3.2.1",
				"platform":"Web",
				"package":"web.rubika.ir",
				"lang_code":"fa"
			}
		}))},url="https://messengerg2c23.iranlms.ir/").json().get("data_enc")))

	def banGroupMember(self, chat_id, user_id):
		return post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"banGroupMember",
			"input":{
				"group_guid": chat_id,
				"member_guid": user_id,
				"action":"Set"
			},
			"client":{
				"app_name":"Main",
				"app_version":"3.2.1",
				"platform":"Web",
				"package":"web.rubika.ir",
				"lang_code":"fa"
			}
		}))},url="https://messengerg2c21.iranlms.ir/")

	def invite(self, chat_id, user_ids):
		return post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"addGroupMembers",
			"input":{
				"group_guid": chat_id,
				"member_guids": user_ids
			},
			"client":{
				"app_name":"Main",
				"app_version":"3.2.1",
				"platform":"Web",
				"package":"web.rubika.ir",
				"lang_code":"fa"
			}
		}))},url="https://messengerg2c22.iranlms.ir/")
	
	def getGroupAdmins(self, chat_id):
		t = False
		while t == False:
			try:
				p = post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
					"client":{
						"app_name":"Main",
						"app_version":"2.9.5",
						"lang_code":"fa",
						"package":"ir.resaneh1.iptv",
						"platform":"Android"
					},
					"input":{
						"group_guid":chat_id
					},
					"method":"getGroupAdminMembers"
				}))},url="https://messengerg2c22.iranlms.ir/")
				p = loads(self.enc.decrypt(p.json().get("data_enc")))
				t = True
			except:
				t = False
		return p

	def getMessagesInfo(self, chat_id, message_ids):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"getMessagesByID",
			"input":{
				"object_guid": chat_id,
				"message_ids": message_ids
			},
			"client":{
				"app_name":"Main",
				"app_version":"3.2.1",
				"platform":"Web",
				"package":"web.rubika.ir",
				"lang_code":"fa"
			}
		}))}, url="https://messengerg2c24.iranlms.ir/").json()["data_enc"])).get("data").get("messages")

	def setMembersAccess(self, chat_id, access_list):
		return post(json={
			"api_version": "4",
			"auth": self.auth,
			"client": {
				"app_name": "Main",
				"app_version": "2.9.5",
				"lang_code": "fa",
				"package": "ir.resaneh1.iptv",
				"platform": "Android"
			},
			"data_enc": self.enc.encrypt(dumps({
				"access_list": access_list,
				"group_guid": chat_id
			})),
			"method": "setGroupDefaultAccess"
		}, url="https://messengerg2c24.iranlms.ir/")

	def getGroupInfo(self, chat_id):
		return loads(self.enc.decrypt(post(
			json={
				"api_version":"5",
				"auth": self.auth,
				"data_enc": self.enc.encrypt(dumps({
					"method":"getGroupInfo",
					"input":{
						"group_guid": chat_id,
					},
					"client":{
						"app_name":"Main",
						"app_version":"3.2.1",
						"platform":"Web",
						"package":"web.rubika.ir",
						"lang_code":"fa"
					}
			}))}, url="https://messengerg2c24.iranlms.ir/").json()["data_enc"]))
	
	def get_updates_all_chats(self):
		t = False
		while t == False:
			try:
				time_stamp = str(random._floor(datetime.datetime.today().timestamp()) - 200)
				p = post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
					"method":"getChatsUpdates",
					"input":{
						"state":time_stamp,
					},
					"client":{
						"app_name":"Main",
						"app_version":"3.2.1",
						"platform":"Web",
						"package":"web.rubika.ir",
						"lang_code":"fa"
					}
				}))},url="https://messengerg2c67.iranlms.ir/")
				p = loads(self.enc.decrypt(p.json().get("data_enc"))).get("data").get("chats")
				t = True
			except:
				t = False
		return p

	def get_updates_chat(self, chat_id):
		time_stamp = str(random._floor(datetime.datetime.today().timestamp()) - 200)
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"getMessagesUpdates",
			"input":{
				"object_guid":chat_id,
				"state":time_stamp
			},
			"client":{
				"app_name":"Main",
				"app_version":"3.2.1",
				"platform":"Web",
				"package":"web.rubika.ir",
				"lang_code":"fa"
			}
		}))},url="https://messengerg2c67.iranlms.ir/").json().get("data_enc"))).get("data").get("updated_messages")
	
	def my_sticker_set(self):
		time_stamp = str(random._floor(datetime.datetime.today().timestamp()) - 200)
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"getMyStickerSets",
			"input":{},
			"client":{
				"app_name":"Main",
				"app_version":"3.2.1",
				"platform":"Web",
				"package":"web.rubika.ir",
				"lang_code":"fa"
			}
		}))},url="https://messengerg2c67.iranlms.ir/").json().get("data_enc"))).get("data")


bot = Bot("wxhowsospgttjkzekifbuuodgylafvrj")
target = "g0BWxYY05027644a4f6b7b371cd5f243"
answered = [bot.getGroupAdmins]
retries = {}
sleeped = False

plus= True

while True:
	try:
		admins = [i["member_guid"] for i in bot.getGroupAdmins(target)["data"]["in_chat_members"]]
		min_id = bot.getGroupInfo(target)["data"]["chat"]["last_message_id"]
		while True:
			try:
				messages = bot.getMessages(target,min_id)
				break
			except:
				continue
		
		open("id.db","w").write(str(messages[-1].get("message_id")))

		for msg in messages:
			if msg["type"]=="Text" and not msg.get("message_id") in answered:
				if not sleeped:
					if msg.get("text") == "!bot" and msg.get("author_object_guid") in admins :
						bot.sendMessage(target, "ربات اکنون فعال است ✅", message_id=msg.get("message_id"))

					elif msg.get("text").startswith("!add") :
						bot.invite(target, [bot.getInfoByUsername(msg.get("text").split(" ")[1][1:])["data"]["chat"]["object_guid"]])
						bot.sendMessage(target, "کاربر به گپ اضافه شد ✅", message_id=msg.get("message_id"))

					elif msg.get("text") == "!info":
						bot.sendMessage(target, "لیسـت دستـــورات ربـات 🤖:\n\n●🤖 !bot : فعال یا غیر فعال بودن بات\n\n●❎ !stop : غیر فعال سازی بات\n\n●✅ !start : فعال سازی بات\n\n●🕘 !time : ساعت\n\n●📅 !date : تاریخ\n\n●📋 !del : حذف پیام با ریپ بر روی ان\n\n●🔒 !lock : بستن چت در گروه\n\n●🔓 !unlock : باز کردن چت در گروه\n\n●❌ !ban : حذف کاربر با ریپ زدن\n\n●✉ !send : ارسال پیام با استفاده از ایدی\n\n●📌 !add : افزودن کاربر به گپ با ایدی\n\n●📜 !info : لیست دستورات ربات\n\n●🆑 !cal :ماشین حساب\n\n●🔴 !user : اطلاعات کاربر با ایدی\n\n●😂 !jok : ارسال جک\n\n●🔵 !font : ارسال فونت\n\n●🔴 !ping : گرفتن پینگ سایت\n\n●🔵 !tran : مترجم انگلیسی")
					elif msg.get("text").startswith("!cal"):
						msd = msg.get("text")
						if plus == True:
							try:
								call = [msd.split(" ")[1], msd.split(" ")[2], msd.split(" ")[3]]
								if call[1] == "+":
									am = float(call[0]) + float(call[2])
									bot.sendMessage(target, "حاصل :\n"+"".join(str(am)), message_id=msg.get("message_id"))
									plus = False
							
								elif call[1] == "-":
									am = float(call[0]) - float(call[2])
									bot.sendMessage(target, "حاصل :\n"+"".join(str(am)), message_id=msg.get("message_id"))
							
								elif call[1] == "*":
									am = float(call[0]) * float(call[2])
									bot.sendMessage(target, "حاصل :\n"+"".join(str(am)), message_id=msg.get("message_id"))
							
								elif call[1] == "/":
									am = float(call[0]) / float(call[2])
									bot.sendMessage(target, "حاصل :\n"+"".join(str(am)), message_id=msg.get("message_id"))
							except IndexError:
								bot.sendMessage(target, "لطفا دستور را به طور صحیح وارد کنید ❌" ,message_id=msg.get("message_id"))
						plus= True
					elif msg.get("text").startswith("!send") :
						bot.sendMessage(bot.getInfoByUsername(msg.get("text").split(" ")[1][1:])["data"]["chat"]["object_guid"], "شما یک پیام ناشناس دارید:\n"+" ".join(msg.get("text").split(" ")[2:]))
						bot.sendMessage(target, "پیام ارسال شد ✅", message_id=msg.get("message_id"))

					elif msg.get("text") == "سلام":
						bot.sendMessage(target, "سلام عزیز", message_id=msg.get("message_id"))

					if  msg.get("text").startswith('!user @'):
						try:
							user_info = bot.getInfoByUsername( msg.get("text")[7:])
							if user_info['data']['exist'] == True:
								if user_info['data']['type'] == 'User':
									bot.sendMessage(target, 'Name User:\n ' + user_info['data']['user']['first_name'] + ' ' + user_info['data']['user']['last_name'] + '\n\nBio User:\n ' + user_info['data']['user']['bio'] + '\n\nGuid:\n ' + user_info['data']['user']['user_guid'] ,  msg.get('message_id'))
									print('sended response')
								else:
									bot.sendMessage(target, 'کانال است ❌' ,  msg.get('message_id'))
									print('sended response')
							else:
								bot.sendMessage(target, "کاربری وجود ندارد ❌" ,  msg.get('message_id'))
								print('sended response')
						except:
							print('server bug6')
							bot.sendMessage(target, "خطا در اجرای دستور مجددا سعی کنید ❌" ,message_id=msg.get("message_id"))
							

					elif msg.get("text") == "!stop" and msg.get("author_object_guid") in admins :
						sleeped = True
						bot.sendMessage(target, "ربات خاموش شد ✅", message_id=msg.get("message_id"))

					elif msg.get("text").startswith("!ping"):
						
						try:
							responser = get(f"https://api.codebazan.ir/ping/?url={msg.get('text').split()[1]}").text
							bot.sendMessage(target, responser,message_id=msg["message_id"])
						except:
							bot.sendMessage(target, "لطفا دستور را به طور صحیح وارد کنید ❌", message_id=msg["message_id"])

					elif msg.get("text").startswith("!tran"):
						
						try:
							responser = get(f"https://api.codebazan.ir/translate/?type=json&from=en&to=fa&text={msg.get('text').split()[1:]}").json()
							al = [responser["result"]]
							bot.sendMessage(msg.get("author_object_guid"), "پاسخ به ترجمه:\n"+"".join(al)).text
							bot.sendMessage(target, "نتیجه به پیوی شما ارسال شد ✅", message_id=msg["message_id"])
						except:
							bot.sendMessage(target, "لطفا دستور را به طور صحیح وارد کنید ❌", message_id=msg["message_id"])

					elif msg.get("text").startswith("!font"):
						#print("\n".join(list(response["result"].values())))
						try:
							response = get(f"https://api.codebazan.ir/font/?text={msg.get('text').split()[1]}").json()
							bot.sendMessage(msg.get("author_object_guid"), "\n".join(list(response["result"].values())[:110])).text
							bot.sendMessage(target, "نتیجه به پیوی شما ارسال شد ✅", message_id=msg["message_id"])
						except:
							bot.sendMessage(target, "لطفا دستور را به طور صحیح وارد کنید ❌", message_id=msg["message_id"])



					elif msg.get("text").startswith("!jok"):
						
						try:
							response = get("https://api.codebazan.ir/jok/").text
							bot.sendMessage(target, response,message_id=msg.get("message_id"))
						except:
							bot.sendMessage(target, "لطفا دستور را به طور صحیح وارد کنید ❌", message_id=msg["message_id"])

					elif msg.get("text") == "!time":
						bot.sendMessage(target, f"Time : {time.localtime().tm_hour} : {time.localtime().tm_min} : {time.localtime().tm_sec}", message_id=msg.get("message_id"))

					elif msg.get("text") == "!date":
						bot.sendMessage(target, f"Date: {time.localtime().tm_year} / {time.localtime().tm_mon} / {time.localtime().tm_mday}", message_id=msg.get("message_id"))

					elif msg.get("text") == "!del" and msg.get("author_object_guid") in admins :
						bot.deleteMessages(target, [msg.get("reply_to_message_id")])
						bot.sendMessage(target, "پیام پاک شد ✅", message_id=msg.get("message_id"))

					# elif msg.get("text").split(" ")[0] in  delmess:
					# 	bot.deleteMessages(target, [msg.get("message_id")])
					# 	bot.sendMessage(target, "یک پیام مستهجن پاک شد ✅", message_id=msg.get("message_id"))


					elif msg.get("text") == "!lock" and msg.get("author_object_guid") in admins :
						print(bot.setMembersAccess(target, ["ViewMembers","ViewAdmins","AddMember"]).text)
						bot.sendMessage(target, "گپ بسته شد ✅", message_id=msg.get("message_id"))

					elif msg.get("text") == "!unlock" and msg.get("author_object_guid") in admins :
						bot.setMembersAccess(target, ["ViewMembers","ViewAdmins","SendMessages","AddMember"])
						bot.sendMessage(target, "گپ باز شد ✅", message_id=msg.get("message_id"))

					elif msg.get("text").startswith("!ban") and msg.get("author_object_guid") in admins :
						try:
							guid = bot.getInfoByUsername(msg.get("text").split(" ")[1][1:])["data"]["chat"]["abs_object"]["object_guid"]
							user = bot.getUserInfo(data['peer_objects'][0]['object_guid'])["data"]["user"]["first_name"]
							if not guid in admins :
								bot.banGroupMember(target, guid)
								bot.sendMessage(target, f"✅ کاربر حذف شد", message_id=msg.get("message_id"))
							else :
								bot.sendMessage(target, f"❎ کاربر حذف نشد", message_id=msg.get("message_id"))
								
						except IndexError:
							a = bot.getMessagesInfo(target, [msg.get("reply_to_message_id")])[0]["author_object_guid"]
							if a in admins:
								bot.sendMessage(target, f"کاربر حذف نشد ❌", message_id=msg.get("message_id"))
							else:
								bot.banGroupMember(target, bot.getMessagesInfo(target, [msg.get("reply_to_message_id")])[0]["author_object_guid"])
								bot.sendMessage(target, f"کاربر حذف شد ✅", message_id=msg.get("message_id"))

				else:
					if msg.get("text") == "!start" and msg.get("author_object_guid") in admins :
						sleeped = False
						bot.sendMessage(target, "ربات فعال شد ✅", message_id=msg.get("message_id"))

			elif msg["type"]=="Event" and not msg.get("message_id") in answered and not sleeped:
				name = bot.getGroupInfo(target)["data"]["group"]["group_title"]
				data = msg['event_data']
				if data["type"]=="RemoveGroupMembers":
					user = bot.getUserInfo(data['peer_objects'][0]['object_guid'])["data"]["user"]["first_name"]
					bot.sendMessage(target, f"خدانگهدار {user} 🗑️", message_id=msg["message_id"])
				
				elif data["type"]=="AddedGroupMembers":
					user = bot.getUserInfo(data['peer_objects'][0]['object_guid'])["data"]["user"]["first_name"]
					bot.sendMessage(target, f"سلام کاربر {user} به گروه {name} خوش اومدید 😃\nلطفا قوانین رو رعایت کن ✅", message_id=msg["message_id"])
				
				elif data["type"]=="LeaveGroup":
					user = bot.getUserInfo(data['performer_object']['object_guid'])["data"]["user"]["first_name"]
					bot.sendMessage(target, f"خدانگهدار {user} 🗑️", message_id=msg["message_id"])
					
				elif data["type"]=="JoinedGroupByLink":
					user = bot.getUserInfo(data['performer_object']['object_guid'])["data"]["user"]["first_name"]
					bot.sendMessage(target, f"سلام کاربر {user}  به گروه {name} خوش اومدید 😃\nلطفا قوانین رو رعایت کن ✅", message_id=msg["message_id"])

			answered.append(msg.get("message_id"))

	except KeyboardInterrupt:
		exit()

	except Exception as e:
		if type(e) in list(retries.keys()):
			if retries[type(e)] < 3:
				retries[type(e)] += 1
				continue
			else:
				retries.pop(type(e))
		else:
			retries[type(e)] = 1
			continue
