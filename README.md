# Ausführungsservice
_Proof-of-Concept_ Implementierung der _Ausführungsservice_ -Komponente der _Privacy Proxy_ Architektur.

Es handelte sich ursprünglich um einen Proxy-Server für die Participatory Sensing Plattform [OpenSense.network](opensense.network). Die [API](https://www.opensense.network/beta/apidocs/) der Plattform wird gespiegelt. Werden Sensordaten abgefragt, überprüft der Service ob zu den angeforderten Daten bzw. Sensoren Nutzungspräferenzen vorliegen.Sind diese verfügbar, werden die Daten entsprechend der dort verzeichneten Regeln vorverarbeitet und erst dann an die anfragende Institution herausgegeben.

## Nutzung

Im folgenden werden mögliche Wege aufgezeigt, um den Ausführungsservice zu testen.

### Voraussetzungen

Angaben zu erforderlichen Programmbibliotheken und Erweiterungen finden sich in der Datei `requirements.txt`.

    certifi==2018.11.29
    chardet==3.0.4
    Click==7.0
    Flask==1.0.2
    idna==2.8
    itsdangerous==1.1.0
    Jinja2==2.10
    MarkupSafe==1.1.0
    requests==2.21.0
    urllib3==1.24.1
    Werkzeug==0.14.1


### a) Lokale Ausführung

Es wird die Nutzng einer vituellen Umgebung [(_virtualenv_)](https://www.dpunkt.de/common/leseproben//12951/2_Ihre%20Entwicklungsumgebung.pdf#page=15) empfohlen.

    >> git clone https://github.com/EMIDD-Projekt/PraeferenzAusfuehrungsService.git

    >> pip install -r requirements.txt

    >> python PolProxServ.py

Anschließend steht der Service unter [`http://127.0.0.1:5000/`]( http://127.0.0.1:5000/) zur Verfügung.

### b) Ausführung als Cloud Service
tbd.

## zusätzliche API-Parameter

Die API des Ausführungservices verhält sich prinzipiell genauso wie die [API](https://www.opensense.network/beta/apidocs/) der Participatory Sensing Plattform [OpenSense.network](opensense.network) (Dokumenatation siehe [hier](https://www.opensense.network/beta/apidocs/)). Werden spezifische Daten einzelner Sensoren (https://www.opensense.network/beta/api/v1.0/sensors/{sensor_id}/values) abgefragt, erwartet der Proxy die Angabe eines spezifischen Verarbeitungszwecks (`purpose`) sowie die Nennung der Identität der anfragenden Institution (`utilizer`) als URL-Parameter in der Form

    (`.../{sensor_id}/values?utilizer=ZZZ&purpose=YYY`).

wobei ZZZ und YYY entsprechend zu ersetzen sind.

Sollte sich in den Meta-Daten des entsprechenden Sensors Angaben über vorhandene Nutzungspräferenzen finden (`"usagePreferenceLink": "URL"`), werden die Präferenzen von der entsprechende URL geladen, ausgewertet und nach der in den Präferenzen angegebenen Vorverarbeitung die zugehörigen Sensorwerte nur in der Form herausgegeben, wie in den Nutzungspräferenzen spezifiziert.