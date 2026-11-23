/**
 * ============================================================================
 * SECURE CONFIGURATION CRYPTO & VAULT ENGINE
 * Designed for Mahendra Mali (Max) Portfolio
 * AES-256-GCM encryption and decryption for sensitive tokens and credentials
 * ============================================================================
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const ROOT_DIR = path.resolve(__dirname, '..');
const CONFIG_FILE = path.join(ROOT_DIR, 'maxconf.json');
const ENC_CONFIG_FILE = path.join(ROOT_DIR, 'maxconf.enc.json');

// Default salt & derived key setup
const DEFAULT_SECRET = process.env.MAX_VAULT_KEY || 'max-portfolio-2026-master-key-9824584454';
const ALGORITHM = 'aes-256-gcm';

function deriveKey(secret) {
  return crypto.scryptSync(secret, 'max-portfolio-salt-2026', 32);
}

function encryptText(text, secret = DEFAULT_SECRET) {
  const key = deriveKey(secret);
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv(ALGORITHM, key, iv);
  
  let encrypted = cipher.update(text, 'utf8', 'hex');
  encrypted += cipher.final('hex');
  const tag = cipher.getAuthTag().toString('hex');
  
  return {
    iv: iv.toString('hex'),
    content: encrypted,
    tag: tag
  };
}

function decryptText(cipherObj, secret = DEFAULT_SECRET) {
  const key = deriveKey(secret);
  const decipher = crypto.createDecipheriv(ALGORITHM, key, Buffer.from(cipherObj.iv, 'hex'));
  decipher.setAuthTag(Buffer.from(cipherObj.tag, 'hex'));
  
  let decrypted = decipher.update(cipherObj.content, 'hex', 'utf8');
  decrypted += decipher.final('utf8');
  return decrypted;
}

function encryptConfigFile() {
  if (!fs.existsSync(CONFIG_FILE)) {
    console.error(`Config file not found: ${CONFIG_FILE}`);
    process.exit(1);
  }

  const raw = fs.readFileSync(CONFIG_FILE, 'utf8');
  const cfg = JSON.parse(raw);

  // Clone and encrypt sensitive fields
  const securedCfg = JSON.parse(JSON.stringify(cfg));

  const sensitiveFields = [
    ['telegram', 'botToken'],
    ['telegram', 'chatId']
  ];

  sensitiveFields.forEach(([section, field]) => {
    if (securedCfg[section] && securedCfg[section][field]) {
      const val = securedCfg[section][field];
      if (typeof val === 'string' && !val.startsWith('ENC_GCM:')) {
        const enc = encryptText(val);
        securedCfg[section][field] = `ENC_GCM:${enc.iv}:${enc.tag}:${enc.content}`;
      }
    }
  });

  // Write maxconf.enc.json
  fs.writeFileSync(ENC_CONFIG_FILE, JSON.stringify(securedCfg, null, 2) + '\n', 'utf8');
  console.log(`[Success] Encrypted sensitive tokens into ${ENC_CONFIG_FILE}`);

  // Create public-safe sanitized config version
  const publicCfg = JSON.parse(JSON.stringify(securedCfg));
  fs.writeFileSync(CONFIG_FILE, JSON.stringify(publicCfg, null, 2) + '\n', 'utf8');
  console.log(`[Success] Updated ${CONFIG_FILE} with secured field tokens`);
}

function decryptConfigFile() {
  if (!fs.existsSync(ENC_CONFIG_FILE)) {
    console.error(`Encrypted config not found: ${ENC_CONFIG_FILE}`);
    process.exit(1);
  }

  const raw = fs.readFileSync(ENC_CONFIG_FILE, 'utf8');
  const cfg = JSON.parse(raw);

  const sensitiveFields = [
    ['telegram', 'botToken'],
    ['telegram', 'chatId']
  ];

  sensitiveFields.forEach(([section, field]) => {
    if (cfg[section] && cfg[section][field]) {
      const val = cfg[section][field];
      if (typeof val === 'string' && val.startsWith('ENC_GCM:')) {
        const parts = val.replace('ENC_GCM:', '').split(':');
        if (parts.length === 3) {
          const cipherObj = { iv: parts[0], tag: parts[1], content: parts[2] };
          try {
            cfg[section][field] = decryptText(cipherObj);
          } catch (err) {
            console.warn(`Could not decrypt ${section}.${field}:`, err.message);
          }
        }
      }
    }
  });

  return cfg;
}

const command = process.argv[2] || 'encrypt';
if (command === 'encrypt') {
  encryptConfigFile();
} else if (command === 'decrypt') {
  const decrypted = decryptConfigFile();
  console.log('[Decrypted Config Content]:');
  console.log(JSON.stringify(decrypted, null, 2));
} else {
  console.log('Usage: node secure-config-crypto.js [encrypt|decrypt]');
}
