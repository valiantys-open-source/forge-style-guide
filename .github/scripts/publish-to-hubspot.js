// test-publish.js
// Dry run (no writes):  HUBSPOT_TOKEN=xxx node test-publish.js
// Live update draft:    HUBSPOT_TOKEN=xxx node test-publish.js --update
// Update + publish:     HUBSPOT_TOKEN=xxx node test-publish.js --update --publish

const PAGE_ID = '207986636573';
const TOKEN = process.env.HUBSPOT_TOKEN;
const BASE = 'https://api.hubapi.com/cms/v3/pages/landing-pages';

const DRY_RUN = !process.argv.includes('--update');
const PUBLISH  = process.argv.includes('--publish');

const headers = {
  'Authorization': `Bearer ${TOKEN}`,
  'Content-Type': 'application/json'
};

const TEST_HTML = `<div style="padding: 2rem;">
  <h2>Test Update</h2>
  <p>This is a test update from the API. Timestamp: ${new Date().toISOString()}</p>
</div>`;

async function getPage() {
  const res = await fetch(`${BASE}/${PAGE_ID}`, { headers });
  if (!res.ok) throw new Error(`GET failed: ${res.status} ${await res.text()}`);
  return res.json();
}

async function updateDraft(page, html) {
  const sections = structuredClone(page.layoutSections);
  sections.body_dnd_area.rows[1][0].rows[0][0].params.description = html;

  if (DRY_RUN) {
    console.log('\n[DRY RUN] Would PATCH layoutSections with this description (first 300 chars):');
    console.log(html.slice(0, 300) + '...');
    console.log('\n[DRY RUN] Target module: widget_1769043508282');
    console.log('[DRY RUN] No changes written.');
    return null;
  }

  const res = await fetch(`${BASE}/${PAGE_ID}`, {
    method: 'PATCH',
    headers,
    body: JSON.stringify({ layoutSections: sections })
  });
  if (!res.ok) throw new Error(`PATCH failed: ${res.status} ${await res.text()}`);
  return res.json();
}

async function publishPage() {
  if (DRY_RUN) {
    console.log('[DRY RUN] Would POST to push-live. Skipping.');
    return;
  }
  const res = await fetch(`${BASE}/${PAGE_ID}/push-live`, {
    method: 'POST',
    headers
  });
  if (!res.ok) throw new Error(`Publish failed: ${res.status} ${await res.text()}`);
  return res.json();
}

async function run() {
  if (!TOKEN) throw new Error('HUBSPOT_TOKEN is not set');

  console.log(`Mode: ${DRY_RUN ? 'DRY RUN' : 'LIVE'}${PUBLISH && !DRY_RUN ? ' + PUBLISH' : ''}\n`);

  console.log('1. Fetching current page...');
  const page = await getPage();
  console.log(`   Page: "${page.name}"`);
  console.log(`   State: ${page.currentState}`);
  console.log(`   Last updated: ${page.updatedAt}`);

  const currentDesc = page.layoutSections?.body_dnd_area?.rows?.[1]?.[0]?.rows?.[0]?.[0]?.params?.description;
  console.log(`\n2. Current description length: ${currentDesc?.length ?? 'NOT FOUND'} chars`);
  if (!currentDesc) throw new Error('Could not locate target module. Check the row path.');

  console.log('\n3. Preparing update...');
  const updated = await updateDraft(page, TEST_HTML);
  if (updated) console.log(`   Draft updated at: ${updated.updatedAt}`);

  if (PUBLISH) {
    console.log('\n4. Publishing...');
    await publishPage();
    if (!DRY_RUN) console.log('   Published successfully.');
  }

  console.log('\nDone.');
}

run().catch(err => {
  console.error('\nError:', err.message);
  process.exit(1);
});