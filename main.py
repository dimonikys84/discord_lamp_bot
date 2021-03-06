import youtube_dl as yt
import urllib.request
import urllib.parse
import re
import discord
import config as cf


client = discord.Client()


def search_n_download(name):
	query_string = urllib.parse.urlencode({"search_query" : name})
	html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
	search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
	link = "http://www.youtube.com/watch?v=" + search_results[0]
	print(link)
	ydl_opts = {
		'restrictfilenames:' : True,
		'outtmpl': '/songs/%(id)s.mp3',
		'forcetitle': 'true',
		'format': 'bestaudio/best',
		'extractaudio' : True,
		'audioformat' : 'mp3',
	}
	with yt.YoutubeDL(ydl_opts) as ydl:
		meta = ydl.extract_info(link, download=False)
		ydl.download([link])
	songid = ('%s' %(meta['id']))
	return songid


@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')


@client.event
async def on_message(message):
	if message.content.startswith('!s'):
		songid = search_n_download(message.content)
		channel = client.get_channel(cf.channel_id)
		server = client.get_server(cf.server_id)
		voice = client.voice_client_in(server)
		if voice != None:
			await voice.disconnect()
		voice = await client.join_voice_channel(channel)
		player = voice.create_ffmpeg_player('songs/' + songid + '.mp3')
		player.volume = 0.15
		player.start()


client.run(cf.token)