const sharp = require('sharp');
const path = require('path');

const sourceDir = __dirname;
const outputDir = path.resolve(__dirname, '../../../../../articles/04-双11购物车先分4类/final-20261013');

const escapeXml = (value) => value
  .replaceAll('&', '&amp;')
  .replaceAll('<', '&lt;')
  .replaceAll('>', '&gt;');

async function renderPhotos() {
  await sharp(path.join(sourceDir, 'cover-source.png'))
    .resize(2820, 1200, { fit: 'cover', position: 'centre' })
    .png({ compressionLevel: 9 })
    .toFile(path.join(outputDir, 'cover.png'));

  await sharp(path.join(sourceDir, 'image-01-source.png'))
    .resize(1600, 1200, { fit: 'cover', position: 'centre' })
    .png({ compressionLevel: 9 })
    .toFile(path.join(outputDir, 'image-01.png'));
}

function infographicOverlay() {
  const rows = [
    { number: '01', title: '计划内必需', body: '核对规格、数量和可接受价格', y: 285, accent: '#829480' },
    { number: '02', title: '计划内悦己', body: '预算装得下，喜欢可以算理由', y: 570, accent: '#829480' },
    { number: '03', title: '折扣冲动', body: '先留信息，隔一晚再决定', y: 858, accent: '#AC735C' },
    { number: '04', title: '凑单添置', body: '比较多花的钱和真正省下的钱', y: 1148, accent: '#AC735C' },
  ];

  const rowText = rows.map(({ number, title, body, y, accent }) => `
    <text x="92" y="${y + 46}" class="num" fill="${accent}">${number}</text>
    <text x="330" y="${y + 72}" class="rowTitle">${escapeXml(title)}</text>
    <text x="330" y="${y + 136}" class="rowBody">${escapeXml(body)}</text>
  `).join('');

  return Buffer.from(`
    <svg width="1200" height="1600" viewBox="0 0 1200 1600" xmlns="http://www.w3.org/2000/svg">
      <style>
        .mainTitle { font-family: "Microsoft YaHei", "SimHei", sans-serif; font-size: 58px; font-weight: 700; fill: #39352F; }
        .num { font-family: "Microsoft YaHei", "SimHei", sans-serif; font-size: 34px; font-weight: 700; letter-spacing: 2px; }
        .rowTitle { font-family: "Microsoft YaHei", "SimHei", sans-serif; font-size: 50px; font-weight: 700; fill: #39352F; }
        .rowBody { font-family: "Microsoft YaHei", "SimHei", sans-serif; font-size: 37px; font-weight: 400; fill: #39352F; }
        .tagline { font-family: "Microsoft YaHei", "SimHei", sans-serif; font-size: 37px; font-weight: 500; fill: #39352F; }
      </style>
      <text x="600" y="142" text-anchor="middle" class="mainTitle">购物车里的东西，先分成4类</text>
      ${rowText}
      <line x1="155" y1="1420" x2="1045" y2="1420" stroke="#AC735C" stroke-width="2" opacity="0.45"/>
      <text x="600" y="1495" text-anchor="middle" class="tagline">不同的购买理由，用不同的方法判断。</text>
    </svg>
  `);
}

async function renderInfographic() {
  const base = await sharp(path.join(sourceDir, 'image-02-base.png'))
    .resize(1200, 1600, { fit: 'fill' })
    .flatten({ background: '#F8F3EB' })
    .modulate({ saturation: 0.78, brightness: 1.02 })
    .png()
    .toBuffer();

  await sharp(base)
    .composite([{ input: infographicOverlay(), top: 0, left: 0 }])
    .png({ compressionLevel: 9 })
    .toFile(path.join(outputDir, 'image-02.png'));
}

async function main() {
  await renderPhotos();
  await renderInfographic();

  for (const name of ['cover.png', 'image-01.png', 'image-02.png']) {
    const metadata = await sharp(path.join(outputDir, name)).metadata();
    process.stdout.write(`${name}\t${metadata.width}x${metadata.height}\t${metadata.format}\n`);
  }
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
