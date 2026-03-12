"""
Erstellt den n8n-Workflow "Follow-up Draft" per REST API.
Webhook -> Code (E-Mail bauen) -> Code (IMAP APPEND) -> SeaTable Update -> Respond
"""
import json
import urllib.request

N8N_URL = "https://n8n.srv1159226.hstgr.cloud"
N8N_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZjdhMjM0OS02ZjdmLTQ0ZjktOTA1Zi1hOTZkMzkzZWRiYWYiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwianRpIjoiZTZjOTc3NGEtMWViYi00NTYxLThhYjctMjQ1NWMyZDNlOTM3IiwiaWF0IjoxNzczMjMxODE5fQ.v9Gds_5giYmEeI0p4_EU5YU6ejq-mmtxEUP0GN7oR0w"

HEADERS = {
    "X-N8N-API-KEY": N8N_API_KEY,
    "Content-Type": "application/json"
}

def n8n_api(path, data=None, method="GET"):
    url = f"{N8N_URL}/api/v1{path}"
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=HEADERS, method=method)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))

# Workflow-Definition
workflow = {
    "name": "Follow-up Draft",
    "nodes": [
        {
            "parameters": {
                "httpMethod": "POST",
                "path": "followup-draft",
                "authentication": "headerAuth",
                "responseMode": "responseNode",
                "options": {}
            },
            "id": "webhook-trigger",
            "name": "Webhook",
            "type": "n8n-nodes-base.webhook",
            "typeVersion": 2,
            "position": [240, 300]
        },
        {
            "parameters": {
                "jsCode": """// E-Mail als RFC 822 String bauen
const { kontaktName, firma, email, betreff, nachricht, rowId } = $input.first().json.body;

if (!email || !betreff || !nachricht) {
  throw new Error('Fehlende Felder: email, betreff oder nachricht');
}

const fromEmail = 'info@transformwerk.digital';
const fromName = 'Mechthild Roelfing - Beratung';
const date = new Date().toUTCString();
const messageId = `<${Date.now()}.${Math.random().toString(36).substr(2)}@transformwerk.digital>`;

// RFC 822 E-Mail mit UTF-8 Encoding
const emailRaw = [
  `From: =?UTF-8?B?${Buffer.from(fromName).toString('base64')}?= <${fromEmail}>`,
  `To: ${email}`,
  `Subject: =?UTF-8?B?${Buffer.from(betreff).toString('base64')}?=`,
  `Date: ${date}`,
  `Message-ID: ${messageId}`,
  `MIME-Version: 1.0`,
  `Content-Type: text/plain; charset=UTF-8`,
  `Content-Transfer-Encoding: base64`,
  `X-Mailer: Transformwerk Follow-up System`,
  ``,
  Buffer.from(nachricht).toString('base64')
].join('\\r\\n');

return [{
  json: {
    emailRaw,
    rowId,
    kontaktName,
    firma,
    email,
    betreff
  }
}];"""
            },
            "id": "build-email",
            "name": "E-Mail bauen",
            "type": "n8n-nodes-base.code",
            "typeVersion": 2,
            "position": [460, 300]
        },
        {
            "parameters": {
                "jsCode": """// IMAP APPEND - Entwurf in Drafts-Ordner legen
const Imap = require('imap');
const { emailRaw, rowId, kontaktName } = $input.first().json;

// IMAP Credentials aus Environment/Credentials
// WICHTIG: Diese Werte muessen in n8n unter Settings > Variables eingetragen werden
const imapConfig = {
  user: $env.IMAP_USER || 'info@transformwerk.digital',
  password: $env.IMAP_PASSWORD || '',
  host: $env.IMAP_HOST || 'imap.hostinger.com',
  port: parseInt($env.IMAP_PORT || '993'),
  tls: true,
  tlsOptions: { rejectUnauthorized: false }
};

if (!imapConfig.password) {
  throw new Error('IMAP_PASSWORD nicht gesetzt! Bitte in n8n Settings > Variables eintragen.');
}

return new Promise((resolve, reject) => {
  const imap = new Imap(imapConfig);

  imap.once('ready', () => {
    // Drafts-Ordner oeffnen (typische Namen probieren)
    const draftsFolder = $env.IMAP_DRAFTS_FOLDER || 'Drafts';

    imap.append(
      emailRaw,
      { mailbox: draftsFolder, flags: ['\\\\Draft', '\\\\Seen'] },
      (err) => {
        imap.end();
        if (err) {
          reject(new Error(`IMAP APPEND fehlgeschlagen: ${err.message}`));
        } else {
          resolve([{
            json: {
              success: true,
              rowId,
              kontaktName,
              message: `Entwurf fuer ${kontaktName} im Drafts-Ordner erstellt`
            }
          }]);
        }
      }
    );
  });

  imap.once('error', (err) => {
    reject(new Error(`IMAP Verbindung fehlgeschlagen: ${err.message}`));
  });

  imap.connect();
});"""
            },
            "id": "imap-append",
            "name": "IMAP APPEND",
            "type": "n8n-nodes-base.code",
            "typeVersion": 2,
            "position": [680, 300]
        },
        {
            "parameters": {
                "method": "PUT",
                "url": "=https://cloud.seatable.io/api-gateway/api/v2/dtables/99f096d0-d82f-40fa-acc3-dcf53458ee65/rows/",
                "authentication": "genericCredentialType",
                "genericAuthType": "httpHeaderAuth",
                "sendBody": True,
                "specifyBody": "json",
                "jsonBody": '={"table_name": "Follow-ups", "row": {"Status": "Entwurf"}, "row_id": "{{ $json.rowId }}"}'
            },
            "id": "seatable-update",
            "name": "SeaTable Status Update",
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 4.2,
            "position": [900, 300],
            "credentials": {}
        },
        {
            "parameters": {
                "respondWith": "json",
                "responseBody": '={{ JSON.stringify({ success: true, message: $json.message || "Entwurf erstellt", rowId: $json.rowId }) }}'
            },
            "id": "respond",
            "name": "Respond",
            "type": "n8n-nodes-base.respondToWebhook",
            "typeVersion": 1.1,
            "position": [1120, 300]
        },
        {
            "parameters": {
                "respondWith": "json",
                "responseBody": '={{ JSON.stringify({ success: false, error: $json.error || "Unbekannter Fehler" }) }}',
                "options": {
                    "responseCode": 500
                }
            },
            "id": "respond-error",
            "name": "Error Response",
            "type": "n8n-nodes-base.respondToWebhook",
            "typeVersion": 1.1,
            "position": [1120, 500]
        }
    ],
    "connections": {
        "Webhook": {
            "main": [
                [{"node": "E-Mail bauen", "type": "main", "index": 0}]
            ]
        },
        "E-Mail bauen": {
            "main": [
                [{"node": "IMAP APPEND", "type": "main", "index": 0}]
            ]
        },
        "IMAP APPEND": {
            "main": [
                [{"node": "SeaTable Status Update", "type": "main", "index": 0}]
            ]
        },
        "SeaTable Status Update": {
            "main": [
                [{"node": "Respond", "type": "main", "index": 0}]
            ]
        }
    },
    "settings": {
        "executionOrder": "v1"
    }
}

print("=== Follow-up Draft Workflow erstellen ===")
result = n8n_api("/workflows", workflow, method="POST")
workflow_id = result.get("id", "unknown")
print(f"Workflow erstellt! ID: {workflow_id}")

# Workflow aktivieren
print("Workflow aktivieren...")
n8n_api(f"/workflows/{workflow_id}/activate", method="POST")
print(f"Workflow aktiviert!")

# Webhook-URL ausgeben
print(f"\n=== FERTIG ===")
print(f"Workflow-ID: {workflow_id}")
print(f"Webhook-URL: {N8N_URL}/webhook/followup-draft")
print(f"\nWICHTIG: Folgende n8n Environment Variables muessen gesetzt werden:")
print(f"  IMAP_USER = info@transformwerk.digital")
print(f"  IMAP_PASSWORD = (Hostinger E-Mail-Passwort)")
print(f"  IMAP_HOST = imap.hostinger.com")
print(f"  IMAP_PORT = 993")
print(f"  IMAP_DRAFTS_FOLDER = Drafts")
print(f"\nBitte in n8n unter Settings > Variables eintragen!")
