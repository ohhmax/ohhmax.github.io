const http = require('http');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const zlib = require('zlib');

const PORT = 7071;
const APK_PATH = path.join(__dirname, 'build/bin/MaxHive-Intelligence.apk');
const APK_FILENAME = 'MaxHive-Intelligence.apk';
const APK_SHA256 = '376264eef70711e3c38d792ee5b0544178cf327f4fb59081218a77120d28ea24';
const DB_PATH = '/home/max/Projects/MyPortfolio-2026/data/visitor_analytics.json';
const ATTACHMENTS_DIR = path.join(__dirname, '..', 'data', 'attachments');
if (!fs.existsSync(ATTACHMENTS_DIR)) {
  try { fs.mkdirSync(ATTACHMENTS_DIR, { recursive: true }); } catch (e) {}
}

const MASTER_SECRET = 'MaxPortfolio2026@SecureMasterKey!';
const GOOGLE_FORM_URL = 'https://docs.google.com/forms/d/e/1FAIpQLSd3Wx27Aw9308pzORR2FZ_e6VKd--hs8gDbhlxMNIV-TNtyAA/formResponse';
const GOOGLE_FIELD_ENTRY = 'entry.132983276';
const RSA_PUB_PATH = path.join(__dirname, '..', 'data', 'keys', 'max_public_key.pem');
const RSA_PRIV_PATH = path.join(__dirname, '..', 'data', 'keys', 'max_private_key.pem');

async function encryptAndRelayToGoogleForm(payload) {
  try {
    const jsonStr = JSON.stringify(payload);
    const compressed = zlib.gzipSync(Buffer.from(jsonStr, 'utf-8'));
    let armored = null;

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
        console.warn('[GooglePipeline] Asymmetric relay warning:', e.message);
      }
    }

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

const server = http.createServer((req, res) => {
  const host = req.headers.host || `localhost:${PORT}`;
  const parsedUrl = new URL(req.url, `http://${host}`);
  const urlPath = parsedUrl.pathname;

  // API: Real-time feed for Android companion (Paginated)
  if (urlPath === '/api/contact/feed' && req.method === 'GET') {
    let inquiries = [];
    let visitors = [];
    let totalVisitors = 0;
    let totalVisits = 0;
    let totalInquiries = 0;

    try {
      if (fs.existsSync(DB_PATH)) {
        const raw = JSON.parse(fs.readFileSync(DB_PATH, 'utf8'));
        inquiries = raw.inquiries || [];
        visitors = raw.visitors || [];
        totalVisitors = raw.totalVisitors || visitors.length;
        totalVisits = raw.totalVisits || visitors.reduce((acc, v) => acc + (v.visits || v.pageViews || 1), 0);
        totalInquiries = raw.totalInquiries || inquiries.length;
      }
    } catch (e) {}

    const limit = Math.min(200, Math.max(1, parseInt(parsedUrl.searchParams.get('limit') || '60', 10)));
    const offset = Math.max(0, parseInt(parsedUrl.searchParams.get('offset') || '0', 10));

    const inquiriesSlice = inquiries.slice(offset, offset + limit).map(inq => {
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
    const visitorsSlice = visitors.slice(offset, offset + limit);

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
      hasMore: (offset + limit) < Math.max(visitors.length, inquiries.length),
      inquiries: inquiriesSlice,
      visitors: visitorsSlice
    }));
    return;
  }

  // API: Google Sheet Live CSV Proxy (Paginated GViz Query Execution)
  if (urlPath === '/api/sheet/live-csv' && req.method === 'GET') {
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

  // API: Streamed file attachment upload (Supports up to 1GB)
  if (urlPath === '/api/attachments/upload' && req.method === 'POST') {
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
      console.log(`[Attachment Upload 7071] Stored ${bytesReceived} bytes -> ${diskPath}`);
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
      res.writeHead(500, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ ok: false, error: err.message }));
    });
    return;
  }


  // API: Streamed file attachment download with HTTP Range support
  if (urlPath.startsWith('/api/attachments/download/') && (req.method === 'GET' || req.method === 'HEAD')) {
    const sub = urlPath.replace('/api/attachments/download/', '');
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
    const range = req.headers.range;

    if (range) {
      const rangeParts = range.replace(/bytes=/, '').split('-');
      const start = parseInt(rangeParts[0], 10);
      const end = rangeParts[1] ? parseInt(rangeParts[1], 10) : stat.size - 1;
      const chunkSize = (end - start) + 1;
      res.writeHead(206, {
        'Content-Range': `bytes ${start}-${end}/${stat.size}`,
        'Accept-Ranges': 'bytes',
        'Content-Length': chunkSize,
        'Content-Type': 'application/octet-stream',
        'Content-Disposition': `attachment; filename="${originalName}"`,
        'Access-Control-Allow-Origin': '*'
      });
      fs.createReadStream(filePath, { start, end }).pipe(res);
    } else {
      res.writeHead(200, {
        'Content-Length': stat.size,
        'Content-Type': 'application/octet-stream',
        'Content-Disposition': `attachment; filename="${originalName}"`,
        'Accept-Ranges': 'bytes',
        'Access-Control-Allow-Origin': '*'
      });
      fs.createReadStream(filePath).pipe(res);
    }
    return;
  }


  // API: Ingestion relay
  if (urlPath === '/api/contact/submit' && req.method === 'POST') {
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', () => {
      try {
        let data = JSON.parse(body);
        if (data && data.encrypted) {
          if (typeof data.encrypted === 'object') {
            data = data.encrypted;
          }
        }
        if (data && data.enc) {
          if (typeof data.enc === 'object') {
            data = data.enc;
          }
        }
        const sender = data.sender || {};
        const telemetry = data.telemetry || {};
        const extractedName = data.name || sender.name || data.fullName || sender.fullName || data.senderName || (data.email ? data.email.split('@')[0] : (sender.email ? sender.email.split('@')[0] : 'Portfolio Submitter'));

        if (fs.existsSync(DB_PATH)) {
          try {
            const raw = JSON.parse(fs.readFileSync(DB_PATH, 'utf8'));
            if (!raw.inquiries) raw.inquiries = [];
            const inquiry = {
              id: data.id || ('inq_' + Date.now().toString(36) + '_' + Math.random().toString(36).substring(2, 6)),
              visitorId: data.visitorId || 'vis_anon',
              name: extractedName,
              email: data.email || sender.email || 'No email provided',
              phone: data.phone || sender.phone || 'Not Provided',
              subject: data.subject || sender.subject || 'Direct Inquiry',
              message: data.message || sender.message || '',
              referredBy: data.referredBy || telemetry.referredBy || '',
              timestamp: data.timestamp || Date.now(),
              status: 'new',
              device: telemetry.device || telemetry.deviceModel || 'Mobile',
              os: telemetry.os || 'Android',
              browser: telemetry.browser || 'Browser',
              ip: telemetry.ip || '127.0.0.1',
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
            raw.inquiries.unshift(inquiry);
            fs.writeFileSync(DB_PATH, JSON.stringify(raw, null, 2), 'utf8');
          } catch (e) {}
        }

        encryptAndRelayToGoogleForm(data).catch(() => {});
        res.writeHead(200, {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        });
        res.end(JSON.stringify({ ok: true }));
      } catch (e) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ ok: false, error: e.message }));
      }
    });
    return;
  }


  // Direct APK download routes
  if (
    urlPath === '/' + APK_FILENAME ||
    urlPath === '/app.apk' ||
    urlPath === '/download' ||
    urlPath.endsWith('.apk')
  ) {
    if (!fs.existsSync(APK_PATH)) {
      res.writeHead(404, { 'Content-Type': 'text/plain' });
      res.end('APK file not found on server.');
      return;
    }

    const stat = fs.statSync(APK_PATH);
    res.writeHead(200, {
      'Content-Type': 'application/vnd.android.package-archive',
      'Content-Disposition': `attachment; filename="${APK_FILENAME}"`,
      'Content-Length': stat.size,
      'Cache-Control': 'no-cache',
      'Access-Control-Allow-Origin': '*'
    });

    const stream = fs.createReadStream(APK_PATH);
    stream.pipe(res);
    return;
  }


  // Web Download Portal Landing Page
  const stat = fs.existsSync(APK_PATH) ? fs.statSync(APK_PATH) : { size: 151552 };
  const sizeKb = (stat.size / 1024).toFixed(1);

  const downloadUrl = `http://${host}/${APK_FILENAME}`;
  const qrUrl = `https://api.qrserver.com/v1/create-qr-code/?size=180x180&data=${encodeURIComponent(downloadUrl)}&bgcolor=0c121e&color=38bdf8`;

  const html = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MaxHive Intelligence - Android Companion</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: #080c14 radial-gradient(circle at 50% 20%, rgba(14, 165, 233, 0.12), transparent 70%);
      color: #F1F5F9;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 24px;
      -webkit-font-smoothing: antialiased;
    }
    .card {
      background: rgba(15, 23, 42, 0.75);
      backdrop-filter: blur(24px);
      -webkit-backdrop-filter: blur(24px);
      border: 1px solid rgba(56, 189, 248, 0.2);
      border-radius: 28px;
      max-width: 420px;
      width: 100%;
      padding: 40px 28px;
      box-shadow: 0 25px 60px -15px rgba(0, 0, 0, 0.7), 0 0 40px rgba(14, 165, 233, 0.1);
      text-align: center;
      position: relative;
      overflow: hidden;
    }
    .badge-icon {
      width: 76px;
      height: 76px;
      margin: 0 auto 20px;
      background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%);
      border-radius: 22px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 34px;
      color: #FFFFFF;
      font-weight: 800;
      box-shadow: 0 12px 30px rgba(37, 99, 235, 0.4), inset 0 1px 1px rgba(255, 255, 255, 0.3);
    }
    h1 {
      font-size: 24px;
      font-weight: 800;
      color: #F8FAFC;
      letter-spacing: -0.5px;
      margin-bottom: 6px;
    }
    .subtitle {
      color: #94A3B8;
      font-size: 13px;
      font-weight: 500;
      margin-bottom: 22px;
    }
    .pill-group {
      display: flex;
      justify-content: center;
      gap: 8px;
      flex-wrap: wrap;
      margin-bottom: 26px;
    }
    .pill {
      background: rgba(30, 41, 59, 0.8);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 100px;
      padding: 5px 12px;
      font-size: 12px;
      font-weight: 600;
      color: #38BDF8;
      letter-spacing: 0.2px;
    }
    .btn-download {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 10px;
      width: 100%;
      padding: 16px 24px;
      background: linear-gradient(135deg, #0ea5e9 0%, #2563eb 100%);
      color: #FFFFFF;
      font-size: 16px;
      font-weight: 700;
      text-decoration: none;
      border-radius: 16px;
      box-shadow: 0 12px 28px rgba(14, 165, 233, 0.35);
      transition: transform 0.18s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.18s ease;
      cursor: pointer;
    }
    .btn-download:hover {
      transform: translateY(-2px);
      box-shadow: 0 16px 36px rgba(14, 165, 233, 0.5);
    }
    .btn-download:active {
      transform: translateY(0);
    }
    .qr-container {
      margin-top: 28px;
      padding-top: 24px;
      border-top: 1px solid rgba(255, 255, 255, 0.07);
    }
    .qr-box {
      width: 172px;
      height: 172px;
      margin: 0 auto 12px;
      background: #0c121e;
      border: 1px solid rgba(56, 189, 248, 0.25);
      border-radius: 16px;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 6px;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
    }
    .qr-box img {
      width: 160px;
      height: 160px;
      border-radius: 10px;
      display: block;
    }
    .qr-label {
      color: #64748B;
      font-size: 12px;
      font-weight: 500;
    }
    .status-row {
      margin-top: 22px;
      display: inline-flex;
      align-items: center;
      gap: 7px;
      font-size: 12px;
      color: #10B981;
      font-weight: 600;
    }
    .status-dot {
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: #10B981;
      box-shadow: 0 0 10px #10B981;
      display: inline-block;
      animation: pulse 2s infinite;
    }
    @keyframes pulse {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.5; transform: scale(0.9); }
    }
  </style>
</head>
<body>
  <div class="card">
    <div class="badge-icon">M</div>
    <h1>MaxHive Intelligence</h1>
    <p class="subtitle">Material 3 Portfolio Telemetry & Companion</p>

    <div class="pill-group">
      <span class="pill">v2.5.0</span>
      <span class="pill">${sizeKb} KB</span>
      <span class="pill">Android 8.0 - 17</span>
    </div>

    <a href="/${APK_FILENAME}" class="btn-download" download>
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
        <polyline points="7 10 12 15 17 10"></polyline>
        <line x1="12" y1="15" x2="12" y2="3"></line>
      </svg>
      <span>Download APK (${sizeKb} KB)</span>
    </a>

    <div class="qr-container">
      <div class="qr-box">
        <img src="${qrUrl}" alt="Scan QR to download APK" loading="lazy" />
      </div>
      <p class="qr-label">Scan with your phone to download directly</p>
    </div>

    <div class="status-row">
      <span class="status-dot"></span>
      <span>Real-time Ingestion Pipeline Active</span>
    </div>
  </div>
</body>
</html>`;

  res.writeHead(200, {
    'Content-Type': 'text/html; charset=utf-8',
    'Cache-Control': 'no-cache'
  });
  res.end(html);
});

server.listen(PORT, '0.0.0.0', () => {
  console.log(`MaxHive APK server listening on http://0.0.0.0:${PORT}`);
});
