import subprocess

class MacVersion:

  def __init__(self, app_name):
    self.app = app_name

  def do_oscacript(self, command):
    cmd = "osascript -e 'tell application \""+self.app+"\" to "+command+"'"
    return self.raw_script(cmd)

  def raw_script(self, cmd):
    try:
        return subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError:
        print "Failed to send message to "+self.app+", is it running?"
        return False

  def playpause(self):
    print "play/pause"
    if (self.app == "Pandora"):
      self.raw_script("osascript -e 'tell application \"pandora\"' -e 'activate' -e 'tell application \"System Events\" to key code 49' -e 'end tell'")
    else:
      self.do_oscacript('playpause')

  def previous(self):
    self.do_oscacript('previous track')

  def next(self):
    if (self.app == "Pandora"):
      self.raw_script("osascript -e 'tell application \"pandora\"' -e 'activate' -e 'tell application \"System Events\" to key code 124' -e 'end tell'")
    else:
      self.do_oscacript('next track')

  def volumeUp(self):
    pass
  def volumeDown(self):
    pass
  def isPlaying(self):
    state = self.do_oscacript("player state as text")
    print (state.strip() == "playing")
    return (state.strip() == "playing")
  def stop(self):
    pass
  def mute(self):
    pass
  def focus(self):
    pass

  def __str__(self):

    if(self.app == "Pandora"):
      return "Unknown State, Yay Pandora!"

    artist = self.do_oscacript("artist of current track as string")
    title = self.do_oscacript("name of current track as string")
    album = self.do_oscacript("album of current track as string")
    if self.isPlaying():
      return title + "<br>" + artist + " - " + album
    else:
      return "Nothing is playing"