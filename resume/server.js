const http = require('http');
const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

const PORT = 8080;
const HOST = '0.0.0.0';
const BASE_DIR = __dirname;

const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.pdf': 'application/pdf',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
  '.woff2': 'font/woff2',
  '.woff': 'font/woff',
  '.ttf': 'font/ttf'
};

const server = http.createServer((req, res) => {
  // Enable CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }

  const url = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
  let pathname = decodeURIComponent(url.pathname);

  // API endpoint to save resume.json and auto-regenerate PDF & PNG
  if (req.method === 'POST' && pathname === '/api/save') {
    let body = '';
    req.on('data', chunk => {
      body += chunk;
      if (body.length > 2 * 1024 * 1024) { // 2MB limit
        req.destroy();
      }
    });

    req.on('end', () => {
      try {
        const parsed = JSON.parse(body);
        const jsonFormatted = JSON.stringify(parsed, null, 2);

        // 1. Write resume.json
        fs.writeFileSync(path.join(BASE_DIR, 'resume.json'), jsonFormatted, 'utf8');

        // 2. Write resume-data.js
        const jsFormatted = `// Auto-generated data layer\nwindow.RESUME_DATA = ${jsonFormatted};\n`;
        fs.writeFileSync(path.join(BASE_DIR, 'resume-data.js'), jsFormatted, 'utf8');

        console.log('📝 resume.json & resume-data.js updated by client');

        // 3. Trigger generate_exports.js in background
        exec('node generate_exports.js', { cwd: BASE_DIR }, (err, stdout, stderr) => {
          if (err) {
            console.error('Export regeneration error:', err);
          } else {
            console.log('✨ Regenerated PDF & PNG successfully');
          }
        });

        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ success: true, message: 'Resume saved and PDF/PNG regenerating!' }));
      } catch (err) {
        console.error('Error saving resume:', err);
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ success: false, error: err.message }));
      }
    });
    return;
  }

  // Default to index.html
  if (pathname === '/') {
    pathname = '/index.html';
  }

  // Security check: prevent directory traversal
  const safePath = path.normalize(pathname).replace(/^(\.\.[\/\\])+/, '');
  const filePath = path.join(BASE_DIR, safePath);

  if (!filePath.startsWith(BASE_DIR)) {
    res.writeHead(403, { 'Content-Type': 'text/plain' });
    res.end('403 Forbidden');
    return;
  }

  fs.stat(filePath, (err, stats) => {
    if (err || !stats.isFile()) {
      res.writeHead(404, { 'Content-Type': 'text/plain' });
      res.end('404 Not Found');
      return;
    }

    const ext = path.extname(filePath).toLowerCase();
    const contentType = MIME_TYPES[ext] || 'application/octet-stream';

    // Prevent caching for live-editing files
    res.setHeader('Cache-Control', 'no-cache, no-store, must-revalidate');
    res.writeHead(200, { 'Content-Type': contentType });

    const stream = fs.createReadStream(filePath);
    stream.pipe(res);
  });
});

server.listen(PORT, HOST, () => {
  console.log('====================================================');
  console.log(`🚀 Mahendra Mali Resume Server is LIVE!`);
  console.log(`🌐 Local:   http://localhost:${PORT}`);
  console.log(`📡 Network: http://10.0.0.187:${PORT}`);
  console.log(`⚡ Port:    ${PORT}`);
  console.log('====================================================');
});
