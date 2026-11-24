/**
 * ============================================================================
 * COPYRIGHT & LICENSE NOTICE
 * Designed and Developed by Mahendra Mali (Max)
 * Website: https://ohhmax.github.io | Contact: ohmaxgit@gmail.com
 *
 * Copyright (c) 2026 Mahendra Mali (Max). All rights reserved.
 * ============================================================================
 */

/**
 * ============================================================================
 * CONTACT FORM & ZERO-PERMISSION CLIENT TELEMETRY ENGINE
 * - Form validation and multi-file attachment handling with preview tray
 * - Direct submission to Cloudflare Worker backend with Telegram Bot forwarding
 * - Zero-permission browser telemetry extraction:
 *   * Mirror Origin Detection (GitHub, GitLab, Codeberg, Localhost)
 *   * Device & Mobile Model Detection
 *   * Battery Level & Charging Status
 *   * Network Quality (4G/5G, Downlink, RTT)
 *   * Display Resolution, DPR & WebGL GPU Renderer
 *   * CPU Cores, RAM, Touch Points & Active Theme
 * - Throttled visit beaconing to prevent duplicate Telegram alerts on refresh
 * ============================================================================
 */

'use strict';

// ============================================================================
// CLOUDFLARE WORKER BACKEND CONFIGURATION
// Relays contact inquiries and visit alerts directly to Telegram group
// ============================================================================
const BACKEND_API_ENDPOINT = (typeof window !== 'undefined' && window.PORTFOLIO_BACKEND_URL)
  ? window.PORTFOLIO_BACKEND_URL
  : 'https://api.ohhmax.workers.dev/api/contact';

const VISIT_API_ENDPOINT = (typeof window !== 'undefined' && window.PORTFOLIO_VISIT_URL)
  ? window.PORTFOLIO_VISIT_URL
  : 'https://api.ohhmax.workers.dev/api/visit';

const VISIT_COUNT_API_ENDPOINT = (typeof window !== 'undefined' && window.PORTFOLIO_VISIT_COUNT_URL)
  ? window.PORTFOLIO_VISIT_COUNT_URL
  : 'https://api.ohhmax.workers.dev/api/visit-count';

// Attachment limits
const MAX_ATTACHMENTS = 5;
const MAX_FILE_SIZE_BYTES = 45 * 1024 * 1024; // 45 MB per file
let selectedAttachmentFiles = [];

/**
 * Haptic feedback helper
 */
function triggerHaptic(pattern = [10]) {
  if (typeof navigator !== 'undefined' && 'vibrate' in navigator) {
    try {
      navigator.vibrate(pattern);
    } catch (e) {}
  }
}

/**
 * Format bytes into human-readable file size string
 */
function formatFileSize(bytes) {
  if (!bytes || bytes === 0) return '0 B';
  const units = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(1024));
  return (bytes / Math.pow(1024, i)).toFixed(1) + ' ' + units[i];
}

/**
 * Shorten file names with ellipsis if exceeding max length
 */
function truncateFileName(name, maxChars = 20) {
  if (!name || name.length <= maxChars) return name;
  const dotIndex = name.lastIndexOf('.');
  if (dotIndex !== -1 && name.length - dotIndex <= 6) {
    const ext = name.substring(dotIndex);
    const base = name.substring(0, dotIndex);
    const leftLen = maxChars - ext.length - 3;
    if (leftLen > 2) {
      return base.substring(0, leftLen) + '...' + ext;
    }
  }
  return name.substring(0, maxChars - 3) + '...';
}

/**
 * Resolve FontAwesome icon class matching file extension or MIME type
 */
function getFileTypeIcon(file) {
  const mime = file.type || '';
  const ext = (file.name || '').split('.').pop().toLowerCase();

  if (mime.startsWith('image/')) return 'fa-solid fa-file-image';
  if (mime.startsWith('video/')) return 'fa-solid fa-file-video';
  if (mime.startsWith('audio/')) return 'fa-solid fa-file-audio';
  if (ext === 'pdf') return 'fa-solid fa-file-pdf';
  if (['zip', 'tar', 'gz', '7z', 'rar'].includes(ext)) return 'fa-solid fa-file-zipper';
  if (['doc', 'docx', 'txt', 'rtf'].includes(ext)) return 'fa-solid fa-file-lines';
  if (['js', 'json', 'py', 'cpp', 'c', 'java', 'html', 'css'].includes(ext)) return 'fa-solid fa-file-code';
  return 'fa-solid fa-file';
}

/**
 * Renders the multi-file chips tray
 */
function renderAttachedFilesTray() {
  const tray = document.getElementById('attachedFilesList');
  if (!tray) return;

  tray.innerHTML = '';
  if (selectedAttachmentFiles.length === 0) {
    tray.style.display = 'none';
    return;
  }

  tray.style.display = 'flex';
  selectedAttachmentFiles.forEach((file, index) => {
    const chip = document.createElement('div');
    chip.className = 'attachment-chip';

    const iconClass = getFileTypeIcon(file);
    const truncated = truncateFileName(file.name, 18);
    const sizeStr = formatFileSize(file.size);

    chip.innerHTML = `
      <i class="${iconClass} attachment-chip-icon"></i>
      <span class="attachment-chip-name" title="${file.name}">${truncated}</span>
      <span class="attachment-chip-size">(${sizeStr})</span>
      <button type="button" class="attachment-chip-remove" data-remove-index="${index}" aria-label="Remove ${file.name}">
        <i class="fa-solid fa-xmark"></i>
      </button>
    `;

    const removeBtn = chip.querySelector('[data-remove-index]');
    if (removeBtn) {
      removeBtn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        selectedAttachmentFiles.splice(index, 1);
        renderAttachedFilesTray();
      });
    }

    tray.appendChild(chip);
  });
}

/**
 * Resets attachment state
 */
function resetAttachmentState() {
  selectedAttachmentFiles = [];
  const fileInput = document.getElementById('contactAttachment');
  if (fileInput) fileInput.value = '';
  renderAttachedFilesTray();
}

/**
 * Initializes file attachment picker input
 */
function initAttachmentPicker() {
  const fileInput = document.getElementById('contactAttachment');
  if (!fileInput) return;

  fileInput.addEventListener('change', (e) => {
    const files = Array.from(e.target.files || []);
    if (files.length === 0) return;

    for (const file of files) {
      if (selectedAttachmentFiles.length >= MAX_ATTACHMENTS) {
        showContactStatus(false, `Maximum ${MAX_ATTACHMENTS} files allowed.`);
        break;
      }
      if (file.size > MAX_FILE_SIZE_BYTES) {
        showContactStatus(false, `"${file.name}" exceeds 45MB limit.`);
        continue;
      }
      const isDuplicate = selectedAttachmentFiles.some(f => f.name === file.name && f.size === file.size);
      if (!isDuplicate) {
        selectedAttachmentFiles.push(file);
      }
    }

    renderAttachedFilesTray();
    fileInput.value = '';
  });
}

/**
 * Displays status message banner
 */
function showContactStatus(success, message) {
  const banner = document.getElementById('contactStatusBanner');
  if (!banner) return;

  banner.className = success ? 'status-banner success' : 'status-banner error';
  banner.textContent = message;
  banner.style.display = 'block';

  setTimeout(() => {
    banner.style.display = 'none';
  }, 4000);
}

// ============================================================================
// ZERO-PERMISSION BROWSER TELEMETRY GATHERER
// Extracts rich client metadata without ever triggering permission dialogues
// ============================================================================

/**
 * Identifies which hosting mirror served the website
 */
function getMirrorOrigin() {
  const host = (typeof window !== 'undefined' && window.location.hostname) ? window.location.hostname.toLowerCase() : '';
  if (host.includes('github.io')) {
    return { name: 'GitHub Pages', mirror: '🐙 GitHub Pages (ohhmax.github.io)', host };
  }
  if (host.includes('gitlab.io')) {
    return { name: 'GitLab Pages', mirror: '🦊 GitLab Pages (ohhmax.gitlab.io)', host };
  }
  if (host.includes('codeberg.page')) {
    return { name: 'Codeberg Pages', mirror: '🏔️ Codeberg Pages (ohhmax.codeberg.page)', host };
  }
  if (host === 'localhost' || host === '127.0.0.1') {
    return { name: 'Localhost Dev', mirror: '💻 Localhost Dev', host };
  }
  return { name: host || 'Web Mirror', mirror: `🌐 ${host || 'Web Mirror'}`, host };
}

/**
 * Extracts battery percentage and charging state (zero permission)
 */
async function getBatteryTelemetry() {
  if (typeof navigator !== 'undefined' && typeof navigator.getBattery === 'function') {
    try {
      const b = await navigator.getBattery();
      const pct = Math.round((b.level || 0) * 100);
      const isCharging = Boolean(b.charging);
      const status = isCharging ? `⚡ ${pct}% (Charging)` : `🔋 ${pct}% (Discharging)`;
      return { level: `${pct}%`, charging: isCharging, status };
    } catch (e) {}
  }
  return { level: 'N/A', charging: false, status: 'Not available' };
}

/**
 * Extracts device model and hardware hints (zero permission)
 */
async function getDeviceModelTelemetry() {
  let model = '';
  let platform = (typeof navigator !== 'undefined' && navigator.platform) ? navigator.platform : '';
  let isMobile = false;

  if (typeof navigator !== 'undefined' && navigator.userAgentData) {
    try {
      isMobile = Boolean(navigator.userAgentData.mobile);
      platform = navigator.userAgentData.platform || platform;
      if (typeof navigator.userAgentData.getHighEntropyValues === 'function') {
        const entropy = await navigator.userAgentData.getHighEntropyValues(['model', 'platform', 'platformVersion']);
        if (entropy.model) model = entropy.model;
        if (entropy.platform) platform = entropy.platform;
      }
    } catch (e) {}
  }

  const ua = (typeof navigator !== 'undefined' && navigator.userAgent) ? navigator.userAgent : '';

  if (!model && ua) {
    const androidMatch = ua.match(/;\s*([A-Za-z0-9_\-\s]+)\s+Build\//);
    if (androidMatch && androidMatch[1]) {
      model = androidMatch[1].trim();
      isMobile = true;
    } else if (/iPhone/i.test(ua)) {
      model = 'Apple iPhone';
      isMobile = true;
    } else if (/iPad/i.test(ua)) {
      model = 'Apple iPad';
      isMobile = true;
    } else if (/Macintosh/i.test(ua)) {
      model = 'Apple Mac';
      isMobile = false;
    } else if (/Windows NT/i.test(ua)) {
      model = 'Windows PC';
      isMobile = false;
    } else if (/Linux/i.test(ua)) {
      model = 'Linux System';
      isMobile = false;
    }
  }

  if (!model) {
    model = isMobile ? 'Mobile Device' : (platform || 'Desktop / Laptop');
  }

  return { model, platform, isMobile };
}

/**
 * Queries WebGL hardware renderer name (zero permission)
 */
function getGpuRenderer() {
  try {
    const canvas = document.createElement('canvas');
    const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
    if (gl) {
      const ext = gl.getExtension('WEBGL_debug_renderer_info');
      if (ext) {
        const renderer = gl.getParameter(ext.UNMASKED_RENDERER_WEBGL);
        if (renderer) return renderer;
      }
      return gl.getParameter(gl.RENDERER) || 'Generic WebGL';
    }
  } catch (e) {}
  return 'Standard Hardware';
}

/**
 * Extracts connection quality and bandwidth info (zero permission)
 */
function getNetworkTelemetry() {
  if (typeof navigator !== 'undefined') {
    const conn = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
    if (conn) {
      const effectiveType = conn.effectiveType ? conn.effectiveType.toUpperCase() : 'Unknown';
      const downlink = conn.downlink ? `${conn.downlink} Mbps` : '';
      const rtt = conn.rtt ? `${conn.rtt} ms` : '';
      const parts = [effectiveType];
      if (downlink) parts.push(downlink);
      if (rtt) parts.push(`RTT: ${rtt}`);
      return {
        type: effectiveType,
        downlink,
        rtt,
        summary: parts.join(' | ')
      };
    }
  }
  return { type: 'Unknown', downlink: '', rtt: '', summary: 'Standard Connection' };
}

/**
 * Gathers screen, viewport, CPU cores, RAM, and locale info
 */
function getHardwareAndDisplayTelemetry() {
  const scr = typeof window !== 'undefined' ? window.screen : null;
  const nav = typeof navigator !== 'undefined' ? navigator : null;

  const width = scr ? scr.width : 0;
  const height = scr ? scr.height : 0;
  const dpr = typeof window !== 'undefined' ? (window.devicePixelRatio || 1) : 1;
  const colorDepth = scr ? scr.colorDepth : 24;
  const viewport = (typeof window !== 'undefined') ? `${window.innerWidth}x${window.innerHeight}` : 'N/A';

  const cores = nav && nav.hardwareConcurrency ? `${nav.hardwareConcurrency} Cores` : 'N/A';
  const memory = nav && nav.deviceMemory ? `${nav.deviceMemory} GB RAM` : 'N/A';
  const touchPoints = nav && typeof nav.maxTouchPoints === 'number' ? nav.maxTouchPoints : 0;
  const touch = touchPoints > 0 ? `Yes (${touchPoints} pts)` : 'No (Mouse/Pointer)';

  const language = nav ? (nav.language || (nav.languages && nav.languages[0]) || 'en') : 'en';
  let timezone = 'UTC';
  try {
    timezone = Intl.DateTimeFormat().resolvedOptions().timeZone || 'UTC';
  } catch (e) {}

  const isDark = typeof window !== 'undefined' && (
    document.body?.classList.contains('dark-theme') ||
    document.documentElement.getAttribute('data-theme') === 'dark' ||
    (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches)
  );

  return {
    screen: `${width}x${height} @ ${dpr}x`,
    viewport,
    colorDepth: `${colorDepth}-bit`,
    cores,
    memory,
    touch,
    language,
    timezone,
    theme: isDark ? 'Dark Theme' : 'Light Theme'
  };
}

/**
 * Aggregates all zero-permission client telemetry into a single payload
 */
async function collectClientTelemetry() {
  const mirrorObj = getMirrorOrigin();
  const battery = await getBatteryTelemetry();
  const devInfo = await getDeviceModelTelemetry();
  const net = getNetworkTelemetry();
  const hw = getHardwareAndDisplayTelemetry();
  const gpu = getGpuRenderer();

  const version = (typeof window !== 'undefined' && window.PORTFOLIO_VERSION)
    ? window.PORTFOLIO_VERSION
    : (document.querySelector('meta[name="portfolio-version"]')?.content || 'v3.9.1');

  return {
    mirror: mirrorObj.mirror,
    mirrorName: mirrorObj.name,
    host: mirrorObj.host,
    portfolioVersion: version,
    deviceModel: devInfo.model,
    platform: devInfo.platform,
    isMobile: devInfo.isMobile,
    batteryStatus: battery.status,
    batteryLevel: battery.level,
    batteryCharging: battery.charging,
    networkSummary: net.summary,
    networkType: net.type,
    screen: hw.screen,
    viewport: hw.viewport,
    gpu: gpu,
    cores: hw.cores,
    memory: hw.memory,
    touch: hw.touch,
    theme: hw.theme,
    language: hw.language,
    timezone: hw.timezone,
    path: (typeof window !== 'undefined') ? (window.location.pathname + window.location.hash) : '/',
    referrer: (typeof document !== 'undefined' && document.referrer) ? document.referrer : 'Direct Entry',
    localTime: new Date().toLocaleString()
  };
}

/**
 * Handles Contact Form Submission
 */
async function handleContactFormSubmit(event) {
  event.preventDefault();

  const form = document.getElementById('contactForm') || document.querySelector('[data-form]');
  const submitBtn = document.getElementById('contactSubmitBtn') || document.querySelector('[data-form-btn]');
  const formWrapper = document.getElementById('contactFormWrapper');
  const successCard = document.getElementById('contactSuccessSummary');

  const firstNameInput = document.getElementById('contactFirstName') || form?.querySelector('input[name="firstname"]');
  const lastNameInput = document.getElementById('contactLastName') || form?.querySelector('input[name="lastname"]');
  const emailInput = document.getElementById('contactEmail') || form?.querySelector('input[name="email"]');
  const phoneInput = document.getElementById('contactPhone') || form?.querySelector('input[name="phone"]');
  const subjectInput = document.getElementById('contactSubject') || form?.querySelector('input[name="subject"]');
  const messageInput = document.getElementById('contactMessage') || form?.querySelector('textarea[name="message"]');

  const firstVal = firstNameInput ? firstNameInput.value.trim() : '';
  const lastVal = lastNameInput ? lastNameInput.value.trim() : '';
  const nameVal = `${firstVal} ${lastVal}`.trim() || (emailInput && emailInput.value ? emailInput.value.split('@')[0] : 'Visitor');
  const emailVal = emailInput ? emailInput.value.trim() : '';
  const phoneVal = phoneInput ? phoneInput.value.trim() : '';
  const subjectVal = subjectInput ? subjectInput.value.trim() : 'General Inquiry';
  const messageVal = messageInput ? messageInput.value.trim() : '';

  if (!nameVal || !emailVal || !messageVal) {
    showContactStatus(false, 'Please complete Name, Email, and Message fields.');
    return;
  }

  triggerHaptic([15]);

  const originalBtnContent = submitBtn ? submitBtn.innerHTML : 'Send Message';
  if (submitBtn) {
    submitBtn.setAttribute('disabled', 'true');
    submitBtn.innerHTML = `
      <span class="btn-spinner"></span>
      <span>Sending Message...</span>
    `;
  }

  try {
    // Gather zero-permission client telemetry
    const telemetry = await collectClientTelemetry();

    // Dispatch to custom backend API if configured
    if (BACKEND_API_ENDPOINT) {
      const formData = new FormData();
      formData.append('name', nameVal);
      formData.append('email', emailVal);
      formData.append('phone', phoneVal);
      formData.append('subject', subjectVal);
      formData.append('message', messageVal);
      formData.append('timestamp', String(Date.now()));
      formData.append('telemetry', JSON.stringify(telemetry));

      selectedAttachmentFiles.forEach((file) => {
        formData.append('attachments', file, file.name);
      });

      const response = await fetch(BACKEND_API_ENDPOINT, {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        throw new Error(`Server responded with status ${response.status}`);
      }
    }

    triggerHaptic([20, 60, 20]);

    // Show success view and reset form inputs
    if (formWrapper && successCard) {
      formWrapper.style.display = 'none';
      if (form) form.reset();
      resetAttachmentState();

      successCard.style.display = 'block';
      successCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
    } else {
      showContactStatus(true, 'Message sent successfully! I will reply promptly.');
      if (form) form.reset();
      resetAttachmentState();
    }
  } catch (err) {
    console.error('Submission error:', err);
    showContactStatus(false, 'Failed to deliver message. Please retry or contact directly via Email / Telegram.');
  } finally {
    if (submitBtn) {
      submitBtn.removeAttribute('disabled');
      submitBtn.innerHTML = originalBtnContent;
    }
  }
}

/**
 * Resets contact form and brings it back after success screen
 */
function handleSendAnotherMessage() {
  triggerHaptic([10]);
  const form = document.getElementById('contactForm');
  const formWrapper = document.getElementById('contactFormWrapper');
  const successCard = document.getElementById('contactSuccessSummary');

  if (form) form.reset();
  resetAttachmentState();

  if (successCard) successCard.style.display = 'none';
  if (formWrapper) {
    formWrapper.style.display = 'block';
    formWrapper.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
}

/**
 * Formats unique visitor counter for display (accurate number matching data/visitor_analytics.json)
 */
function formatVisitorDisplay(count) {
  const num = parseInt(count, 10);
  if (isNaN(num)) return '1,000';
  return num.toLocaleString();
}

/**
 * Initializes and updates the Total Unique Visitors counter in Share section
 */
async function initShareVisitorCounter() {
  const countEl = document.getElementById('shareVisitorCount');
  if (!countEl) return;

  const cached = localStorage.getItem('portfolio_unique_visitors') || '1000';
  countEl.textContent = formatVisitorDisplay(cached);

  try {
    const res = await fetch(VISIT_COUNT_API_ENDPOINT, { mode: 'cors' });
    if (res.ok) {
      const data = await res.json();
      if (data && typeof data.count === 'number') {
        localStorage.setItem('portfolio_unique_visitors', String(data.count));
        countEl.textContent = formatVisitorDisplay(data.count);
      }
    }
  } catch (e) {}
}

/**
 * Asynchronously pings Cloudflare Worker backend to deliver live visit notification to Telegram
 * strictly throttled per browser session and 30-minute cooldown to prevent spam on page refreshes
 */
async function pingVisitBeacon() {
  if (!VISIT_API_ENDPOINT) return;
  try {
    const now = Date.now();
    const sessionVisited = sessionStorage.getItem('portfolio_visited_session');
    const lastVisitTs = parseInt(localStorage.getItem('portfolio_last_visit_ts') || '0', 10);
    const THIRTY_MINUTES = 30 * 60 * 1000;

    // Do not dispatch beacon if already sent in this browser session or within 30 min cooldown
    if (sessionVisited || (now - lastVisitTs < THIRTY_MINUTES)) {
      initShareVisitorCounter();
      return;
    }

    sessionStorage.setItem('portfolio_visited_session', 'true');
    localStorage.setItem('portfolio_last_visit_ts', String(now));

    // Gather complete client telemetry
    const telemetry = await collectClientTelemetry();

    fetch(VISIT_API_ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(telemetry),
      mode: 'cors'
    }).then(res => res.json()).then(data => {
      if (data && data.count) {
        localStorage.setItem('portfolio_unique_visitors', String(data.count));
        const countEl = document.getElementById('shareVisitorCount');
        if (countEl) countEl.textContent = formatVisitorDisplay(data.count);
      }
    }).catch(() => {});
  } catch (e) {}
}

// Initialize on DOM Ready
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('contactForm') || document.querySelector('[data-form]');
  if (form) {
    form.addEventListener('submit', handleContactFormSubmit);
  }

  const sendAgainBtn = document.getElementById('contactSendAgainBtn');
  if (sendAgainBtn) {
    sendAgainBtn.addEventListener('click', handleSendAnotherMessage);
  }

  initAttachmentPicker();
  pingVisitBeacon();
  initShareVisitorCounter();
});
