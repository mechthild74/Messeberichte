"""Insert Follow-up test data into SeaTable"""
import json
import urllib.request

API_TOKEN = "f2cecb26770c4f3d3e5b98f549ba5ab21e0899d0"
DTABLE_UUID = "99f096d0-d82f-40fa-acc3-dcf53458ee65"

req = urllib.request.Request(
    "https://cloud.seatable.io/api/v2.1/dtable/app-access-token/",
    headers={"Authorization": f"Token {API_TOKEN}"}
)
with urllib.request.urlopen(req) as resp:
    token_data = json.loads(resp.read().decode("utf-8"))
    access_token = token_data["access_token"]

GW_URL = f"https://cloud.seatable.io/api-gateway/api/v2/dtables/{DTABLE_UUID}"
HEADERS = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

def api_post(path, data):
    body = json.dumps(data).encode("utf-8")
    r = urllib.request.Request(f"{GW_URL}{path}", data=body, headers=HEADERS, method="POST")
    with urllib.request.urlopen(r) as resp:
        return json.loads(resp.read().decode("utf-8"))

rows = [
    {
        "Messe": "SHK+E Essen",
        "Kontakt-Name": "Peter Nowak",
        "Firma": "Nowak Gebaeudetechnik",
        "E-Mail": "p.nowak@nowak-gebaeudetechnik.de",
        "Betreff": "Unser Gespraech auf der SHK+E - Ersttermin KW13",
        "Nachricht": "Hallo Herr Nowak,\n\nvielen Dank fuer das spannende Gespraech auf der SHK+E in Essen! Ihr Vorhaben, den Angebotsprozess zu digitalisieren, finde ich sehr vielversprechend.\n\nWie besprochen melde ich mich fuer unser Erstgespraech in KW13.\n\nPasst Ihnen Dienstag oder Mittwoch besser?\n\nHerzliche Gruesse\nMechthild Roelfing",
        "Kanal": "E-Mail",
        "Prioritaet": "Hoch",
        "Status": "Offen"
    },
    {
        "Messe": "SHK+E Essen",
        "Kontakt-Name": "Max Feldmann",
        "Firma": "Feldmann Haustechnik GmbH",
        "E-Mail": "feldmann@feldmann-haustechnik.de",
        "Betreff": "Von der SHK+E: Angebotserstellung in 30 statt 180 Minuten?",
        "Nachricht": "Hallo Herr Feldmann,\n\nes hat mich gefreut, Sie auf der SHK+E kennenzulernen! Ihr Problem mit der Angebotserstellung kenne ich von mehreren SHK-Betrieben.\n\nIch habe eine Idee fuer ein Mini-Pilotprojekt.\n\nHaetten Sie naechste Woche 30 Minuten fuer ein kurzes Telefonat?\n\nBeste Gruesse\nMechthild Roelfing",
        "Kanal": "E-Mail",
        "Prioritaet": "Hoch",
        "Status": "Offen"
    },
    {
        "Messe": "SHK+E Essen",
        "Kontakt-Name": "Juergen Brandt",
        "Firma": "SHK-Innung Essen",
        "E-Mail": "brandt@shk-innung-essen.de",
        "Betreff": "Vortrag beim Digitalisierungs-Stammtisch - ich bin dabei!",
        "Nachricht": "Hallo Herr Brandt,\n\nvielen Dank fuer die Einladung zum Digitalisierungs-Stammtisch! Ich sage sehr gerne zu.\n\nAls Thema schlage ich vor: KI im Handwerksbuero.\n\nKoennen Sie mir den genauen Termin im April durchgeben?\n\nHerzliche Gruesse\nMechthild Roelfing",
        "Kanal": "E-Mail",
        "Prioritaet": "Hoch",
        "Status": "Offen"
    },
    {
        "Messe": "SHK+E Essen",
        "Kontakt-Name": "Sandra Kiefer",
        "Firma": "Kiefer Sanitaer & Bad",
        "E-Mail": "s.kiefer@kiefer-sanitaer.de",
        "Betreff": "Schluss mit WhatsApp-Chaos bei der Einsatzplanung?",
        "Nachricht": "Hallo Frau Kiefer,\n\nunser Gespraech auf der SHK+E hat mich nicht losgelassen. 6 Monteure per WhatsApp und Zettel zu koordinieren ist frustrierend.\n\nDarf ich Ihnen in 30 Minuten zeigen, wie das aussehen koennte?\n\nBeste Gruesse\nMechthild Roelfing",
        "Kanal": "E-Mail",
        "Prioritaet": "Hoch",
        "Status": "Offen"
    },
    {
        "Messe": "SHK+E Essen",
        "Kontakt-Name": "Lisa Hartmann",
        "Firma": "Viessmann Digital",
        "E-Mail": "lisa.hartmann@viessmann.com",
        "Betreff": "Integrationspartnerschaft Viessmann-Plattform - naechste Schritte?",
        "Nachricht": "Hallo Frau Hartmann,\n\ndanke fuer das interessante Gespraech auf der SHK+E! Die Idee, Workflow-Automatisierung als Ergaenzung zur Viessmann-Plattform anzubieten, finde ich spannend.\n\nSollen wir einen kurzen Call machen?\n\nHerzliche Gruesse\nMechthild Roelfing",
        "Kanal": "E-Mail",
        "Prioritaet": "Mittel",
        "Status": "Offen"
    },
    {
        "Messe": "Hannover Messe",
        "Kontakt-Name": "Dr. Thomas Weber",
        "Firma": "Siemens Digital Industries",
        "E-Mail": "thomas.weber@siemens.com",
        "Betreff": "KI-Automatisierung fuer Fertigungsbetriebe - Partnerprogramm",
        "Nachricht": "Hallo Herr Dr. Weber,\n\nvielen Dank fuer das aufschlussreiche Gespraech auf der Hannover Messe!\n\nAls KI-Beraterin sehe ich grosses Potenzial, die Siemens-Loesungen in Fertigungs-KMU zu bringen.\n\nKoennten wir ueber das Partnerprogramm sprechen?\n\nHerzliche Gruesse\nMechthild Roelfing",
        "Kanal": "E-Mail",
        "Prioritaet": "Mittel",
        "Status": "Offen"
    },
    {
        "Messe": "Hannover Messe",
        "Kontakt-Name": "Michael Krause",
        "Firma": "Krause Metallbau GmbH",
        "E-Mail": "m.krause@krause-metallbau.de",
        "Betreff": "Ihr Qualitaetsproblem bei Schweissnaehten - KI-Loesung in 4 Wochen?",
        "Nachricht": "Hallo Herr Krause,\n\ndie 8% Ausschussrate bei den Schweissnaehten kann KI-basierte Qualitaetskontrolle direkt adressieren.\n\nIch schlage ein Pilotprojekt vor: In 4 Wochen setzen wir eine Kamera + KI-Loesung auf.\n\nHaetten Sie naechste Woche 45 Minuten?\n\nBeste Gruesse\nMechthild Roelfing",
        "Kanal": "E-Mail",
        "Prioritaet": "Hoch",
        "Status": "Offen"
    },
    {
        "Messe": "Hannover Messe",
        "Kontakt-Name": "Anna Chen",
        "Firma": "Bosch Connected Industry",
        "E-Mail": "anna.chen@bosch.com",
        "Betreff": "Nexeed-Integration fuer Mittelstaendler - Zusammenarbeit?",
        "Nachricht": "Hallo Frau Chen,\n\ndanke fuer die spannende Demo der Nexeed-Plattform!\n\nIch koennte als Implementierungspartnerin die Bruecke bauen.\n\nSollen wir einen kurzen Call machen?\n\nHerzliche Gruesse\nMechthild Roelfing",
        "Kanal": "LinkedIn",
        "Prioritaet": "Mittel",
        "Status": "Offen"
    },
    {
        "Messe": "Hannover Messe",
        "Kontakt-Name": "Jens Hoffmann",
        "Firma": "Hoffmann Praezisionstechnik",
        "E-Mail": "j.hoffmann@hoffmann-praezision.de",
        "Betreff": "Fachkraeftemangel loesen mit KI-Assistenten?",
        "Nachricht": "Hallo Herr Hoffmann,\n\nKI kann repetitive Aufgaben automatisieren: Angebotserstellung, Auftragserfassung, Qualitaetsdokumentation.\n\nDarf ich Ihnen in 30 Minuten die groessten Automatisierungspotenziale zeigen?\n\nBeste Gruesse\nMechthild Roelfing",
        "Kanal": "E-Mail",
        "Prioritaet": "Hoch",
        "Status": "Offen"
    }
]

result = api_post("/rows/", {
    "table_name": "Follow-ups",
    "rows": rows
})

print(f"Eingefuegt: {result.get('inserted_row_count', 0)} Zeilen")
print("Fertig!")
