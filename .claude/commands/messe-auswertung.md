# Messe-Auswertung

> Rohdaten eines Messebesuchs auswerten und strukturierte Outputs erstellen.

## Variablen

messe_name: $ARGUMENTS (Name der Messe, z.B. "IFH Nürnberg 2026")

---

## Anweisungen

### Schritt 1: Kontext laden

Lies die folgenden Dateien, um die Auswertung korrekt durchzuführen:

- `reference/messe-kategorien.md` — Kategorie-Definitionen
- `reference/messe-ki-prompts.md` — Prompts für die Auswertung
- `reference/messe-auswertung-template.md` — Template für die Zusammenfassung
- `reference/messe-marketing-aktionen-template.md` — Template für den Aktionsplan
- `context/strategy.md` — Strategische Prioritäten als Bewertungsrahmen

### Schritt 2: Rohdaten einlesen

Prüfe, ob Rohdaten vorhanden sind:

1. **Als Datei:** `outputs/messen/[messe-name]/rohdaten.md`
2. **Im Chat:** Der User kann Rohdaten direkt im Chat einfügen (Copy-Paste aus SeaTable)

Falls keine Rohdaten gefunden werden, frage den User danach.

### Schritt 3: Messe-Ordner anlegen

Erstelle den Ordner `outputs/messen/[datum]-[messe-name-slug]/` falls noch nicht vorhanden.

Beispiel: `outputs/messen/2026-03-15-ifh-nuernberg/`

### Schritt 4: Zusammenfassung erstellen

Wende Prompt 1 (Messe-Zusammenfassung) aus `reference/messe-ki-prompts.md` auf die Rohdaten an.

Schreibe das Ergebnis in: `outputs/messen/[ordner]/auswertung.md`

Verwende das Template aus `reference/messe-auswertung-template.md` als Grundstruktur.

### Schritt 5: Marketing-Aktionsplan ableiten

Wende Prompt 2 (Marketing-Aktionsplan) aus `reference/messe-ki-prompts.md` auf die Zusammenfassung an.

Schreibe das Ergebnis in: `outputs/messen/[ordner]/marketing-aktionen.md`

Verwende das Template aus `reference/messe-marketing-aktionen-template.md` als Grundstruktur.

Beachte die strategischen Prioritäten aus `context/strategy.md`:
- Kundenakquise
- Referenzprojekte
- Sichtbarkeit
- Partnerschaften

### Schritt 6: Follow-up-Nachrichten generieren

Wende Prompt 3 (Kontakt-Follow-up-Generator) aus `reference/messe-ki-prompts.md` auf alle #kontakt-Einträge an.

Schreibe das Ergebnis in: `outputs/messen/[ordner]/follow-ups.md`

### Schritt 6b: Follow-ups in SeaTable einfügen

Füge die generierten Follow-ups als Einzelzeilen in die SeaTable-Tabelle "Follow-ups" (Table-ID: `Nid7`) ein.

Erstelle ein Python-Script oder nutze die SeaTable API direkt:
- **API Gateway:** `https://cloud.seatable.io/api-gateway/api/v2/dtables/{uuid}/rows/`
- **Methode:** POST mit `table_name: "Follow-ups"`
- **Felder pro Zeile:** Messe, Kontakt-Name, Firma, E-Mail, Betreff, Nachricht, Kanal, Prioritaet, Status (initial "Offen")
- **API-Token:** Aus `.env` laden (`Seatable API Key`)

Beispiel-Zeile:
```json
{
  "Messe": "IFH Nürnberg 2026",
  "Kontakt-Name": "Max Mustermann",
  "Firma": "Mustermann GmbH",
  "E-Mail": "max@mustermann.de",
  "Betreff": "Unser Gespräch auf der IFH",
  "Nachricht": "Hallo Herr Mustermann, ...",
  "Kanal": "E-Mail",
  "Prioritaet": "Hoch",
  "Status": "Offen"
}
```

### Schritt 7: Zusammenfassung an den User

Liefere dem User:

1. **Executive Summary** der Messe (3-5 Sätze)
2. **Anzahl** erfasster Einträge pro Kategorie
3. **Top-3 Sofort-Aktionen** aus dem Aktionsplan
4. **Hinweis** auf die erstellten Dateien im Output-Ordner
5. **Empfehlung** für die nächsten Schritte

### Schritt 8: current-data.md aktualisieren

Aktualisiere den Messe-Kalender in `context/current-data.md`:
- Status der Messe auf "Ausgewertet" setzen
- Anzahl erfasster Einträge notieren
