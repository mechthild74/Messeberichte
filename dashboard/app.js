// ==============================================
// Transformwerk Messe Dashboard
// Connects to SeaTable API for live data
// ==============================================

// --- CONFIG ---
const CONFIG = {
    API_PROXY: 'api.php'
};

// Kategorie-ID to Name mapping (SeaTable returns option IDs in API)
const KAT_MAP = {
    '534713': 'kontakt',
    '148879': 'trend',
    '103515': 'pain',
    '123561': 'idee',
    '404015': 'wettbewerb',
    '537524': 'foto',
    '348225': 'zitat',
    '255330': 'produkt',
    '270903': 'notiz'
};

const KAT_LABELS = {
    kontakt: 'Kontakte',
    trend: 'Trends',
    pain: 'Pain Points',
    idee: 'Ideen',
    wettbewerb: 'Wettbewerber',
    foto: 'Fotos',
    zitat: 'Zitate',
    produkt: 'Produkte',
    notiz: 'Notizen'
};

const KAT_COLORS = {
    kontakt: '#14b8a6',
    trend: '#3b82f6',
    pain: '#ef4444',
    idee: '#f59e0b',
    wettbewerb: '#8b5cf6',
    foto: '#ec4899',
    zitat: '#6b7280',
    produkt: '#0d9488',
    notiz: '#94a3b8'
};

const KAT_EMOJIS = {
    kontakt: '🤝',
    trend: '📈',
    pain: '😤',
    idee: '💡',
    wettbewerb: '🏁',
    foto: '📸',
    zitat: '💬',
    produkt: '🔧',
    notiz: '📝'
};

let allRows = [];
let charts = {};
let currentReport = null;

// --- DATA FETCHING ---

function apiUrl(action, extra = '') {
    const token = localStorage.getItem('tw_auth_token') || '';
    return `${CONFIG.API_PROXY}?action=${action}&token=${encodeURIComponent(token)}${extra}`;
}

async function fetchRows() {
    const resp = await fetch(apiUrl('rows'));
    if (!resp.ok) throw new Error('API-Fehler');
    const data = await resp.json();
    if (data.error) throw new Error(data.error);
    return data.rows || [];
}

async function fetchReport(messeName, type) {
    const resp = await fetch(apiUrl('report', `&messe=${encodeURIComponent(messeName)}&type=${encodeURIComponent(type)}`));
    if (!resp.ok) return null;
    const data = await resp.json();
    return data.error ? null : (data.html || null);
}

async function fetchReportsList(messeName) {
    const resp = await fetch(apiUrl('reports', `&messe=${encodeURIComponent(messeName)}`));
    if (!resp.ok) return [];
    const data = await resp.json();
    return data.error ? [] : (data.rows || []).map(r => r['6RFa'] || '');
}

// --- DATA PROCESSING ---

function parseRow(row) {
    const katIds = row['lC6b'] || [];
    const katName = katIds.length > 0 ? (KAT_MAP[katIds[0]] || 'notiz') : 'notiz';

    let inhalt = row['CRS4'] || '';
    if (typeof inhalt === 'object') inhalt = inhalt.text || inhalt.preview || '';

    let raw = row['m9hw'] || '';
    if (typeof raw === 'object') raw = raw.text || raw.preview || '';

    return {
        messe: row['0000'] || '',
        kategorie: katName,
        inhalt: inhalt,
        raw: raw,
        timestamp: row['_ctime'] || '',
        id: row['_id']
    };
}

function getMesseNames(rows) {
    const names = new Set();
    rows.forEach(r => {
        const parsed = parseRow(r);
        if (parsed.messe) names.add(parsed.messe);
    });
    return Array.from(names).sort();
}

function filterByMesse(rows, messeName) {
    return rows
        .map(parseRow)
        .filter(r => r.messe === messeName);
}

function countByKategorie(entries) {
    const counts = {};
    entries.forEach(e => {
        counts[e.kategorie] = (counts[e.kategorie] || 0) + 1;
    });
    return counts;
}

function getEntriesByDate(entries) {
    const byDate = {};
    entries.forEach(e => {
        const date = e.timestamp ? e.timestamp.split('T')[0] : 'unbekannt';
        byDate[date] = (byDate[date] || 0) + 1;
    });
    return byDate;
}

// --- UI RENDERING ---

async function init() {
    try {
        allRows = await fetchRows();
        const messen = getMesseNames(allRows);
        const select = document.getElementById('messeSelect');

        if (messen.length === 0) {
            select.innerHTML = '<option value="">Keine Messen</option>';
            document.getElementById('loading').style.display = 'none';
            document.getElementById('emptyState').style.display = 'block';
            return;
        }

        select.innerHTML = messen.map(m =>
            `<option value="${m}">${m}</option>`
        ).join('');

        loadMesse();
    } catch (err) {
        console.error('Fehler beim Laden:', err);
        document.getElementById('loading').innerHTML =
            `<p style="color: var(--red)">Fehler beim Laden der Daten. Bitte SeaTable-Verbindung prüfen.</p>`;
    }
}

function loadMesse() {
    const messeName = document.getElementById('messeSelect').value;
    if (!messeName) return;

    const entries = filterByMesse(allRows, messeName);
    const counts = countByKategorie(entries);

    document.getElementById('loading').style.display = 'none';
    document.getElementById('emptyState').style.display = 'none';
    document.getElementById('dashboard').style.display = 'block';

    renderKPIs(entries, counts);
    renderCharts(entries, counts);
    renderKontakte(entries);
    renderPainPoints(entries);
    renderTrends(entries);
    renderZitate(entries);
    renderFollowups(messeName);
    checkReports(messeName);

    document.getElementById('lastUpdate').textContent =
        `Aktualisiert: ${new Date().toLocaleString('de-DE')}`;
}

function renderKPIs(entries, counts) {
    const total = entries.length;
    const kontakte = counts.kontakt || 0;
    const pains = counts.pain || 0;
    const ideen = (counts.idee || 0) + (counts.trend || 0);
    const wettbewerb = counts.wettbewerb || 0;

    // Calculate entries per day
    const dates = new Set(entries.map(e => e.timestamp.split('T')[0]));
    const days = Math.max(dates.size, 1);
    const rate = (total / days).toFixed(1);

    document.getElementById('kpiTotal').textContent = total;
    document.getElementById('kpiTotalSub').textContent = `in ${counts ? Object.keys(counts).length : 0} Kategorien`;
    document.getElementById('kpiKontakte').textContent = kontakte;
    document.getElementById('kpiPains').textContent = pains;
    document.getElementById('kpiIdeen').textContent = ideen;
    document.getElementById('kpiWettbewerb').textContent = wettbewerb;
    document.getElementById('kpiRate').textContent = rate;
    document.getElementById('kpiRateSub').textContent = `${total} Einträge / ${days} Tag${days > 1 ? 'e' : ''}`;
}

function renderCharts(entries, counts) {
    // Destroy existing charts
    Object.values(charts).forEach(c => c.destroy());
    charts = {};

    // Kategorien Donut
    const katLabels = Object.keys(counts).map(k => KAT_LABELS[k] || k);
    const katValues = Object.values(counts);
    const katColors = Object.keys(counts).map(k => KAT_COLORS[k] || '#94a3b8');

    const ctx1 = document.getElementById('kategorienChart').getContext('2d');
    charts.kategorien = new Chart(ctx1, {
        type: 'doughnut',
        data: {
            labels: katLabels,
            datasets: [{
                data: katValues,
                backgroundColor: katColors,
                borderWidth: 2,
                borderColor: '#ffffff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        font: { family: 'Inter', size: 12 },
                        padding: 12,
                        usePointStyle: true,
                        pointStyleWidth: 10
                    }
                }
            }
        }
    });

    // Zeitverlauf Bar
    const byDate = getEntriesByDate(entries);
    const dateLabels = Object.keys(byDate).sort();
    const dateValues = dateLabels.map(d => byDate[d]);

    const ctx2 = document.getElementById('zeitverlaufChart').getContext('2d');
    charts.zeitverlauf = new Chart(ctx2, {
        type: 'bar',
        data: {
            labels: dateLabels.map(d => {
                const date = new Date(d);
                return date.toLocaleDateString('de-DE', { day: '2-digit', month: '2-digit' });
            }),
            datasets: [{
                label: 'Einträge',
                data: dateValues,
                backgroundColor: 'rgba(20, 184, 166, 0.7)',
                borderColor: '#14b8a6',
                borderWidth: 1,
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { stepSize: 1, font: { family: 'Inter', size: 12 } },
                    grid: { color: 'rgba(0,0,0,0.05)' }
                },
                x: {
                    ticks: { font: { family: 'Inter', size: 12 } },
                    grid: { display: false }
                }
            }
        }
    });
}

function renderKontakte(entries) {
    const kontakte = entries.filter(e => e.kategorie === 'kontakt');
    document.getElementById('kontaktBadge').textContent = kontakte.length;

    const tbody = document.querySelector('#kontakteTable tbody');
    if (kontakte.length === 0) {
        tbody.innerHTML = '<tr><td colspan="3" style="text-align:center;color:var(--text-muted)">Keine Kontakte erfasst</td></tr>';
        return;
    }

    tbody.innerHTML = kontakte.map(k => {
        const date = new Date(k.timestamp);
        const dateStr = date.toLocaleDateString('de-DE', { day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit' });
        // Try to extract name (first part before comma)
        const parts = k.inhalt.split(',');
        const name = parts[0] || 'Unbekannt';
        const details = parts.slice(1).join(',').trim();

        return `<tr>
            <td><strong>${escapeHtml(name)}</strong></td>
            <td>${escapeHtml(details.substring(0, 150))}${details.length > 150 ? '...' : ''}</td>
            <td style="white-space:nowrap;font-size:12px;color:var(--text-muted)">${dateStr}</td>
        </tr>`;
    }).join('');
}

function renderPainPoints(entries) {
    const pains = entries.filter(e => e.kategorie === 'pain');
    document.getElementById('painBadge').textContent = pains.length;

    const list = document.getElementById('painList');
    if (pains.length === 0) {
        list.innerHTML = '<li style="color:var(--text-muted)">Keine Pain Points erfasst</li>';
        return;
    }

    list.innerHTML = pains.map(p =>
        `<li><span class="insight-tag pain">Pain</span>${escapeHtml(truncate(p.inhalt, 200))}</li>`
    ).join('');
}

function renderTrends(entries) {
    const trends = entries.filter(e => e.kategorie === 'trend' || e.kategorie === 'idee');
    document.getElementById('trendBadge').textContent = trends.length;

    const list = document.getElementById('trendList');
    if (trends.length === 0) {
        list.innerHTML = '<li style="color:var(--text-muted)">Keine Trends/Ideen erfasst</li>';
        return;
    }

    list.innerHTML = trends.map(t =>
        `<li><span class="insight-tag ${t.kategorie}">${t.kategorie === 'trend' ? 'Trend' : 'Idee'}</span>${escapeHtml(truncate(t.inhalt, 200))}</li>`
    ).join('');
}

function renderZitate(entries) {
    const zitate = entries.filter(e => e.kategorie === 'zitat');
    const section = document.getElementById('zitateSection');

    if (zitate.length === 0) {
        section.style.display = 'none';
        return;
    }

    section.style.display = 'block';
    const list = document.getElementById('zitateList');
    list.innerHTML = zitate.map(z => {
        // Try to split quote from source (look for " — " or " - ")
        const parts = z.inhalt.split(/\s[—–-]\s/);
        const quote = parts[0] || z.inhalt;
        const source = parts[1] || '';

        return `<div class="zitat-card">
            "${escapeHtml(quote)}"
            ${source ? `<div class="zitat-source">— ${escapeHtml(source)}</div>` : ''}
        </div>`;
    }).join('');
}

// --- FOLLOW-UPS ---

// Follow-ups Spalten-Keys (Table: Nid7)
const FU_KEYS = {
    messe: '0000',
    name: '0tI2',
    firma: 'z3pF',
    email: 'f8a9',
    betreff: 'PC98',
    nachricht: 'V3ud',
    kanal: 'HdnU',
    prioritaet: 'rJ0T',
    status: 'u601'
};

async function fetchFollowups(messeName) {
    const resp = await fetch(apiUrl('followups', `&messe=${encodeURIComponent(messeName)}`));
    if (!resp.ok) return [];
    const data = await resp.json();
    return data.error ? [] : (data.rows || []);
}

async function renderFollowups(messeName) {
    const section = document.getElementById('followupsSection');
    const list = document.getElementById('followupsList');
    const badge = document.getElementById('followupBadge');

    try {
        const rows = await fetchFollowups(messeName);
        if (rows.length === 0) {
            section.style.display = 'none';
            return;
        }

        section.style.display = 'block';
        badge.textContent = rows.length;

        list.innerHTML = rows.map(row => {
            const name = row[FU_KEYS.name] || 'Unbekannt';
            const firma = row[FU_KEYS.firma] || '';
            const email = row[FU_KEYS.email] || '';
            const betreff = row[FU_KEYS.betreff] || '';
            const kanal = row[FU_KEYS.kanal] || 'E-Mail';
            const rowId = row['_id'];

            // Single-Select gibt ID oder String zurueck
            let prioritaet = row[FU_KEYS.prioritaet] || '';
            if (typeof prioritaet === 'object') prioritaet = prioritaet.name || '';
            let status = row[FU_KEYS.status] || 'Offen';
            if (typeof status === 'object') status = status.name || 'Offen';

            const prioClass = prioritaet.toLowerCase();
            const statusClass = status.toLowerCase();
            const isOffen = status === 'Offen';
            const hasEmail = !!email;

            return `<div class="followup-card" data-row-id="${rowId}">
                <div class="followup-card-header">
                    <div>
                        <div class="followup-name">${escapeHtml(name)}</div>
                        <div class="followup-firma">${escapeHtml(firma)} ${kanal !== 'E-Mail' ? '(' + escapeHtml(kanal) + ')' : ''}</div>
                    </div>
                    <span class="status-badge ${statusClass}">${escapeHtml(status)}</span>
                </div>
                <div class="followup-betreff">${escapeHtml(betreff)}</div>
                <div class="followup-footer">
                    <div class="followup-meta">
                        <span class="priority-badge ${prioClass}">${escapeHtml(prioritaet)}</span>
                        ${email ? `<span style="font-size:12px;color:var(--text-muted)">${escapeHtml(email)}</span>` : ''}
                    </div>
                    <div class="followup-actions">
                        ${isOffen && hasEmail ? `<button class="btn-draft" onclick="createDraft('${rowId}')" id="btnDraft-${rowId}">Draft erstellen</button>` : ''}
                        ${status !== 'Gesendet' ? `<button class="btn-sent" onclick="markSent('${rowId}')" id="btnSent-${rowId}">Gesendet</button>` : ''}
                    </div>
                </div>
            </div>`;
        }).join('');
    } catch (err) {
        console.error('Follow-ups laden fehlgeschlagen:', err);
        section.style.display = 'none';
    }
}

async function createDraft(rowId) {
    const btn = document.getElementById(`btnDraft-${rowId}`);
    if (!btn) return;

    btn.disabled = true;
    btn.textContent = 'Wird erstellt...';

    // Daten aus der Karte holen
    const card = document.querySelector(`[data-row-id="${rowId}"]`);
    const name = card.querySelector('.followup-name')?.textContent || '';
    const firma = card.querySelector('.followup-firma')?.textContent || '';
    const betreff = card.querySelector('.followup-betreff')?.textContent || '';

    try {
        // Follow-up-Daten nochmal aus SeaTable holen (fuer volle Nachricht)
        const messeName = document.getElementById('messeSelect').value;
        const rows = await fetchFollowups(messeName);
        const row = rows.find(r => r['_id'] === rowId);
        if (!row) throw new Error('Follow-up nicht gefunden');

        let nachricht = row[FU_KEYS.nachricht] || '';
        if (typeof nachricht === 'object') nachricht = nachricht.text || nachricht.preview || '';

        const resp = await fetch(apiUrl('create-draft'), {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                rowId,
                kontaktName: row[FU_KEYS.name] || '',
                firma: row[FU_KEYS.firma] || '',
                email: row[FU_KEYS.email] || '',
                betreff: row[FU_KEYS.betreff] || '',
                nachricht
            })
        });

        if (!resp.ok) throw new Error('Draft-Erstellung fehlgeschlagen');

        btn.textContent = 'Entwurf erstellt';
        btn.classList.add('success');

        // Status-Badge aktualisieren
        const statusBadge = card.querySelector('.status-badge');
        if (statusBadge) {
            statusBadge.textContent = 'Entwurf';
            statusBadge.className = 'status-badge entwurf';
        }
    } catch (err) {
        console.error('Draft erstellen fehlgeschlagen:', err);
        btn.textContent = 'Fehler!';
        btn.disabled = false;
        setTimeout(() => { btn.textContent = 'Draft erstellen'; }, 3000);
    }
}

async function markSent(rowId) {
    const btn = document.getElementById(`btnSent-${rowId}`);
    if (!btn) return;

    btn.disabled = true;
    btn.textContent = 'Wird gespeichert...';

    try {
        const resp = await fetch(apiUrl('update-followup-status'), {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ rowId, status: 'Gesendet' })
        });

        if (!resp.ok) throw new Error('Status-Update fehlgeschlagen');

        const card = document.querySelector(`[data-row-id="${rowId}"]`);
        const statusBadge = card?.querySelector('.status-badge');
        if (statusBadge) {
            statusBadge.textContent = 'Gesendet';
            statusBadge.className = 'status-badge gesendet';
        }

        // Buttons entfernen
        const actions = card?.querySelector('.followup-actions');
        if (actions) actions.innerHTML = '';
    } catch (err) {
        console.error('Status update fehlgeschlagen:', err);
        btn.textContent = 'Fehler!';
        btn.disabled = false;
        setTimeout(() => { btn.textContent = 'Gesendet'; }, 3000);
    }
}

// --- REPORTS ---

async function checkReports(messeName) {
    const reports = ['auswertung', 'marketing-aktionen', 'follow-ups'];
    const btnIds = ['btnAuswertung', 'btnMarketing', 'btnFollowups'];

    // Fetch available reports from SeaTable
    const available = await fetchReportsList(messeName);

    for (let i = 0; i < reports.length; i++) {
        const btn = document.getElementById(btnIds[i]);
        if (available.includes(reports[i])) {
            btn.disabled = false;
            btn.textContent = 'Anzeigen';
            btn.closest('.report-card').classList.add('available');
        } else {
            btn.disabled = true;
            btn.textContent = 'Nicht verfügbar';
            btn.closest('.report-card').classList.remove('available');
        }
    }
}

async function showReport(type) {
    const messeName = document.getElementById('messeSelect').value;

    try {
        const html = await fetchReport(messeName, type);
        if (!html) return;

        const titles = {
            'auswertung': 'Messe-Auswertung',
            'marketing-aktionen': 'Marketing-Aktionen',
            'follow-ups': 'Follow-up-Nachrichten'
        };

        document.getElementById('modalTitle').textContent = titles[type] || type;
        document.getElementById('modalBody').innerHTML = html;
        document.getElementById('reportModal').style.display = 'flex';
        currentReport = type;
        document.body.style.overflow = 'hidden';
    } catch (err) {
        console.error('Report laden fehlgeschlagen:', err);
    }
}

function closeModal() {
    document.getElementById('reportModal').style.display = 'none';
    document.body.style.overflow = '';
    currentReport = null;
}

function exportPDF() {
    const element = document.getElementById('modalBody');
    const messeName = document.getElementById('messeSelect').value;
    const slug = messeName.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

    html2pdf().set({
        margin: [15, 15, 15, 15],
        filename: `${slug}-${currentReport}.pdf`,
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2 },
        jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
    }).from(element).save();
}

// Close modal on Escape
document.addEventListener('keydown', e => {
    if (e.key === 'Escape') closeModal();
});

// Close modal on backdrop click
document.getElementById('reportModal')?.addEventListener('click', e => {
    if (e.target === e.currentTarget) closeModal();
});

// --- HELPERS ---

function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

function truncate(str, len) {
    return str.length > len ? str.substring(0, len) + '...' : str;
}

// --- AUTH ---

function checkAuth() {
    return !!localStorage.getItem('tw_auth_token');
}

function showApp() {
    document.getElementById('loginScreen').style.display = 'none';
    document.getElementById('appHeader').style.display = '';
    document.getElementById('appMain').style.display = '';
    document.getElementById('appFooter').style.display = '';
}

async function doLogin(event) {
    event.preventDefault();
    const pw = document.getElementById('loginPassword').value;
    const errorEl = document.getElementById('loginError');
    errorEl.style.display = 'none';

    try {
        const resp = await fetch(`${CONFIG.API_PROXY}?action=login&password=${encodeURIComponent(pw)}`);
        const data = await resp.json();
        if (data.ok && data.token) {
            localStorage.setItem('tw_auth_token', data.token);
            showApp();
            init();
        } else {
            errorEl.style.display = 'block';
        }
    } catch {
        errorEl.textContent = 'Verbindungsfehler';
        errorEl.style.display = 'block';
    }
}

// --- INIT ---

(async function startup() {
    if (checkAuth()) {
        showApp();
        try {
            await init();
        } catch {
            // Token ungültig — zurück zum Login
            localStorage.removeItem('tw_auth_token');
            location.reload();
        }
    }
    // Sonst: Login-Screen ist bereits sichtbar (HTML-Standard)
})();
