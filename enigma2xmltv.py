import urllib.request
import datetime
import xml.etree.cElementTree as ET
import os.path

class enigma2xmltv():
    def __init__(self, server, lang: str = "de", time_offset: str = "+0100"):
        '''
        server: IP oder Hostname der des enigma webinterfaces
        lang: Länderkürzel deiner Sprache
        time_offset: Zeitoffset der EPG-Daten zu UTC
        '''
        self.server = "http://" + server + "/web/epgservice?sRef="
        self.lang = lang
        self.time_offset = time_offset
        self.channels = []
        self.raw_epg = {}
        self.epg = {}

    def add_channel(self, *channels):
        '''
        Kanäle zum grabben hinzufügen.
        *channels: Kanal 1, Kanal 2, ...
        '''
        for c in channels:
            self.channels.append(c)

    def show_channels(self):
        '''
        Gibt alle hinzugefügten Kanäle zurück.
        '''
        print(self.channels)

    def del_channel(self, id):
        '''
        Löscht einen Kanal aus der Liste.
        id: Wenn ein integer wird der entsprechende Index gelöscht
        id: Wenn ein string wird der entsprechende Kanal gelöscht
        '''
        if ( type(id) == int ):
            try:
                self.channels.pop(id)
            except:
                pass
        elif ( type(id) == str):
            try:
                self.channels.remove(id)
            except:
                pass

    def load_channel_epg(self, id):
        '''
        Läd das EPG eines Kanals, der über add_channel hinzugefügt wurde.
        name: Name des Kanals, desen EPG geladen werden soll.
        '''
        self.raw_epg[id] = urllib.request.urlopen(self.server + id, timeout=3).read().decode('utf8')

    def load_epg(self):
        '''
        Läd das EPG aller Kanäle die über add_channel hinzugefügt wurden herunter.
        '''
        for c in self.channels:
            self.load_channel_epg(c)

    def convert_channel(self, channel):
        '''
        Konvertiert das EPG eines Kanals in das XMLTV-Format
        name: Name des Kanals
        '''
        if ( channel in self.raw_epg ):
            if "e2eventservicename" not in self.raw_epg[channel]:
                # Das scheint kein gültiges EPG zu sein.
                # Gibt es den Kanal vielleicht nicht?
                self.raw_epg[channel] = None
            
            myroot = ET.fromstring(self.raw_epg[channel])
            myxml = ET.Element("tv", {"generator-info-name": "Enigma2XMLTV", "generator-info-url": "https://github.com/dsiggi/enigma2xmltv"})

            for x in range(0,len(myroot)):
                name = ""
                desc = ""
                descext = ""
                title = ""
                start = ""
                end = ""
                duration = ""

                for e in myroot[x]:
                    if e.tag == "e2eventservicename":
                        if e.text is not None:
                            name = e.text
                    elif e.tag == "e2eventtitle":
                        if e.text is not None:
                            title = e.text
                    elif e.tag == "e2eventdescription":
                        if e.text is not None:
                            desc = e.text
                    elif e.tag == "e2eventdescriptionextended":
                        if e.text is not None:
                            descext = e.text
                    elif e.tag == "e2eventstart":
                        if e.text is not None:
                            start = datetime.datetime.fromtimestamp(int(e.text)).strftime('%Y%m%d%H%M%S')
                    elif e.tag == "e2eventduration":
                        if e.text is not None:
                            duration = int(e.text)
                            end = datetime.datetime(int(start[:4]), int(start[4:6]), int(start[6:8]), int(start[8:10]), int(start[10:12]), int(start[12:14])) \
                                + datetime.timedelta(seconds=duration)
                            end = end.strftime('%Y%m%d%H%M%S')

                myprog = ET.SubElement(myxml, "programme", {'start': start + " " + self.time_offset, 'stop': end + " " + self.time_offset, 'channel': name} )
                ET.SubElement(myprog, "title", { "lang": self.lang }).text = title
                ET.SubElement(myprog, "sub-title", { "lang": self.lang }).text = desc
                ET.SubElement(myprog, "category").text = ""
                ET.SubElement(myprog, "desc", { "lang": self.lang }).text = descext

            # Hinzufügen der Kanalinfos
            mychannel = ET.Element("channel", {"id": name} )
            ET.SubElement(mychannel, "display-name", {"lang": self.lang}).text = name
            myxml.insert(0, mychannel)

            self.epg[channel] = ET.ElementTree(myxml)

    def convert_channels(self):
        '''
        Konvertiert das EPG aller Kanäle in das XMLTV-Format
        '''
        for e in self.raw_epg:
            self.convert_channel(e)

    def save_epg(self, path: str):
        '''
        Speichert das EPG im XMLTV-Format ab.
        path: Pfad in dem die Datei(en) gespeichert werden sollen.
        '''
        if ( not os.path.exists(path) ):
            raise OSError("Pfad " + path + " existiert nicht.")

        for e in self.epg:
            ET.indent(self.epg[e], space="\t", level=0)
            self.epg[e].write(path + "/" + e + ".xml", encoding='utf-8')


