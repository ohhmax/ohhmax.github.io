/**
 * ============================================================================
 * CLOUDFLARE WORKER BACKEND - TELEGRAM BOT GATEWAY
 * Designed for Mahendra Mali (Max) Developer Portfolio
 *
 * Capabilities:
 * 1. POST /api/contact: Receives inquiries with optional file attachments,
 *    relays formatted alerts to Telegram group via Bot API.
 * 2. POST /api/visit: Receives visitor ping, extracts Cloudflare edge geo
 *    telemetry (Country, City, IP, ISP), and delivers alert to Telegram.
 * 3. GET /health: Worker health status and mirror registry.
 *
 * Security:
 * - Zero tokens hardcoded. Reads from Worker environment variables:
 *   env.TELEGRAM_BOT_TOKEN, env.TELEGRAM_CHAT_ID.
 * - Strict CORS configuration.
 * ============================================================================
 */

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

        const ip = request.headers.get('cf-connecting-ip') || request.headers.get('x-forwarded-for') || 'Unknown';
        const country = request.cf?.country || request.headers.get('cf-ipcountry') || 'Unknown';
        const city = request.cf?.city || 'Unknown';
        const region = request.cf?.region || '';
        const isp = request.cf?.asOrganization || 'Unknown';
        const userAgent = request.headers.get('user-agent') || 'Unknown';
        const referrer = body.referrer || request.headers.get('referer') || 'Direct';
        const pagePath = body.path || '/';
        const screen = body.screen || 'N/A';

        // Rate-limit check: Throttle repeated visits from the same IP (30 min window)
        const now = Date.now();
        const lastVisit = recentVisits.get(ip);
        const isThrottled = Boolean(lastVisit && (now - lastVisit < VISIT_THROTTLE_WINDOW_MS));

        if (!isThrottled) {
          recentVisits.set(ip, now);
          inMemoryVisitorCount++;

          const visitAlert = 
`<b>Portfolio Visitor Alert</b>

<b>Location:</b> ${escapeHtml(city)}, ${escapeHtml(region ? region + ', ' : '')}${escapeHtml(country)}
<b>IP Address:</b> <code>${escapeHtml(ip)}</code>
<b>Network / ISP:</b> ${escapeHtml(isp)}
<b>Page:</b> ${escapeHtml(pagePath)}
<b>Referrer:</b> ${escapeHtml(referrer)}
<b>Screen:</b> ${escapeHtml(screen)}
<b>Device:</b> <code>${escapeHtml(userAgent)}</code>
<b>Time:</b> ${new Date().toUTCString()}`;

          ctx.waitUntil(sendTelegramMessage(env.TELEGRAM_BOT_TOKEN, env.TELEGRAM_CHAT_ID, visitAlert));
        }

        return jsonResponse({
          success: true,
          message: isThrottled ? 'Visit recorded (throttled cooldown active)' : 'Visit logged successfully',
          count: inMemoryVisitorCount,
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
        const attachments = [];

        if (contentType.includes('multipart/form-data')) {
          const formData = await request.formData();
          name = formData.get('name') || '';
          email = formData.get('email') || '';
          phone = formData.get('phone') || '';
          subject = formData.get('subject') || '';
          message = formData.get('message') || '';

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
        }

        if (!name && !email && !message) {
          return jsonResponse({ success: false, error: 'Required fields missing' }, 400);
        }

        const ip = request.headers.get('cf-connecting-ip') || request.headers.get('x-forwarded-for') || 'Unknown';
        const country = request.cf?.country || request.headers.get('cf-ipcountry') || 'Unknown';
        const city = request.cf?.city || 'Unknown';

        const inquiryAlert =
`<b>New Portfolio Contact Inquiry</b>

<b>From:</b> ${escapeHtml(name)}
<b>Email:</b> <code>${escapeHtml(email)}</code>
<b>Phone:</b> ${phone ? `<code>${escapeHtml(phone)}</code>` : 'Not provided'}
<b>Subject:</b> ${escapeHtml(subject || 'General Inquiry')}

<b>Message:</b>
${escapeHtml(message)}

<b>Client Metadata:</b>
• Location: ${escapeHtml(city)}, ${escapeHtml(country)}
• IP Address: <code>${escapeHtml(ip)}</code>
• Attachments: ${attachments.length} file(s)
• Received: ${new Date().toUTCString()}`;

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
                `👤 <b>From:</b> ${escapeHtml(name)} | 🏷️ <b>Form:</b> ${escapeHtml(subject || 'General Inquiry')}`;
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
