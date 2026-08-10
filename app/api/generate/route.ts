import { NextRequest, NextResponse } from 'next/server';
import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

const SYSTEM_PROMPT = `You are a senior full-stack engineer. Generate complete, working code.
Output ONLY valid JSON in this exact format:
{
  "files": [
    { "path": "app/page.tsx", "content": "..." },
    { "path": "package.json", "content": "..." }
  ],
  "readme": "Setup instructions...",
  "commands": ["npm install", "npm run dev"]
}
Use Next.js 15 App Router + TypeScript + Tailwind. Make it production-ready.`;

export async function POST(req: NextRequest) {
  try {
    const { prompt } = await req.json();

    if (!prompt) {
      return NextResponse.json({ error: 'Prompt is required' }, { status: 400 });
    }

    const completion = await openai.chat.completions.create({
      model: 'gpt-4o',
      messages: [
        { role: 'system', content: SYSTEM_PROMPT },
        { role: 'user', content: prompt },
      ],
      temperature: 0.3,
      response_format: { type: 'json_object' },
    });

    const content = completion.choices[0].message.content;
    const parsed = JSON.parse(content || '{}');

    return NextResponse.json(parsed);
  } catch (error: any) {
    console.error(error);
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}