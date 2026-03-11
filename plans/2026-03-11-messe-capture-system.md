# Plan: Messe-Capture-System — Telegram-basierte Messeeindrücke erfassen & in Marketing-Aktivitäten umwandeln

**Erstellt:** 2026-03-11
**Status:** Entwurf
**Anforderung:** System aufbauen, das während Fachmessebesuchen (SHK/Handwerk) über Telegram Eindrücke, Ideen und Kontakte erfasst, diese automatisch zu strukturierten Zusammenfassungen aufbereitet und daraus konkrete Marketing-Aktivitäten für Wachstum ableitet.

---

## Überblick

### Was dieser Plan erreicht

Ein End-to-End-System, das den gesamten Messe-Workflow abdeckt: Von der schnellen Erfassung per Telegram-Nachrichten während der Messe (Text, Sprache, Fotos) über die automatische Strukturierung und Zusammenfassung durch KI bis hin zur Ableitung konkreter, priorisierter Marketing-Aktivitäten. Das System wird als n8n-Workflow implementiert und liefert nach jeder Messe ein fertiges Aktionsdokument.

### Warum das wichtig ist

Fachmessen sind für Mechthild als Gründerin in der Akquise-Phase eine der wertvollsten Quellen für Markteinblicke, Kontakte und Content-Ideen. Ohne strukturierte Erfassung gehen Eindrücke verloren. Mit diesem System wird jeder Messebesuch systematisch in Wachstumsaktivitäten umgewandelt — direkt verknüpft mit den strategischen Prioritäten Kundenakquise, Sichtbarkeit und Referenzprojekte.

---

## Aktueller Zustand

### Relevante bestehende Struktur

- `context/strategy.md` — Strategische Prioritäten (Kundenakquise, Sichtbarkeit, Referenzprojekte)
- `context/business-info.md` — Zielkunden: Handwerksbetriebe, KMUs
- `context/current-data.md` — Pipeline-Tracking, Tooling (n8n, Make.com, Brevo)
- `outputs/` — Leer, bereit für Messe-Outputs
- `reference/` — Leer, bereit für Templates
- `scripts/` — Leer, bereit für Automatisierungsskripte

### Lücken oder Probleme, die adressiert werden

- **Kein Erfassungssystem:** Aktuell keine strukturierte Methode, Messeeindrücke in Echtzeit festzuhalten
- **Kein Messe-Nachbereitungsprozess:** Keine Vorlage oder Workflow für die Auswertung nach einer Messe
- **Keine Verbindung Messe → Marketing:** Kein definierter Prozess, wie Messeeinblicke in konkrete Aktivitäten münden
- **Kein Telegram-Workflow:** Telegram als Capture-Kanal ist noch nicht eingerichtet

---

## Vorgeschlagene Änderungen

### Zusammenfassung der Änderungen

- Telegram-Bot erstellen und als Eingangskanal konfigurieren
- n8n-Workflow bauen: Telegram → Zwischenspeicher → KI-Zusammenfassung → Aktionsplan
- Messe-Vorbereitungs-Template erstellen (welche Infos gezielt erfassen)
- Messe-Auswertungs-Template erstellen (Struktur für das Endergebnis)
- Prompt-Template für die KI-Auswertung erstellen
- Claude-Command `/messe-auswertung` für die manuelle Nachbereitung im Workspace
- CLAUDE.md aktualisieren

### Neue Dateien erstellen

| Dateipfad | Zweck |
| --- | --- |
| `reference/messe-capture-anleitung.md` | Anleitung: Wie während der Messe Telegram-Nachrichten strukturiert senden |
| `reference/messe-kategorien.md` | Kategorie-System für Messe-Inputs (Kontakte, Trends, Wettbewerber, Ideen, Pain Points) |
| `reference/messe-auswertung-template.md` | Template für das fertige Messe-Auswertungsdokument |
| `reference/messe-marketing-aktionen-template.md` | Template für abgeleitete Marketing-Aktivitäten mit Priorisierung |
| `reference/messe-ki-prompts.md` | KI-Prompts für Zusammenfassung und Aktionsableitung |
| `.claude/commands/messe-auswertung.md` | Command: Rohdaten aus Messe auswerten und Aktionsplan erstellen |
| `outputs/messen/` | Verzeichnis für Messe-Auswertungen (pro Messe ein Ordner) |

### Zu ändernde Dateien

| Dateipfad | Änderungen |
| --- | --- |
| `CLAUDE.md` | Messe-Workflow dokumentieren, neuen Command auflisten, `outputs/messen/` in Struktur ergänzen |
| `context/current-data.md` | Messe-Pipeline/Kalender ergänzen |

### Zu löschende Dateien

Keine.

---

## Design-Entscheidungen

### Getroffene Schlüsselentscheidungen

1. **Telegram als Capture-Kanal:** Telegram ist auf dem Handy schnell erreichbar, unterstützt Text, Sprache und Fotos, und hat eine hervorragende Bot-API. Ideal für unterwegs auf der Messe — keine App-Wechsel nötig.

2. **Hashtag-basierte Kategorisierung:** Nachrichten werden mit einfachen Hashtags kategorisiert (#kontakt, #trend, #idee, #pain, #wettbewerb, #foto). Das ist schnell zu tippen und ermöglicht automatische Sortierung im n8n-Workflow.

3. **n8n als Automatisierungsplattform (nicht Make.com):** n8n ist bereits im Einsatz für SHK-Projekte, self-hosted auf Hostinger (`n8n.srv1159226.hstgr.cloud`), und bietet native Telegram-Integration + KI-Nodes. Es existiert bereits ein Workflow "Telegram Support", auf dem aufgebaut wird.

4. **Aufbau auf bestehendem "Telegram Support" Workflow:** In n8n existiert bereits ein Workflow namens "Telegram Support" mit Telegram-Integration. Dieser wird als Basis verwendet und um die Messe-Capture-Logik erweitert — kein Neubau von Grund auf.

5. **SeaTable als Zwischenspeicher (nicht SeaTable/Airtable):** SeaTable ist DSGVO-konform (Server in Deutschland/EU), self-hostbar, bietet eine Airtable-ähnliche Oberfläche mit API-Zugang und ist direkt in n8n integrierbar. Erfüllt die Datenschutzanforderungen für personenbezogene Kontaktdaten von der Messe.

6. **Zweistufige Verarbeitung — Sammeln + Auswerten:** Während der Messe wird nur gesammelt (SeaTable als Zwischenspeicher). Die KI-Auswertung läuft erst nach der Messe als separater Schritt — das gibt Kontrolle über die Qualität und erlaubt manuelle Ergänzungen.

7. **Claude baut den n8n-Workflow direkt über MCP:** Der n8n-Server ist per MCP-Integration erreichbar. Claude erstellt und konfiguriert den Workflow direkt in n8n — kein manueller Import nötig.

8. **Hybrid-Ansatz: n8n-Automatisierung + Claude-Command:** n8n übernimmt die Echtzeit-Erfassung und Strukturierung. Der Claude-Command `/messe-auswertung` übernimmt die tiefere Analyse und Marketing-Ableitung im Workspace — hier kann Mechthild im Dialog nachschärfen.

9. **Sprachnachrichten via Whisper/OpenAI transkribieren:** Auf der Messe ist Tippen oft unpraktisch. Sprachnachrichten werden automatisch transkribiert und wie Textnachrichten weiterverarbeitet.

### Betrachtete Alternativen

- **WhatsApp statt Telegram:** Keine offene Bot-API, Business-API komplex und kostenpflichtig → verworfen
- **Notion/Obsidian als Capture:** Zu langsam auf dem Handy, kein One-Click-Capture → verworfen
- **Alles in n8n mit KI:** Möglich, aber der Claude-Workspace bietet bessere interaktive Analyse-Möglichkeiten → Hybrid gewählt
- **Google Forms als Capture:** Zu viele Klicks pro Eintrag, killt den Flow auf der Messe → verworfen
- **SeaTable/Airtable als Speicher:** Nicht DSGVO-konform für personenbezogene Kontaktdaten → SeaTable gewählt (EU-Server, self-hostbar)
- **Neuen Workflow von Grund auf bauen:** Bestehender "Telegram Support" Workflow bietet bereits Telegram-Anbindung → darauf aufbauen spart Zeit und nutzt vorhandene Credentials

### Offene Fragen

1. **SeaTable-Account:** Ist bereits ein SeaTable-Account vorhanden oder muss einer erstellt werden? (Free-Tier reicht für den Start)
2. **Whisper-API oder lokales Modell?** Für Sprachtranskription — OpenAI Whisper API ist einfach, kostet minimal. Alternativ: Groq (schneller, free tier)
3. **Messe-Kalender:** Welche konkreten Messen stehen an? (Termine, Orte, Schwerpunkte) — wird für die Vorbereitung gebraucht
4. **Bot-Name:** Wie soll der Telegram-Bot heißen? z.B. `@transformwerk_messe_bot`
5. **"Telegram Support" Workflow:** Struktur und Nodes des bestehenden Workflows müssen vor der Implementierung analysiert werden, um die beste Erweiterungsstrategie zu bestimmen

---

## Architektur des Systems

### Datenfluss

```
WÄHREND DER MESSE:
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│  Telegram    │────▶│  n8n         │────▶│  SeaTable    │
│  (Handy)     │     │  Webhook     │     │  "Messe-Roh"    │
│              │     │  + Whisper   │     │                  │
│ Text/Voice/  │     │  Transkrip.  │     │ Timestamp        │
│ Foto + #Tag  │     │              │     │ Kategorie        │
└─────────────┘     └──────────────┘     │ Inhalt           │
                                          │ Medien-URL       │
                                          └─────────────────┘

NACH DER MESSE:
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│  SeaTable    │────▶│  n8n oder    │────▶│  Strukturierte   │
│  "Messe-Roh"    │     │  Claude      │     │  Zusammenfassung │
│                  │     │  Workspace   │     │  + Aktionsplan   │
└─────────────────┘     │  /messe-     │     │                  │
                         │  auswertung  │     │  outputs/messen/ │
                         └──────────────┘     └──────────────────┘
```

### Telegram-Nachrichtenformat (Anleitung für die Messe)

```
#kontakt Max Müller, Firma XYZ, Heizungsbauer, 50 MA,
interessiert an Digitalisierung Auftragsmanagement,
hat aktuell alles in Excel. Tel: 0171-xxx

#trend Viele Aussteller zeigen KI-Telefonassistenten,
scheint DAS Thema zu sein. Sintratec und Voicebot.de
als Anbieter gesehen.

#pain Mehrere Handwerker klagen über doppelte Dateneingabe
zwischen Büroanwendung und Baustellendoku

#idee LinkedIn-Post über die Top-3 Digitalisierungstrends
von der Messe schreiben

#wettbewerb Firma ABC bietet ähnliche Automatisierung an,
Fokus aber auf große Betriebe >100 MA, Preise ab 5k/Monat

#foto [Foto von Standpräsentation mit interessantem Workflow]
```

### Kategorien und deren Marketing-Relevanz

| Hashtag | Kategorie | Marketing-Output |
| --- | --- | --- |
| `#kontakt` | Personen/Firmen | Follow-up-Liste, LinkedIn-Vernetzung, Angebot senden |
| `#trend` | Branchentrends | Content-Ideen (Blog, LinkedIn, Webinar-Themen) |
| `#pain` | Kundenprobleme | Pain-Point-basiertes Marketing, Lösungs-Content |
| `#idee` | Eigene Ideen | Direkte Aufgaben für Content/Angebote |
| `#wettbewerb` | Wettbewerber | Positionierung schärfen, Differenzierung kommunizieren |
| `#foto` | Visuelles | Social Media Content, Dokumentation |
| `#zitat` | Aussagen | Testimonial-Material, Content-Snippets |
| `#produkt` | Interessante Produkte/Tools | Partnerschafts-Potenzial, eigenes Tooling erweitern |

---

## Schritt-für-Schritt-Aufgaben

### Schritt 1: Telegram-Bot erstellen

Einen Telegram-Bot über @BotFather erstellen und Token sichern.

**Aktionen:**

- In Telegram @BotFather öffnen
- `/newbot` ausführen, Name vergeben (z.B. "Transformwerk Messe Bot")
- Username vergeben (z.B. `transformwerk_messe_bot`)
- Bot-Token sicher speichern (wird in n8n gebraucht)
- Bot-Beschreibung setzen: "Messe-Eindrücke erfassen für Transformwerk"
- Optional: Bot-Profilbild setzen

**Betroffene Dateien:**

- Keine Workspace-Dateien — Telegram-Konfiguration

---

### Schritt 2: SeaTable als Zwischenspeicher einrichten

Eine SeaTable-Base erstellen, die alle Messe-Nachrichten datenschutzkonform (DSGVO) speichert.

**Aktionen:**

- SeaTable-Account erstellen (falls nicht vorhanden) auf seatable.io (Free-Tier, EU-Server)
- Base erstellen: "Messe-Capture"
- Tabelle "Einträge" mit Spalten:
  - `Timestamp` (Datum/Uhrzeit, automatisch)
  - `Messe` (Text — Name der Messe)
  - `Kategorie` (Single Select: kontakt, trend, pain, idee, wettbewerb, foto, zitat, produkt, notiz)
  - `Inhalt` (Long Text — Nachrichtentext ohne Hashtag)
  - `Medien-URL` (URL — falls Foto/Voice)
  - `Transkription` (Long Text — falls Sprachnachricht)
  - `Roh-Nachricht` (Long Text — Original-Telegram-Nachricht)
- API-Token generieren für n8n-Zugriff (SeaTable → Einstellungen → API-Tokens)
- n8n SeaTable Credentials einrichten (n8n hat native SeaTable-Nodes)

**Betroffene Dateien:**

- `.env` — SeaTable API-Token und Base-URL ergänzen

---

### Schritt 3: n8n-Workflow bauen — Messe-Capture (via MCP)

Den bestehenden "Telegram Support" Workflow in n8n analysieren und darauf aufbauend den Messe-Capture-Workflow erstellen. **Claude baut den Workflow direkt über die n8n-MCP-Integration** — kein manueller Import nötig.

**Vorgehen:**

1. Bestehenden "Telegram Support" Workflow über MCP laden und analysieren
2. Vorhandene Telegram-Credentials und Bot-Konfiguration identifizieren
3. Workflow erweitern oder als Kopie mit Messe-Logik erstellen

**Workflow-Nodes:**

**Node 1: Telegram Trigger** (aus bestehendem Workflow übernehmen)
- Trigger auf neue Nachrichten an den Bot
- Text, Voice und Photo unterstützen

**Node 2: Switch — Nachrichtentyp**
- Unterscheidung: Text / Voice / Photo
- Routing auf entsprechende Verarbeitungspfade

**Node 3a: Voice-Pfad — Audio herunterladen**
- Telegram File API: Voice-Datei herunterladen
- Weiterleitung an Whisper

**Node 3b: Voice-Pfad — Whisper Transkription**
- OpenAI Whisper API (oder Groq)
- Sprache: Deutsch
- Output: Transkribierter Text

**Node 3c: Photo-Pfad — Foto-URL extrahieren**
- Telegram File API: Bild-URL generieren
- Caption als Text extrahieren

**Node 4: Merge — Alle Pfade zusammenführen**
- Einheitliches Format: Text-Inhalt + optionale Medien-URL

**Node 5: Hashtag-Extraktion (Code-Node)**
- Regex: erstes `#wort` aus der Nachricht extrahieren
- Mapping auf Kategorie
- Fallback-Kategorie: `notiz` falls kein Hashtag

**Node 6: Aktive Messe bestimmen**
- Aus SeaTable-Konfig-Tabelle oder als Workflow-Variable
- Alternativ: Messe-Name per Bot-Command `/messe IFH Nürnberg` setzen

**Node 7: SeaTable — Zeile schreiben**
- n8n SeaTable-Node: Neue Zeile in Base "Messe-Capture", Tabelle "Einträge"
- Felder: Timestamp, Messe, Kategorie, Inhalt, Medien-URL, Transkription, Roh-Nachricht

**Node 8: Telegram — Bestätigung senden**
- Kurze Bestätigung zurück an Chat

**Implementierung via MCP:**
- Claude erstellt den Workflow direkt in n8n über die MCP-Server-Verbindung
- Kein manueller JSON-Export/Import nötig
- Workflow wird in n8n unter "Messe Capture" gespeichert und aktiviert

**Betroffene Dateien:**

- Direkt in n8n (via MCP) — kein lokaler JSON-Export nötig

---

### Schritt 4: Telegram-Bot-Commands konfigurieren

Hilfreiche Bot-Commands für die schnelle Bedienung während der Messe.

**Aktionen:**

- Folgende Commands via @BotFather registrieren:
  - `/start` — Bot starten, Begrüßung mit Kurzanleitung
  - `/messe [Name]` — Aktive Messe setzen (z.B. `/messe IFH Nürnberg 2026`)
  - `/status` — Zeigt aktuelle Messe + Anzahl erfasster Einträge pro Kategorie
  - `/export` — Löst die Zusammenfassungs-Generierung aus (Post-Messe)
  - `/hilfe` — Zeigt Hashtag-Übersicht und Beispiele

- In n8n entsprechende Command-Handler bauen

**Betroffene Dateien:**

- `scripts/n8n-messe-capture-workflow.json` (erweitern)

---

### Schritt 5: Capture-Anleitung erstellen

Ein Referenzdokument, das Mechthild vor jeder Messe kurz durchlesen kann.

**Aktionen:**

- Datei `reference/messe-capture-anleitung.md` erstellen mit:
  - Hashtag-Übersicht mit Beispielen
  - Tipps für effektive Erfassung (kurze Nachrichten, ein Gedanke pro Nachricht)
  - Sprachnachrichten-Tipps (deutlich sprechen, Kontext nennen)
  - Foto-Tipps (Caption mit Hashtag dazu)
  - Bot-Commands Übersicht
  - Checkliste: Was vor der Messe einrichten (Bot starten, Messe setzen)

**Betroffene Dateien:**

- `reference/messe-capture-anleitung.md` (neu)

---

### Schritt 6: Kategorien-Referenz erstellen

Detaillierte Beschreibung jeder Kategorie und wofür sie steht.

**Aktionen:**

- Datei `reference/messe-kategorien.md` erstellen mit:
  - Jede Kategorie (#kontakt, #trend, #pain, #idee, #wettbewerb, #foto, #zitat, #produkt)
  - Definition: Was gehört rein?
  - Beispiel-Nachrichten
  - Marketing-Output: Was wird daraus abgeleitet?

**Betroffene Dateien:**

- `reference/messe-kategorien.md` (neu)

---

### Schritt 7: KI-Prompts für Auswertung erstellen

Prompts, die die Rohdaten in strukturierte Zusammenfassungen und Aktionspläne verwandeln.

**Aktionen:**

- Datei `reference/messe-ki-prompts.md` erstellen mit:

**Prompt 1: Messe-Zusammenfassung**
- Input: Alle Einträge einer Messe aus SeaTable
- Output: Strukturierte Zusammenfassung nach Kategorien
- Enthält: Key Takeaways, Top-Kontakte, dominante Trends, häufigste Pain Points

**Prompt 2: Marketing-Aktionsplan**
- Input: Messe-Zusammenfassung
- Output: Priorisierte Liste von Marketing-Aktivitäten
- Struktur:
  - Sofort-Aktionen (24-48h): Follow-up-E-Mails, LinkedIn-Vernetzung
  - Kurzfristig (1-2 Wochen): LinkedIn-Posts, Blog-Artikel
  - Mittelfristig (1-3 Monate): Webinar-Themen, Angebotsideen, Partnerschafts-Ansprachen
- Jede Aktion mit: Beschreibung, Kanal, Ziel, Priorität (hoch/mittel/niedrig), geschätzter Aufwand

**Prompt 3: Kontakt-Follow-up-Generator**
- Input: Alle #kontakt-Einträge
- Output: Personalisierte Follow-up-Nachricht pro Kontakt (E-Mail oder LinkedIn)

**Betroffene Dateien:**

- `reference/messe-ki-prompts.md` (neu)

---

### Schritt 8: Auswertungs-Templates erstellen

Templates für die finalen Output-Dokumente.

**Aktionen:**

- Datei `reference/messe-auswertung-template.md` erstellen:
  ```
  # Messe-Auswertung: [Messe-Name]
  **Datum:** [Datum]
  **Ort:** [Ort]
  **Erfasste Einträge:** [Anzahl]

  ## Executive Summary
  [3-5 Sätze: wichtigste Erkenntnisse]

  ## Kontakte
  | Name | Firma | Rolle | Interesse | Follow-up |

  ## Branchentrends
  [Zusammenfassung der beobachteten Trends]

  ## Pain Points der Zielgruppe
  [Häufigste Probleme, die gehört wurden]

  ## Wettbewerber-Beobachtungen
  [Wer war da, was bieten sie, wie positionieren sie sich]

  ## Content-Ideen
  [Aus Trends, Pain Points und Gesprächen abgeleitet]

  ## Fotos & Visuelles
  [Dokumentation mit Kontext]
  ```

- Datei `reference/messe-marketing-aktionen-template.md` erstellen:
  ```
  # Marketing-Aktionen aus Messe: [Messe-Name]
  **Erstellt:** [Datum]
  **Basiert auf:** [Link zu Auswertung]

  ## Sofort-Aktionen (24-48h nach Messe)
  - [ ] [Aktion] — Kanal: [X] — Priorität: Hoch

  ## Kurzfristig (1-2 Wochen)
  - [ ] [Aktion] — Kanal: [X] — Priorität: [X]

  ## Mittelfristig (1-3 Monate)
  - [ ] [Aktion] — Kanal: [X] — Priorität: [X]

  ## Content-Pipeline
  | Thema | Format | Kanal | Deadline | Status |

  ## Follow-ups
  | Kontakt | Aktion | Deadline | Status |
  ```

**Betroffene Dateien:**

- `reference/messe-auswertung-template.md` (neu)
- `reference/messe-marketing-aktionen-template.md` (neu)

---

### Schritt 9: Claude-Command `/messe-auswertung` erstellen

Ein Slash-Command, der Rohdaten einliest und die volle Auswertung im Workspace durchführt.

**Aktionen:**

- Datei `.claude/commands/messe-auswertung.md` erstellen
- Der Command soll:
  1. Rohdaten entgegennehmen (Copy-Paste aus SeaTable oder als Datei in `outputs/messen/[messe-name]/rohdaten.md`)
  2. Kategorien-Referenz und KI-Prompts aus `reference/` laden
  3. Strukturierte Zusammenfassung erstellen → `outputs/messen/[messe-name]/auswertung.md`
  4. Marketing-Aktionsplan ableiten → `outputs/messen/[messe-name]/marketing-aktionen.md`
  5. Follow-up-Nachrichten für Kontakte generieren → `outputs/messen/[messe-name]/follow-ups.md`
  6. Zusammenfassung der Ergebnisse an den User geben

**Betroffene Dateien:**

- `.claude/commands/messe-auswertung.md` (neu)

---

### Schritt 10: Output-Verzeichnisstruktur anlegen

Ordnerstruktur für Messe-Outputs vorbereiten.

**Aktionen:**

- Verzeichnis `outputs/messen/` erstellen
- README oder `.gitkeep` für die Struktur
- Konvention festlegen: `outputs/messen/YYYY-MM-DD-[messe-name]/`
  - `rohdaten.md` — Exportierte Rohdaten
  - `auswertung.md` — Strukturierte Zusammenfassung
  - `marketing-aktionen.md` — Priorisierter Aktionsplan
  - `follow-ups.md` — Generierte Follow-up-Nachrichten

**Betroffene Dateien:**

- `outputs/messen/` (neu)

---

### Schritt 11: CLAUDE.md aktualisieren

Den Messe-Workflow in der Kern-Dokumentation verankern.

**Aktionen:**

- In CLAUDE.md ergänzen:
  - `outputs/messen/` in die Workspace-Struktur-Tabelle
  - `/messe-auswertung` in den Commands-Abschnitt
  - Kurzbeschreibung des Messe-Capture-Workflows
  - Referenz auf `reference/messe-*` Dateien

**Betroffene Dateien:**

- `CLAUDE.md`

---

### Schritt 12: current-data.md um Messe-Kalender ergänzen

Anstehende Messen tracken.

**Aktionen:**

- In `context/current-data.md` neuen Abschnitt ergänzen:
  ```
  ## Messe-Kalender

  | Messe | Datum | Ort | Schwerpunkt | Status |
  | --- | --- | --- | --- | --- |
  | [Messe eintragen] | [Datum] | [Ort] | [SHK/Handwerk/etc.] | Geplant |
  ```

**Betroffene Dateien:**

- `context/current-data.md`

---

## Verbindungen & Abhängigkeiten

### Dateien, die diesen Bereich referenzieren

- `CLAUDE.md` — Muss den neuen Command und die Messe-Outputs widerspiegeln
- `context/current-data.md` — Messe-Kalender und -Ergebnisse tracken
- `context/strategy.md` — Messebesuche unterstützen Priorität 1 (Kundenakquise) und 2 (Sichtbarkeit)

### Nötige Updates für Konsistenz

- CLAUDE.md: Workspace-Struktur und Commands aktualisieren
- current-data.md: Messe-Tracking-Abschnitt ergänzen
- Zukünftig: Messe-Kontakte in eine CRM-Pipeline überführen (spätere Erweiterung)

### Auswirkungen auf bestehende Workflows

- Keine bestehenden Workflows werden verändert
- Der Messe-Workflow ist ein neuer, eigenständiger Workflow
- Er ergänzt die bestehende Webinar-Pipeline (Messe-Kontakte → Webinar-Einladungen als mögliche Synergie)

---

## Validierungs-Checkliste

- [ ] Telegram-Bot erstellt und erreichbar
- [ ] SeaTable-Base eingerichtet mit korrekten Spalten (DSGVO-konform)
- [ ] n8n-Workflow via MCP erstellt und getestet (Text-Nachricht → SeaTable-Eintrag)
- [ ] Sprachnachrichten werden korrekt transkribiert
- [ ] Fotos werden mit Caption erfasst
- [ ] Hashtag-Extraktion funktioniert korrekt
- [ ] Bestätigungsnachricht kommt zurück
- [ ] Bot-Commands (`/messe`, `/status`, `/hilfe`) funktionieren
- [ ] Alle Reference-Dateien erstellt und vollständig
- [ ] `/messe-auswertung` Command erstellt und funktionsfähig
- [ ] Output-Verzeichnisstruktur angelegt
- [ ] CLAUDE.md aktualisiert
- [ ] current-data.md um Messe-Kalender ergänzt
- [ ] End-to-End-Test: 5 Test-Nachrichten → Auswertung → Aktionsplan

---

## Erfolgskriterien

Die Implementierung ist abgeschlossen, wenn:

1. Mechthild auf einer Messe per Telegram Eindrücke in unter 10 Sekunden pro Nachricht erfassen kann
2. Alle Nachrichten automatisch kategorisiert und in SeaTable gespeichert werden (DSGVO-konform)
3. Nach der Messe mit `/messe-auswertung` eine vollständige, strukturierte Zusammenfassung mit priorisierten Marketing-Aktionen erstellt wird
4. Der gesamte Prozess dokumentiert ist und ohne technisches Wissen wiederholt werden kann

---

## Notizen

### Mögliche Erweiterungen (nicht Teil dieses Plans)

- **Automatische LinkedIn-Posts:** Aus #trend und #pain Einträgen automatisch Post-Entwürfe generieren
- **CRM-Integration:** Kontakte direkt in ein CRM (z.B. Brevo) überführen
- **Messe-Dashboard:** Live-Übersicht der erfassten Einträge während der Messe (Simple Webseite oder Notion)
- **Automatische Webinar-Einladungen:** Messe-Kontakte direkt in Brevo-Webinar-Liste aufnehmen
- **Foto-OCR:** Visitenkarten automatisch erfassen und als Kontakt anlegen
- **Sentiment-Analyse:** Stimmung der Pain Points automatisch bewerten

### Abhängigkeiten von Dritten

- Telegram Bot API (kostenlos)
- n8n-Instanz (self-hosted auf Hostinger, bereits vorhanden)
- SeaTable (Free-Tier: kostenlos, EU-Server, DSGVO-konform)
- OpenAI Whisper API oder Groq (für Sprachtranskription, geringe Kosten)
- OpenAI/Claude API (für KI-Zusammenfassung, optional — kann auch komplett über Claude Workspace laufen)

### Bereits vorhandene Infrastruktur

- n8n-Server: `n8n.srv1159226.hstgr.cloud` (Hostinger, self-hosted)
- n8n MCP-Zugang: konfiguriert (via supergateway)
- Bestehender "Telegram Support" Workflow mit Telegram-Credentials
- Telegram-Bot (aus bestehendem Workflow — prüfen ob wiederverwendbar)

### Kosteneinschätzung

- Telegram Bot: kostenlos
- SeaTable Free-Tier: kostenlos (bis 10.000 Zeilen, 2 GB Speicher)
- Whisper API: ~0,006$/Minute → bei 50 Sprachnachrichten à 30 Sek. = ~0,15$ pro Messe
- n8n: bereits vorhanden (self-hosted auf Hostinger)
- Gesamt pro Messe: unter 1€ variable Kosten
