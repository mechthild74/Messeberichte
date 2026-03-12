# Plan: Follow-up E-Mail-Drafts automatisieren

**Erstellt:** 2026-03-12
**Status:** Implementiert
**Anforderung:** Neue SeaTable-Tabelle für strukturierte Follow-ups, Dashboard-Button "Draft erstellen", n8n-Webhook der per IMAP APPEND einen Entwurf in den Outlook-Drafts-Ordner legt

---

## Überblick

### Was dieser Plan erreicht

Nach einer Messe-Auswertung werden die generierten Follow-up-Nachrichten als einzelne Zeilen in einer neuen SeaTable-Tabelle gespeichert. Im Dashboard erscheint pro Kontakt ein "Draft erstellen"-Button. Ein Klick darauf triggert einen n8n-Webhook, der die E-Mail per IMAP APPEND als Entwurf in den Outlook-Drafts-Ordner legt. Der Status in SeaTable wird auf "Entwurf" aktualisiert.

### Warum das wichtig ist

Follow-up-Nachrichten nach Messen sind zeitkritisch (24-48h). Aktuell muss jede E-Mail manuell erstellt werden — Betreff und Text aus der Auswertung abtippen. Mit dieser Automatisierung reduziert sich der Aufwand pro Follow-up auf einen Klick + kurze Prüfung in Outlook.

---

## Aktueller Zustand

### Relevante bestehende Struktur

| Datei/Komponente | Zweck |
| --- | --- |
| `outputs/messen/*/follow-ups.md` | Follow-up-Nachrichten als Markdown (unstrukturiert) |
| `dashboard/reports/` (SeaTable G7m3) | Follow-ups als HTML-Blob in Reports-Tabelle |
| `.claude/commands/messe-auswertung.md` | Generiert Follow-ups in Schritt 6 |
| `reference/messe-ki-prompts.md` | Prompt 3 = Follow-up-Generator |
| `dashboard/app.js` | Zeigt Follow-ups nur als Report im Modal |
| `dashboard/api.php` | PHP-Proxy für SeaTable-Zugriff |
| n8n Workflow `kMA6sVg1x2KkITCo` | Messe-Capture (nicht relevant, aber Referenz für n8n-Patterns) |

### Lücken oder Probleme, die adressiert werden

- Follow-ups existieren nur als Fließtext (Markdown/HTML) — nicht als einzelne, adressierbare Datensätze
- Kein Weg, direkt aus dem Dashboard eine Aktion auszulösen
- E-Mails müssen komplett manuell erstellt werden (Copy-Paste aus Auswertung)
- Kein Tracking, welche Follow-ups schon versendet wurden

---

## Vorgeschlagene Änderungen

### Zusammenfassung der Änderungen

1. Neue SeaTable-Tabelle "Follow-ups" mit strukturierten Feldern
2. Neuer n8n-Workflow "Follow-up Draft" (Webhook → IMAP APPEND → SeaTable Status-Update)
3. Dashboard: Neue Follow-ups-Sektion mit "Draft erstellen"-Buttons
4. API-Proxy: Neue Endpoints für Follow-ups und Webhook-Trigger
5. `/messe-auswertung` anpassen: Follow-ups auch als Einzelzeilen in SeaTable schreiben

### Neue Dateien erstellen

| Dateipfad | Zweck |
| --- | --- |
| `scripts/setup-followups-table.py` | SeaTable-Tabelle "Follow-ups" anlegen |
| `scripts/create-followup-draft-workflow.py` | n8n-Workflow für E-Mail-Draft-Erstellung |

### Zu ändernde Dateien

| Dateipfad | Änderungen |
| --- | --- |
| `dashboard/app.js` | Neue Sektion Follow-ups mit Buttons, Webhook-Aufruf |
| `dashboard/index.html` | HTML für Follow-ups-Sektion |
| `dashboard/style.css` | Styling für Follow-up-Karten und Buttons |
| `dashboard/api.php` | Neue Endpoints: `action=followups`, `action=create-draft` |
| `.claude/commands/messe-auswertung.md` | Schritt 6 erweitern: Follow-ups in SeaTable schreiben |
| `CLAUDE.md` | Neue Tabelle und Workflow dokumentieren |
| `context/current-data.md` | Infrastruktur-Status aktualisieren |

---

## Design-Entscheidungen

### Getroffene Schlüsselentscheidungen

1. **IMAP APPEND statt SMTP:** User will Entwürfe prüfen vor dem Senden — IMAP APPEND legt die Mail direkt in den Drafts-Ordner, SMTP würde sofort senden.

2. **Separate SeaTable-Tabelle statt Spalten in Einträge-Tabelle:** Follow-ups sind ein eigener Datentyp mit eigenem Lebenszyklus (Offen → Entwurf → Gesendet). Eine eigene Tabelle hält das Schema sauber.

3. **n8n-Webhook statt direkter IMAP-Aufruf aus PHP:** n8n hat bereits Credential-Management und Node-basierte Fehlerbehandlung. Der Webhook ist ein einfacher HTTP-Aufruf, der von überall getriggert werden kann.

4. **Dashboard-Button pro Kontakt statt Batch-Aktion:** Jeder Follow-up kann individuell angepasst werden. User sieht Status pro Kontakt.

5. **Token-Auth auf Webhook:** Der n8n-Webhook bekommt einen Header-Token, damit nicht jeder den Webhook aufrufen kann.

### Betrachtete Alternativen

- **Microsoft Graph API:** Sauberer für Outlook-Drafts, aber erfordert Azure AD App Registration + OAuth. Zu komplex für ein Hostinger-Mailkonto.
- **SMTP mit "Nicht senden"-Flag:** SMTP hat kein Draft-Konzept. Nicht möglich.
- **SeaTable Button-Spalte:** SeaTable hat eigene Buttons, aber die können keine externen Webhooks triggern.

### Offene Fragen

1. **E-Mail-Adresse des Hostinger-Kontos:** Welche Absender-Adresse wird verwendet? (z.B. mechthild@transformwerk.digital)
2. **IMAP-Zugangsdaten:** Host, Port, User, Passwort für das Hostinger-Mailkonto (werden in n8n als Credential gespeichert)
3. **Drafts-Ordnername:** Bei IMAP heißt der Entwürfe-Ordner je nach Konfiguration "Drafts", "Entwürfe" oder "INBOX.Drafts". Muss getestet werden.

---

## Schritt-für-Schritt-Aufgaben

### Schritt 1: SeaTable-Tabelle "Follow-ups" anlegen

Erstelle eine neue Tabelle in der bestehenden SeaTable-Base mit folgenden Spalten:

| Spalte | Typ | Beschreibung |
| --- | --- | --- |
| Messe | Text | Name der Messe |
| Kontakt-Name | Text | Voller Name des Kontakts |
| Firma | Text | Firmenname |
| E-Mail | Text | E-Mail-Adresse (falls bekannt) |
| Betreff | Text | E-Mail-Betreff |
| Nachricht | Long Text | E-Mail-Body (Plain Text) |
| Kanal | Text | E-Mail, LinkedIn, Telefon |
| Prioritaet | Single Select | Hoch, Mittel, Niedrig |
| Status | Single Select | Offen, Entwurf, Gesendet |

**Aktionen:**
- Python-Script `scripts/setup-followups-table.py` erstellen und ausführen
- Tabellen-ID und Spalten-Keys dokumentieren

**Betroffene Dateien:**
- `scripts/setup-followups-table.py` (neu)

---

### Schritt 2: Bestehende Follow-up-Testdaten einfügen

Aus den bestehenden Follow-ups (SHK+E Essen + Hannover Messe) die strukturierten Daten extrahieren und als Einzelzeilen in die neue Tabelle einfügen.

**Aktionen:**
- Script schreiben das die Follow-up-Daten parsed und in SeaTable einfügt
- Für jeden Kontakt eine Zeile mit Betreff, Nachricht, etc.
- Status initial auf "Offen"

**Betroffene Dateien:**
- `scripts/setup-followups-table.py` (erweitern)

---

### Schritt 3: n8n-Workflow "Follow-up Draft" erstellen

Neuer n8n-Workflow mit diesen Nodes:

1. **Webhook-Trigger:** Empfängt POST-Request mit Follow-up-Daten (kontaktName, firma, email, betreff, nachricht, rowId)
2. **Code-Node "E-Mail bauen":** Baut RFC 822 E-Mail-String (From, To, Subject, Body, Date, Message-ID)
3. **IMAP-Node oder Code-Node:** Verbindet per IMAP zum Hostinger-Mailserver und führt APPEND auf den Drafts-Ordner aus
4. **SeaTable-Update:** Setzt den Status der Follow-up-Zeile auf "Entwurf"
5. **Respond to Webhook:** Gibt Erfolg/Fehler zurück

**Hinweis:** n8n hat keinen nativen "IMAP APPEND"-Node. Zwei Optionen:
- **Option A:** Code-Node mit `nodemailer` + IMAP-Library (n8n hat `imap` als built-in)
- **Option B:** Code-Node der direkt per `net`/`tls` eine IMAP-Verbindung aufbaut

Empfehlung: Option A (Code-Node), da einfacher und robuster.

**Aktionen:**
- Script `scripts/create-followup-draft-workflow.py` erstellen
- n8n-Workflow per REST API anlegen
- IMAP-Credentials in n8n anlegen (manuell durch User)
- Workflow testen mit einem Beispiel-Follow-up

**Betroffene Dateien:**
- `scripts/create-followup-draft-workflow.py` (neu)

---

### Schritt 4: API-Proxy erweitern

Neue Endpoints in `api.php`:

- `action=followups&messe=Name` — Alle Follow-ups einer Messe aus SeaTable laden
- `action=create-draft` (POST) — Webhook an n8n triggern mit Follow-up-Daten

**Aktionen:**
- Neuen FOLLOWUPS_TABLE_ID in PHP-Config aufnehmen
- Endpoint `followups` implementiert: Zeilen aus Follow-ups-Tabelle laden
- Endpoint `create-draft` implementiert: POST an n8n-Webhook weiterleiten, Ergebnis zurückgeben

**Betroffene Dateien:**
- `dashboard/api.php`

---

### Schritt 5: Dashboard Follow-ups-Sektion

Neue Sektion im Dashboard zwischen "Zitate" und "Reports":

**HTML-Struktur:**
- Überschrift "Follow-ups" mit Badge (Anzahl)
- Karten pro Kontakt: Name, Firma, Betreff, Priorität, Status-Badge
- Button "Draft erstellen" (nur wenn Status = "Offen" und E-Mail vorhanden)
- Button "Gesendet" zum manuellen Markieren nach Versand
- Visuelles Feedback nach Draft-Erstellung (Button wird grün, Text ändert zu "Entwurf erstellt")

**JavaScript:**
- `fetchFollowups(messeName)` — Daten von API laden
- `renderFollowups(entries)` — Karten rendern
- `createDraft(rowId, data)` — API-Call an `create-draft` Endpoint
- `markSent(rowId)` — Status auf "Gesendet" setzen

**Aktionen:**
- HTML-Sektion in index.html einfügen
- CSS für Follow-up-Karten in style.css
- JS-Funktionen in app.js
- In `loadMesse()` den Aufruf `renderFollowups()` ergänzen

**Betroffene Dateien:**
- `dashboard/index.html`
- `dashboard/style.css`
- `dashboard/app.js`

---

### Schritt 6: `/messe-auswertung` erweitern

Schritt 6 des Commands anpassen: Nach Generierung der Follow-up-Nachrichten diese auch als Einzelzeilen in die SeaTable Follow-ups-Tabelle schreiben.

**Aktionen:**
- In der Command-Datei Schritt 6 um SeaTable-Insert erweitern
- Claude soll nach Generierung der follow-ups.md die Daten strukturiert extrahieren und per API einfügen
- Alternativ: Hinweis an User, dass Follow-ups manuell importiert werden können

**Betroffene Dateien:**
- `.claude/commands/messe-auswertung.md`

---

### Schritt 7: Dokumentation aktualisieren

**Aktionen:**
- `CLAUDE.md`: Neue Tabelle, neuen Workflow, neue Dashboard-Sektion dokumentieren
- `context/current-data.md`: Infrastruktur-Status aktualisieren
- Memory-Datei aktualisieren mit neuen Table-IDs und Workflow-ID

**Betroffene Dateien:**
- `CLAUDE.md`
- `context/current-data.md`

---

### Schritt 8: Testen

**Aktionen:**
- IMAP-Credentials in n8n einrichten (User muss Hostinger-Mail-Zugangsdaten liefern)
- Drafts-Ordnername ermitteln (IMAP LIST-Befehl)
- Einen Test-Draft erstellen über den Dashboard-Button
- Prüfen ob der Entwurf in Outlook erscheint
- Status-Update in SeaTable verifizieren

**Betroffene Dateien:**
- Keine (manueller Test)

---

## Verbindungen & Abhängigkeiten

### Dateien, die diesen Bereich referenzieren

- `CLAUDE.md` — System-Architektur-Abschnitt
- `context/current-data.md` — Infrastruktur-Status
- `.claude/commands/messe-auswertung.md` — Schritt 6 Follow-ups

### Nötige Updates für Konsistenz

- SeaTable-Spalten-Keys der neuen Tabelle in CLAUDE.md dokumentieren
- n8n-Workflow-ID in CLAUDE.md und Memory dokumentieren
- `.env.dashboard` um n8n-Webhook-URL erweitern

### Auswirkungen auf bestehende Workflows

- `/messe-auswertung` wird erweitert (Schritt 6), bestehende Funktionalität bleibt erhalten
- Dashboard bekommt neue Sektion, bestehende Sektionen bleiben unverändert
- Reports-Tabelle und Einträge-Tabelle werden nicht verändert

---

## Validierungs-Checkliste

- [ ] SeaTable-Tabelle "Follow-ups" existiert mit korrekten Spalten
- [ ] Testdaten (SHK+E + Hannover) als Einzelzeilen in der Tabelle
- [ ] n8n-Workflow "Follow-up Draft" aktiv und erreichbar per Webhook
- [ ] IMAP APPEND legt Entwurf in Outlook-Drafts-Ordner
- [ ] Dashboard zeigt Follow-ups pro Messe mit Status
- [ ] "Draft erstellen"-Button triggert Webhook und aktualisiert Status
- [ ] api.php Endpoints `followups` und `create-draft` funktionieren mit Token-Auth
- [ ] CLAUDE.md und current-data.md aktualisiert
- [ ] Hostinger-Deploy: Dateien hochladen + Hard Refresh (Ctrl+Shift+R)

---

## Erfolgskriterien

Die Implementierung ist abgeschlossen, wenn:

1. Im Dashboard sind alle Follow-ups einer Messe als Karten sichtbar mit Name, Firma, Betreff, Priorität und Status
2. Ein Klick auf "Draft erstellen" legt einen E-Mail-Entwurf im Outlook-Drafts-Ordner an
3. Der Status in SeaTable wird automatisch auf "Entwurf" gesetzt
4. Der gesamte Flow funktioniert: Dashboard → api.php → n8n Webhook → IMAP APPEND → Outlook

---

## Notizen

- **IMAP-Credentials:** Müssen manuell in n8n eingerichtet werden. User braucht: Host (z.B. imap.hostinger.com), Port (993), Username (E-Mail), Passwort.
- **Drafts-Ordner:** Der Name variiert je nach Mailserver-Konfiguration. Muss per IMAP LIST ermittelt werden. Typisch: "Drafts", "INBOX.Drafts", "Entwürfe".
- **Zukunft:** Schritt "Gesendet"-Markierung könnte auch automatisiert werden (n8n prüft ob Mail im Sent-Ordner liegt).
- **Zukunft:** LinkedIn-Follow-ups könnten als Browser-Tab geöffnet werden statt als Mail-Draft.
