"""
Setup Follow-ups-Tabelle in SeaTable + Testdaten einfügen
Erstellt: 2026-03-12
"""
import json
import urllib.request

API_TOKEN = "f2cecb26770c4f3d3e5b98f549ba5ab21e0899d0"
DTABLE_UUID = "99f096d0-d82f-40fa-acc3-dcf53458ee65"

# --- Access Token holen ---
req = urllib.request.Request(
    "https://cloud.seatable.io/api/v2.1/dtable/app-access-token/",
    headers={"Authorization": f"Token {API_TOKEN}"}
)
with urllib.request.urlopen(req) as resp:
    token_data = json.loads(resp.read().decode("utf-8"))
    access_token = token_data["access_token"]

# API Gateway v2 (SeaTable Cloud 5.3+)
GW_URL = f"https://cloud.seatable.io/api-gateway/api/v2/dtables/{DTABLE_UUID}"
HEADERS = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

def api_call(path, data=None, method="GET"):
    url = f"{GW_URL}{path}"
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"Error {e.code}: {e.read().decode('utf-8')}")
        raise

# --- Schritt 1: Tabelle erstellen (ohne Single-Select, die werden separat angelegt) ---
print("=== Follow-ups-Tabelle erstellen ===")
result = api_call("/tables/", {
    "table_name": "Follow-ups",
    "columns": [
        {"column_name": "Messe", "column_type": "text"},
        {"column_name": "Kontakt-Name", "column_type": "text"},
        {"column_name": "Firma", "column_type": "text"},
        {"column_name": "E-Mail", "column_type": "text"},
        {"column_name": "Betreff", "column_type": "text"},
        {"column_name": "Nachricht", "column_type": "long-text"},
        {"column_name": "Kanal", "column_type": "text"},
        {"column_name": "Prioritaet", "column_type": "single-select"},
        {"column_name": "Status", "column_type": "single-select"}
    ]
}, method="POST")

table_id = result.get("_id", "unknown")
print(f"Tabelle erstellt! Table-ID: {table_id}")

# Spalten-Keys auslesen
columns = result.get("columns", [])
col_keys = {}
for col in columns:
    col_keys[col["name"]] = col["key"]
    print(f"  {col['name']}: {col['key']}")

print(f"\nSpalten-Keys: {json.dumps(col_keys, ensure_ascii=False)}")

# --- Schritt 2: Testdaten einfügen ---
print("\n=== Testdaten einfügen ===")

# SHK+E Essen Follow-ups
shk_followups = [
    {
        "messe": "SHK+E Essen",
        "name": "Peter Nowak",
        "firma": "Nowak Gebäudetechnik",
        "email": "p.nowak@nowak-gebaeudetechnik.de",
        "betreff": "Unser Gespräch auf der SHK+E — Ersttermin KW13",
        "nachricht": "Hallo Herr Nowak,\n\nvielen Dank für das spannende Gespräch auf der SHK+E in Essen! Ihr Vorhaben, den Angebotsprozess bei Nowak Gebäudetechnik zu digitalisieren, finde ich sehr vielversprechend — gerade bei Ihrer Betriebsgröße lässt sich hier enorm viel Zeit sparen.\n\nWie besprochen melde ich mich für unser Erstgespräch in KW13. Ich schlage vor, dass wir uns 45 Minuten nehmen und drei Punkte anschauen: (1) Ihren aktuellen Angebotsprozess im Detail, (2) die Schnittstellen zwischen HubSpot und Ihren anderen Systemen, und (3) konkrete Quick Wins, die sich schnell umsetzen lassen.\n\nPasst Ihnen Dienstag oder Mittwoch besser? Gerne per Teams oder vor Ort in Dortmund.\n\nHerzliche Grüße\nMechthild Rölfing",
        "kanal": "E-Mail",
        "prioritaet": "Hoch",
        "status": "Offen"
    },
    {
        "messe": "SHK+E Essen",
        "name": "Max Feldmann",
        "firma": "Feldmann Haustechnik GmbH",
        "email": "feldmann@feldmann-haustechnik.de",
        "betreff": "Von der SHK+E: Angebotserstellung in 30 statt 180 Minuten?",
        "nachricht": "Hallo Herr Feldmann,\n\nes hat mich gefreut, Sie auf der SHK+E kennenzulernen! Ihr Problem mit der Angebotserstellung — 2-3 Stunden pro Angebot mit Buderus-Konfigurator und Excel — kenne ich von mehreren SHK-Betrieben.\n\nIch habe eine Idee für ein Mini-Pilotprojekt: In 2 Wochen setzen wir eine Automatisierung auf, die Ihre Konfigurator-Daten direkt ins Angebot übernimmt. Kein Abtippen mehr, deutlich weniger Fehler. Das Risiko ist minimal — wenn es nicht funktioniert, kostet Sie es nur ein Erstgespräch.\n\nHätten Sie nächste Woche 30 Minuten für ein kurzes Telefonat, in dem ich Ihnen den Ansatz zeige?\n\nBeste Grüße\nMechthild Rölfing",
        "kanal": "E-Mail",
        "prioritaet": "Hoch",
        "status": "Offen"
    },
    {
        "messe": "SHK+E Essen",
        "name": "Jürgen Brandt",
        "firma": "SHK-Innung Essen",
        "email": "brandt@shk-innung-essen.de",
        "betreff": "Vortrag beim Digitalisierungs-Stammtisch — ich bin dabei!",
        "nachricht": "Hallo Herr Brandt,\n\nvielen Dank für die Einladung zum Digitalisierungs-Stammtisch der SHK-Innung! Ich sage sehr gerne zu.\n\nAls Thema schlage ich vor: \"KI im Handwerksbüro — was heute schon geht (und was sich wirklich lohnt)\". Ich würde eine Live-Demo einbauen und ganz praktisch zeigen, wie ein KI-Telefonassistent oder eine automatisierte Einsatzplanung im Alltag aussieht. Dazu eine kurze Checkliste zum Mitnehmen.\n\nKönnen Sie mir den genauen Termin im April und den Rahmen (Dauer, Teilnehmerzahl, Technik) durchgeben? Dann bereite ich alles passend vor.\n\nHerzliche Grüße\nMechthild Rölfing",
        "kanal": "E-Mail",
        "prioritaet": "Hoch",
        "status": "Offen"
    },
    {
        "messe": "SHK+E Essen",
        "name": "Sandra Kiefer",
        "firma": "Kiefer Sanitär & Bad",
        "email": "s.kiefer@kiefer-sanitaer.de",
        "betreff": "Schluss mit WhatsApp-Chaos bei der Einsatzplanung?",
        "nachricht": "Hallo Frau Kiefer,\n\nunser Gespräch auf der SHK+E hat mich nicht losgelassen — 6 Monteure per WhatsApp und Zettel zu koordinieren, das kenne ich von mehreren Betrieben, und ich weiß, wie frustrierend das ist.\n\nIch arbeite gerade an einer Lösung genau für dieses Problem: eine digitale Einsatzplanung, die morgens automatisch den Tagesplan erstellt und bei Umplanungen alle Betroffenen sofort informiert. Kein WhatsApp-Ping-Pong mehr.\n\nDarf ich Ihnen in einem kurzen 30-Minuten-Gespräch zeigen, wie das aussehen könnte? Völlig unverbindlich — ich möchte vor allem verstehen, wo bei Ihnen die größten Zeitfresser stecken.\n\nBeste Grüße\nMechthild Rölfing",
        "kanal": "E-Mail",
        "prioritaet": "Hoch",
        "status": "Offen"
    },
    {
        "messe": "SHK+E Essen",
        "name": "Lisa Hartmann",
        "firma": "Viessmann Digital",
        "email": "lisa.hartmann@viessmann.com",
        "betreff": "Integrationspartnerschaft Viessmann-Plattform — nächste Schritte?",
        "nachricht": "Hallo Frau Hartmann,\n\ndanke für das interessante Gespräch auf der SHK+E! Die Idee, Workflow-Automatisierung als Ergänzung zur Viessmann-Plattform für Fachhandwerker anzubieten, finde ich spannend.\n\nKonkret könnte ich mir vorstellen, dass wir Integrationen zwischen der Viessmann-Plattform und gängigen Handwerker-Tools (ERP, Baustellendoku, Terminplanung) automatisieren — das ist genau mein Spezialgebiet.\n\nSollen wir in den nächsten 2 Wochen einen kurzen Call machen, um die Möglichkeiten auszuloten?\n\nHerzliche Grüße\nMechthild Rölfing",
        "kanal": "E-Mail",
        "prioritaet": "Mittel",
        "status": "Offen"
    }
]

# Hannover Messe Follow-ups (aus Testdaten)
hannover_followups = [
    {
        "messe": "Hannover Messe",
        "name": "Dr. Thomas Weber",
        "firma": "Siemens Digital Industries",
        "email": "thomas.weber@siemens.com",
        "betreff": "KI-Automatisierung für Fertigungsbetriebe — Ihr Partnerprogramm",
        "nachricht": "Hallo Herr Dr. Weber,\n\nvielen Dank für das aufschlussreiche Gespräch auf der Hannover Messe! Die Möglichkeiten der Siemens Industrial Edge Plattform in Kombination mit KI-gestützter Automatisierung finde ich sehr spannend.\n\nAls KI-Beraterin für den Mittelstand sehe ich großes Potenzial, die Siemens-Lösungen als Integrationspartnerin in Fertigungs-KMU zu bringen. Viele meiner Kunden suchen genau diese Brücke zwischen Shopfloor und digitaler Welt.\n\nKönnten wir in den nächsten Wochen über das Partnerprogramm sprechen?\n\nHerzliche Grüße\nMechthild Rölfing",
        "kanal": "E-Mail",
        "prioritaet": "Mittel",
        "status": "Offen"
    },
    {
        "messe": "Hannover Messe",
        "name": "Michael Krause",
        "firma": "Krause Metallbau GmbH",
        "email": "m.krause@krause-metallbau.de",
        "betreff": "Ihr Qualitätsproblem bei Schweißnähten — KI-Lösung in 4 Wochen?",
        "nachricht": "Hallo Herr Krause,\n\nunser Gespräch auf der Hannover Messe hat mir gezeigt, dass wir Ihnen schnell helfen können. Die 8% Ausschussrate bei den Schweißnähten ist ein Problem, das KI-basierte Qualitätskontrolle direkt adressieren kann.\n\nIch schlage ein Pilotprojekt vor: In 4 Wochen setzen wir eine Kamera + KI-Lösung an einer Ihrer Schweißstationen auf. Sie sehen sofort, ob und wie viel Ausschuss reduziert werden kann.\n\nHätten Sie nächste Woche 45 Minuten für ein Erstgespräch?\n\nBeste Grüße\nMechthild Rölfing",
        "kanal": "E-Mail",
        "prioritaet": "Hoch",
        "status": "Offen"
    },
    {
        "messe": "Hannover Messe",
        "name": "Anna Chen",
        "firma": "Bosch Connected Industry",
        "email": "anna.chen@bosch.com",
        "betreff": "Nexeed-Integration für Mittelständler — Zusammenarbeit?",
        "nachricht": "Hallo Frau Chen,\n\ndanke für die spannende Demo der Nexeed-Plattform auf der Hannover Messe! Besonders die Predictive-Maintenance-Module haben mich beeindruckt.\n\nAls Beraterin sehe ich den Bedarf bei KMU, die solche Lösungen wollen, aber nicht die interne IT haben. Ich könnte als Implementierungspartnerin die Brücke bauen.\n\nSollen wir einen kurzen Call machen, um die Möglichkeiten zu besprechen?\n\nHerzliche Grüße\nMechthild Rölfing",
        "kanal": "LinkedIn",
        "prioritaet": "Mittel",
        "status": "Offen"
    },
    {
        "messe": "Hannover Messe",
        "name": "Jens Hoffmann",
        "firma": "Hoffmann Präzisionstechnik",
        "email": "j.hoffmann@hoffmann-praezision.de",
        "betreff": "Fachkräftemangel lösen mit KI-Assistenten?",
        "nachricht": "Hallo Herr Hoffmann,\n\nIhr Fachkräfteproblem auf der Hannover Messe hat mich nachdenklich gemacht. Drei offene Stellen seit Monaten — das bremst Ihr Wachstum enorm.\n\nKI kann zwar keine Fachkräfte ersetzen, aber repetitive Aufgaben automatisieren: Angebotserstellung, Auftragserfassung, Qualitätsdokumentation. So hat Ihr bestehendes Team mehr Kapazität für die wertschöpfende Arbeit.\n\nDarf ich Ihnen in 30 Minuten zeigen, wo bei Ihnen die größten Automatisierungspotenziale liegen?\n\nBeste Grüße\nMechthild Rölfing",
        "kanal": "E-Mail",
        "prioritaet": "Hoch",
        "status": "Offen"
    }
]

# Zeilen-Daten in SeaTable-Format umwandeln
def to_row(fu, col_keys):
    row = {}
    row[col_keys.get("Messe", "0000")] = fu["messe"]
    row[col_keys.get("Kontakt-Name", "")] = fu["name"]
    row[col_keys.get("Firma", "")] = fu["firma"]
    row[col_keys.get("E-Mail", "")] = fu["email"]
    row[col_keys.get("Betreff", "")] = fu["betreff"]
    row[col_keys.get("Nachricht", "")] = fu["nachricht"]
    row[col_keys.get("Kanal", "")] = fu["kanal"]
    row[col_keys.get("Prioritaet", "")] = fu["prioritaet"]
    row[col_keys.get("Status", "")] = fu["status"]
    return row

# Alle Follow-ups einfügen
all_followups = shk_followups + hannover_followups
rows_to_insert = [to_row(fu, col_keys) for fu in all_followups]

# Batch-Insert (max 1000 pro Request)
print(f"\nFüge {len(rows_to_insert)} Follow-ups ein...")
result = api_call(f"/rows/", {
    "table_id": table_id,
    "rows": rows_to_insert
}, method="POST")

inserted = result.get("inserted_row_count", 0) if isinstance(result, dict) else len(result)
print(f"Eingefügt: {inserted} Zeilen")

print(f"\n=== FERTIG ===")
print(f"Follow-ups Table-ID: {table_id}")
print(f"Spalten-Keys:")
for name, key in col_keys.items():
    print(f"  {name}: {key}")
print(f"\nBitte die Table-ID und Spalten-Keys in .env.dashboard und CLAUDE.md notieren!")
