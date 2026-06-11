const https = require('https');
const fs = require('fs');
const path = require('path');

const SUPABASE_URL = 'https://fxngzjloawdymcavvnle.supabase.co';
const ANON_KEY = 'sb_publishable_0A3jQtUMd2YMHfu1JKZ8fw_KdhLuqND';
const OUT_DIR = path.join(__dirname, '..', '..', 'knowledge-base', 'aizdec');

function apiFetch(endpoint) {
  return new Promise((resolve, reject) => {
    const url = `${SUPABASE_URL}/rest/v1/${endpoint}`;
    const opts = {
      headers: {
        'apikey': ANON_KEY,
        'authorization': `Bearer ${ANON_KEY}`,
        'accept-profile': 'public',
        'accept': 'application/json',
      }
    };
    https.get(url, opts, res => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try { resolve(JSON.parse(data)); }
        catch (e) { reject(new Error(`JSON parse error: ${e.message}\nData: ${data.slice(0, 200)}`)); }
      });
    }).on('error', reject);
  });
}

// Конвертация BlockNote inline content в текст
function inlineToText(content) {
  if (!Array.isArray(content)) return '';
  return content.map(item => {
    if (item.type === 'text') {
      let t = item.text || '';
      const s = item.styles || {};
      if (s.bold) t = `**${t}**`;
      if (s.italic) t = `_${t}_`;
      if (s.code) t = `\`${t}\``;
      if (s.strike) t = `~~${t}~~`;
      return t;
    }
    if (item.type === 'link') {
      const text = inlineToText(item.content);
      return `[${text}](${item.href})`;
    }
    return item.text || '';
  }).join('');
}

// Конвертация одного BlockNote блока в Markdown
function blockToMd(block, depth = 0) {
  if (!block) return '';
  const indent = '  '.repeat(depth);
  const text = inlineToText(block.content);
  const children = (block.children || []).map(c => blockToMd(c, depth + 1)).filter(Boolean).join('\n');

  let result = '';
  switch (block.type) {
    case 'heading': {
      const level = block.props?.level || 2;
      result = `${'#'.repeat(level)} ${text}`;
      break;
    }
    case 'paragraph':
      result = text ? text : '';
      break;
    case 'bulletListItem':
      result = `${indent}- ${text}`;
      break;
    case 'numberedListItem':
      result = `${indent}1. ${text}`;
      break;
    case 'checkListItem': {
      const checked = block.props?.checked ? 'x' : ' ';
      result = `${indent}- [${checked}] ${text}`;
      break;
    }
    case 'codeBlock': {
      const lang = block.props?.language || '';
      result = `\`\`\`${lang}\n${text}\n\`\`\``;
      break;
    }
    case 'image': {
      const url = block.props?.url || '';
      const caption = block.props?.caption || text || 'image';
      result = url ? `![${caption}](${url})` : '';
      break;
    }
    case 'video': {
      const url = block.props?.url || '';
      result = url ? `[Видео](${url})` : '';
      break;
    }
    case 'file': {
      const url = block.props?.url || '';
      const name = block.props?.name || text || 'file';
      result = url ? `[${name}](${url})` : '';
      break;
    }
    case 'table': {
      // Простая таблица
      const rows = block.content?.rows || [];
      if (rows.length === 0) break;
      const mdRows = rows.map(row =>
        '| ' + (row.cells || []).map(cell => inlineToText(cell)).join(' | ') + ' |'
      );
      const separator = '| ' + (rows[0]?.cells || []).map(() => '---').join(' | ') + ' |';
      result = [mdRows[0], separator, ...mdRows.slice(1)].join('\n');
      break;
    }
    case 'divider':
      result = '---';
      break;
    case 'quote':
      result = text ? `> ${text}` : '';
      break;
    case 'toggle': {
      result = text ? `**${text}**` : '';
      break;
    }
    default:
      result = text || '';
  }

  const parts = [result, children].filter(Boolean);
  return parts.join('\n');
}

// Конвертация массива блоков в Markdown
function blocksToMd(blocks) {
  if (!Array.isArray(blocks)) return '';
  return blocks
    .map(b => blockToMd(b))
    .filter(Boolean)
    .join('\n\n');
}

function sanitizeFilename(slug) {
  return slug.replace(/[^a-z0-9\-_]/gi, '-') + '.md';
}

async function main() {
  console.log('Получаю список курсов...');
  const courses = await apiFetch('courses?select=*&order=position.asc');
  console.log(`Курсов: ${courses.length}`);

  console.log('Получаю все уроки...');
  const lessons = await apiFetch(
    'lessons?select=*,course:courses(slug,title)&order=course_id,position.asc'
  );
  console.log(`Уроков: ${lessons.length}`);

  // Группируем уроки по курсу
  const byCourse = Object.create(null);
  for (const lesson of lessons) {
    const courseSlug = lesson.course?.slug || lesson.course_id;
    if (!byCourse[courseSlug]) byCourse[courseSlug] = [];
    byCourse[courseSlug].push(lesson);
  }

  fs.mkdirSync(OUT_DIR, { recursive: true });

  // Для каждого курса — папка, для каждого урока — файл
  const indexLines = ['# ИИздец — База знаний\n', `Источник: aizdec.me  \nСобрано: ${new Date().toLocaleDateString('ru-RU')}\n`];

  for (const course of courses) {
    const courseLessons = byCourse[course.slug] || [];
    if (courseLessons.length === 0) continue;

    const courseDir = path.join(OUT_DIR, course.slug);
    fs.mkdirSync(courseDir, { recursive: true });

    indexLines.push(`\n## ${course.title}\n`);
    let num = 0;

    for (const lesson of courseLessons) {
      num++;
      const md = blocksToMd(lesson.content);
      const filename = sanitizeFilename(lesson.slug);
      const filepath = path.join(courseDir, filename);

      const hasContent = md.trim().length > 0;
      const body = hasContent ? md : '_Контент урока пуст._';

      const file = `# ${lesson.title}\n\n**Курс:** ${course.title}  \n**URL:** https://www.aizdec.me/courses/${course.slug}/${lesson.slug}\n\n---\n\n${body}\n`;
      fs.writeFileSync(filepath, file, 'utf8');

      const status = hasContent ? '✅' : '⚠️';
      indexLines.push(`${num}. ${status} [${lesson.title}](./${course.slug}/${filename})`);
      process.stdout.write(`  [${num}] ${lesson.title} — ${hasContent ? md.length + ' символов' : 'пусто'}\n`);
    }
  }

  fs.writeFileSync(path.join(OUT_DIR, 'index.md'), indexLines.join('\n'), 'utf8');

  const total = lessons.length;
  const withContent = lessons.filter(l => Array.isArray(l.content) && l.content.length > 0).length;
  console.log(`\nГотово! ${withContent}/${total} уроков с контентом.`);
  console.log(`Файлы: ${OUT_DIR}`);
}

main().catch(err => { console.error(err); process.exit(1); });
