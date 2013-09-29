
import sys		#for cmd line argv
sys.path.insert(0,'../lib')
import time		#for delay
from pygsr import Pygsr
import re
import urllib, urllib2
import pygst
pygst.require('0.10')
import gst
import gobject
import os
import neuron

def playmp3(file):

	mainloop = gobject.MainLoop()
	pl = gst.element_factory_make("playbin", "player")
	pl.set_property('uri','file://'+os.path.abspath(file))
	pl.set_state(gst.STATE_PLAYING)

	

def ttsout(lang, text):

    output = open('out.mp3','w')    	

    #process text into chunks
    text = text.replace('\n','')
    text_list = re.split('(\,|\.)', text)
    combined_text = []
    for idx, val in enumerate(text_list):
        if idx % 2 == 0:
            combined_text.append(val)
        else:
            joined_text = ''.join((combined_text.pop(),val))
            if len(joined_text) < 100:
                combined_text.append(joined_text)
            else:
                subparts = re.split('( )', joined_text)
                temp_string = ""
                temp_array = []
                for part in subparts:
                    temp_string = temp_string + part
                    if len(temp_string) > 80:
                        temp_array.append(temp_string)
                        temp_string = ""
                #append final part
                temp_array.append(temp_string)
                combined_text.extend(temp_array)
    #download chunks and write them to the output file
    for idx, val in enumerate(combined_text):
        mp3url = "http://translate.google.com/translate_tts?tl=%s&q=%s&total=%s&idx=%s" % (lang, urllib.quote(val), len(combined_text), idx)
        headers = {"Host":"translate.google.com",
          "Referer":"http://www.gstatic.com/translate/sound_player2.swf",
          "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.163 Safari/535.19"}
        req = urllib2.Request(mp3url, '', headers)
        sys.stdout.write('.')
        sys.stdout.flush()
        if len(val) > 0:
            try:
                response = urllib2.urlopen(req)
                output.write(response.read())
                time.sleep(.5)
            except urllib2.HTTPError as e:
                print ('%s' % e)
    output.close()

    print('Saved MP3 to %s' % output.name)



if __name__ == "__main__":
    	speech = Pygsr()
	s_neuron = neuron.Neuron(("",23310))
	s_neuron.start()

	while True:
		if s_neuron.vesicle == "stopspeech":
			sys.exit(-1)

		speech.record(5) # duration in seconds (3)
		try:
			phrase, complete_response = speech.speech_to_text('en_US') # select the language
			s_neuron.axonFire("",("",23301))
		except urllib2.HTTPError, error:
			phrase= "eh?"			
			pass		
		print phrase
		 
		#use string in combination with the translate url as the stream to be played
		ttsout("en",phrase)

		playmp3("out.mp3")
		#requires a delay, if the py process closes before the mp3 has finished it will be cut off.
		time.sleep(2)

	
