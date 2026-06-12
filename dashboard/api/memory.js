export const config = { runtime: 'edge' };

const FILES = {
  learning: 'memory/compiled/learning.md',
  goals:    'memory/compiled/goals.md',
};

export default async function handler(request) {
  const { searchParams } = new URL(request.url);
  const file = searchParams.get('file');
  const path = FILES[file];

  if (!path) {
    return new Response('', { status: 400 });
  }

  const token = process.env.GITHUB_TOKEN;
  const url = `https://raw.githubusercontent.com/artemyevvvv-cloud/telegramassist/main/${path}`;

  try {
    const upstream = await fetch(url, {
      headers: token ? { Authorization: `token ${token}` } : {},
    });

    if (!upstream.ok) {
      return new Response('', { status: 200 });
    }

    const text = await upstream.text();
    return new Response(text, {
      headers: {
        'Content-Type': 'text/plain; charset=utf-8',
        'Cache-Control': 'no-store',
      },
    });
  } catch {
    return new Response('', { status: 200 });
  }
}
