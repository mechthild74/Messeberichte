# CLAUDE.md

Diese Datei gibt Claude Code (claude.ai/code) Anweisungen für die Arbeit in diesem Repository.

---

## Was das hier ist

Dies ist ein **Claude Workspace für Fachmesse-Strategie** — eine strukturierte Umgebung für die Planung, Erfassung und Auswertung von Fachmessebesuchen im Handwerk (SHK). Ziel: Messebesuche systematisch in Marketing-Aktivitäten und Kundenakquise umwandeln.

Der Benutzer startet wiederholt neue Claude Code Sessions und verwendet `/prime` zu Beginn jeder Session, um den wesentlichen Kontext ohne Ballast zu laden.

**Diese Datei (CLAUDE.md) ist das Fundament.** Sie wird automatisch am Anfang jeder Session geladen. Halte sie aktuell — sie ist die Single Source of Truth dafür, wie Claude diesen Workspace verstehen und darin arbeiten soll.

---

## Die Claude-User-Beziehung

Claude arbeitet als **Agenten-Assistent** mit Zugriff auf die Workspace-Ordner, Kontext-Dateien, Commands und Outputs. Die Beziehung ist:

- **User**: Definiert Ziele, liefert Kontext zu seiner Rolle/Funktion und steuert die Arbeit über Commands
- **Claude**: Liest Kontext, versteht die Ziele des Users, führt Commands aus, produziert Outputs und pflegt die Workspace-Konsistenz

Claude sollte sich immer über `/prime` am Session-Start orientieren, dann mit vollem Bewusstsein dafür handeln, wer der User ist, was er erreichen möchte und wie dieser Workspace das unterstützt.

---

## Workspace-Struktur

```
.
├── CLAUDE.md              # Diese Datei — Kern-Kontext, immer geladen
├── .mcp.json              # MCP-Server-Konfiguration (n8n-Zugang)
├── .env                   # API-Keys und Secrets (NICHT committen!)
├── .claude/
│   └── commands/          # Slash-Commands, die Claude ausführen kann
│       ├── prime.md       # /prime — Session-Initialisierung
│       ├── create-plan.md # /create-plan — Implementierungspläne erstellen
│       ├── implement.md   # /implement — Pläne umsetzen
│       ├── shutdown.md    # /shutdown — Session sauber beenden
│       └── messe-auswertung.md # /messe-auswertung — Messe-Rohdaten auswerten
├── context/               # Hintergrund-Kontext über den User und das Projekt
├── plans/                 # Implementierungspläne erstellt von /create-plan
├── outputs/               # Arbeitsergebnisse und Deliverables
│   └── messen/            # Messe-Auswertungen (pro Messe ein Ordner)
├── reference/             # Vorlagen, Beispiele, wiederverwendbare Patterns
│   ├── messe-capture-anleitung.md   # Anleitung für Telegram-Erfassung
│   ├── messe-kategorien.md          # Kategorie-System (#kontakt, #trend, etc.)
│   ├── messe-ki-prompts.md          # KI-Prompts für Zusammenfassung & Aktionsplan
│   ├── messe-auswertung-template.md # Template für Messe-Zusammenfassung
│   └── messe-marketing-aktionen-template.md # Template für Marketing-Aktionsplan
└── scripts/               # Automatisierungsskripte (falls zutreffend)
```

**Verzeichnisse:**

| Verzeichnis  | Zweck                                                                                   |
| ------------ | --------------------------------------------------------------------------------------- |
| `context/`   | Wer der User ist, seine Rolle, aktuelle Prioritäten, Strategien. Gelesen von `/prime`. |
| `plans/`     | Detaillierte Implementierungspläne. Erstellt mit `/create-plan`, umgesetzt mit `/implement`. |
| `outputs/`   | Deliverables, Analysen, Reports und Arbeitsergebnisse.                                 |
| `reference/` | Hilfreiche Dokumentation, Vorlagen und Patterns für verschiedene Workflows.            |
| `scripts/`   | Automatisierungs- und Tooling-Skripte.                                                 |

---

## Commands

### /prime

**Zweck:** Neue Session mit vollem Kontext-Bewusstsein initialisieren.

Am Anfang jeder Session ausführen. Claude wird:

1. CLAUDE.md und Kontext-Dateien lesen
2. Verständnis von User, Workspace und Zielen zusammenfassen
3. Bereitschaft zur Unterstützung bestätigen

### /create-plan [anforderung]

**Zweck:** Detaillierten Implementierungsplan erstellen, bevor Änderungen gemacht werden.

Verwenden beim Hinzufügen neuer Funktionalität, Commands, Skripte oder bei strukturellen Änderungen. Erzeugt ein gründliches Plan-Dokument in `plans/`, das Kontext, Begründung und schrittweise Aufgaben erfasst.

Beispiel: `/create-plan Wettbewerbs-Analyse-Command hinzufügen`

### /implement [plan-pfad]

**Zweck:** Einen mit /create-plan erstellten Plan umsetzen.

Liest den Plan, führt jeden Schritt der Reihe nach aus, validiert die Arbeit und aktualisiert den Plan-Status.

Beispiel: `/implement plans/2026-01-28-wettbewerbs-analyse-command.md`

### /shutdown

**Zweck:** Session sauber beenden — Workspace scannen, aufräumen, CLAUDE.md und Context aktualisieren.

### /messe-auswertung [messe-name]

**Zweck:** Rohdaten eines Messebesuchs auswerten und strukturierte Outputs erstellen.

Liest Messe-Rohdaten (aus Datei oder Chat), erstellt Zusammenfassung, Marketing-Aktionsplan und Follow-up-Nachrichten. Outputs landen in `outputs/messen/[datum]-[messe-name]/`.

Beispiel: `/messe-auswertung IFH Nürnberg 2026`

---

## Messe-Capture-Workflow

### Überblick

System zur strukturierten Erfassung und Auswertung von Fachmessebesuchen:
1. **Während der Messe:** Telegram-Bot erfasst Eindrücke (#kontakt, #trend, #pain, #idee, #wettbewerb, #foto, #zitat, #produkt)
2. **Automatische Verarbeitung:** n8n-Workflow → Hashtag-Extraktion → SeaTable-Speicherung (DSGVO-konform)
3. **Nach der Messe:** `/messe-auswertung` erstellt strukturierte Zusammenfassung + priorisierten Marketing-Aktionsplan

### Referenzdokumente

- `reference/messe-capture-anleitung.md` — Anleitung für die Telegram-Erfassung (vor jeder Messe lesen)
- `reference/messe-kategorien.md` — Detaillierte Kategorie-Definitionen mit Beispielen
- `reference/messe-ki-prompts.md` — KI-Prompts für Zusammenfassung und Aktionsableitung
- `reference/messe-auswertung-template.md` — Template für Messe-Zusammenfassungen
- `reference/messe-marketing-aktionen-template.md` — Template für Marketing-Aktionspläne

### Output-Struktur

Pro Messe wird ein Ordner erstellt: `outputs/messen/YYYY-MM-DD-[messe-name]/`
- `rohdaten.md` — Exportierte Rohdaten aus SeaTable
- `auswertung.md` — Strukturierte Zusammenfassung
- `marketing-aktionen.md` — Priorisierter Aktionsplan
- `follow-ups.md` — Personalisierte Follow-up-Nachrichten

### Infrastruktur-Status

- **Telegram-Bot:** Credentials bereits in n8n vorhanden (aus "Telegram Support" Workflow)
- **SeaTable:** Base "Messe-Capture" eingerichtet, API-Key in `.env` hinterlegt
- **n8n-Workflow:** Noch zu bauen (Schritt 3-4 des Plans) — bestehender Workflow hat bereits Telegram Trigger + Switch + OpenAI Whisper Transkription
- **Workspace-Dateien:** Vollständig implementiert

---

## Integrationen

### n8n (via MCP)

Der Workspace hat eine MCP-Verbindung zum n8n-Server auf Hostinger (`n8n.srv1159226.hstgr.cloud`). Claude kann Workflows direkt in n8n erstellen, lesen und bearbeiten. Konfiguration in `.mcp.json`.

**Bestehende Workflows:**
- "Telegram Support" — Basis für den Messe-Capture-Workflow (enthält: Telegram Trigger, Switch, OpenAI Whisper Transkription)

**Hinweis:** MCP-Verbindung muss zu Session-Start geprüft werden — in der ersten Session (2026-03-11) waren die n8n-MCP-Tools nicht geladen. Ggf. Session neu starten, wenn n8n-Tools benötigt werden.

---

## Aktuelle Pläne

| Plan | Status | Beschreibung |
| --- | --- | --- |
| `plans/2026-03-11-messe-capture-system.md` | Teilweise implementiert | Telegram-basiertes Messe-Capture-System mit SeaTable + n8n + Claude-Auswertung — Workspace-Dateien fertig, Infrastruktur (Bot, SeaTable, n8n) noch offen |

---

## Kritische Anweisung: Diese Datei pflegen

**Wann immer Claude Änderungen am Workspace macht, MUSS Claude prüfen, ob CLAUDE.md aktualisiert werden muss.**

Nach jeder Änderung — ob Commands, Skripte, Workflows oder Strukturänderungen — frage:

1. Fügt diese Änderung neue Funktionalität hinzu, die Benutzer kennen müssen?
2. Ändert sie die oben dokumentierte Workspace-Struktur?
3. Sollte ein neuer Command aufgelistet werden?
4. Braucht context/ neue Dateien dafür?

Falls ja, aktualisiere die entsprechenden Abschnitte. Diese Datei muss immer den aktuellen Zustand des Workspace widerspiegeln, damit zukünftige Sessions genauen Kontext haben.

**Beispiele für Änderungen, die CLAUDE.md-Updates erfordern:**

- Neuen Slash-Command hinzufügen → im Commands-Abschnitt ergänzen
- Neuen Output-Typ erstellen → in Workspace-Struktur dokumentieren oder Abschnitt erstellen
- Skript hinzufügen → Zweck und Verwendung dokumentieren
- Workflow-Patterns ändern → entsprechende Dokumentation aktualisieren

---

## Für Benutzer, die dieses Template herunterladen

Um diesen Workspace an deine eigenen Bedürfnisse anzupassen, fülle deine Kontext-Dokumente in `context/` aus und passe sie nach Bedarf an. Verwende dann `/create-plan` zum Planen und `/implement` zum Umsetzen struktureller Änderungen. So bleibt alles synchron — besonders CLAUDE.md, die immer den aktuellen Zustand des Workspace widerspiegeln muss.

---

## Session-Workflow

1. **Start**: `/prime` ausführen, um Kontext zu laden
2. **Arbeiten**: Commands verwenden oder Claude direkt mit Aufgaben beauftragen
3. **Änderungen planen**: `/create-plan` vor größeren Ergänzungen verwenden
4. **Umsetzen**: `/implement` zum Ausführen von Plänen verwenden
5. **Pflegen**: Claude aktualisiert CLAUDE.md und context/ während sich der Workspace weiterentwickelt

---

## Notizen

- Kontext minimal aber ausreichend halten — kein Bloat
- Pläne in `plans/` mit datierten Dateinamen für die Historie
- Outputs nach Typ/Zweck in `outputs/` organisiert
- Referenzmaterialien in `reference/` zur Wiederverwendung
