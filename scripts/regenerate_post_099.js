/**
 * Regenerate failed Post 099 image
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

// Load environment variables
require('dotenv').config();

const OPENAI_API_KEY = process.env.OPENAI_API_KEY;
const OUTPUT_DIR = 'C:\\Users\\MarieLexisDad\\docs\\modelit-instagram-images';

// Post 099 data
const post = {
  post_id: '099',
  theme: 'Teacher Time-Savers',
  topic: 'Teacher wellness and time management',
  image_description: 'Clean, minimalist graphic showing balanced scales with teacher wellness icons, positive energy, ModelIT blue with white space, conveying work-life balance'
};

function enhancePrompt(description, theme, topic) {
  const themeVisuals = {
    'Teacher Time-Savers': 'organized workspace, clock with positive energy, digital tools, streamlined efficiency'
  };

  const visualElements = themeVisuals[theme];

  return `Create a professional Instagram post image (1080x1080px square) for ModelIT K12.

VISUAL STYLE:
- Modern, minimalist design
- Primary color: Deep blue (#0f6de6)
- Clean white or light background
- Professional and scientific aesthetic
- Lots of white space
- High contrast for mobile viewing

CONTENT:
${visualElements}

THEME: ${theme}
TOPIC: ${topic}

REQUIREMENTS:
- Square format (1080x1080px)
- No text overlays
- Instagram-optimized (bright, clean, eye-catching)
- Professional quality
- Suitable for teacher audience

AVOID:
- Cluttered designs
- Dark or muddy colors
- Stock photo clichés
- Text in the image
- Overly complex illustrations

Think: Apple meets science classroom - sleek, inspiring, accessible.`;
}

function generateImage() {
  return new Promise((resolve, reject) => {
    const prompt = enhancePrompt(post.image_description, post.theme, post.topic);

    const requestBody = JSON.stringify({
      model: 'dall-e-3',
      prompt: prompt,
      n: 1,
      size: '1024x1024',
      quality: 'standard'
    });

    const options = {
      hostname: 'api.openai.com',
      path: '/v1/images/generations',
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${OPENAI_API_KEY}`,
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(requestBody)
      }
    };

    console.log(`🔄 Regenerating Post ${post.post_id}...`);
    console.log(`   Theme: ${post.theme}`);
    console.log(`   Topic: ${post.topic}`);

    const req = https.request(options, (res) => {
      let data = '';

      res.on('data', (chunk) => {
        data += chunk;
      });

      res.on('end', () => {
        if (res.statusCode === 200) {
          const result = JSON.parse(data);
          const imageUrl = result.data[0].url;

          // Download the image
          https.get(imageUrl, (imgRes) => {
            const outputPath = path.join(OUTPUT_DIR, `Post_${post.post_id}_Image.png`);
            const fileStream = fs.createWriteStream(outputPath);

            imgRes.pipe(fileStream);

            fileStream.on('finish', () => {
              fileStream.close();
              console.log(`✅ Post ${post.post_id}: Successfully regenerated!`);
              console.log(`📁 Saved to: ${outputPath}`);
              resolve();
            });
          }).on('error', (err) => {
            console.error(`❌ Download error: ${err.message}`);
            reject(err);
          });
        } else {
          console.error(`❌ API Error ${res.statusCode}: ${data}`);
          reject(new Error(`API returned ${res.statusCode}`));
        }
      });
    });

    req.on('error', (err) => {
      console.error(`❌ Request error: ${err.message}`);
      reject(err);
    });

    req.write(requestBody);
    req.end();
  });
}

// Run the regeneration
generateImage()
  .then(() => {
    console.log('\n✅ Regeneration complete!');
    process.exit(0);
  })
  .catch((err) => {
    console.error('\n❌ Regeneration failed:', err.message);
    process.exit(1);
  });
