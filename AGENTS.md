# Agent-Konfiguration für automatic_christmas_bell

## Berechtigungen

### Immer erlaubt (ohne Rückfrage)

#### Dateisystem-Operationen
- `mkdir` – Verzeichnisse erstellen
- `mv` – Dateien/Verzeichnisse verschieben
- `cp` – Dateien kopieren
- `rm <datei>` – Einzelne Dateien löschen
- `ls`, `cd`, `pwd` – Navigation und Anzeige
- `cat`, `grep`, `find` – Leseoperationen

#### Git-Operationen
- `git add` – Staging von Änderungen
- `git commit` – Lokales Commit
- `git status` – Status abfragen
- `git log` – History anzeigen
- `git diff` – Unterschiede anzeigen
- `git pull` – Änderungen abrufen

#### Bearbeitung
- `edit` – Dateien bearbeiten
- `write_file` – Dateien erstellen/überschreiben
- `read_file` – Dateien lesen

### Erfordert Rückfrage

- `git push` – Änderungen zu Remote pushen
- `rm -rf` – Rekursives Löschen
- `git reset --hard` – Harter Reset
- `git stash drop` – Stash löschen
- `git push --force` – Force-Push

---

## Projektspezifische Regeln

### Arbeitsweise
- Alle Dateioperationen im Projektverzeichnis und Unterordnern sind ohne Nachfrage erlaubt
- Fokus auf klare, kurze Kommunikation
- Code-Änderungen nur nach Rücksprache (außer neue Dateien in `docs/`)

### Dokumentation
- `README.md` – Anwendung im Fokus (kurz, prägnant)
- `docs/` – Detaillierte Implementierung
- `LIZENZ` – Lizenzinformationen

---

## Verzeichnisstruktur

```
automatic_christmas_bell/
├── AGENTS.md           # Diese Konfiguration
├── README.md           # Anwendung
├── buttons.ino         # Arduino-Sketch
├── weihnachtsglocke.fzz
├── weihnachtsglocke_Schaltplan.png
├── weihnachtsglocke_Schaltplan.svg
├── LIZENZ
├── .gitignore
└── docs/
    └── IMPLEMENTIERUNG.md  # Umsetzung
```

---

*Letzte Aktualisierung: 25. Oktober 2025*
