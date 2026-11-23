/**
 * MaxPortfolio - High-Performance Static Server, Live-Reload & Visitor Intelligence Hub
 * Ports: 7070 (Primary) & 7072 (Live Mirror)
 * Features:
 * - Real-time Live-Reload: Automatically reloads open browser tabs when HTML, CSS, JS, or JSON changes
 * - Zero-Cache HTTP delivery for instant edits
 * - Dual-Port listener (7070 and 7072) accessible on localhost and local network (LAN)
 * - Visitor telemetry and contact form ingestion
 */
'use strict';

const http = require('http');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const os = require('os');
const zlib = require('zlib');

const MASTER_SECRET = 'MaxPortfolio2026@SecureMasterKey!';
const GOOGLE_FORM_URL = 'https://docs.google.com/forms/d/e/1FAIpQLSd3Wx27Aw9308pzORR2FZ_e6VKd--hs8gDbhlxMNIV-TNtyAA/formResponse';
const GOOGLE_FIELD_ENTRY = 'entry.132983276';
const RSA_PUB_PATH = path.join(__dirname, '..', 'data', 'keys', 'max_public_key.pem');

async function encryptAndRelayToGoogleForm(payload) {
  try {
    const jsonStr = JSON.stringify(payload);
    const compressed = zlib.gzipSync(Buffer.from(jsonStr, 'utf-8'));
    let armored = null;

    // Asymmetric RSA-OAEP + AES-256-GCM Hybrid Path
    if (fs.existsSync(RSA_PUB_PATH)) {
      try {
        const pubPem = fs.readFileSync(RSA_PUB_PATH, 'utf8');
        const aesKey = crypto.randomBytes(32);
        const iv = crypto.randomBytes(12);

        const encAesKey = crypto.publicEncrypt({
          key: pubPem,
          padding: crypto.constants.RSA_PKCS1_OAEP_PADDING,
          oaepHash: 'sha1'
        }, aesKey);

        const cipher = crypto.createCipheriv('aes-256-gcm', aesKey, iv);
        const encData = Buffer.concat([cipher.update(compressed), cipher.final()]);
        const tag = cipher.getAuthTag();

        const packed = Buffer.concat([encAesKey, iv, encData, tag]);
        armored = 'MAXASYM1:' + packed.toString('base64');
      } catch (e) {
        console.warn('[GooglePipeline] Asymmetric relay warning, falling back to symmetric:', e.message);
      }
    }

    // Fallback: Symmetric AES-256-GCM
    if (!armored) {
      const key = crypto.createHash('sha256').update(MASTER_SECRET).digest();
      const iv = crypto.randomBytes(12);
      const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);
      const encrypted = Buffer.concat([cipher.update(compressed), cipher.final()]);
      const tag = cipher.getAuthTag();

      const finalCipher = Buffer.concat([iv, encrypted, tag]);
      armored = 'MAXENC1:' + finalCipher.toString('base64');
    }

    const postData = new URLSearchParams();
    postData.append(GOOGLE_FIELD_ENTRY, armored);
    postData.append('fvv', '1');
    postData.append('pageHistory', '0');

    const res = await fetch(GOOGLE_FORM_URL, {
      method: 'POST',
      body: postData.toString(),
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'MaxHive-VaultServer/1.0'
      }
    });
    console.log(`[GooglePipeline] Encrypted payload delivered to Google Form. Status: ${res.status}`);
    return true;
  } catch (err) {
    console.error('[GooglePipeline] Relay failed:', err.message);
    return false;
  }
}

const CLIENT_ENCRYPTION_KEY = 'MaxPortfolio2026_ClientEncryptionKey_9824584454_01';
const MASTER_DECRYPTION_KEY = 'MaxPortfolio2026_MasterDecryptionKey_9824584454_02';

function decryptPayload(encStr) {
  if (!encStr || typeof encStr !== 'string') return null;
  try {
    if (encStr.startsWith('MAXENC1:')) {
      const b64 = encStr.substring('MAXENC1:'.length).trim();
      const raw = Buffer.from(b64, 'base64');
      if (raw.length < 28) return null;
      const iv = raw.subarray(0, 12);
      const cipherWithTag = raw.subarray(12);
      const tag = cipherWithTag.subarray(cipherWithTag.length - 16);
      const ct = cipherWithTag.subarray(0, cipherWithTag.length - 16);

      const keyBytes = crypto.createHash('sha256').update(CLIENT_ENCRYPTION_KEY).digest();
      const decipher = crypto.createDecipheriv('aes-256-gcm', keyBytes, iv);
      decipher.setAuthTag(tag);
      let dec = Buffer.concat([decipher.update(ct), decipher.final()]);
      try {
        dec = zlib.gunzipSync(dec);
      } catch (e) {}
      return JSON.parse(dec.toString('utf8'));
    }
  } catch (e) {
    console.warn('[VaultServer] Decrypt payload notice:', e.message);
  }
  return null;
}

const PORT = 7070;
const PORT_ALT = 7072;
const ROOT = path.resolve(__dirname, '..');
const DB_PATH = path.join(ROOT, 'data', 'visitor_analytics.json');

const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
  '.mp4': 'video/mp4',
  '.webm': 'video/webm',
  '.pdf': 'application/pdf',
  '.txt': 'text/plain; charset=utf-8',
  '.xml': 'application/xml; charset=utf-8',
  '.b64': 'text/plain; charset=utf-8'
};

const ATTACHMENTS_DIR = path.join(ROOT, 'data', 'attachments');
if (!fs.existsSync(ATTACHMENTS_DIR)) {
  try { fs.mkdirSync(ATTACHMENTS_DIR, { recursive: true }); } catch (e) {}
}

// In-memory runtime state backed by DB_PATH with sliding window buffer for high volume
let analyticsDb = {
  version: '3.2.0',
  lastUpdated: Date.now(),
  totalVisitors: 0,
  totalVisits: 0,
  totalInquiries: 0,
  visitors: [],
  inquiries: []
};

function loadDatabase() {
  try {
    if (fs.existsSync(DB_PATH)) {
      const raw = fs.readFileSync(DB_PATH, 'utf8');
      analyticsDb = JSON.parse(raw);
      if (!Array.isArray(analyticsDb.visitors)) analyticsDb.visitors = [];
      if (!Array.isArray(analyticsDb.inquiries)) analyticsDb.inquiries = [];
      if (!analyticsDb.totalVisitors) analyticsDb.totalVisitors = analyticsDb.visitors.length;
      if (!analyticsDb.totalVisits) {
        analyticsDb.totalVisits = analyticsDb.visitors.reduce((acc, v) => acc + (v.visits || v.pageViews || 1), 0);
      }
      if (!analyticsDb.totalInquiries) analyticsDb.totalInquiries = analyticsDb.inquiries.length;
      console.log(`[DB] Successfully loaded ${analyticsDb.visitors.length} cached visitors (${analyticsDb.totalVisits} total visits) and ${analyticsDb.inquiries.length} inquiries.`);
    }
  } catch (err) {
    console.error('[DB Error] Failed to load visitor database:', err.message);
  }
}

let saveTimeout = null;
function saveDatabaseDebounced() {
  if (saveTimeout) clearTimeout(saveTimeout);
  saveTimeout = setTimeout(() => {
    try {
      analyticsDb.lastUpdated = Date.now();
      fs.writeFileSync(DB_PATH, JSON.stringify(analyticsDb, null, 2), 'utf8');
    } catch (e) {
      console.error('[DB Error] Failed to persist database:', e.message);
    }
  }, 1000);
}

loadDatabase();

// Parse client user-agent into readable device/os/browser
function parseUserAgent(ua) {
  if (!ua) return { device: 'Desktop', os: 'Linux', browser: 'Browser' };
  let device = 'Desktop';
  let os = 'Unknown OS';
  let browser = 'Unknown Browser';

  if (/mobile/i.test(ua)) device = 'Mobile';
  else if (/ipad|tablet/i.test(ua)) device = 'Tablet';

  if (/android/i.test(ua)) os = 'Android';
  else if (/iphone|ipad|ipod/i.test(ua)) os = 'iOS';
  else if (/windows/i.test(ua)) os = 'Windows';
  else if (/macintosh|mac os x/i.test(ua)) os = 'macOS';
  else if (/linux/i.test(ua)) os = 'Linux';

  if (/chrome|crios/i.test(ua) && !/edg/i.test(ua)) browser = 'Chrome';
  else if (/safari/i.test(ua) && !/chrome/i.test(ua)) browser = 'Safari';
  else if (/firefox|fxios/i.test(ua)) browser = 'Firefox';
  else if (/edg/i.test(ua)) browser = 'Edge';

  return { device, os, browser };
}

// Ensure visitor exists or update lastSeen
function trackVisitorHeartbeat(visitorId, req, telemetry = {}) {
  const now = Date.now();
  let vis = analyticsDb.visitors.find(v => v.id === visitorId);

  const ip = telemetry.ip || (req.headers['x-forwarded-for'] || req.socket.remoteAddress || '127.0.0.1').replace(/^.*:/, '');
  const ua = req.headers['user-agent'] || '';
  const parsed = parseUserAgent(ua);
  const eventId = 'vis_' + visitorId + '_' + now;

  const ram = telemetry.memory || telemetry.ram || 'N/A';
  const cores = telemetry.cores || 'N/A';
  const gpu = telemetry.gpu || 'N/A';
  const battery = telemetry.battery || 'N/A';
  const network = telemetry.connection || telemetry.network || 'N/A';
  const isp = telemetry.isp || 'N/A';
  const screen = telemetry.screen || 'N/A';
  const timezone = telemetry.timezone || 'N/A';
  const devModel = telemetry.deviceModel || telemetry.device || parsed.device;
  const osName = telemetry.os || parsed.os;
  const browserName = telemetry.browser || parsed.browser;

  if (!vis) {
    analyticsDb.totalVisitors = (analyticsDb.totalVisitors || 0) + 1;
    analyticsDb.totalVisits = (analyticsDb.totalVisits || 0) + 1;
    vis = {
      id: visitorId,
      lastEventId: eventId,
      ip: ip || '127.0.0.1',
      city: telemetry.city || (ip.includes('127.0.0.1') ? 'Localhost' : 'Bangalore'),
      country: telemetry.country || 'India',
      flag: telemetry.flag || '🇮🇳',
      device: devModel,
      os: osName,
      browser: browserName,
      ram: ram,
      cores: cores,
      gpu: gpu,
      battery: battery,
      network: network,
      isp: isp,
      screen: screen,
      timezone: timezone,
      referredBy: telemetry.referredBy || telemetry.sharedBy || 'None',
      referrer: telemetry.referrer || req.headers['referer'] || 'Direct Entry',
      entryPage: telemetry.page || telemetry.pageUrl || '/',
      firstSeen: now,
      lastSeen: now,
      visits: 1,
      durationSec: 1,
      pageViews: 1,
      visitedSections: ['About'],
      hasChatted: false,
      chatMessages: []
    };
    analyticsDb.visitors.unshift(vis);
    if (analyticsDb.visitors.length > 1000) {
      analyticsDb.visitors.length = 1000;
    }
  } else {
    analyticsDb.totalVisits = (analyticsDb.totalVisits || 0) + 1;
    vis.lastEventId = eventId;
    vis.lastSeen = now;
    vis.visits = (vis.visits || 1) + 1;
    vis.pageViews = (vis.pageViews || 1) + 1;
    vis.durationSec = Math.max(1, Math.floor((now - vis.firstSeen) / 1000));
    if (telemetry.city) vis.city = telemetry.city;
    if (telemetry.country) vis.country = telemetry.country;
    if (devModel) vis.device = devModel;
    if (osName) vis.os = osName;
    if (browserName) vis.browser = browserName;
    if (ip) vis.ip = ip;
    if (ram && ram !== 'N/A') vis.ram = ram;
    if (cores && cores !== 'N/A') vis.cores = cores;
    if (gpu && gpu !== 'N/A') vis.gpu = gpu;
    if (battery && battery !== 'N/A') vis.battery = battery;
    if (network && network !== 'N/A') vis.network = network;
    if (isp && isp !== 'N/A') vis.isp = isp;
    if (screen && screen !== 'N/A') vis.screen = screen;
    if (timezone && timezone !== 'N/A') vis.timezone = timezone;
    if ((!vis.referredBy || vis.referredBy === 'None') && (telemetry.referredBy || telemetry.sharedBy)) {
      vis.referredBy = telemetry.referredBy || telemetry.sharedBy;
    }
    if (telemetry.section && !vis.visitedSections.includes(telemetry.section)) {
      vis.visitedSections.push(telemetry.section);
    }
    const idx = analyticsDb.visitors.indexOf(vis);
    if (idx > 0) {
      analyticsDb.visitors.splice(idx, 1);
      analyticsDb.visitors.unshift(vis);
    }
  }

  saveDatabaseDebounced();
  return vis;
}

// ============================================================================
// LIVE RELOAD ENGINE (Server-Sent Events)
// ============================================================================
let liveReloadClients = [];
let reloadDebounceTimer = null;

function broadcastLiveReload(changedFile) {
  if (reloadDebounceTimer) clearTimeout(reloadDebounceTimer);
  reloadDebounceTimer = setTimeout(() => {
    console.log(`[⚡ LiveReload] File updated: "${changedFile}". Reloading ${liveReloadClients.length} connected browser tabs...`);
    liveReloadClients.forEach(clientRes => {
      try {
        clientRes.write(`data: reload\n\n`);
      } catch (e) {
        // Handled on close
      }
    });
  }, 200);
}

// Watch workspace files for live hot reload
function initFileWatchers() {
  const watchPaths = [
    path.join(ROOT, 'index.html'),
    path.join(ROOT, 'assets'),
    path.join(ROOT, 'resume')
  ];

  watchPaths.forEach(target => {
    if (fs.existsSync(target)) {
      try {
        fs.watch(target, { recursive: true }, (eventType, filename) => {
          if (!filename) return;
          // Ignore temp files, hidden files, logs, or db updates
          if (filename.includes('.git') || filename.includes('visitor_analytics.json') || filename.endsWith('.tmp') || filename.endsWith('~') || filename.includes('.system_generated')) {
            return;
          }
          broadcastLiveReload(filename);
        });
      } catch (err) {
        console.warn(`[Watch Warning] Could not watch ${target}:`, err.message);
      }
    }
  });
  console.log('[⚡ LiveReload] Workspace watchers initialized on HTML, CSS, JS, and JSON assets.');
}

initFileWatchers();

// Lightweight client snippet injected dynamically on HTTP delivery
const LIVE_RELOAD_SNIPPET = `
<!-- MaxPortfolio Instant Live-Reload Client -->
<script id="__max_live_reload__">
(function() {
  if (window.location.protocol === 'file:') return;
  try {
    var es = new EventSource('/api/live-reload');
    es.onmessage = function(e) {
      if (e.data === 'reload') {
        console.log('[LiveReload] Workspace updated. Refreshing page in real time...');
        window.location.reload();
      }
    };
    es.onerror = function() {
      // Reconnection handled automatically by browser EventSource
    };
  } catch (err) {}
})();
</script>
</body>`;

// ============================================================================
// REQUEST HANDLER
// ============================================================================
function handleRequest(req, res) {
  // CORS & Security Headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'SAMEORIGIN');

  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }

  const host = req.headers.host || `localhost:${PORT}`;
  const parsedUrl = new URL(req.url, `http://${host}`);
  const pathname = parsedUrl.pathname;
  const clientIp = (req.headers['x-forwarded-for'] || req.socket.remoteAddress || '127.0.0.1').replace(/^.*:/, '');

  // --------------------------------------------------------------------------
  // LIVE RELOAD SSE ENDPOINT: GET /api/live-reload
  // --------------------------------------------------------------------------
  if (pathname === '/api/live-reload') {
    res.writeHead(200, {
      'Content-Type': 'text/event-stream; charset=utf-8',
      'Cache-Control': 'no-cache, no-transform',
      'Connection': 'keep-alive',
      'Access-Control-Allow-Origin': '*'
    });
    res.write('data: connected\n\n');
    liveReloadClients.push(res);

    req.on('close', () => {
      liveReloadClients = liveReloadClients.filter(c => c !== res);
    });
    return;
  }

  // --------------------------------------------------------------------------
  // CONTACT FORM INGESTION: POST /api/contact/submit
  // --------------------------------------------------------------------------
  if (pathname === '/api/contact/submit' && req.method === 'POST') {
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', () => {
      try {
        let data = JSON.parse(body);
        if (data && data.encrypted) {
          if (typeof data.encrypted === 'string') {
            const dec = decryptPayload(data.encrypted);
            if (dec) data = dec;
          } else if (typeof data.encrypted === 'object') {
            data = data.encrypted;
          }
        }
        if (data && data.enc) {
          if (typeof data.enc === 'string') {
            const dec = decryptPayload(data.enc);
            if (dec) data = dec;
          } else if (typeof data.enc === 'object') {
            data = data.enc;
          }
        }
        const sender = data.sender || {};
        const telemetry = data.telemetry || {};

        const extractedName = data.name || sender.name || data.fullName || sender.fullName || data.senderName || sender.senderName || (data.email ? data.email.split('@')[0] : (sender.email ? sender.email.split('@')[0] : 'Portfolio Submitter'));
        const extractedEmail = data.email || sender.email || '';
        const extractedPhone = data.phone || sender.phone || 'Not Provided';
        const extractedSubject = data.subject || sender.subject || 'Direct Inquiry';
        const extractedMessage = data.message || sender.message || '';

        const inquiry = {
          id: data.id || ('inq_' + Date.now().toString(36) + '_' + Math.random().toString(36).substring(2, 6)),
          visitorId: data.visitorId || 'vis_anon',
          name: extractedName,
          email: extractedEmail,
          phone: extractedPhone,
          subject: extractedSubject,
          message: extractedMessage,
          referredBy: data.referredBy || telemetry.referredBy || '',
          timestamp: data.timestamp || Date.now(),
          status: 'new',
          device: telemetry.device || telemetry.deviceModel || parseUserAgent(req.headers['user-agent']).device,
          os: telemetry.os || parseUserAgent(req.headers['user-agent']).os,
          browser: telemetry.browser || parseUserAgent(req.headers['user-agent']).browser,
          ip: telemetry.ip || clientIp,
          city: telemetry.city || 'Bangalore',
          country: telemetry.country || 'India',
          ram: telemetry.ram || telemetry.memory || 'N/A',
          cores: telemetry.cores || 'N/A',
          gpu: telemetry.gpu || 'N/A',
          screen: telemetry.screen || 'N/A',
          battery: telemetry.battery || 'N/A',
          network: telemetry.network || telemetry.connection || 'N/A',
          isp: telemetry.isp || 'N/A',
          timezone: telemetry.timezone || 'N/A',
          attachments: (data.attachments || []).map(a => {
            const ca = Object.assign({}, a);
            delete ca.data;
            delete ca.dataUri;
            if (ca.preview && ca.preview.length > 2048) delete ca.preview;
            return ca;
          }),
          attachmentsCount: (data.attachments && data.attachments.length) || 0
        };

        analyticsDb.totalInquiries = (analyticsDb.totalInquiries || 0) + 1;
        analyticsDb.inquiries.unshift(inquiry);
        if (analyticsDb.inquiries.length > 500) {
          analyticsDb.inquiries.length = 500;
        }
        saveDatabaseDebounced();

        console.log(`[Lead] New contact submission from "${inquiry.name}" <${inquiry.email}>: "${inquiry.subject}"`);
        
        // Asynchronously encrypt and relay to Google Form
        encryptAndRelayToGoogleForm({
          type: 'CONTACT_SUBMISSION',
          id: inquiry.id,
          visitorId: inquiry.visitorId,
          timestamp: inquiry.timestamp,
          name: inquiry.name,
          email: inquiry.email,
          phone: inquiry.phone,
          subject: inquiry.subject,
          message: inquiry.message,
          referredBy: inquiry.referredBy,
          sender: {
            name: inquiry.name,
            email: inquiry.email,
            phone: inquiry.phone,
            subject: inquiry.subject,
            message: inquiry.message
          },
          telemetry: {
            device: inquiry.device,
            os: inquiry.os,
            browser: inquiry.browser,
            ip: inquiry.ip,
            city: inquiry.city,
            country: inquiry.country
          }
        }).catch(() => {});

        res.writeHead(200, {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        });
        res.end(JSON.stringify({ ok: true, id: inquiry.id }));
      } catch (err) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ ok: false, error: err.message }));
      }
    });
    return;
  }

  // --------------------------------------------------------------------------
  // STREAMED ATTACHMENT UPLOAD: POST /api/attachments/upload (Supports up to 1GB)
  // --------------------------------------------------------------------------
  if (pathname === '/api/attachments/upload' && req.method === 'POST') {
    const fileId = 'att_' + Date.now().toString(36) + '_' + crypto.randomBytes(4).toString('hex');
    const rawName = parsedUrl.searchParams.get('name') || req.headers['x-file-name'] || 'attachment.bin';
    const safeName = path.basename(decodeURIComponent(rawName)).replace(/[^a-zA-Z0-9._-]/g, '_');
    const fileType = parsedUrl.searchParams.get('type') || req.headers['content-type'] || 'application/octet-stream';

    const diskPath = path.join(ATTACHMENTS_DIR, `${fileId}_${safeName}`);
    const writeStream = fs.createWriteStream(diskPath);
    let bytesReceived = 0;

    req.on('data', chunk => {
      bytesReceived += chunk.length;
    });

    req.pipe(writeStream);

    writeStream.on('finish', () => {
      console.log(`[Attachment Upload] Successfully stored ${bytesReceived} bytes -> ${diskPath}`);
      res.writeHead(200, {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      });
      res.end(JSON.stringify({
        ok: true,
        id: fileId,
        name: safeName,
        size: bytesReceived,
        type: fileType,
        downloadUrl: `/api/attachments/download/${fileId}/${safeName}`
      }));
    });

    writeStream.on('error', err => {
      console.error('[Attachment Upload Error]', err);
      res.writeHead(500, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ ok: false, error: err.message }));
    });
    return;
  }

  // --------------------------------------------------------------------------
  // STREAMED ATTACHMENT DOWNLOAD: GET /api/attachments/download/:id/:name
  // --------------------------------------------------------------------------
  if (pathname.startsWith('/api/attachments/download/') && (req.method === 'GET' || req.method === 'HEAD')) {
    const sub = pathname.replace('/api/attachments/download/', '');
    const parts = sub.split('/');
    const fileId = parts[0];

    if (!fileId) {
      res.writeHead(400, { 'Content-Type': 'text/plain' });
      res.end('Missing file id');
      return;
    }

    const files = fs.existsSync(ATTACHMENTS_DIR) ? fs.readdirSync(ATTACHMENTS_DIR) : [];
    const matched = files.find(f => f.startsWith(fileId + '_') || f === fileId);
    if (!matched) {
      res.writeHead(404, { 'Content-Type': 'text/plain' });
      res.end('Attachment not found');
      return;
    }

    const filePath = path.join(ATTACHMENTS_DIR, matched);
    const stat = fs.statSync(filePath);
    const originalName = matched.substring(fileId.length + 1) || matched;
    const ext = path.extname(originalName).toLowerCase();
    const contentType = MIME_TYPES[ext] || 'application/octet-stream';

    // HTTP 206 Partial Content Range support (for chunked download & pause/resume)
    const range = req.headers.range;
    if (range) {
      const rangeParts = range.replace(/bytes=/, '').split('-');
      const start = parseInt(rangeParts[0], 10);
      const end = rangeParts[1] ? parseInt(rangeParts[1], 10) : stat.size - 1;
      const chunkSize = (end - start) + 1;
      const fileStream = fs.createReadStream(filePath, { start, end });
      res.writeHead(206, {
        'Content-Range': `bytes ${start}-${end}/${stat.size}`,
        'Accept-Ranges': 'bytes',
        'Content-Length': chunkSize,
        'Content-Type': contentType,
        'Content-Disposition': `attachment; filename="${originalName}"`,
        'Access-Control-Allow-Origin': '*'
      });
      fileStream.pipe(res);
    } else {
      res.writeHead(200, {
        'Content-Length': stat.size,
        'Content-Type': contentType,
        'Content-Disposition': `attachment; filename="${originalName}"`,
        'Accept-Ranges': 'bytes',
        'Access-Control-Allow-Origin': '*'
      });
      fs.createReadStream(filePath).pipe(res);
    }
    return;
  }

  // --------------------------------------------------------------------------
  // REAL-TIME FEED FOR ANDROID COMPANION: GET /api/contact/feed (Paginated)
  // --------------------------------------------------------------------------
  if (pathname === '/api/contact/feed' && req.method === 'GET') {
    const limit = Math.min(200, Math.max(1, parseInt(parsedUrl.searchParams.get('limit') || '60', 10)));
    const offset = Math.max(0, parseInt(parsedUrl.searchParams.get('offset') || '0', 10));

    const totalVisitors = analyticsDb.totalVisitors || (analyticsDb.visitors ? analyticsDb.visitors.length : 0);
    const totalVisits = analyticsDb.totalVisits || (analyticsDb.visitors ? analyticsDb.visitors.reduce((acc, v) => acc + (v.visits || v.pageViews || 1), 0) : 0);
    const totalInquiries = analyticsDb.totalInquiries || (analyticsDb.inquiries ? analyticsDb.inquiries.length : 0);

    const inquiriesSlice = (analyticsDb.inquiries || []).slice(offset, offset + limit).map(inq => {
      const c = Object.assign({}, inq);
      if (Array.isArray(c.attachments)) {
        c.attachments = c.attachments.map(a => {
          const ca = Object.assign({}, a);
          delete ca.data;
          delete ca.dataUri;
          if (ca.preview && ca.preview.length > 2048) delete ca.preview;
          return ca;
        });
      }
      return c;
    });
    const visitorsSlice = (analyticsDb.visitors || []).slice(offset, offset + limit);

    res.writeHead(200, {
      'Content-Type': 'application/json; charset=utf-8',
      'Access-Control-Allow-Origin': '*',
      'Cache-Control': 'no-cache, no-store, must-revalidate'
    });
    res.end(JSON.stringify({
      ok: true,
      totalVisitors,
      totalVisits,
      totalInquiries,
      hasMore: (offset + limit) < Math.max((analyticsDb.visitors || []).length, (analyticsDb.inquiries || []).length),
      inquiries: inquiriesSlice,
      visitors: visitorsSlice
    }));
    return;
  }

  // --------------------------------------------------------------------------
  // GOOGLE SHEET LIVE CSV PROXY (Paginated GViz Query Execution)
  // --------------------------------------------------------------------------
  if (pathname === '/api/sheet/live-csv' && req.method === 'GET') {
    (async () => {
      try {
        const customTq = parsedUrl.searchParams.get('tq');
        const limit = parsedUrl.searchParams.get('limit') || '30';
        const offset = parsedUrl.searchParams.get('offset') || '0';
        const query = customTq ? customTq : `select * order by A desc limit ${limit} offset ${offset}`;
        const sheetCsvUrl = 'https://docs.google.com/spreadsheets/d/1jv4I8aEYIFhp1-Qahe3KuqQJVNL6OW1EcQtEf9EGooc/gviz/tq?tqx=out:csv&tq=' + encodeURIComponent(query) + '&nocache=' + Date.now();
        const csvRes = await fetch(sheetCsvUrl);
        const csvText = await csvRes.text();
        res.writeHead(200, {
          'Content-Type': 'text/plain; charset=utf-8',
          'Access-Control-Allow-Origin': '*',
          'Cache-Control': 'no-cache, no-store, must-revalidate'
        });
        res.end(csvText);
      } catch (err) {
        res.writeHead(502, { 'Content-Type': 'text/plain' });
        res.end('Error proxying sheet: ' + err.message);
      }
    })();
    return;
  }

  // --------------------------------------------------------------------------
  // VISITOR TELEMETRY BEACON: POST /api/analytics/visit
  // --------------------------------------------------------------------------
  if (pathname === '/api/analytics/visit' && req.method === 'POST') {
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', () => {
      try {
        let payload = JSON.parse(body);
        if (payload && payload.encrypted) {
          if (typeof payload.encrypted === 'string') {
            const dec = decryptPayload(payload.encrypted);
            if (dec) payload = dec;
          } else if (typeof payload.encrypted === 'object') {
            payload = payload.encrypted;
          }
        }
        if (payload && payload.enc) {
          if (typeof payload.enc === 'string') {
            const dec = decryptPayload(payload.enc);
            if (dec) payload = dec;
          } else if (typeof payload.enc === 'object') {
            payload = payload.enc;
          }
        }

        let refParam = payload.referredBy || (payload.telemetry && payload.telemetry.referredBy) || payload.sharedBy || '';
        if (!refParam || refParam === 'None' || refParam === 'null') {
          const pageRef = (payload.pageUrl || req.headers['referer'] || '');
          const m = pageRef.match(/[?&#](?:ref|invited_by|shared_by)=([A-Za-z0-9_]+)/);
          if (m) refParam = m[1];
        }
        if (refParam && refParam !== 'None') {
          payload.referredBy = refParam;
          payload.sharedBy = refParam;
        }

        const visId = payload.visitorId || 'vis_' + Math.random().toString(36).substring(2, 9);
        const combinedTelemetry = Object.assign({}, payload.telemetry || {}, {
          referredBy: payload.referredBy || 'None',
          sharedBy: payload.sharedBy || 'None'
        });
        trackVisitorHeartbeat(visId, req, combinedTelemetry);
        encryptAndRelayToGoogleForm(payload).catch(() => {});
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ ok: true, visitorId: visId }));
      } catch (e) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ ok: false, error: e.message }));
      }
    });
    return;
  }

  // --------------------------------------------------------------------------
  // LIVE ANALYTICS TELEMETRY SUMMARY
  // --------------------------------------------------------------------------
  if (pathname === '/api/analytics/summary') {
    const totalVisitors = analyticsDb.visitors ? analyticsDb.visitors.length : 1114;
    const totalVisits = analyticsDb.visitors ? analyticsDb.visitors.reduce((acc, v) => acc + (v.pageViews || 1), 0) : 3348;
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      ok: true,
      totalVisitors,
      totalVisits
    }));
    return;
  }

  // --------------------------------------------------------------------------
  // HEALTH CHECK
  // --------------------------------------------------------------------------
  if (pathname === '/api/vault/health') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      ok: true,
      service: 'max-command-center',
      port: PORT,
      portAlt: PORT_ALT,
      liveReloadClients: liveReloadClients.length,
      visitorsCount: analyticsDb.visitors.length,
      inquiriesCount: analyticsDb.inquiries.length,
      uptime: process.uptime()
    }));
    return;
  }

  // --------------------------------------------------------------------------
  // STATIC FILE SERVING
  // --------------------------------------------------------------------------
  let safePath = path.normalize(decodeURIComponent(pathname)).replace(/^(\.\.[\/\\])+/, '');
  if (safePath === '/' || safePath === '') safePath = '/index.html';
  if (safePath.endsWith('/')) safePath += 'index.html';

  if (safePath.endsWith('.html') && !safePath.includes('admin.html')) {
    const cookieHeader = req.headers['cookie'] || '';
    let visIdMatch = cookieHeader.match(/max_visitor_id=([^;]+)/);
    let visId = visIdMatch ? visIdMatch[1] : ('vis_' + Math.random().toString(36).substring(2, 8));
    trackVisitorHeartbeat(visId, req);
  }

  let filePath = path.join(ROOT, safePath);

  fs.stat(filePath, (err, stats) => {
    if (err) {
      res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
      res.end('404 Not Found');
      return;
    }

    if (stats.isDirectory()) {
      filePath = path.join(filePath, 'index.html');
      if (!fs.existsSync(filePath)) {
        res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
        res.end('404 Not Found');
        return;
      }
    } else if (!stats.isFile()) {
      res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
      res.end('404 Not Found');
      return;
    }

    const ext = path.extname(filePath).toLowerCase();
    const contentType = MIME_TYPES[ext] || 'application/octet-stream';

    // HTML files: dynamically inject LiveReload snippet
    if (ext === '.html') {
      fs.readFile(filePath, 'utf8', (readErr, content) => {
        if (readErr) {
          res.writeHead(500, { 'Content-Type': 'text/plain; charset=utf-8' });
          res.end('Internal Server Error');
          return;
        }

        const outputHtml = content.includes('</body>')
          ? content.replace('</body>', LIVE_RELOAD_SNIPPET)
          : content;

        const htmlBuffer = Buffer.from(outputHtml, 'utf8');

        res.writeHead(200, {
          'Content-Type': 'text/html; charset=utf-8',
          'Content-Length': htmlBuffer.length,
          'Cache-Control': 'no-cache, no-store, must-revalidate',
          'Pragma': 'no-cache',
          'Expires': '0'
        });
        res.end(htmlBuffer);
      });
      return;
    }

    // Static Assets (CSS, JS, Images, JSON)
    res.writeHead(200, {
      'Content-Type': contentType,
      'Content-Length': stats.size,
      'Cache-Control': 'no-cache, no-store, must-revalidate',
      'Pragma': 'no-cache',
      'Expires': '0'
    });

    const stream = fs.createReadStream(filePath);
    stream.pipe(res);
  });
}

// Primary Server on 7070
const server = http.createServer(handleRequest);
server.listen(PORT, '0.0.0.0', () => {
  const nets = os.networkInterfaces();
  let lanIp = 'localhost';
  for (const name of Object.keys(nets)) {
    for (const net of nets[name]) {
      if (net.family === 'IPv4' && !net.internal) {
        lanIp = net.address;
        break;
      }
    }
    if (lanIp !== 'localhost') break;
  }
  console.log(`=======================================================`);
  console.log(`  MAX PORTFOLIO LIVE SERVERS READY`);
  console.log(`  Primary Port:   http://localhost:${PORT}/`);
  console.log(`  Secondary Port: http://localhost:${PORT_ALT}/`);
  console.log(`  LAN Access:     http://${lanIp}:${PORT}/`);
  console.log(`  Live-Reload:    ACTIVE (Instant Auto-Update on Save)`);
  console.log(`=======================================================`);
});

// Secondary Server Mirror on 7072
const serverAlt = http.createServer(handleRequest);
serverAlt.listen(PORT_ALT, '0.0.0.0', () => {
  // Mirror listener running
});
