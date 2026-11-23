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
 * CONTACT FORM ENGINE
 * - Direct submission to configurable backend API endpoint
 * - Multi-file attachment handling with preview tray
 * - Form validation and responsive feedback
 * - Zero visitor tracking, zero telemetry overhead
 * ============================================================================
 */

'use strict';

// ============================================================================
// BACKEND CONFIGURATION
// Add your custom backend API endpoint URL here (e.g., 'https://api.yourdomain.com/contact')
// When set, form submissions will be POSTed directly to this endpoint with FormData.
// If empty, the form will display the success screen locally.
// ============================================================================
const BACKEND_API_ENDPOINT = '';

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
    // Dispatch to custom backend API if configured
    if (BACKEND_API_ENDPOINT) {
      const formData = new FormData();
      formData.append('name', nameVal);
      formData.append('email', emailVal);
      formData.append('phone', phoneVal);
      formData.append('subject', subjectVal);
      formData.append('message', messageVal);
      formData.append('timestamp', String(Date.now()));

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
});
