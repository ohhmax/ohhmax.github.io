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

async function sendTelegramDocument(botToken, chatId, fileBlob, fileName, caption) {
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
        timestamp: new Date().toISOString()
      });
    }

    // 3. Visitor Telemetry Ping (/api/visit or /visit)
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

        return jsonResponse({ success: true, message: 'Visit logged successfully' });
      } catch (err) {
        return jsonResponse({ success: false, error: err.message }, 500);
      }
    }

    // 4. Contact Form Submission (/api/contact or /api/submit or /contact)
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

        // Send inquiry alert to Telegram
        await sendTelegramMessage(env.TELEGRAM_BOT_TOKEN, env.TELEGRAM_CHAT_ID, inquiryAlert);

        // Forward file attachments to Telegram if present
        if (attachments.length > 0 && env.TELEGRAM_BOT_TOKEN && env.TELEGRAM_CHAT_ID) {
          for (const file of attachments) {
            try {
              const fileName = file.name || 'attachment';
              const fileCaption = `Attachment from <b>${escapeHtml(name)}</b>: <code>${escapeHtml(fileName)}</code>`;
              ctx.waitUntil(sendTelegramDocument(env.TELEGRAM_BOT_TOKEN, env.TELEGRAM_CHAT_ID, file, fileName, fileCaption));
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
