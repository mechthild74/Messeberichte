# Aktuelle Daten — Messe-App

---

## Messe-Kalender

| Messe | Datum | Ort | Schwerpunkt | Status |
| --- | --- | --- | --- | --- |
| SHK+E Essen | 17.–20. März 2026 | Messe Essen | Sanitär, Heizung, Klima, Elektro | Testdaten vorhanden (31 Einträge, 5 Kontakte) |
| Hannover Messe | 20.–24. April 2026 | Deutsche Messe Hannover | Industrie, Fertigung, Digital | Testdaten vorhanden (23 Einträge, 4 Kontakte) |

_Messen hier eintragen, sobald Termine feststehen. Nach Auswertung Status auf "Ausgewertet" setzen._

## Infrastruktur-Status

| Komponente | Status | Details |
| --- | --- | --- |
| Telegram-Bot | Aktiv | Credentials in n8n, Bot-Commands (/messe, /status, /hilfe) |
| n8n-Workflow "Messe Capture" | Aktiv | ID: `kMA6sVg1x2KkITCo` — Text, Sprache, Foto, Commands |
| SeaTable "Messe-Capture" | Aktiv | Einträge (ID: `ZtiH`) + Reports (ID: `G7m3`) + Follow-ups (ID: `Nid7`) |
| n8n-Workflow "Follow-up Draft" | Erstellt | ID: `SrRcsrSPY1gHRcFB` — muss noch aktiviert werden, IMAP-Credentials fehlen |
| Dashboard | Deployed | eventdashboard.transformwerk.digital — mit Follow-ups-Sektion |
| `/messe-auswertung` | Funktioniert | Erstellt Auswertung, Marketing-Aktionen, Follow-ups + SeaTable-Insert |

## Offene Punkte

- Testdaten in SeaTable löschen vor echter Messe (17. März)
- Foto-Pfad im n8n-Workflow testen
- n8n Follow-up Draft Workflow aktivieren + IMAP-Credentials eintragen
- Drafts-Ordnername ermitteln (IMAP LIST — typisch: "Drafts", "INBOX.Drafts", "Entwürfe")
- Dashboard-Dateien auf Hostinger hochladen (api.php, app.js, style.css, index.html) + Hard Refresh (Ctrl+Shift+R)

---

_Regelmäßig aktualisieren._
