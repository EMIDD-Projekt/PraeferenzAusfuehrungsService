# Ausführungsservice
_Proof-of-Concept_ Implementierung der _Ausführungsservice_ -Komponente der _Privacy Proxy_ Architektur.

Es handelt sich um einen Proxy-Server für die Participatory Sensing Plattform [OpenSense.network](opensense.network). Die API der Plattform wird gespiegelt. Werden Sensordaten abgefragt, überprüft der Service ob zu den angeforderten Daten Nutzungspräferenzen vorliegen. Sind diese verfügbar, werden die Daten entsprechend der dort verzeichneten Regeln vorverarbeitet und erst dann an die anfragende Institution herausgegeben.

## Nutzung

Im folgenden werden mögliche Wege aufgezeigt, um den Ausführungsservice zu testen:

a) lokale Ausführung

b) Ausführung als Cloud-Service

### Lokale Ausführung
Es wird die Nutzng einer vituellen Umgebung [(_virtualenv_)](https://www.dpunkt.de/common/leseproben//12951/2_Ihre%20Entwicklungsumgebung.pdf#page=15) empfohlen.

    >> pip install -r requirements.txt

    >> python PolProxServ.py

