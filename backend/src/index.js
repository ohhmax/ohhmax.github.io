/**
 * ============================================================================
 * CLOUDFLARE WORKER BACKEND - TELEGRAM BOT GATEWAY
 * Designed for Mahendra Mali (Max) Developer Portfolio
 *
 * Capabilities:
 * 1. POST /api/contact: Receives inquiries with optional file attachments,
 *    relays formatted HTML alerts with rich telemetry to Telegram group via Bot API.
 * 2. POST /api/visit: Receives visitor telemetry beacon, extracts Cloudflare edge
 *    geo telemetry (Flag, Country, Region/State, City, Postal, ISP, ASN, Colo, IP)
 *    and client zero-permission device specs (Model, Battery, Network, GPU, Screen),
 *    and delivers alert to Telegram.
 * 3. GET /api/visit-count: Returns total unique visitor count (baseline 1,000).
 * 4. GET /health: Worker health status, mirror registry, and version info.
 *
 * Security:
 * - Zero tokens hardcoded. Reads from Worker environment variables:
 *   env.TELEGRAM_BOT_TOKEN, env.TELEGRAM_CHAT_ID.
 * - Strict CORS headers allowing safe cross-origin requests from all portfolio mirrors.
 * ============================================================================
 */

const PORTFOLIO_VERSION = 'v3.9.2';

const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Requested-With',
  'Access-Control-Max-Age': '86400',
};

// In-memory unique visitor telemetry tracking and rate throttling (baseline matches data/visitor_analytics.json)
let inMemoryVisitorCount = 1000;
const recentVisits = new Map();
const VISIT_THROTTLE_WINDOW_MS = 30 * 60 * 1000; // 30 minutes cooldown

function jsonResponse(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      ...CORS_HEADERS,
      'Content-Type': 'application/json; charset=utf-8',
    },
  });
}

function escapeHtml(text) {
  if (!text) return '';
  return String(text)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}

/**
 * Generates Unicode flag emoji from 2-letter ISO country code
 */
function getCountryFlag(countryCode) {
  if (!countryCode || countryCode === 'Unknown' || countryCode.length !== 2) return '🌐';
  try {
    const codePoints = countryCode
      .toUpperCase()
      .split('')
      .map(char => 127397 + char.charCodeAt(0));
    return String.fromCodePoint(...codePoints);
  } catch (e) {
    return '🌐';
  }
}

/**
 * Resolves full country name from 2-letter ISO country code
 */
function getCountryName(countryCode) {
  if (!countryCode || countryCode === 'Unknown' || countryCode.length !== 2) return countryCode || 'Unknown';
  try {
    const regionNames = new Intl.DisplayNames(['en'], { type: 'region' });
    return regionNames.of(countryCode.toUpperCase()) || countryCode;
  } catch (e) {
    return countryCode;
  }
}

/**
 * Resolves mirror identity badge from hostname or telemetry
 */
function getMirrorBadge(host, mirrorHint) {
  if (mirrorHint && typeof mirrorHint === 'string' && mirrorHint.length > 2) {
    return mirrorHint;
  }
  const h = (host || '').toLowerCase();
  if (h.includes('github.io')) return '🐙 GitHub Pages (ohhmax.github.io)';
  if (h.includes('gitlab.io')) return '🦊 GitLab Pages (ohhmax.gitlab.io)';
  if (h.includes('codeberg.page')) return '🏔️ Codeberg Pages (ohhmax.codeberg.page)';
  if (h.includes('localhost') || h.includes('127.0.0.1')) return '💻 Localhost Dev';
  return `🌐 ${host || 'Web Mirror'}`;
}

/**
 * Classifies file attachment with matching emoji and clean badge label
 */
function getFileBadge(fileName) {
  const ext = (fileName.split('.').pop() || '').toLowerCase();
  if (['png', 'jpg', 'jpeg', 'webp', 'gif', 'svg', 'bmp', 'avif'].includes(ext)) {
    return { emoji: '🖼️', label: 'Image Attachment' };
  }
  if (['pdf'].includes(ext)) {
    return { emoji: '📄', label: 'PDF Document' };
  }
  if (['zip', 'rar', '7z', 'tar', 'gz', 'bz2'].includes(ext)) {
    return { emoji: '📦', label: 'Archive / Package' };
  }
  if (['doc', 'docx', 'odt', 'rtf', 'txt', 'md'].includes(ext)) {
    return { emoji: '📝', label: 'Document / Text' };
  }
  if (['xls', 'xlsx', 'csv'].includes(ext)) {
    return { emoji: '📊', label: 'Spreadsheet / Data' };
  }
  if (['js', 'ts', 'jsx', 'tsx', 'py', 'java', 'c', 'cpp', 'rs', 'go', 'html', 'css', 'json', 'yaml', 'yml', 'sh', 'sql', 'php'].includes(ext)) {
    return { emoji: '💻', label: 'Source Code / Data' };
  }
  if (['mp4', 'mov', 'avi', 'mkv', 'webm'].includes(ext)) {
    return { emoji: '🎬', label: 'Video File' };
  }
  if (['mp3', 'wav', 'ogg', 'm4a', 'flac'].includes(ext)) {
    return { emoji: '🎵', label: 'Audio File' };
  }
  return { emoji: '📎', label: 'Attached File' };
}

async function sendTelegramMessage(botToken, chatId, htmlText) {
  if (!botToken || !chatId) {
    console.warn('Telegram bot credentials not configured in Worker environment.');
    return { ok: false, error: 'Telegram secrets missing' };
  }

  const endpoint = `https://api.telegram.org/bot${botToken}/sendMessage`;
  try {
    const res = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        chat_id: chatId,
        text: htmlText,
        parse_mode: 'HTML',
        disable_web_page_preview: true,
      }),
    });
    return await res.json();
  } catch (err) {
    console.error('Telegram dispatch error:', err);
    return { ok: false, error: err.message };
  }
}

async function sendTelegramDocument(botToken, chatId, fileBlob, fileName, caption, replyToMessageId = null) {
  if (!botToken || !chatId) return { ok: false };

  const endpoint = `https://api.telegram.org/bot${botToken}/sendDocument`;
  try {
    const formData = new FormData();
    formData.append('chat_id', chatId);
    formData.append('document', fileBlob, fileName);
    if (caption) {
      formData.append('caption', caption);
      formData.append('parse_mode', 'HTML');
    }
    if (replyToMessageId) {
      formData.append('reply_to_message_id', String(replyToMessageId));
    }

    const res = await fetch(endpoint, {
      method: 'POST',
      body: formData,
    });
    return await res.json();
  } catch (err) {
    console.error('Telegram file upload error:', err);
    return { ok: false, error: err.message };
  }
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname.replace(/\/+$/, '') || '/';

    // 1. Handle CORS Preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        status: 204,
        headers: CORS_HEADERS,
      });
    }

    // 2. Health & Root Probe
    if (path === '' || path === '/' || path === '/health') {
      return jsonResponse({
        status: 'online',
        service: 'MaxPortfolio Cloudflare Worker Gateway',
        version: PORTFOLIO_VERSION,
        mirrors: [
          'https://ohhmax.github.io',
          'https://ohhmax.gitlab.io',
          'https://ohhmax.codeberg.page'
        ],
        uniqueVisitors: inMemoryVisitorCount,
        timestamp: new Date().toISOString()
      });
    }

    // 3. Unique Visitor Counter Endpoint (/api/visit-count or /visit-count)
    if ((path === '/api/visit-count' || path === '/visit-count') && request.method === 'GET') {
      return jsonResponse({
        success: true,
        count: inMemoryVisitorCount,
        baseline: 1000,
        version: PORTFOLIO_VERSION,
        timestamp: Date.now()
      });
    }

    // 4. Visitor Telemetry Ping (/api/visit or /visit)
    if ((path === '/api/visit' || path === '/visit') && request.method === 'POST') {
      try {
        let body = {};
        try {
          body = await request.json();
        } catch (e) {
          body = {};
        }

        // Cloudflare Edge Geolocation and Network Headers
        const ip = request.headers.get('cf-connecting-ip') || request.headers.get('x-forwarded-for') || 'Unknown';
        const countryCode = request.cf?.country || request.headers.get('cf-ipcountry') || 'Unknown';
        const countryName = getCountryName(countryCode);
        const city = request.cf?.city || 'Unknown';
        const region = request.cf?.region || request.cf?.regionCode || '';
        const postalCode = request.cf?.postalCode || '';
        const isp = request.cf?.asOrganization || 'Unknown';
        const asn = request.cf?.asn ? String(request.cf.asn) : '';
        const colo = request.cf?.colo || 'Unknown';
        const flag = getCountryFlag(countryCode);

        // Client Telemetry (Zero-Permission Web APIs)
        const mirrorBadge = getMirrorBadge(body.host, body.mirror);
        const version = body.portfolioVersion || PORTFOLIO_VERSION;
        const deviceModel = body.deviceModel || 'Standard Browser';
        const platform = body.platform || 'Unknown';
        const isMobile = body.isMobile ? 'Mobile' : 'Desktop';
        const batteryStatus = body.batteryStatus || 'N/A';
        const networkSummary = body.networkSummary || 'N/A';
        const screen = body.screen || 'N/A';
        const viewport = body.viewport || 'N/A';
        const gpu = body.gpu || 'Standard GPU';
        const cores = body.cores || 'N/A';
        const memory = body.memory || 'N/A';
        const touch = body.touch || 'N/A';
        const theme = body.theme || 'Dark Mode';
        const language = body.language || 'en';
        const timezone = body.timezone || request.cf?.timezone || 'UTC';
        const pagePath = body.path || '/';
        const referrer = body.referrer || request.headers.get('referer') || 'Direct Entry';
        const localTime = body.localTime || new Date().toUTCString();

        // Rate-limit check: Throttle repeated visits from the same IP (30 min window)
        const now = Date.now();
        const lastVisit = recentVisits.get(ip);
        const isThrottled = Boolean(lastVisit && (now - lastVisit < VISIT_THROTTLE_WINDOW_MS));

        if (!isThrottled) {
          recentVisits.set(ip, now);
          inMemoryVisitorCount++;

          const visitAlert =
`⚡ <b>PORTFOLIO VISITOR ALERT</b>

🌐 <b>Host Mirror:</b> ${escapeHtml(mirrorBadge)}
🏷️ <b>Version:</b> <code>${escapeHtml(version)}</code>

📍 <b>Visitor Location:</b>
${flag} <b>Country:</b> ${escapeHtml(countryName)} (<code>${escapeHtml(countryCode)}</code>)
🏛️ <b>Region / State:</b> ${escapeHtml(region || 'N/A')}
🏙️ <b>City / Postal:</b> ${escapeHtml(city)}${postalCode ? ` (${escapeHtml(postalCode)})` : ''}
🏢 <b>ISP / ASN:</b> ${escapeHtml(isp)}${asn ? ` (AS${escapeHtml(asn)})` : ''}
📡 <b>Datacenter / IP:</b> <code>${escapeHtml(colo)}</code> | <code>${escapeHtml(ip)}</code>

📱 <b>Device & Hardware Telemetry:</b>
📱 <b>Model:</b> <b>${escapeHtml(deviceModel)}</b>
💻 <b>Platform:</b> ${escapeHtml(platform)} (${isMobile})
🔋 <b>Battery:</b> <b>${escapeHtml(batteryStatus)}</b>
📶 <b>Connection:</b> ${escapeHtml(networkSummary)}
🖥️ <b>Display & Viewport:</b> ${escapeHtml(screen)} [${escapeHtml(viewport)}]
🎮 <b>GPU Renderer:</b> <code>${escapeHtml(gpu)}</code>
🧠 <b>System Specs:</b> ${escapeHtml(cores)} | ${escapeHtml(memory)} | Touch: ${escapeHtml(touch)}

🧭 <b>Navigation Context:</b>
🔗 <b>Active Page:</b> <code>${escapeHtml(pagePath)}</code>
🧭 <b>Traffic Referrer:</b> ${escapeHtml(referrer)}
🎨 <b>Theme & Locale:</b> ${escapeHtml(theme)} | ${escapeHtml(language)} (${escapeHtml(timezone)})
🕒 <b>Visitor Time:</b> ${escapeHtml(localTime)}`;

          ctx.waitUntil(sendTelegramMessage(env.TELEGRAM_BOT_TOKEN, env.TELEGRAM_CHAT_ID, visitAlert));
        }

        return jsonResponse({
          success: true,
          message: isThrottled ? 'Visit recorded (throttled cooldown active)' : 'Visit logged successfully',
          count: inMemoryVisitorCount,
          version: PORTFOLIO_VERSION,
          throttled: isThrottled
        });
      } catch (err) {
        return jsonResponse({ success: false, error: err.message }, 500);
      }
    }

    // 5. Contact Form Submission (/api/contact or /api/submit or /contact)
    if ((path === '/api/contact' || path === '/api/submit' || path === '/contact') && request.method === 'POST') {
      try {
        const contentType = request.headers.get('content-type') || '';
        let name = '';
        let email = '';
        let phone = '';
        let subject = '';
        let message = '';
        let telemetryRaw = null;
        const attachments = [];

        if (contentType.includes('multipart/form-data')) {
          const formData = await request.formData();
          name = formData.get('name') || '';
          email = formData.get('email') || '';
          phone = formData.get('phone') || '';
          subject = formData.get('subject') || '';
          message = formData.get('message') || '';
          telemetryRaw = formData.get('telemetry') || null;

          const files = formData.getAll('attachments');
          for (const item of files) {
            if (item && typeof item === 'object' && item.size > 0) {
              attachments.push(item);
            }
          }
        } else {
          const json = await request.json();
          name = json.name || '';
          email = json.email || '';
          phone = json.phone || '';
          subject = json.subject || '';
          message = json.message || '';
          telemetryRaw = json.telemetry || null;
        }

        if (!name && !email && !message) {
          return jsonResponse({ success: false, error: 'Required fields missing' }, 400);
        }

        // Parse client telemetry object if attached
        let tel = {};
        try {
          if (typeof telemetryRaw === 'string') {
            tel = JSON.parse(telemetryRaw);
          } else if (typeof telemetryRaw === 'object' && telemetryRaw !== null) {
            tel = telemetryRaw;
          }
        } catch (e) {
          tel = {};
        }

        // Edge Geolocation
        const ip = request.headers.get('cf-connecting-ip') || request.headers.get('x-forwarded-for') || 'Unknown';
        const countryCode = request.cf?.country || request.headers.get('cf-ipcountry') || 'Unknown';
        const countryName = getCountryName(countryCode);
        const city = request.cf?.city || 'Unknown';
        const region = request.cf?.region || request.cf?.regionCode || '';
        const postalCode = request.cf?.postalCode || '';
        const isp = request.cf?.asOrganization || 'Unknown';
        const asn = request.cf?.asn ? String(request.cf.asn) : '';
        const colo = request.cf?.colo || 'Unknown';
        const flag = getCountryFlag(countryCode);

        // Resolved Client Attributes
        const mirrorBadge = getMirrorBadge(tel.host, tel.mirror);
        const version = tel.portfolioVersion || PORTFOLIO_VERSION;
        const deviceModel = tel.deviceModel || 'Standard Browser';
        const platform = tel.platform || 'Unknown';
        const batteryStatus = tel.batteryStatus || 'N/A';
        const networkSummary = tel.networkSummary || 'N/A';
        const screen = tel.screen || 'N/A';
        const gpu = tel.gpu || 'Standard GPU';
        const cores = tel.cores || 'N/A';
        const memory = tel.memory || 'N/A';
        const theme = tel.theme || 'Dark Mode';
        const language = tel.language || 'en';
        const timezone = tel.timezone || request.cf?.timezone || 'UTC';

        const inquiryAlert =
`📬 <b>NEW PORTFOLIO CONTACT INQUIRY</b>

🌐 <b>Host Mirror:</b> ${escapeHtml(mirrorBadge)}
🏷️ <b>Version:</b> <code>${escapeHtml(version)}</code>

👤 <b>Sender Details:</b>
• <b>Name:</b> <b>${escapeHtml(name)}</b>
• <b>Email:</b> <code>${escapeHtml(email)}</code>
• <b>Phone:</b> ${phone ? `<code>${escapeHtml(phone)}</code>` : '<i>Not provided</i>'}
• <b>Subject:</b> <b>${escapeHtml(subject || 'General Inquiry')}</b>

💬 <b>Message Content:</b>
<blockquote>${escapeHtml(message)}</blockquote>

📎 <b>Attached Files:</b> ${attachments.length > 0 ? `<b>${attachments.length} file(s) attached</b>` : 'None'}

📍 <b>Sender Geolocation:</b>
${flag} <b>Location:</b> ${escapeHtml(city)}, ${escapeHtml(region ? region + ', ' : '')}${escapeHtml(countryName)} (<code>${escapeHtml(countryCode)}</code>)${postalCode ? ` - ${escapeHtml(postalCode)}` : ''}
🏢 <b>ISP / Network:</b> ${escapeHtml(isp)}${asn ? ` (AS${escapeHtml(asn)})` : ''}
📡 <b>Datacenter / IP:</b> <code>${escapeHtml(colo)}</code> | <code>${escapeHtml(ip)}</code>

📱 <b>Sender Device & Environment:</b>
📱 <b>Device Model:</b> <b>${escapeHtml(deviceModel)}</b> (${escapeHtml(platform)})
🔋 <b>Battery Status:</b> <b>${escapeHtml(batteryStatus)}</b>
📶 <b>Network:</b> ${escapeHtml(networkSummary)}
🖥️ <b>Display & GPU:</b> ${escapeHtml(screen)} | <code>${escapeHtml(gpu)}</code>
🧠 <b>Hardware:</b> ${escapeHtml(cores)} | ${escapeHtml(memory)}
🎨 <b>Theme / Lang:</b> ${escapeHtml(theme)} | ${escapeHtml(language)} (${escapeHtml(timezone)})
🕒 <b>Submitted At:</b> ${new Date().toUTCString()}`;

        // Send inquiry alert to Telegram and capture returned message_id
        const inquiryRes = await sendTelegramMessage(env.TELEGRAM_BOT_TOKEN, env.TELEGRAM_CHAT_ID, inquiryAlert);
        const replyToMessageId = (inquiryRes && inquiryRes.ok && inquiryRes.result) ? inquiryRes.result.message_id : null;

        // Forward file attachments to Telegram if present as replies with emojis and clean labels
        if (attachments.length > 0 && env.TELEGRAM_BOT_TOKEN && env.TELEGRAM_CHAT_ID) {
          for (const file of attachments) {
            try {
              const fileName = file.name || 'attachment';
              const badge = getFileBadge(fileName);
              const fileCaption = `${badge.emoji} <b>${badge.label}</b>\n` +
                `📁 <b>File:</b> <code>${escapeHtml(fileName)}</code>\n` +
                `👤 <b>From:</b> ${escapeHtml(name)} | 🏷️ <b>Subject:</b> ${escapeHtml(subject || 'General Inquiry')}`;
              ctx.waitUntil(sendTelegramDocument(
                env.TELEGRAM_BOT_TOKEN,
                env.TELEGRAM_CHAT_ID,
                file,
                fileName,
                fileCaption,
                replyToMessageId
              ));
            } catch (fileErr) {
              console.error('File forwarding notice:', fileErr);
            }
          }
        }

        return jsonResponse({
          success: true,
          message: 'Message delivered to Telegram group successfully',
          version: PORTFOLIO_VERSION,
          timestamp: Date.now()
        });
      } catch (err) {
        console.error('Contact handler error:', err);
        return jsonResponse({ success: false, error: err.message }, 500);
      }
    }

    return jsonResponse({ error: 'Endpoint not found', path }, 404);
  }
};
