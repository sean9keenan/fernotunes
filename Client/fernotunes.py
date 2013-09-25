# from pytify import Spotify
from twisted.internet import reactor
from autobahn.websocket import WebSocketClientFactory, \
                               WebSocketClientProtocol, \
                               connectWS
import os
if not os.name == "posix":
  from pytify import Spotify
else:
  import subprocess


app_name = "Spotify"

def do_oscacript(command):
  cmd = "osascript -e 'tell application \""+app_name+"\" to "+command+"'"
  try:
      return subprocess.check_output(cmd, shell=True)
  except subprocess.CalledProcessError:
      print "Failed to send message to "+app_name+", is it running?"
      return False

class MacVersion:
  def playpause(self):
    print "play/pause"
    do_oscacript('playpause')

  def previous(self):
    do_oscacript('previous track')

  def next(self):
    do_oscacript('next track')

  def volumeUp(self):
    pass
  def volumeDown(self):
    pass
  def isPlaying(self):
    state = do_oscacript("player state as text")
    print (state.strip() == "playing")
    return (state.strip() == "playing")
  def stop(self):
    pass
  def mute(self):
    pass
  def focus(self):
    pass

  def __str__(self):
    artist = do_oscacript("artist of current track as string")
    title = do_oscacript("name of current track as string")
    album = do_oscacript("album of current track as string")
    if self.isPlaying():
      return title + "<br>" + artist + " - " + album
    else:
      return "Nothing is playing"

spotify = None
if os.name == "posix":
  spotify = MacVersion()
else:
  spotify = Spotify()

allCommands = [spotify.playpause,
               spotify.previous,
               spotify.next,
               spotify.volumeUp,
               spotify.volumeDown,
               spotify.isPlaying,
               spotify.stop,
               spotify.mute,
               spotify.focus]

def validCall(parameters):
  return True

def restartFactory():
  connectWS(factory)

class EchoClientProtocol(WebSocketClientProtocol):

  def sendHello(self):
    self.sendMessage(str(spotify))

  def onOpen(self):
    self.sendHello()

  def onMessage(self, msg, binary):
    print "Got message: " + msg
    parameters = [x.strip() for x in msg.split(',')]
    try:
      if validCall(parameters):
        allCommands[int(parameters[0])]()
        self.sendMessage(str(spotify))
    except Exception, e:
      print "Invalid Command passed" + str(e)

  def onClose(self, reason, r2, r3):
    print "Connection Closed: " + str(reason) + str(r2) + str(r3)
    restartFactory()

factory = WebSocketClientFactory("ws://fernotunesclient.skeenan.com", debug = False)
factory.protocol = EchoClientProtocol
connectWS(factory)
reactor.run()