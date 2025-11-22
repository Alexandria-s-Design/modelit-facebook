/**
 * Generate all 104 ModelIT Instagram images using OpenAI DALL-E
 * Version 2: Simplified prompts and better error handling
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

// Load environment variables from PowerShell profile
const OPENAI_API_KEY = process.env.OPENAI_API_KEY;

// Configuration
const JSON_FILE = 'C:\\Users\\MarieLexisDad\\docs\\ModelIT_Instagram_104_Posts_Complete.json';
const OUTPUT_DIR = 'C:\\Users\\MarieLexisDad\\docs\\modelit-instagram-images';

// Theme-specific visual keywords (simplified)
const THEME_VISUALS = {
  "Systems Thinking & Modeling": "interconnected network, biological systems, flowing connections",
  "Hands-On STEM Activities": "students working together, science lab, interactive classroom",
  "Teacher Time-Savers": "organized desk, digital tools, efficient workflow",
  "Student Engagement Strategies": "excited students learning, lightbulb moment, classroom discovery"
};

/**
 * Load all posts from JSON
 */
function loadPosts() {
  const data = JSON.parse(fs.readFileSync(JSON_FILE, 'utf8'));
  return data.posts;
}

/**
 * Create output directory if it doesn't exist
 */
function createOutputDirectory() {
  if (!fs.existsSync(OUTPUT_DIR)) {
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
  }
  console.log(`📁 Output directory: ${OUTPUT_DIR}\n`);
}

/**
 * Create simplified prompt for DALL-E
 */
function createSimplifiedPrompt(theme, topic) {
  const visualElements = THEME_VISUALS[theme] || "educational classroom scene";

  // Keep it under 1000 characters for DALL-E
  return `Professional Instagram square image for ModelIT K12 educational platform.
Modern minimalist style with deep blue (#0f6de6) accents and clean white background.
Theme: ${theme}
Visual: ${visualElements} representing "${topic}"
Square 1080x1080px, no text, high contrast, professional, suitable for teachers.
Style: clean, inspiring, Apple-like aesthetic for science education.`;
}

/**
 * Download image from URL
 */
function downloadImage(url, filepath) {
  return new Promise((resolve, reject) => {
    const file = fs.createWriteStream(filepath);
    https.get(url, (response) => {
      response.pipe(file);
      file.on('finish', () => {
        file.close();
        resolve(true);
      });
    }).on('error', (err) => {
      fs.unlink(filepath, () => {});
      reject(err);
    });
  });
}

/**
 * Generate image using OpenAI DALL-E
 */
async function generateImageOpenAI(prompt, outputPath, postId) {
  if (!OPENAI_API_KEY) {
    console.log(`❌ Post ${postId}: No OPENAI_API_KEY found`);
    return { success: false, error: 'No API key' };
  }

  const data = JSON.stringify({
    model: 'dall-e-3',
    prompt: prompt,
    n: 1,
    size: '1024x1024',
    quality: 'standard'
  });

  const options = {
    hostname: 'api.openai.com',
    port: 443,
    path: '/v1/images/generations',
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${OPENAI_API_KEY}`,
      'Content-Type': 'application/json',
      'Content-Length': data.length
    }
  };

  return new Promise((resolve) => {
    const req = https.request(options, (res) => {
      let responseData = '';

      res.on('data', (chunk) => {
        responseData += chunk;
      });

      res.on('end', async () => {
        if (res.statusCode === 200) {
          try {
            const result = JSON.parse(responseData);
            const imageUrl = result.data[0].url;

            // Download the image
            await downloadImage(imageUrl, outputPath);
            console.log(`✅ Post ${postId}: Generated successfully`);
            resolve({ success: true });
          } catch (err) {
            console.log(`❌ Post ${postId}: Error: ${err.message}`);
            resolve({ success: false, error: err.message });
          }
        } else {
          let errorMsg = `API error ${res.statusCode}`;
          try {
            const errorData = JSON.parse(responseData);
            errorMsg = errorData.error?.message || errorMsg;
            console.log(`❌ Post ${postId}: ${errorMsg}`);
          } catch (e) {
            console.log(`❌ Post ${postId}: ${errorMsg}`);
            console.log(`   Response: ${responseData.substring(0, 200)}`);
          }
          resolve({ success: false, error: errorMsg });
        }
      });
    });

    req.on('error', (err) => {
      console.log(`❌ Post ${postId}: Request error: ${err.message}`);
      resolve({ success: false, error: err.message });
    });

    req.write(data);
    req.end();
  });
}

/**
 * Sleep for specified milliseconds
 */
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Main function to generate all 104 images
 */
async function generateAllImages() {
  console.log("🎨 Starting image generation for all 104 posts...\n");

  // Check API key
  if (!OPENAI_API_KEY) {
    console.log("❌ ERROR: OPENAI_API_KEY environment variable not found!");
    console.log("Please set your OpenAI API key in the environment variables.");
    return { successful: 0, failed: 0, total: 0 };
  }

  // Load posts
  const posts = loadPosts();
  console.log(`📊 Loaded ${posts.length} posts\n`);

  // Create output directory
  createOutputDirectory();

  // Track progress
  let successful = 0;
  let failed = 0;
  let skipped = 0;
  const failures = [];

  // Generate each image
  for (let i = 0; i < posts.length; i++) {
    const post = posts[i];
    const postId = post.post_id;
    const theme = post.theme;
    const topic = post.topic;
    const filename = post.image_filename;
    const outputPath = path.join(OUTPUT_DIR, filename);

    // Skip if already exists
    if (fs.existsSync(outputPath)) {
      console.log(`⏭️  Post ${postId}: Already exists, skipping`);
      successful++;
      skipped++;
      continue;
    }

    console.log(`\n📸 Generating image ${i + 1}/104: ${postId}`);
    console.log(`   Theme: ${theme}`);
    console.log(`   Topic: ${topic.substring(0, 60)}...`);

    // Create simplified prompt
    const prompt = createSimplifiedPrompt(theme, topic);

    // Try to generate
    const result = await generateImageOpenAI(prompt, outputPath, postId);

    if (result.success) {
      successful++;
    } else {
      failed++;
      failures.push({ postId, theme, topic, error: result.error });

      // If we get rate limited, wait longer
      if (result.error && result.error.includes('rate')) {
        console.log(`   ⏳ Rate limited, waiting 60 seconds...`);
        await sleep(60000);
      }
    }

    // Rate limiting - wait between requests
    if (i < posts.length - 1) {
      const waitTime = 5000; // 5 seconds
      console.log(`   ⏳ Waiting ${waitTime/1000} seconds before next request...`);
      await sleep(waitTime);
    }

    // Progress update every 10 images
    if ((i + 1) % 10 === 0) {
      console.log(`\n📊 Progress: ${i + 1}/104 (${((i + 1) / 104 * 100).toFixed(1)}%)`);
      console.log(`   ✅ Successful: ${successful} (${skipped} skipped)`);
      console.log(`   ❌ Failed: ${failed}\n`);
    }
  }

  // Final summary
  console.log("\n" + "=".repeat(70));
  console.log("🎉 IMAGE GENERATION COMPLETE!");
  console.log("=".repeat(70));
  console.log(`✅ Successfully generated: ${successful}/${posts.length} (${skipped} already existed)`);
  console.log(`❌ Failed: ${failed}/${posts.length}`);
  console.log(`📁 Images saved to: ${OUTPUT_DIR}`);

  // Show failures if any
  if (failures.length > 0) {
    console.log(`\n❌ Failed posts (${failures.length}):`);
    failures.forEach(f => {
      console.log(`   Post ${f.postId}: ${f.error}`);
    });
  }

  console.log("=".repeat(70));

  // Save failure report if needed
  if (failures.length > 0) {
    const reportPath = path.join(OUTPUT_DIR, 'generation_failures.json');
    fs.writeFileSync(reportPath, JSON.stringify(failures, null, 2));
    console.log(`\n📝 Failure report saved to: ${reportPath}`);
  }

  return { successful, failed, total: posts.length, failures };
}

// Run if called directly
if (require.main === module) {
  generateAllImages().catch(console.error);
}

module.exports = { generateAllImages };
