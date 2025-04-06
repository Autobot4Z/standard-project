# My Project

Standardisierte Struktur für wartbaren Python-Code.


## Wichtige Dinge zum Start

Keywords und deren Bedeutung:
- TODO: Hier gibt es Verbesserungs- oder Handlungsbedarf
- CRITICAL PATH: Prüfe zuerst hier bei Fehlern

Erstelle Kommentare Blockweise (ca. ein Kommentar pro Zeile Code), d.h. vor Funktionen oder wenn nötig in Funktionen. 
Kommentare sollten stets übersichtlich gehalten werden.

*Führe folgene Commands aus (Nur beim ersten Mal):*
- pip install -r requirements.txt
- pre-commit install


## Einarbeitung

In docs/ findest du alle Dokumente, die zum Verstehen des Codes notwenig sind.
In jedem Ordner ist eine README.md für ein besseres Verständnis, wozu der Ordner genutzt wird und wenn nötig eine SOP.md die beschreibt was zu tun ist.

*WICHTIG:* Bei Änderungen Dokumente in docs/ aktuell halten

memory-bank/ ist nur für Cline/Roo/Cursor - dadurch versteht die KI den Code.


## Git Commit & Git Push

Mit pre-commit werden automatisch alle Tests in tests/ ausgeführt und geprüft, ob der Code funktioniert. 
Schlägt die Prüfung fehl, wird NICHT commited!

*WICHTIG:* Vor dem pushen immer CHANGELOG.md aktualisieren.