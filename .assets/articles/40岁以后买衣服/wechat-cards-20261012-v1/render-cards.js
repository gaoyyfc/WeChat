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
  muted: '#746E65',
  line: '#D9CFC2',
  white: '#FFFDFC',
};

const font = "Microsoft YaHei, PingFang SC, sans-serif";

function esc(s) {
  return String(s)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;');
}

function textBlock({ x, y, lines, size, weight = 400, color = C.coffee, lineHeight = 1.5, anchor = 'start', letterSpacing = 0 }) {
  const tspans = lines.map((line, i) =>
    `<tspan x="${x}" dy="${i === 0 ? 0 : Math.round(size * lineHeight)}">${esc(line)}</tspan>`
  ).join('');
  return `<text x="${x}" y="${y}" text-anchor="${anchor}" font-family="${font}" font-size="${size}" font-weight="${weight}" fill="${color}" letter-spacing="${letterSpacing}">${tspans}</text>`;
}

function svgWrap(content) {
  return Buffer.from(`<svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" xmlns="http://www.w3.org/2000/svg">${content}</svg>`);
}

function brandPill(x, y, label = '烟火有主意') {
  return `
    <rect x="${x}" y="${y}" width="220" height="54" rx="27" fill="${C.cream}" fill-opacity="0.94"/>
    <circle cx="${x + 28}" cy="${y + 27}" r="7" fill="${C.terra}"/>
    <text x="${x + 50}" y="${y + 35}" font-family="${font}" font-size="24" font-weight="600" fill="${C.coffee}">${label}</text>`;
}

async function compose(baseName, outName, overlay) {
  const basePath = path.join(BASE, baseName);
  const outPath = path.join(FINAL, outName);
  await sharp(basePath)
    .resize(W, H, { fit: 'cover', position: 'centre' })
    .composite([{ input: svgWrap(overlay), top: 0, left: 0 }])
    .png({ compressionLevel: 9, adaptiveFiltering: true })
    .toFile(outPath);
  return outPath;
}

async function card1() {
  const overlay = `
    ${brandPill(68, 64)}
    <rect x="0" y="815" width="1200" height="785" fill="${C.cream}" fill-opacity="0.985"/>
    <rect x="78" y="895" width="62" height="8" rx="4" fill="${C.terra}"/>
    ${textBlock({ x: 78, y: 982, lines: ['打折买的衣服，', '为什么反而最容易闲置？'], size: 58, weight: 700, lineHeight: 1.28 })}
    ${textBlock({ x: 80, y: 1182, lines: ['买的时候觉得捡了便宜，', '回家后才发现——', '穿着不舒服，不好打理，', '也找不到现成的衣服搭。'], size: 37, lineHeight: 1.48, color: C.muted })}
    <line x1="80" y1="1430" x2="1120" y2="1430" stroke="${C.line}" stroke-width="2"/>
    ${textBlock({ x: 80, y: 1505, lines: ['最后，它只是挂在衣柜里。'], size: 36, weight: 700, color: C.terra })}
  `;
  return compose('base-01.png', 'card-01-hook.png', overlay);
}

async function card2() {
  const overlay = `
    <rect x="0" y="0" width="548" height="1600" fill="${C.cream}" fill-opacity="0.965"/>
    <rect x="68" y="82" width="8" height="168" rx="4" fill="${C.terra}"/>
    ${textBlock({ x: 105, y: 130, lines: ['烟火有主意'], size: 24, weight: 600, color: C.sage, letterSpacing: 2 })}
    ${textBlock({ x: 68, y: 340, lines: ['衣服真正的成本，', '不只写在吊牌上'], size: 51, weight: 700, lineHeight: 1.35 })}
    ${textBlock({ x: 70, y: 600, lines: ['领口扎，穿半天就想脱；', '版型紧，坐下来不自在；', '洗过几次就懒得再穿；', '为了搭它，还要再买', '裤子和鞋。'], size: 36, lineHeight: 1.52, color: C.muted })}
    <rect x="68" y="1048" width="414" height="196" rx="26" fill="${C.terra}" fill-opacity="0.12"/>
    ${textBlock({ x: 100, y: 1115, lines: ['这些麻烦，', '也算在衣服的价格里。'], size: 38, weight: 700, lineHeight: 1.48, color: C.terra })}
    <line x1="68" y1="1455" x2="474" y2="1455" stroke="${C.line}" stroke-width="2"/>
    ${textBlock({ x: 68, y: 1512, lines: ['理性消费 · 实用经验'], size: 24, weight: 500, color: C.sage, letterSpacing: 2 })}
  `;
  return compose('base-02.png', 'card-02-resonance.png', overlay);
}

async function card3() {
  const overlay = `
    ${brandPill(68, 58)}
    <rect x="0" y="790" width="1200" height="810" fill="${C.cream}" fill-opacity="0.985"/>
    <rect x="74" y="862" width="58" height="8" rx="4" fill="${C.sage}"/>
    ${textBlock({ x: 74, y: 946, lines: ['试衣服，别只站着照镜子'], size: 56, weight: 700 })}
    <rect x="70" y="1020" width="500" height="345" rx="30" fill="${C.white}" stroke="${C.line}" stroke-width="2"/>
    <circle cx="133" cy="1087" r="34" fill="${C.terra}"/>
    <text x="133" y="1099" text-anchor="middle" font-family="${font}" font-size="28" font-weight="700" fill="${C.white}">摸</text>
    ${textBlock({ x: 186, y: 1099, lines: ['摸一摸'], size: 34, weight: 700, color: C.terra })}
    ${textBlock({ x: 112, y: 1178, lines: ['领口、袖口、里衬', '贴着皮肤时舒服吗？'], size: 35, lineHeight: 1.55, color: C.muted })}
    <rect x="630" y="1020" width="500" height="345" rx="30" fill="${C.white}" stroke="${C.line}" stroke-width="2"/>
    <circle cx="693" cy="1087" r="34" fill="${C.sage}"/>
    <text x="693" y="1099" text-anchor="middle" font-family="${font}" font-size="28" font-weight="700" fill="${C.white}">动</text>
    ${textBlock({ x: 746, y: 1099, lines: ['动一动'], size: 34, weight: 700, color: C.sage })}
    ${textBlock({ x: 672, y: 1178, lines: ['坐下、抬手、走两步，', '有没有勒、卡、往上跑？'], size: 34, lineHeight: 1.55, color: C.muted })}
    <rect x="70" y="1410" width="1060" height="112" rx="24" fill="${C.coffee}" fill-opacity="0.06"/>
    ${textBlock({ x: 600, y: 1478, lines: ['缩水、掉色和起球，不能靠短时间试穿确定。'], size: 31, weight: 500, color: C.muted, anchor: 'middle' })}
  `;
  return compose('base-03.png', 'card-03-method-fit.png', overlay);
}

async function card4() {
  const overlay = `
    ${brandPill(68, 58)}
    <rect x="0" y="770" width="1200" height="830" fill="${C.cream}" fill-opacity="0.985"/>
    <rect x="72" y="840" width="62" height="8" rx="4" fill="${C.terra}"/>
    ${textBlock({ x: 72, y: 926, lines: ['付款前，看看洗护标签', '和自己的衣柜'], size: 54, weight: 700, lineHeight: 1.32 })}
    <rect x="70" y="1080" width="1060" height="150" rx="28" fill="${C.white}" stroke="${C.line}" stroke-width="2"/>
    <circle cx="132" cy="1155" r="33" fill="${C.terra}"/>
    <text x="132" y="1167" text-anchor="middle" font-family="${font}" font-size="25" font-weight="700" fill="${C.white}">洗</text>
    ${textBlock({ x: 190, y: 1138, lines: ['看洗护'], size: 32, weight: 700, color: C.terra })}
    ${textBlock({ x: 190, y: 1191, lines: ['能不能机洗，是否需要熨烫或专业洗护。'], size: 34, color: C.muted })}
    <rect x="70" y="1260" width="1060" height="150" rx="28" fill="${C.white}" stroke="${C.line}" stroke-width="2"/>
    <circle cx="132" cy="1335" r="33" fill="${C.sage}"/>
    <text x="132" y="1347" text-anchor="middle" font-family="${font}" font-size="25" font-weight="700" fill="${C.white}">搭</text>
    ${textBlock({ x: 190, y: 1318, lines: ['想搭配'], size: 32, weight: 700, color: C.sage })}
    ${textBlock({ x: 190, y: 1371, lines: ['有没有现成裤子、鞋子和外套可以搭。'], size: 34, color: C.muted })}
    ${textBlock({ x: 600, y: 1505, lines: ['不好打理，又要继续添置，再低的折扣也未必划算。'], size: 32, weight: 600, color: C.coffee, anchor: 'middle' })}
  `;
  return compose('base-04.png', 'card-04-method-care-match.png', overlay);
}

async function card5() {
  const overlay = `
    ${textBlock({ x: 600, y: 126, lines: ['烟火有主意 · 购前检查'], size: 24, weight: 600, color: C.sage, anchor: 'middle', letterSpacing: 2 })}
    ${textBlock({ x: 600, y: 225, lines: ['付款前，给自己30秒'], size: 62, weight: 700, color: C.coffee, anchor: 'middle' })}
    <rect x="118" y="410" width="90" height="90" rx="45" fill="${C.terra}"/>
    <text x="163" y="468" text-anchor="middle" font-family="${font}" font-size="34" font-weight="700" fill="${C.white}">动</text>
    ${textBlock({ x: 254, y: 444, lines: ['动一动'], size: 40, weight: 700, color: C.terra })}
    ${textBlock({ x: 254, y: 505, lines: ['坐下、抬手、走两步。'], size: 36, color: C.muted })}
    <rect x="118" y="725" width="90" height="90" rx="45" fill="${C.sage}"/>
    <text x="163" y="783" text-anchor="middle" font-family="${font}" font-size="34" font-weight="700" fill="${C.white}">翻</text>
    ${textBlock({ x: 254, y: 759, lines: ['翻一翻'], size: 40, weight: 700, color: C.sage })}
    ${textBlock({ x: 254, y: 820, lines: ['查看成分与洗护说明。'], size: 36, color: C.muted })}
    <rect x="118" y="1042" width="90" height="90" rx="45" fill="${C.coffee}"/>
    <text x="163" y="1100" text-anchor="middle" font-family="${font}" font-size="34" font-weight="700" fill="${C.white}">想</text>
    ${textBlock({ x: 254, y: 1076, lines: ['想一想'], size: 40, weight: 700, color: C.coffee })}
    ${textBlock({ x: 254, y: 1137, lines: ['有没有现成衣物可以搭配。'], size: 36, color: C.muted })}
    ${textBlock({ x: 600, y: 1378, lines: ['烟火有主意'], size: 40, weight: 700, color: C.terra, anchor: 'middle', letterSpacing: 3 })}
    ${textBlock({ x: 600, y: 1443, lines: ['不劝你盲目多买，也不劝你一味将就。'], size: 30, color: C.coffee, anchor: 'middle' })}
    ${textBlock({ x: 600, y: 1497, lines: ['一起把钱花明白，把日子过舒服。'], size: 30, color: C.coffee, anchor: 'middle' })}
  `;
  return compose('base-05.png', 'card-05-checklist.png', overlay);
}

async function makePreview(files) {
  const thumbW = 340;
  const thumbH = 453;
  const gap = 28;
  const margin = 32;
  const canvasW = 3 * thumbW + 4 * gap;
  const canvasH = 2 * thumbH + 3 * gap;
  const positions = [
    [gap, gap],
    [2 * gap + thumbW, gap],
    [3 * gap + 2 * thumbW, gap],
    [Math.round((canvasW - 2 * thumbW - gap) / 2), 2 * gap + thumbH],
    [Math.round((canvasW - 2 * thumbW - gap) / 2) + thumbW + gap, 2 * gap + thumbH],
  ];
  const comps = [];
  for (let i = 0; i < files.length; i++) {
    const thumb = await sharp(files[i]).resize(thumbW, thumbH, { fit: 'cover' }).png().toBuffer();
    comps.push({ input: thumb, left: positions[i][0], top: positions[i][1] });
  }
  const previewPath = path.join(FINAL, 'preview-five-cards.png');
  await sharp({
    create: { width: canvasW, height: canvasH, channels: 4, background: C.cream },
  }).composite(comps).png({ compressionLevel: 9 }).toFile(previewPath);
  return previewPath;
}

async function main() {
  const outputs = await Promise.all([card1(), card2(), card3(), card4(), card5()]);
  const preview = await makePreview(outputs);
  console.log(JSON.stringify({ outputs, preview }, null, 2));
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
