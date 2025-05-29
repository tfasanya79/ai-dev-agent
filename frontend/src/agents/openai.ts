// src/agents/openai.ts
import { OpenAI } from 'openai';

const openai = new OpenAI({
  apiKey: import.meta.env.VITE_OPENAI_API_KEY,
  dangerouslyAllowBrowser: true, // ✅ for browser use
});

// ✅ Real implementation using OpenAI
export async function generateCode(prompt: string): Promise<string> {
  const chatCompletion = await openai.chat.completions.create({
    model: 'gpt-4',
    messages: [
      { role: 'system', content: 'You are a helpful coding assistant.' },
      { role: 'user', content: `Write code for: ${prompt}` },
    ],
  });

  return chatCompletion.choices[0].message.content || '⚠️ No response';
}

// 🔧 Mocked (temporary) implementations for other modules
export async function fixBugs(prompt: string): Promise<string> {
  return `// Bug fixed for:\n${prompt}\n\nfunction fixedExample() {\n  console.log("Bug resolved");\n}`;
}

export async function writeTests(prompt: string): Promise<string> {
  return `// Unit tests for:\n${prompt}\n\ntest("example test", () => {\n  expect(true).toBe(true);\n});`;
}

export async function explainCode(prompt: string): Promise<string> {
  return `// Explanation for:\n${prompt}\n\nThis code defines a function that logs "Hello, World!" to the console.`;
}

export async function refactorCode(prompt: string): Promise<string> {
  return `// Refactored version of:\n${prompt}\n\nfunction refactoredExample() {\n  console.log("Refactored cleanly");\n}`;
}
