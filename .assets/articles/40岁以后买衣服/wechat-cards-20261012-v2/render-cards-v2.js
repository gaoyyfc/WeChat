const path = require('path');
const sharp = require('sharp');

const ROOT = __dirname;
const BASE = path.join(ROOT, 'base-images');
const FINAL = path.join(ROOT, 'final');
const W = 1200;
const H = 1600;

const C = {
  cream: '#F8F3EB',
  terra: '#AC735C',
  sage: '#829480',
  coffee: '#39352F',
  muted: '#625D56',
  line: '#D9CFC2',
  white: '#FFFDFC',
};

const font = 'Microsoft YaHei, PingFang SC, sans-serif';

function esc(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;');
}

function textBlock({ x, y, lines, size, weight = 400, color = C.coffee, lineHeight = 1.5, anchor = 'start', letterSpacing = 0 }) {
  const tspans = lines.map((line, index) =>
    `<tspan x="${x}" dy="${index === 0 ? 0 : Math.round(size * lineHeight)}">${esc(line)}</tspan>`
  ).join('');
  return `<text x="${x}" y="${y}" text-anchor="${anchor}" font-family="${font}" font-size="${size}" font-weight="${weight}" fill="${color}" letter-spacing="${letterSpacing}">${tspans}</text>`;
}

function svg(content, width = W, height = H) {
  return Buffer.from(`<svg width="${width}" height="${height}" viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg">${content}</svg>`);
}

function brandPill(x, y) {
  return `
    <rect x="${x}" y="${y}" width="220" height="54" rx="27" fill="${C.cream}" fill-opacity="0.94"/>
    <circle cx="${x + 28}" cy="${y + 27}" r="7" fill="${C.terra}"/>
    <text x="${x + 50}" y="${y + 35}" font-family="${font}" font-size="24" font-weight="600" fill="${C.coffee}">烟火有主意</text>`;
}

async function makePhotoTextCard({ baseName, photoHeight, position = 'centre', overlay, outputName }) {
  const photo = await sharp(path.join(BASE, baseName))
    .resize(W, photoHeight, { fit: 'cover', position })
    .png()
    .toBuffer();
  const output = path.join(FINAL, outputName);
  await sharp({ create: { width: W, height: H, channels: 4, background: C.cream } })
    .composite([
      { input: photo, top: 0, left: 0 },
      { input: svg(overlay), top: 0, left: 0 },
    ])
    .png({ compressionLevel: 9, adaptiveFiltering: true })
    .toFile(output);
  return output;
}

async function card2() {
  const overlay = `
    ${brandPill(70, 58)}
    <rect x="0" y="720" width="1200" height="880" fill="${C.cream}"/>
    <rect x="74" y="790" width="62" height="8" rx="4" fill="${C.terra}"/>
    ${textBlock({ x: 74, y: 878, lines: ['衣服真正的成本，', '不只写在吊牌上'], size: 56, weight: 700, lineHeight: 1.28 })}
    ${textBlock({ x: 78, y: 1074, lines: [
      '领口不舒服，穿半天就想脱；',
      '洗护麻烦，总要熨烫或送洗；',
      '为了搭它，还要再买裤子和鞋。'
    ], size: 39, lineHeight: 1.6, color: C.muted })}
    <line x1="78" y1="1312" x2="1122" y2="1312" stroke="${C.line}" stroke-width="2"/>
    ${textBlock({ x: 78, y: 1402, lines: ['这些麻烦，也算在衣服的价格里。'], size: 42, weight: 700, color: C.terra })}
    ${textBlock({ x: 78, y: 1518, lines: ['理性消费 · 实用经验'], size: 26, weight: 600, color: C.sage, letterSpacing: 2 })}
  `;
  return makePhotoTextCard({
    baseName: 'base-02.png',
    photoHeight: 720,
    position: 'right',
    overlay,
    outputName: 'card-02-resonance-v2.png',
  });
}

async function card3() {
  const overlay = `
    ${brandPill(70, 58)}
    <rect x="0" y="730" width="1200" height="870" fill="${C.cream}"/>
    <rect x="70" y="795" width="58" height="8" rx="4" fill="${C.sage}"/>
    ${textBlock({ x: 70, y: 878, lines: ['试衣服，别只站着照镜子'], size: 56, weight: 700 })}

    <rect x="70" y="947" width="510" height="366" rx="30" fill="${C.white}" stroke="${C.line}" stroke-width="2"/>
    <circle cx="137" cy="1020" r="38" fill="${C.terra}"/>
    <text x="137" y="1034" text-anchor="middle" font-family="${font}" font-size="30" font-weight="700" fill="${C.white}">摸</text>
    ${textBlock({ x: 197, y: 1034, lines: ['摸一摸'], size: 38, weight: 700, color: C.terra })}
    ${textBlock({ x: 112, y: 1125, lines: ['领口、袖口、里衬', '贴着皮肤时舒服吗？'], size: 38, lineHeight: 1.55, color: C.muted })}

    <rect x="620" y="947" width="510" height="366" rx="30" fill="${C.white}" stroke="${C.line}" stroke-width="2"/>
    <circle cx="687" cy="1020" r="38" fill="${C.sage}"/>
    <text x="687" y="1034" text-anchor="middle" font-family="${font}" font-size="30" font-weight="700" fill="${C.white}">动</text>
    ${textBlock({ x: 747, y: 1034, lines: ['动一动'], size: 38, weight: 700, color: C.sage })}
    ${textBlock({ x: 662, y: 1125, lines: ['坐下、抬手、走两步，', '有没有勒、卡、往上跑？'], size: 36, lineHeight: 1.55, color: C.muted })}

    <rect x="70" y="1380" width="1060" height="130" rx="26" fill="${C.coffee}" fill-opacity="0.07"/>
    ${textBlock({ x: 600, y: 1457, lines: ['缩水、掉色和起球，不能靠短时间试穿确定。'], size: 34, weight: 600, color: C.coffee, anchor: 'middle' })}
  `;
  return makePhotoTextCard({
    baseName: 'base-03-v2.png',
    photoHeight: 730,
    position: 'top',
    overlay,
    outputName: 'card-03-method-fit-v2.png',
  });
}

async function card5() {
  const overlay = `
    ${textBlock({ x: 600, y: 106, lines: ['烟火有主意 · 购前检查'], size: 26, weight: 600, color: C.sage, anchor: 'middle', letterSpacing: 2 })}
    ${textBlock({ x: 600, y: 205, lines: ['付款前，给自己30秒'], size: 64, weight: 700, color: C.coffee, anchor: 'middle' })}

    <circle cx="162" cy="455" r="50" fill="${C.terra}"/>
    <text x="162" y="472" text-anchor="middle" font-family="${font}" font-size="38" font-weight="700" fill="${C.white}">动</text>
    ${textBlock({ x: 250, y: 438, lines: ['动一动'], size: 46, weight: 700, color: C.terra })}
    ${textBlock({ x: 250, y: 510, lines: ['坐下、抬手、走两步。'], size: 42, weight: 500, color: C.coffee })}

    <circle cx="162" cy="770" r="50" fill="${C.sage}"/>
    <text x="162" y="787" text-anchor="middle" font-family="${font}" font-size="38" font-weight="700" fill="${C.white}">翻</text>
    ${textBlock({ x: 250, y: 753, lines: ['翻一翻'], size: 46, weight: 700, color: C.sage })}
    ${textBlock({ x: 250, y: 825, lines: ['查看成分与洗护说明。'], size: 42, weight: 500, color: C.coffee })}

    <circle cx="162" cy="1080" r="50" fill="${C.coffee}"/>
    <text x="162" y="1097" text-anchor="middle" font-family="${font}" font-size="38" font-weight="700" fill="${C.white}">想</text>
    ${textBlock({ x: 250, y: 1063, lines: ['想一想'], size: 46, weight: 700, color: C.coffee })}
    ${textBlock({ x: 250, y: 1135, lines: ['有没有现成衣物可以搭配。'], size: 42, weight: 500, color: C.coffee })}

    ${textBlock({ x: 600, y: 1374, lines: ['烟火有主意'], size: 54, weight: 700, color: C.terra, anchor: 'middle', letterSpacing: 4 })}
    ${textBlock({ x: 600, y: 1455, lines: ['不劝你盲目多买，也不劝你一味将就。'], size: 34, weight: 500, color: C.coffee, anchor: 'middle' })}
    ${textBlock({ x: 600, y: 1515, lines: ['一起把钱花明白，把日子过舒服。'], size: 34, weight: 600, color: C.coffee, anchor: 'middle' })}
  `;
  const output = path.join(FINAL, 'card-05-checklist-v2.png');
  await sharp(path.join(BASE, 'base-05.png'))
    .resize(W, H, { fit: 'cover', position: 'centre' })
    .composite([{ input: svg(overlay), top: 0, left: 0 }])
    .png({ compressionLevel: 9, adaptiveFiltering: true })
    .toFile(output);
  return output;
}

async function makePreview(files) {
  const thumbW = 340;
  const thumbH = 453;
  const gap = 28;
  const canvasW = 3 * thumbW + 4 * gap;
  const canvasH = 2 * thumbH + 3 * gap;
  const positions = [
    [gap, gap],
    [2 * gap + thumbW, gap],
    [3 * gap + 2 * thumbW, gap],
    [Math.round((canvasW - 2 * thumbW - gap) / 2), 2 * gap + thumbH],
    [Math.round((canvasW - 2 * thumbW - gap) / 2) + thumbW + gap, 2 * gap + thumbH],
  ];
  const layers = [];
  for (let index = 0; index < files.length; index += 1) {
    const thumb = await sharp(files[index]).resize(thumbW, thumbH, { fit: 'cover' }).png().toBuffer();
    layers.push({ input: thumb, left: positions[index][0], top: positions[index][1] });
  }
  const output = path.join(FINAL, 'preview-five-cards-v2.png');
  await sharp({ create: { width: canvasW, height: canvasH, channels: 4, background: C.cream } })
    .composite(layers)
    .png({ compressionLevel: 9 })
    .toFile(output);
  return output;
}

async function makeMobilePreview(files) {
  const cardW = 375;
  const cardH = 500;
  const gap = 24;
  const output = path.join(FINAL, 'qa-mobile-revised-v2.png');
  const layers = [];
  for (let index = 0; index < files.length; index += 1) {
    const thumb = await sharp(files[index]).resize(cardW, cardH, { fit: 'cover' }).png().toBuffer();
    layers.push({ input: thumb, left: gap + index * (cardW + gap), top: gap });
  }
  await sharp({ create: { width: files.length * cardW + (files.length + 1) * gap, height: cardH + 2 * gap, channels: 4, background: '#EEE8DE' } })
    .composite(layers)
    .png({ compressionLevel: 9 })
    .toFile(output);
  return output;
}

async function main() {
  const [c2, c3, c5] = await Promise.all([card2(), card3(), card5()]);
  const cards = [
    path.join(FINAL, 'card-01-hook.png'),
    c2,
    c3,
    path.join(FINAL, 'card-04-method-care-match.png'),
    c5,
  ];
  const preview = await makePreview(cards);
  const mobilePreview = await makeMobilePreview([c2, c3, c5]);
  console.log(JSON.stringify({ cards, preview, mobilePreview }, null, 2));
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
