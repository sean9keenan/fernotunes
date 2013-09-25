# from pytify import Spotify
from twisted.internet import reactor
from autobahn.websocket import WebSocketClientFactory, \
                               WebSocketClientProtocol, \
                               connectWS

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

def validCall(self, parameters):
  return True

def restartFactory():
  connectWS(factory)

class EchoClientProtocol(WebSocketClientProtocol):

  def sendHello(self):
    self.sendMessage("Hello, world!")

  def onOpen(self):
    self.sendHello()

  def onMessage(self, msg, binary):
    print "Got message: " + msg
    parameters = [x.strip() for x in msg.split(',')]
    try:
      if validCall(parameters):
        allCommands[int(parameters[0])]
        self.sendMessage(str(spotify))
    except Exception, e:
      print "Invalid Command passed"

  def onClose(self, reason, r2, r3):
    print "Connection Closed: " + str(reason) + str(r2) + str(r3)
    restartFactory()

factory = WebSocketClientFactory("ws://fernotunesclient.skeenan.com", debug = False)
factory.protocol = EchoClientProtocol
connectWS(factory)
reactor.run()