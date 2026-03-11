# Messe-Capture-Anleitung

> Kurzanleitung für die strukturierte Erfassung von Messeeindrücken per Telegram-Bot.
> Vor jeder Messe einmal durchlesen — dauert 2 Minuten.

---

## Vor der Messe

### Checkliste

- [ ] Telegram-Bot öffnen (Suche: `@transformwerk_messe_bot` oder wie konfiguriert)
- [ ] `/start` senden, um sicherzugehen, dass der Bot aktiv ist
- [ ] `/messe IFH Nürnberg 2026` senden (Messe-Name setzen)
- [ ] Testnachricht senden: `#test Alles funktioniert`
- [ ] Bestätigung abwarten

### Handy vorbereiten

- Telegram-Bot als Favorit/Pin markieren für schnellen Zugriff
- Sprachnachrichten-Funktion testen
- Handy geladen, mobile Daten aktiv

---

## Während der Messe: So erfasst du Eindrücke

### Grundprinzip

**Eine Nachricht = ein Gedanke.** Starte jede Nachricht mit einem Hashtag.

### Hashtag-Übersicht

| Hashtag | Wofür | Beispiel |
|---|---|---|
| `#kontakt` | Personen/Firmen, die du triffst | `#kontakt Max Müller, Firma XYZ, Heizungsbauer, interessiert an Digitalisierung` |
| `#trend` | Branchentrends, die dir auffallen | `#trend Viele Aussteller zeigen KI-Telefonassistenten` |
| `#pain` | Probleme, die Handwerker ansprechen | `#pain Doppelte Dateneingabe zwischen Büro und Baustelle` |
| `#idee` | Eigene Ideen für Content/Angebote | `#idee LinkedIn-Post über Top-3 Trends schreiben` |
| `#wettbewerb` | Wettbewerber und deren Angebote | `#wettbewerb Firma ABC bietet ähnliches, aber nur ab 100 MA` |
| `#foto` | Fotos mit Kontext | Foto senden + Caption: `#foto Interessanter Workflow am Stand von XYZ` |
| `#zitat` | Aussagen, die dir auffallen | `#zitat "Wir tippen alles dreimal ab" — Heizungsbauer aus Köln` |
| `#produkt` | Interessante Tools/Produkte | `#produkt Sintratec zeigt neues Planungstool für SHK` |

### Kein Hashtag?

Wenn du keinen Hashtag verwendest, wird die Nachricht als `notiz` gespeichert. Funktioniert auch — aber Hashtags machen die spätere Auswertung viel besser.

---

## Tipps für effektive Erfassung

### Textnachrichten

- **Kurz und knapp** — Stichpunkte reichen, keine ganzen Sätze nötig
- **Ein Gedanke pro Nachricht** — nicht mehrere Themen mischen
- **Kontext mitgeben** — "Heizungsbauer, 50 MA, aus Köln" statt nur "netter Typ"
- **Bei Kontakten:** Name, Firma, Branche, Größe, Interesse, Kontaktdaten

### Sprachnachrichten

- Ideal, wenn Tippen zu langsam ist (z.B. zwischen zwei Ständen)
- **Hashtag am Anfang ansagen:** "Hashtag Kontakt — Gerade mit Max Müller von XYZ gesprochen..."
- Deutlich sprechen, kurze Sätze
- Hintergrundgeräusche auf Messen sind normal — die Transkription kommt damit klar

### Fotos

- Foto senden **mit Caption** (das Textfeld unter dem Foto)
- Caption mit Hashtag starten: `#foto Stand von XYZ mit interessantem Workflow`
- Visitenkarten fotografieren mit `#kontakt` als Caption
- Produktdemos, Standaufbauten, Preislisten — alles festhalten

---

## Bot-Commands

| Command | Funktion |
|---|---|
| `/start` | Bot starten, Begrüßung |
| `/messe [Name]` | Aktive Messe setzen (z.B. `/messe IFH Nürnberg 2026`) |
| `/status` | Zeigt aktuelle Messe + Anzahl Einträge pro Kategorie |
| `/hilfe` | Zeigt Hashtag-Übersicht |
| `/export` | Löst Zusammenfassung aus (nach der Messe) |

---

## Nach der Messe

1. Im Bot `/status` prüfen — wie viele Einträge hast du erfasst?
2. Optional: Noch fehlende Eindrücke nachtragen (geht auch nach der Messe)
3. Im Claude-Workspace `/messe-auswertung` ausführen für die vollständige Analyse
4. Follow-ups innerhalb von 24-48h versenden

---

## Faustregel

> Lieber eine Nachricht zu viel als zu wenig. Die KI-Auswertung kann filtern — aber was nicht erfasst ist, ist verloren.
