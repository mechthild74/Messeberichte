<?php
/**
 * SeaTable API Proxy — Token serverseitig, Header-Auth
 */

header('Content-Type: application/json; charset=utf-8');

// --- KONFIGURATION aus .env.dashboard laden ---
$envFile = __DIR__ . '/../.env.dashboard';
if (!file_exists($envFile)) {
    $envFile = __DIR__ . '/.env.dashboard';
}

$config = [];
if (file_exists($envFile)) {
    foreach (file($envFile, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES) as $line) {
        if (str_starts_with(trim($line), '#')) continue;
        $parts = explode('=', $line, 2);
        if (count($parts) === 2) {
            $config[trim($parts[0])] = trim($parts[1]);
        }
    }
}

$API_TOKEN        = $config['SEATABLE_API_TOKEN'] ?? '';
$DTABLE_UUID      = $config['SEATABLE_DTABLE_UUID'] ?? '';
$ENTRIES_TABLE_ID = $config['ENTRIES_TABLE_ID'] ?? '';
$REPORTS_TABLE_ID = $config['REPORTS_TABLE_ID'] ?? '';
$FOLLOWUPS_TABLE_ID = $config['FOLLOWUPS_TABLE_ID'] ?? '';
$N8N_WEBHOOK_URL    = $config['N8N_WEBHOOK_URL'] ?? '';
$DASHBOARD_PASSWORD = $config['DASHBOARD_PASSWORD'] ?? '';

if (!$API_TOKEN || !$DTABLE_UUID) {
    http_response_code(500);
    echo json_encode(['error' => 'Server-Konfiguration fehlt (.env.dashboard)']);
    exit;
}

// --- AUTH: Passwort-Hash als Token ---
$VALID_TOKEN = hash('sha256', $DASHBOARD_PASSWORD . '::tw-dashboard');

$action = $_GET['action'] ?? '';

// Login: Passwort prüfen, Token zurückgeben
if ($action === 'login') {
    $pw = $_POST['password'] ?? $_GET['password'] ?? '';
    if ($pw === $DASHBOARD_PASSWORD) {
        echo json_encode(['ok' => true, 'token' => $VALID_TOKEN]);
    } else {
        http_response_code(401);
        echo json_encode(['error' => 'Falsches Passwort']);
    }
    exit;
}

// Alle anderen Aktionen: Token prüfen (aus URL-Parameter)
$clientToken = $_GET['token'] ?? '';
if ($clientToken !== $VALID_TOKEN) {
    http_response_code(401);
    echo json_encode(['error' => 'Nicht eingeloggt']);
    exit;
}

// --- HELPERS ---

function apiError($msg, $code = 500) {
    http_response_code($code);
    echo json_encode(['error' => $msg]);
    exit;
}

function seatable_request($url, $headers = []) {
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    curl_setopt($ch, CURLOPT_TIMEOUT, 15);
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    if ($httpCode >= 400) {
        apiError("SeaTable API Fehler (HTTP $httpCode)", $httpCode);
    }

    return json_decode($response, true);
}

function getAccessToken($apiToken) {
    $data = seatable_request(
        'https://cloud.seatable.io/api/v2.1/dtable/app-access-token/',
        ["Authorization: Token $apiToken"]
    );
    return $data['access_token'] ?? null;
}

function fetchTable($accessToken, $dtableUuid, $tableId) {
    $url = "https://cloud.seatable.io/api-gateway/api/v2/dtables/$dtableUuid/rows/?table_id=$tableId&limit=1000";
    return seatable_request($url, ["Authorization: Bearer $accessToken"]);
}

// --- ROUTING ---

$accessToken = getAccessToken($API_TOKEN);
if (!$accessToken) {
    apiError('Konnte keinen Access Token holen');
}

if ($action === 'rows') {
    $data = fetchTable($accessToken, $DTABLE_UUID, $ENTRIES_TABLE_ID);

    $messeFilter = $_GET['messe'] ?? '';
    if ($messeFilter && isset($data['rows'])) {
        $data['rows'] = array_values(array_filter($data['rows'], function($row) use ($messeFilter) {
            return ($row['0000'] ?? '') === $messeFilter;
        }));
    }
    echo json_encode($data);

} elseif ($action === 'reports') {
    $data = fetchTable($accessToken, $DTABLE_UUID, $REPORTS_TABLE_ID);

    $messeFilter = $_GET['messe'] ?? '';
    if ($messeFilter && isset($data['rows'])) {
        $data['rows'] = array_values(array_filter($data['rows'], function($row) use ($messeFilter) {
            return ($row['0000'] ?? '') === $messeFilter;
        }));
    }
    echo json_encode($data);

} elseif ($action === 'report') {
    $messe = $_GET['messe'] ?? '';
    $type = $_GET['type'] ?? '';
    if (!$messe || !$type) {
        apiError('Parameter messe und type erforderlich', 400);
    }

    $data = fetchTable($accessToken, $DTABLE_UUID, $REPORTS_TABLE_ID);

    $found = null;
    foreach ($data['rows'] ?? [] as $row) {
        $rowMesse = $row['0000'] ?? '';
        $rowType = $row['6RFa'] ?? '';
        if (is_array($rowType)) $rowType = $rowType[0] ?? '';
        if ($rowMesse === $messe && $rowType === $type) {
            $found = $row;
            break;
        }
    }

    if ($found) {
        echo json_encode([
            'messe' => $found['0000'] ?? '',
            'type' => $type,
            'html' => $found['k62Q'] ?? '',
            'version' => $found['dDa5'] ?? 1
        ]);
    } else {
        apiError('Report nicht gefunden', 404);
    }

} elseif ($action === 'followups') {
    if (!$FOLLOWUPS_TABLE_ID) {
        apiError('FOLLOWUPS_TABLE_ID nicht konfiguriert', 500);
    }
    $data = fetchTable($accessToken, $DTABLE_UUID, $FOLLOWUPS_TABLE_ID);

    $messeFilter = $_GET['messe'] ?? '';
    if ($messeFilter && isset($data['rows'])) {
        $data['rows'] = array_values(array_filter($data['rows'], function($row) use ($messeFilter) {
            return ($row['0000'] ?? '') === $messeFilter;
        }));
    }
    echo json_encode($data);

} elseif ($action === 'create-draft') {
    if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
        apiError('POST erforderlich', 405);
    }
    if (!$N8N_WEBHOOK_URL) {
        apiError('N8N_WEBHOOK_URL nicht konfiguriert', 500);
    }

    $input = json_decode(file_get_contents('php://input'), true);
    if (!$input || !isset($input['rowId'])) {
        apiError('rowId erforderlich', 400);
    }

    // POST an n8n Webhook weiterleiten
    $ch = curl_init($N8N_WEBHOOK_URL);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($input));
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Content-Type: application/json'
    ]);
    curl_setopt($ch, CURLOPT_TIMEOUT, 30);
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    if ($httpCode >= 400) {
        apiError("n8n Webhook Fehler (HTTP $httpCode)", $httpCode);
    }

    echo $response ?: json_encode(['ok' => true]);

} elseif ($action === 'update-followup-status') {
    if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
        apiError('POST erforderlich', 405);
    }

    $input = json_decode(file_get_contents('php://input'), true);
    $rowId = $input['rowId'] ?? '';
    $status = $input['status'] ?? '';
    if (!$rowId || !$status) {
        apiError('rowId und status erforderlich', 400);
    }

    // SeaTable Row updaten
    $url = "https://cloud.seatable.io/api-gateway/api/v2/dtables/$DTABLE_UUID/rows/";
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'PUT');
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode([
        'table_name' => 'Follow-ups',
        'row' => ['Status' => $status],
        'row_id' => $rowId
    ]));
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        "Authorization: Bearer $accessToken",
        'Content-Type: application/json'
    ]);
    curl_setopt($ch, CURLOPT_TIMEOUT, 15);
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    if ($httpCode >= 400) {
        apiError("SeaTable Update Fehler (HTTP $httpCode)", $httpCode);
    }

    echo json_encode(['ok' => true, 'status' => $status]);

} else {
    apiError('Unbekannte Aktion', 400);
}
