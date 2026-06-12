const FILES = {
  learning: 'memory/compiled/learning.md',
  goals:    'memory/compiled/goals.md',
};

export default async function handler(req, res) {
  const { file } = req.query;
  const path = FILES[file];

  if (!path) {
    return res.status(400).send('');
  }

  const token = process.env.GITHUB_TOKEN;
  const url = `https://raw.githubusercontent.com/artemyevvvv-cloud/telegramassist/main/${path}`;

  try {
    const upstream = await fetch(url, {
      headers: token ? { Authorization: `token ${token}` } : {},
    });

    if (!upstream.ok) {
      return res.status(200).send('');
    }

    const text = await upstream.text();
    res.setHeader('Cache-Control', 'no-store');
    res.setHeader('Content-Type', 'text/plain; charset=utf-8');
    return res.status(200).send(text);
  } catch {
    return res.status(200).send('');
  }
}
