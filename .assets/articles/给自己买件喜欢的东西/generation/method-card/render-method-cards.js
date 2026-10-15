const fs = require('fs');
const path = require('path');
const sharp = require('sharp');

const base = __dirname;
const jobs = [
  ['image-02-method-card-horizontal.svg', 'image-02-method-card-horizontal.png', 1440, 1080],
  ['image-02-method-card-vertical.svg', 'image-02-method-card-vertical.png', 1080, 1440],
];

(async () => {
  for (const [source, output, width, height] of jobs) {
    const input = fs.readFileSync(path.join(base, source));
    await sharp(input, { density: 144 })
      .resize(width, height, { fit: 'fill' })
      .png({ compressionLevel: 9, adaptiveFiltering: true })
      .toFile(path.join(base, output));
  }
})().catch((error) => {
  console.error(error);
  process.exit(1);
});
