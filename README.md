#sourceBox
===
Synchronisations Struktur für kolaboratives Arbeiten auf textbasierten Dateien


###### Note
	
	This is a project of a cource in internet communications at the technical university of munich. Since the course is in German, all documentation and comments will also be in German. If you wish to use our code for your own project, please contact us.


## Basis:
---

** Thema 3: **  P2P/Webserver basierter Dateiaustausch

## Mindestanforderungen:
---------------------------
* Nutzer tauschen Dateien, die in einem Ordner liegen, automatisch untereinander aus
* Nutzer kann sich alle möglichen Ordner anzeigen lassen
* Nutzer sollen miteinander Ordner teilen können
* Inhalte geteilter Ordner sollen immer synchron gehalten werden
	*  Hinzufügen einer Datei -> Automatisches Aktualisieren der Ordner aller Abonnenten
	* Löschen einer Datei -> Automatisches Aktualisieren der Ordner aller Abonnenten
* Grundstruktur können reine P2P/Server Architekturen oder hybride Architekturen sein

* Reaktion auf Fehlerfälle


## Termine
---------------------------
** Mo. 03.06. 15:00 **  Präsentation der Idee als Poster in PowerPoint





## Features
---------------------------
* Lock-Funktion für einzelne Dateiparts
* Intelligentes Versionskontrollsystem: Automatisches Commit/Checkout bei Datei öffnen/schließen
* Plattformunabhängigkeit: Windows, Linux, MacOS,
* Grafische Oberfläche / PlugIn für Dateimanager


## Implementierung in Python
---------------------------

### Frameworks



## Architektur
---------------------------
Zunächst Mindestanforderungen

* Konzept: Lock-Modfy-Write  	
      http://de.wikipedia.org/wiki/Versionsverwaltung
	Backend: SVN
*  Struktur: Client/Server
* ggf. Verwendung bestehender Protokolle wie WebDAV




