#!/usr/bin/env node

const https = require('https');
const fs = require('fs');
const path = require('path');
const os = require('os');

let API_KEY = process.env.WERYAI_API_KEY || '';

if (!API_KEY) {
  try {
    const configPath = path.join(os.homedir(), '.openclaw', 'openclaw.json');
    if (fs.existsSync(configPath)) {
      const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
      if (config.weryai && config.weryai.apiKey) {
        API_KEY = config.weryai.apiKey;
      }
    }
  } catch (e) {}
}

if (!API_KEY) {
  console.error("Error: WERYAI_API_KEY is not set.");
  process.exit(1);
}

const args = process.argv.slice(2);
const action = args[0];

if (!action) {
  console.log(`
Usage: node weryai-media-editor.js <action> [options]
Actions:
  upscale <image_url>          - Upscale an image
  remove-bg <image_url>        - Remove background from an image
  i2v <image_url> "<prompt>"   - Image to Video
  face-swap <target> <source>  - Swap faces (target image URL, source face URL)
`);
  process.exit(1);
}

function request(url, options, body = null) {
  return new Promise((resolve, reject) => {
    const req = https.request(url, options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try { resolve(JSON.parse(data)); } 
        catch (e) { resolve(data); }
      });
    });
    req.on('error', reject);
    if (body) req.write(typeof body === 'string' ? body : JSON.stringify(body));
    req.end();
  });
}

async function pollStatus(taskId) {
  console.log(`Polling task ${taskId}...`);
  while (true) {
    await new Promise(r => setTimeout(r, 3000));
    const statusRes = await request(`https://api.weryai.com/growthai/v1/generation/${taskId}/status`, {
      method: 'GET',
      headers: { 'x-api-key': API_KEY }
    });
    
    if (statusRes.status === 'success' || statusRes.status === 'completed') {
      return statusRes.output_url || statusRes.result_url || statusRes.data;
    } else if (statusRes.status === 'failed') {
      throw new Error(`Task failed: ${JSON.stringify(statusRes)}`);
    }
    process.stdout.write('.');
  }
}

async function run() {
  try {
    let endpoint = '';
    let payload = {};

    switch(action) {
      case 'upscale':
        endpoint = 'https://api.weryai.com/growthai/v1/image/upscale';
        payload = { image_url: args[1], scale: 2 };
        break;
      case 'remove-bg':
        endpoint = 'https://api.weryai.com/growthai/v1/image/remove-background';
        payload = { image_url: args[1] };
        break;
      case 'i2v':
        endpoint = 'https://api.weryai.com/growthai/v1/video/image-to-video';
        payload = { image_url: args[1], prompt: args[2] || "animate this image" };
        break;
      case 'face-swap':
        endpoint = 'https://api.weryai.com/growthai/v1/image/face-swap';
        payload = { target_image_url: args[1], source_image_url: args[2] };
        break;
      default:
        console.log("Unknown action.");
        process.exit(1);
    }

    console.log(`Triggering ${action}...`);
    const submitRes = await request(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'x-api-key': API_KEY }
    }, payload);

    if (!submitRes.task_id && !submitRes.id) {
       if(submitRes.url || submitRes.output_url) {
           console.log(`\nSuccess! Result URL: ${submitRes.url || submitRes.output_url}`);
           return;
       }
       throw new Error(`Failed to submit: ${JSON.stringify(submitRes)}`);
    }

    const taskId = submitRes.task_id || submitRes.id;
    const finalResult = await pollStatus(taskId);
    console.log(`\nSuccess! Result: ${finalResult}`);
  } catch (err) {
    console.error("\nError:", err.message);
  }
}

run();
