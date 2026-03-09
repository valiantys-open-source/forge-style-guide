// .github/scripts/publish-to-hubspot.js
import { readFileSync } from 'fs';

const PAGE_ID = '207986636573';
const TOKEN = process.env.HUBSPOT_TOKEN;
const BASE = 'https://api.hubapi.com/cms/v3/pages/landing-pages';

const headers = {
  'Authorization': `Bearer ${TOKEN}`,
  'Content-Type': 'application/json'
};

async function getPage() {
  const res = await fetch(`${BASE}/${PAGE_ID}`, { headers });
  if (!res.ok) throw new Error(`GET failed: ${res.status} ${await res.text()}`);
  return res.json();
}

async function updateAndPublish(html) {
  const page = await getPage();
  const sections = structuredClone(page.layoutSections);
  sections.body_dnd_area.rows[1][0].rows[0][0].params.description = html;

  const patch = await fetch(`${BASE}/${PAGE_ID}`, {
    method: 'PATCH',
    headers,
    body: JSON.stringify({ layoutSections: sections })
  });
  if (!patch.ok) throw new Error(`PATCH failed: ${patch.status} ${await patch.text()}`);

  const publish = await fetch(`${BASE}/${PAGE_ID}/push-live`, {
    method: 'POST',
    headers
  });
  if (!publish.ok) throw new Error(`Publish failed: ${publish.status} ${await publish.text()}`);
}

async function run() {
  if (!TOKEN) throw new Error('HUBSPOT_TOKEN is not set');

  // Read the snippet output from the Python conversion step
  const html = readFileSync('./forge_style_guide_snippet.html', 'utf8');
  console.log(`Read snippet HTML: ${html.length} chars`);

  await updateAndPublish(html);
  console.log('Published successfully.');
}

run().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});