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

    >> python execution.py


* validate(policy):

      Validate a passed YaPPL-Policy against the Standard YaPPL-Schema.

      arguments:
      policy -- the YaPPL-Policy to validate

      In order to validate a policy, a JSON file containing the Schema has to
      be present


## class YaPPL
Methods defined here:

* getExcludedPurpose(self):

      Return ALL excluded Purposes.

      arguments:
      none

      If a requested processing purpose is in this list,all data transfer
      should be prohibited

* getExcludedUtilizer(self):

      Return ALL excluded Utilizers.

      arguments:
      none

      If the requesting institution is in this list, all data transfer should
      be prohibited

* getTrRules(self):

      Return all Transformation Rules.

      arguments:
      none

      This method enables the execution of data transformations according to
      the rules in a policy. A desired transformation depends on given
      combinations of Purposes and Utilizers.
      e.g.:
      If the requesting institution is in the returned ['Utilizer'] list AND
      the requested processing purpose is in the ['Purpose'] list, the
      functions inside the ['Transformation'] list have to be performed before
      data transfer.

* newRule(self, permittedPurpose, excludedPurpose, permittedUtilizer, excludedUtilizer, transformation):

      Append a new Rule to a Preference.

      arguments:
      permittedPurpose -- [list] of permitted purposes
      excludedPurpose -- [list] of excluded purposes
      permittedUtilizer -- [list] of permitted utilizers
      excludedUtilizer -- [list] of excluded utilizers
      transformation -- [list] of transformation objects

* updateRule(self, ruleID, permittedPurpose=[], excludedPurpose=[], permittedUtilizer=[], excludedUtilizer=[], transformation=[]):

      Update a Rule with new Values.

      arguments:
      ruleID -- ID of the rule to be updated
      permittedPurpose -- [list] of permitted purposes
      excludedPurpose -- [list] of excluded purposes
      permittedUtilizer -- [list] of permitted utilizers
      excludedUtilizer -- [list] of excluded utilizers
      transformation -- [list] of transformation objects

      at least the ID and ONE updated Value should be present

* createPolicy(self):

      Create a YaPPL compliant Policy in JSON format from the respective python object.

      arguments:
      none

* archiveRule(self, ruleID):

      Archive a Rule for potential audits.

      arguments:
      ruleID -- the ID of the rule to be archived
