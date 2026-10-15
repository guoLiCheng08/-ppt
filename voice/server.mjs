import { spawn } from 'node:child_process';
import readline from 'node:readline';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const root = path.dirname(fileURLToPath(import.meta.url));
const voiceScript = path.join(root, 'codex-voice.ps1');

function reply(id, result) {
  process.stdout.write(`${JSON.stringify({ jsonrpc: '2.0', id, result })}\n`);
}

function errorReply(id, code, message) {
  process.stdout.write(`${JSON.stringify({
    jsonrpc: '2.0',
    id,
    error: { code, message },
  })}\n`);
}

function runSpeech(text, rate, volume) {
  return new Promise((resolve, reject) => {
    const child = spawn('powershell.exe', [
      '-NoProfile',
      '-ExecutionPolicy', 'Bypass',
      '-File', voiceScript,
      '-Text', text,
      '-Rate', String(rate),
      '-Volume', String(volume),
    ], { windowsHide: true });

    let stderr = '';
    child.stderr.on('data', (chunk) => { stderr += chunk.toString(); });
    child.once('error', reject);
    child.once('close', (code) => {
      if (code === 0) resolve();
      else reject(new Error(stderr.trim() || `PowerShell exited with code ${code}`));
    });
  });
}

async function handle(message) {
  const { id, method, params = {} } = message;

  if (method === 'initialize') {
    return reply(id, {
      protocolVersion: params.protocolVersion ?? '2024-11-05',
      capabilities: { tools: {} },
      serverInfo: { name: 'codex-local-voice', version: '1.0.0' },
    });
  }

  if (method === 'notifications/initialized' || method === 'ping') {
    if (id !== undefined) reply(id, {});
    return;
  }

  if (method === 'tools/list') {
    return reply(id, {
      tools: [{
        name: 'speak_text',
        description: '用 Windows 本地语音朗读一段简短的中文任务总结。',
        inputSchema: {
          type: 'object',
          properties: {
            text: { type: 'string', description: '需要朗读的文字，建议不超过三句话。' },
            rate: { type: 'integer', minimum: -10, maximum: 10, default: 0 },
            volume: { type: 'integer', minimum: 0, maximum: 100, default: 100 },
          },
          required: ['text'],
          additionalProperties: false,
        },
      }],
    });
  }

  if (method === 'tools/call') {
    if (params.name !== 'speak_text') {
      return errorReply(id, -32602, `Unknown tool: ${params.name}`);
    }

    const text = typeof params.arguments?.text === 'string'
      ? params.arguments.text.trim()
      : '';
    const rate = Number.isInteger(params.arguments?.rate) ? params.arguments.rate : 0;
    const volume = Number.isInteger(params.arguments?.volume) ? params.arguments.volume : 100;

    if (!text) return errorReply(id, -32602, 'text must not be empty');
    if (text.length > 2000) return errorReply(id, -32602, 'text must be at most 2000 characters');
    if (rate < -10 || rate > 10) return errorReply(id, -32602, 'rate must be between -10 and 10');
    if (volume < 0 || volume > 100) return errorReply(id, -32602, 'volume must be between 0 and 100');

    try {
      await runSpeech(text, rate, volume);
      return reply(id, {
        content: [{ type: 'text', text: '语音朗读已完成。' }],
      });
    } catch (error) {
      return reply(id, {
        isError: true,
        content: [{ type: 'text', text: `语音朗读失败：${error.message}` }],
      });
    }
  }

  if (id !== undefined) errorReply(id, -32601, `Method not found: ${method}`);
}

const input = readline.createInterface({ input: process.stdin, crlfDelay: Infinity });
input.on('line', async (line) => {
  if (!line.trim()) return;
  try {
    await handle(JSON.parse(line));
  } catch (error) {
    errorReply(null, -32700, `Invalid request: ${error.message}`);
  }
});
