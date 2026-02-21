⚠️ Archived, moved to Codeberg: https://codeberg.org/dsiggi/enigma2xmltv ⚠️

# HomeBankCSV

Mit diesem Python modul lässt sich das EPG von TV-Receivern mit enigma2 System herunterladen und in das XMLTV-Format wandeln.

Getestet mit folgendem Gerät:
- Dreambox DM820HD

## Beispiel
```python
from enigma2xmltv import enigma2xmltv

# Init mit der IP des Receivers
x = enigma2xmltv("192.168.0.115")

# Mehrere Sender hinzufügen
# Das Erste HD
x.add_channel("1%3A0%3A19%3A2B5C%3A41B%3A1%3AFFFF0000%3A0%3A0%3A0%3A")
# ZDF HD
x.add_channel("1%3A0%3A19%3A2B66%3A437%3A1%3AFFFF0000%3A0%3A0%3A0%3A")
# Tele 5 HD & Comedy Central
x.add_channel("1%3A0%3A19%3AC37B%3A2719%3AF001%3AFFFF0000%3A0%3A0%3A0%3A",
                "1%3A0%3A19%3AC382%3A271A%3AF001%3AFFFF0000%3A0%3A0%3A0%3A")

# Entfernen von ZDF HD
x.del_channel("1%3A0%3A19%3A2B66%3A437%3A1%3AFFFF0000%3A0%3A0%3A0%3A")

# ##############################
# Beispiel zum laden des EPGs aller Sender
# ##############################

# EPG aller Sender laden
x.load_epg()

# EPG aller geladenen Sender konvertieren
x.convert_channels()

# Abspeichern der EPG-Daten im XMLTV-Format
x.save_epg(".")

# ##############################
# Beispiel zum laden des EPGs von bestimmten Sendern
# ##############################

# EPG von Das Erste HD laden
x.load_channel_epg("1%3A0%3A19%3A2B5C%3A41B%3A1%3AFFFF0000%3A0%3A0%3A0%3A")
# EPG von Comedy Central laden
x.load_channel_epg("1%3A0%3A19%3AC382%3A271A%3AF001%3AFFFF0000%3A0%3A0%3A0%3A")

# EPG aller geladenen Sender konvertieren (Das Erste HD & Comedy Central)
x.convert_channels()
# Oder nur das EPG eines bestimmten Senders konvertieren (Das Erste HD)
x.convert_channel("1%3A0%3A19%3A2B5C%3A41B%3A1%3AFFFF0000%3A0%3A0%3A0%3A")

# Abspeichern der EPG-Daten im XMLTV-Format
x.save_epg(".")

```



