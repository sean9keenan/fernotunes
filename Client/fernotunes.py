# from pytify import Spotify
from twisted.internet import reactor
from autobahn.websocket import WebSocketClientFactory, \
                               WebSocketClientProtocol, \
                               connectWS
import os
import argparse

if not os.name == "posix":
  from pytify import Spotify
else:
  mac = __import__('MacVersion')

spotify = None
if os.name == "posix":
  spotify = mac.MacVersion("Spotify")
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

  def onOpen(self):
    self.sendMessage(str(spotify))

  def onMessage(self, msg, binary):
    print "Got message: " + msg
    parameters = [x.strip() for x in msg.split(',')]
    try:
      if validCall(parameters):
        allCommands[int(parameters[0])]()
        self.sendMessage(str(spotify))
    except Exception, e:
      print "Invalid Command passed: " + str(e)

  def onClose(self, reason, r2, r3):
    print "Connection Closed: " + str(reason) + str(r2) + str(r3)
    restartFactory()


if __name__ == "__main__":

  parser = argparse.ArgumentParser(description='Play music remotely!')
  parser.add_argument('-s', dest='subdomain', default='fernotunesclient',
                      help='Subdomain to run this on', type=str)
  parser.add_argument('-a', dest='app_name', default='spotify',
                      help='App to run this on', type=str)
  args = parser.parse_args()
  spotify.app = args.app_name

  factory = WebSocketClientFactory("ws://"+args.subdomain+".skeenan.com", debug = False)
  factory.protocol = EchoClientProtocol
  connectWS(factory)
  reactor.run()