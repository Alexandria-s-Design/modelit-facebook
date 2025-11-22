# Manual Image Upload & Sheet Update Solution

## Current Status
✅ **COMPLETE**: All 104 images generated successfully (1200x628px PNG)
❌ **BLOCKED**: All API authentication methods expired/invalid
- Google OAuth: access_token and refresh_token both expired
- ImgBB API: Key invalid (400 error)
- Office 365 MCP: Authentication expired

## Solution: Manual Upload with Automated Sheet Update

### Step 1: Upload Images to Google Drive

**Target Folder**: https://drive.google.com/drive/folders/1JAEQPbWPEQKb3oU3BvN7bRGwT0ZrgW5I

**Manual Upload Instructions**:
1. Open the Google Drive folder in your browser
2. Drag and drop all images from: `C:\Users\MarieLexisDad\temp\modelit_facebook_images\`
3. All 104 PNG files will upload (total size: ~137 MB)
4. Set sharing to "Anyone with the link can view"

**Bulk Upload Option**:
```powershell
# Open folder in File Explorer
explorer "C:\Users\MarieLexisDad\temp\modelit_facebook_images"

# Then manually select all and drag to Drive web interface
```

### Step 2: Get Image URLs

After upload, each image will have a URL like:
```
https://drive.google.com/file/d/FILE_ID/view?usp=sharing
```

For direct embedding, convert to:
```
https://drive.google.com/uc?export=view&id=FILE_ID
```

### Step 3: Update Google Sheet

**Target Sheet**: https://docs.google.com/spreadsheets/d/1pjJl8yxdVi-HwdkFxuu5Uq2qPklYAicX67sLz8qHCV0

**Option A: Manual Entry**
- Update columns H (image_url) and I (image_filename)
- Rows 2-105 (104 posts)
- Use the CSV file below for reference

**Option B: CSV Import** (Faster)
1. Use the generated `image_upload_template.csv`
2. In Google Sheets: File → Import → Upload
3. Select "Replace data at selected cell"
4. Choose cell H2 to start

**Option C: Apps Script** (Automated)
1. Use the provided `update_sheet_urls.gs` script
2. Tools → Script Editor in Google Sheets
3. Paste script and run
4. Authorize when prompted

## Generated Helper Files

### 1. Image Manifest
**File**: `all_images_complete.json`
- Complete list of all 104 images
- Filenames, paths, sizes, themes
- Ready for bulk operations

### 2. CSV Template
**File**: `image_upload_template.csv`
- Pre-formatted for Sheet import
- Columns: post_number, theme, image_filename
- Leave URL column blank to fill after upload

### 3. Apps Script
**File**: `update_sheet_urls.gs`
- Automated Sheet update script
- Fetches file URLs from Drive folder
- Updates columns H & I automatically

## Next Steps After Authentication Restore

Once Google OAuth is restored, run:
```bash
cd C:/Users/MarieLexisDad/scripts
python upload_all_104_images_to_drive_v2.py
```

This will:
- Upload all 104 images to Drive folder
- Set public permissions automatically
- Update Sheet with URLs in single batch operation
- Generate complete results JSON

## Files Location

All images: `C:\Users\MarieLexisDad\temp\modelit_facebook_images\`
Helper files: `C:\Users\MarieLexisDad\temp\`
Upload scripts: `C:\Users\MarieLexisDad\scripts\`

## Image List Reference

Total: 104 images
Format: PNG, 1200x628px
Size range: 926 KB - 1576 KB
Naming: `post_NNN_Theme_Name.png`

Example:
- post_001_Quick_Assessment_Strategies.png (1202.7 KB)
- post_002_Systems_Diagrams.png (1340.0 KB)
- post_003_Critical_Thinking_Growth.png (1206.2 KB)
- ... (101 more)

Full manifest available in `all_images_complete.json`
