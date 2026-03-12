# CLAUDE.md

Diese Datei gibt Claude Code (claude.ai/code) Anweisungen für die Arbeit in diesem Repository.

---

## Was das hier ist

Dies ist der **Messe-App Workspace** — ein vollautomatisiertes System für die Planung, Erfassung und Auswertung von Fachmessebesuchen. Telegram-Bot erfasst Eindrücke, n8n verarbeitet sie, SeaTable speichert sie, Dashboard visualisiert sie, Claude wertet aus.

**Andere Projekte (Webinar, Kundenprojekte, etc.) werden in separaten Workspaces verwaltet.**

**Diese Datei (CLAUDE.md) ist das Fundament.** Sie wird automatisch am Anfang jeder Session geladen. Halte sie aktuell.

---

## Workspace-Struktur

```
.
├── CLAUDE.md              # Diese Datei — immer geladen
├── .mcp.json              # MCP-Server-Konfiguration (n8n)
├── .env                   # API-Keys und Secrets (NICHT committen!)
├── .claude/commands/      # Slash-Commands
├── context/               # Kontext: Wer, Strategie, aktueller Stand
├── plans/                 # Implementierungspläne
├── outputs/messen/        # Auswertungen pro Messe
├── reference/             # Templates, Kategorien, KI-Prompts
├── scripts/               # Python-Skripte (SeaTable, n8n)
└── dashboard/             # Event-Dashboard (HTML/CSS/JS/PHP)
```

---

## Commands

| Command | Zweck |
| --- | --- |
| `/prime` | Session-Start: Kontext laden, Verständnis bestätigen |
| `/create-plan` | Implementierungsplan erstellen vor größeren Änderungen |
| `/implement` | Plan umsetzen |
| `/messe-auswertung` | Rohdaten auswerten → Zusammenfassung + Aktionsplan + Follow-ups |
| `/shutdown` | Session sauber beenden, Workspace aktualisieren |

---

## System-Architektur

### Erfassung (während der Messe)

1. User schickt Telegram-Nachricht an Bot (Text, Sprache oder Foto)
2. n8n-Workflow `kMA6sVg1x2KkITCo` verarbeitet:
   - Text → Hashtag-Extraktion → Kategorie + Inhalt
   - Sprache → OpenAI Whisper → Text → wie oben
   - Foto → Speicherung mit Beschreibung
   - Commands (/messe, /status, /hilfe) → Bot-Steuerung
3. Ergebnis wird in SeaTable gespeichert (Tabelle `ZtiH`)
4. Bot bestätigt mit Kategorie-Emoji

### Kategorien

`#kontakt` `#trend` `#pain` `#idee` `#wettbewerb` `#foto` `#zitat` `#produkt` `#notiz`

### Dashboard (eventdashboard.transformwerk.digital)

- Live-Daten aus SeaTable via PHP-Proxy (`api.php`)
- KPIs, Charts (Chart.js), Kontakte-Tabelle, Pain Points, Trends, Zitate
- **Follow-ups-Sektion:** Karten pro Kontakt mit "Draft erstellen" und "Gesendet"-Buttons
- Reports dynamisch aus SeaTable-Tabelle `G7m3`
- PDF-Export via html2pdf.js
- Token-basierte Auth (Passwort in `.env.dashboard`)

### Follow-up-Drafts (E-Mail-Entwürfe)

- Dashboard-Button "Draft erstellen" → api.php → n8n Webhook → IMAP APPEND → Outlook Drafts
- n8n-Workflow `SrRcsrSPY1gHRcFB` ("Follow-up Draft")
- Absender: `info@transformwerk.digital`
- IMAP-Credentials als n8n Environment Variables (IMAP_USER, IMAP_PASSWORD, IMAP_HOST, IMAP_PORT, IMAP_DRAFTS_FOLDER)
- Status-Tracking in SeaTable: Offen → Entwurf → Gesendet

### Auswertung (nach der Messe)

`/messe-auswertung [name]` → erstellt:
- `outputs/messen/[datum]-[name]/auswertung.md`
- `outputs/messen/[datum]-[name]/marketing-aktionen.md`
- `outputs/messen/[datum]-[name]/follow-ups.md`
- Reports werden auch in SeaTable Reports-Tabelle geschrieben

---

## Technische Details

| Komponente | Detail |
| --- | --- |
| n8n-Server | `n8n.srv1159226.hstgr.cloud` |
| n8n-Workflow Messe Capture | ID: `kMA6sVg1x2KkITCo` |
| n8n-Workflow Follow-up Draft | ID: `SrRcsrSPY1gHRcFB` |
| n8n Webhook Follow-up | `https://n8n.srv1159226.hstgr.cloud/webhook/followup-draft` |
| SeaTable Einträge-Tabelle | ID: `ZtiH` |
| SeaTable Reports-Tabelle | ID: `G7m3` |
| SeaTable Follow-ups-Tabelle | ID: `Nid7` |
| SeaTable Spalten-Keys | `0000`=Messe, `lC6b`=Kategorie, `CRS4`=Inhalt, `m9hw`=Roh-Nachricht |
| SeaTable Reports-Keys | `0000`=Messe, `6RFa`=Report-Typ, `k62Q`=HTML-Content, `dDa5`=Version |
| SeaTable Follow-ups-Keys | `0000`=Messe, `0tI2`=Kontakt-Name, `z3pF`=Firma, `f8a9`=E-Mail, `PC98`=Betreff, `V3ud`=Nachricht, `HdnU`=Kanal, `rJ0T`=Prioritaet, `u601`=Status |
| Kategorie-IDs | kontakt=534713, trend=148879, pain=103515, idee=123561, wettbewerb=404015, foto=537524, zitat=348225, produkt=255330, notiz=270903 |
| Dashboard | eventdashboard.transformwerk.digital |
| MCP | Konfiguriert in `.mcp.json`, aber instabil — REST API mit API-Key als Fallback |

---

## Referenzdokumente

- `reference/messe-capture-anleitung.md` — Telegram-Erfassungs-Anleitung
- `reference/messe-kategorien.md` — Kategorie-Definitionen mit Beispielen
- `reference/messe-ki-prompts.md` — KI-Prompts für Auswertung
- `reference/messe-auswertung-template.md` — Template Zusammenfassung
- `reference/messe-marketing-aktionen-template.md` — Template Aktionsplan

---

## Kritische Anweisung: Diese Datei pflegen

Nach jeder Workspace-Änderung prüfen:
1. Neue Funktionalität → hier dokumentieren
2. Strukturänderung → Baum aktualisieren
3. Technische IDs/Keys geändert → Tabelle aktualisieren
4. Neuer Command → Commands-Tabelle ergänzen

---

## Session-Workflow

1. `/prime` → Kontext laden
2. Arbeiten / Commands nutzen
3. `/create-plan` vor größeren Änderungen
4. `/implement` zum Umsetzen
5. `/shutdown` zum Beenden
