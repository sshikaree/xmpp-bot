#!/usr/bin/env python
#_*_ coding: utf-8 _*_

import xmpp, sys
import urllib2, re
from time import sleep
from random import randint, choice

NICK = '-=Bot=-'
TO = 'Chat Room'
client = None



def messageCB(conn, msg):

	sender = str(msg.getFrom())
	if not isinstance(sender, unicode):
		sender = unicode(sender, 'utf-8')
	else:
		sender = sender.decode('utf-8')
	try:
		sender_nick = sender.split('/')[1]
	except:
		sender_nick = ''

	content = msg.getBody()
	if not isinstance(content, unicode):
		content = unicode(content, 'utf-8')

	# if not isinstance(msg, unicode):
	#  	msg = unicode(str(msg), 'utf-8')

	print (": ".join([sender_nick, content]))
#	print u"Sender: %s" % sender
#	print u"Content: %s" % content
	# print msg

	global client
	if NICK in content:
		client.send(xmpp.protocol.Message(TO, 'Привет!', 'groupchat'))

	if 'weather!' in content and sender_nick != NICK:
		city = content.split('!')[1].split(' ')[0]
		weather(city)
	if 'bot!help' in content and sender_nick != NICK:
		show_help()
	if 'bot!bash' in content and sender_nick != NICK:
		bash()

def StepOn(conn):
	try:
		conn.Process(1)
	except KeyboardInterrupt:
		return 0
	return 1

def GoOn(conn):
	while StepOn(conn):
		pass
################################################


def show_help():
	commands = {'weather!_город_':'Погода в данном городе',
			'bot!bash':'Рандомная цитата с bash.im'}
	for command in commands:
		mess = ": ".join([command, commands[command]])
		client.send(xmpp.protocol.Message(TO, mess, 'groupchat'))

def weather(city):
	adress = 'http://pogoda.yandex.ru/' + city
	headers = {'User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 2.0.50727)'}
	r = urllib2.Request(adress, headers = headers)

	u = urllib2.urlopen(r)
	data = u.read()

	patt = re.compile(r'<div class=\"b-thermometer__now\">(.+?)</div>')
	match = re.findall(patt, data)

	if match:	
		for string in match:
			# print string
			mess = ' : '.join([str(city).capitalize(), str(string)])
			client.send(xmpp.protocol.Message(TO, mess, 'groupchat'))
	else:
		client.send(xmpp.protocol.Message(TO, 'Город не найден...', 'groupchat'))


	u.close()
	sleep(1)
	
def bash():
	adress = 'http://bash.im/byrating/' + str(randint(1,25))
	headers = {'User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 2.0.50727)'}
	r = urllib2.Request(adress, headers = headers)
	u = urllib2.urlopen(r)
	data = u.read()
	
	patt = re.compile(r'<div class=\"text\">(.+?)</div>')
	match = re.findall(patt, data)
	if match:
		mess = choice(match)
		mess = unicode(mess, 'cp1251').replace('<br>', '\n')
		
		client.send(xmpp.protocol.Message(TO, mess, 'groupchat'))
	 
	u.close() 
	sleep(1)

#####################################################33

	

def main():

	xmpp_jid = ''
	xmpp_pwd = ''
	

	CONF = 'Chat Room/-=Bot=-'
	TO = 'Chat Room'

	jid = xmpp.protocol.JID(xmpp_jid)
	global client
	client = xmpp.Client(jid.getDomain(), debug = [])
	client.connect()
	if client.auth(jid.getNode(), xmpp_pwd, resource = 'xmpp-py') == None:
		print "Authentication failed!"
		sys.exit(0)
	client.send(xmpp.Presence(to = CONF))

	client.RegisterHandler('message', messageCB)

	GoOn(client)
	# Sending message:
	# client.send(xmpp.protocol.Message(TO, 'Hello!', 'groupchat'))

	

if __name__ == '__main__':
	main()
