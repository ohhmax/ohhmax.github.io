/**
 * submit-indexnow.js
 * Automated IndexNow ping submission utility for Mahendra Mali Portfolio.
 * Pings api.indexnow.org and bing.com to notify search engines immediately of URL changes.
 */

const https = require('https');

const HOST = 'ohhmax.github.io';
const KEY = 'c4a89df2019b48c69772dc3fa08e49bc';
const KEY_LOCATION = `https://${HOST}/${KEY}.txt`;

const URL_LIST = [
  `https://${HOST}/`,
  `https://${HOST}/about/`,
  `https://${HOST}/projects/`,
  `https://${HOST}/maxnet/`,
  `https://${HOST}/resume/`,
  `https://${HOST}/testimonials/`,
  `https://${HOST}/milestones/`,
  `https://${HOST}/gallery/`,
  `https://${HOST}/contact/`,
  `https://${HOST}/cv-resume-latest-info.html`,
  `https://${HOST}/resume.json`,
  `https://${HOST}/llms.txt`,
  `https://${HOST}/llms-full.txt`
];

const payload = JSON.stringify({
  host: HOST,
  key: KEY,
  keyLocation: KEY_LOCATION,
  urlList: URL_LIST
});

const ENDPOINTS = [
  { hostname: 'api.indexnow.org', path: '/indexnow' },
  { hostname: 'www.bing.com', path: '/indexnow' }
];

function submit(endpoint) {
  return new Promise((resolve) => {
    const options = {
      hostname: endpoint.hostname,
      port: 443,
      path: endpoint.path,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'Content-Length': Buffer.byteLength(payload)
      },
      timeout: 10000
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        resolve({
          host: endpoint.hostname,
          statusCode: res.statusCode,
          statusMessage: res.statusMessage,
          responseBody: data
        });
      });
    });

    req.on('error', (err) => {
      resolve({
        host: endpoint.hostname,
        statusCode: 0,
        error: err.message
      });
    });

    req.on('timeout', () => {
      req.destroy();
      resolve({
        host: endpoint.hostname,
        statusCode: 408,
        error: 'Timeout after 10000ms'
      });
    });

    req.write(payload);
    req.end();
  });
}

async function main() {
  console.log('======================================================');
  console.log('       INDEXNOW SUBMISSION - MAHENDRA MALI');
  console.log('======================================================');
  console.log(`Host: ${HOST}`);
  console.log(`Key:  ${KEY}`);
  console.log(`Key Location: ${KEY_LOCATION}`);
  console.log(`Total URLs to Submit: ${URL_LIST.length}`);
  console.log('------------------------------------------------------');

  for (const ep of ENDPOINTS) {
    console.log(`Submitting to https://${ep.hostname}${ep.path}...`);
    const res = await submit(ep);
    if (res.statusCode === 200 || res.statusCode === 202) {
      console.log(`  ✔ SUCCESS [${res.statusCode}] Accepted by ${ep.hostname}`);
    } else {
      console.log(`  ℹ STATUS [${res.statusCode}] ${res.statusMessage || res.error || ''}`);
    }
  }

  console.log('======================================================');
  console.log('IndexNow submission cycle complete.');
}

if (require.main === module) {
  main().catch((err) => {
    console.error('Fatal error during IndexNow submission:', err);
    process.exit(1);
  });
}

module.exports = { submit, URL_LIST };
