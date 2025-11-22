# ModelIT K12 Instagram Automation Guide
## Make.com + Ayrshare Complete Setup

---

## Overview

This guide shows you how to **fully automate** your 104 Instagram posts using:
- **JSON data file** (all posts pre-configured)
- **Make.com** (automation platform)
- **Ayrshare** (social media posting API)
- **Google Drive** (image storage)

**End Result**: Set it and forget it - all 104 posts automatically posted at the right times over 52 weeks!

---

## Architecture

```
JSON File (all 104 posts)
       ↓
Make.com Scenario (scheduler)
       ↓
Ayrshare API (posts to Instagram)
       ↓
Instagram Account (@modelitk12)
```

---

## Prerequisites

### 1. **Ayrshare Account**
- Sign up at: https://www.ayrshare.com
- **Plan needed**: Growth Plan ($149/month) or higher
  - Includes Instagram scheduling
  - 1,000 posts/month (more than enough for 104 posts)
- Get your **API key** from Settings → API

### 2. **Make.com Account**
- Sign up at: https://www.make.com
- **Free plan** works (1,000 operations/month)
- Or **Core plan** ($9/month) for more operations

### 3. **Google Drive**
- You already have this
- Will store images for posts
- Make.com can access files directly

### 4. **Instagram Business Account**
- Connected to Facebook Page
- Ayrshare will post through Facebook/Instagram API

---

## Step 1: Prepare Your Images

### Upload Images to Google Drive

**Folder Structure**:
```
📁 ModelIT Instagram Campaign
   ├── Post_001_Image.png
   ├── Post_002_Image.png
   ├── Post_003_Image.png
   └── ... (all 104 images)
```

**Get Public URLs for Each Image**:
1. Right-click image in Google Drive
2. Click "Get link"
3. Set to "Anyone with the link"
4. Copy URL
5. Format it for direct access:
   - Original: `https://drive.google.com/file/d/FILE_ID/view?usp=sharing`
   - Direct: `https://drive.google.com/uc?export=view&id=FILE_ID`

**Or Use Make.com to Auto-Generate URLs** (recommended):
- Make.com can list files from Google Drive
- Automatically get download URLs
- No manual work needed!

---

## Step 2: Set Up Ayrshare

### Connect Instagram to Ayrshare

1. Log into Ayrshare dashboard
2. Go to **Integrations** → **Social Accounts**
3. Click **Connect Instagram**
4. Follow Instagram Business Account connection flow
5. Verify connection is active

### Get Your API Key

1. Go to **Settings** → **API**
2. Copy your **API Key**
3. Save it securely (you'll need it for Make.com)

### Test API

Using Make.com's HTTP module or Postman:

```json
POST https://app.ayrshare.com/api/post
Headers:
  Authorization: Bearer YOUR_API_KEY
  Content-Type: application/json

Body:
{
  "post": "Test post from Ayrshare API!",
  "platforms": ["instagram"],
  "scheduleDate": "2025-01-05T19:00:00Z"
}
```

If successful, you'll get a response with `status: "success"`

---

## Step 3: Create Make.com Scenario

### Scenario Architecture

**Trigger**: Scheduled (runs weekly)
**Actions**:
1. Read JSON file (from Google Drive or HTTP)
2. Filter posts for current week
3. For each post:
   - Get image URL from Google Drive
   - Format caption
   - Call Ayrshare API to schedule post

### Scenario Blueprint

**Module 1: Scheduler**
- **Type**: Schedule
- **Frequency**: Every Sunday at 6:00 AM
- **Why**: Schedules the week's posts ahead of time

**Module 2: HTTP - Get JSON**
- **Type**: HTTP → Make a request
- **URL**: Your JSON file location (Google Drive public URL or GitHub)
- **Method**: GET
- **Parse response**: Yes

**Module 3: Iterator**
- **Type**: Flow Control → Iterator
- **Array**: `{{2.data.posts}}`
- **Why**: Loops through each post in JSON

**Module 4: Filter - Current Week**
- **Type**: Filter
- **Condition**: `{{4.week}}` equals `{{formatDate(now, "W")}}`
- **Why**: Only process posts for current week

**Module 5: Google Drive - Get File**
- **Type**: Google Drive → Download a File
- **File Name**: `{{4.image_filename}}`
- **Folder**: ModelIT Instagram Campaign

**Module 6: Ayrshare - Schedule Post**
- **Type**: HTTP → Make a request
- **URL**: `https://app.ayrshare.com/api/post`
- **Method**: POST
- **Headers**:
  - `Authorization`: `Bearer YOUR_AYRSHARE_API_KEY`
  - `Content-Type`: `application/json`
- **Body**:
```json
{
  "post": "{{4.caption}}",
  "platforms": {{4.platforms}},
  "scheduleDate": "{{4.schedule_date}}",
  "mediaUrls": ["{{5.data.webContentLink}}"]
}
```

**Module 7: Error Handler** (optional)
- Catches failed posts
- Logs to Google Sheets or sends email alert

---

## Step 4: Simplified Automation (Recommended Approach)

### Option A: Weekly Manual Trigger

**Instead of fully automated**, manually trigger each week:

1. **Sunday morning routine** (5 minutes):
   - Open Make.com scenario
   - Click "Run once"
   - Scenario reads JSON, schedules this week's 2 posts
   - Done!

**Benefits**:
- Full control
- Review posts before they go out
- No risk of automated mistakes
- Free Make.com plan works

### Option B: Batch Schedule All 104 at Once

**One-time setup**:
1. Upload all 104 images to Google Drive
2. Run Make.com scenario ONCE
3. It schedules all 104 posts for their designated dates
4. Walk away - done for the year!

**Make.com Scenario for Batch**:
- No filter needed
- Iterator loops through ALL 104 posts
- Each one scheduled with Ayrshare
- Total operations: ~104 (within free plan!)

---

## Step 5: Make.com Scenario Template (Copy-Paste Ready)

### Full Scenario JSON

Save this as a `.json` file and import into Make.com:

```json
{
  "name": "ModelIT Instagram Automation",
  "flow": [
    {
      "id": 1,
      "module": "builtin:BasicScheduler",
      "version": 1,
      "parameters": {
        "interval": 1,
        "unit": "week",
        "day": "sunday",
        "time": "06:00"
      }
    },
    {
      "id": 2,
      "module": "http:ActionSendData",
      "version": 3,
      "parameters": {},
      "mapper": {
        "url": "YOUR_JSON_FILE_URL",
        "method": "get",
        "parseResponse": true
      }
    },
    {
      "id": 3,
      "module": "builtin:FlowControl",
      "version": 1,
      "parameters": {},
      "mapper": {
        "array": "{{2.data.posts}}"
      }
    },
    {
      "id": 4,
      "module": "gateway:Filter",
      "version": 1,
      "parameters": {},
      "filter": {
        "name": "Current Week Only",
        "conditions": [
          [
            {
              "a": "{{3.week}}",
              "o": "number:equal",
              "b": "{{formatDate(now, \"W\")}}"
            }
          ]
        ]
      }
    },
    {
      "id": 5,
      "module": "google:ActionUploadFile",
      "version": 5,
      "parameters": {
        "account": "YOUR_GOOGLE_DRIVE_ACCOUNT"
      },
      "mapper": {
        "fileName": "{{3.image_filename}}",
        "folder": "YOUR_FOLDER_ID"
      }
    },
    {
      "id": 6,
      "module": "http:ActionSendData",
      "version": 3,
      "parameters": {},
      "mapper": {
        "url": "https://app.ayrshare.com/api/post",
        "method": "post",
        "headers": [
          {
            "name": "Authorization",
            "value": "Bearer YOUR_AYRSHARE_API_KEY"
          },
          {
            "name": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": "{\"post\": \"{{3.caption}}\", \"platforms\": {{3.platforms}}, \"scheduleDate\": \"{{3.schedule_date}}\", \"mediaUrls\": [\"{{5.data.webContentLink}}\"]}"
      }
    }
  ]
}
```

**To Use**:
1. Replace `YOUR_JSON_FILE_URL` with your hosted JSON file
2. Replace `YOUR_GOOGLE_DRIVE_ACCOUNT` with your connected account
3. Replace `YOUR_FOLDER_ID` with your Google Drive folder ID
4. Replace `YOUR_AYRSHARE_API_KEY` with your actual API key
5. Import into Make.com
6. Test and activate!

---

## Step 6: Alternative - No Make.com Needed

### Use Ayrshare's Bulk Upload Feature

Ayrshare supports **CSV bulk uploads**:

1. Convert JSON to CSV
2. Upload to Ayrshare dashboard
3. Ayrshare schedules all posts automatically

**CSV Format**:
```csv
post,platforms,scheduleDate,mediaUrls
"Caption for post 1","instagram","2025-01-05T19:00:00Z","https://drive.google.com/..."
"Caption for post 2","instagram","2025-01-08T19:00:00Z","https://drive.google.com/..."
```

**Steps**:
1. Go to Ayrshare Dashboard
2. Click **Bulk Upload**
3. Upload CSV
4. Review and confirm
5. All posts scheduled!

**This is the EASIEST approach** - no Make.com needed!

---

## JSON to CSV Conversion Script

I can create a Python script that converts your JSON to Ayrshare CSV format:

```python
import json
import csv

# Load JSON
with open('modelit_instagram_posts_master.json', 'r') as f:
    data = json.load(f)

# Create CSV
with open('modelit_ayrshare_bulk_upload.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['post', 'platforms', 'scheduleDate', 'mediaUrls'])

    for post in data['posts']:
        writer.writerow([
            post['caption'],
            'instagram',
            post['schedule_date'],
            f"https://drive.google.com/uc?export=view&id=IMAGE_ID_{post['post_id']}"
        ])

print("CSV created! Upload to Ayrshare.")
```

---

## Recommended Workflow

### **Best Approach for You**

Based on your setup with Make.com and Ayrshare, here's my recommendation:

**Week 0 (Setup)**:
1. Generate all 104 images (we'll do this together)
2. Upload images to Google Drive folder
3. Get public URLs for each image
4. Update JSON file with image URLs
5. Create Ayrshare account and connect Instagram

**Week 1 (Initial Posts)**:
1. Manually schedule first 2 posts via Ayrshare dashboard (test)
2. Verify they post correctly
3. Gather initial analytics

**Week 2-4 (Build Automation)**:
1. Create Make.com scenario
2. Test with Week 2 posts
3. Refine based on results
4. Set up error handling

**Week 5-52 (Autopilot)**:
1. Scenario runs weekly
2. Automatically schedules next 2 posts
3. You just monitor performance
4. Engage with comments

---

## Tracking & Analytics

### Google Sheets Tracker (For Performance)

While posts are automated, you'll want to track performance:

**Columns**:
- Post #
- Posted Date
- Theme
- Topic
- Likes
- Comments
- Saves
- Shares
- Engagement Rate
- Top Comment
- What Worked / Lessons Learned

**Update Process**:
- Every Monday: Pull analytics from Instagram
- Log performance metrics
- Identify patterns
- Adjust future content

---

## Cost Breakdown

### **Option 1: Ayrshare CSV Bulk Upload** (Recommended)
- **Ayrshare**: $149/month (or $99/month annual)
- **Google Drive**: Free
- **Total**: $149/month
- **Effort**: One-time upload, zero ongoing work

### **Option 2: Make.com Automation**
- **Make.com Free Plan**: $0/month (1,000 operations)
- **Ayrshare**: $149/month
- **Total**: $149/month
- **Effort**: Initial setup, then weekly monitoring

### **Option 3: Manual (No Automation)**
- **Google Drive**: Free
- **Instagram App**: Free
- **Total**: $0/month
- **Effort**: 10-15 minutes/week to post manually

**My Recommendation**: Start with **Option 3 (Manual)** for first month to test, then upgrade to **Option 1 (Ayrshare Bulk)** once you validate the content performs well.

---

## Next Steps

1. **Review the JSON file** I created with first 4 posts
2. **Decide on automation approach**:
   - Full automation (Ayrshare bulk upload)
   - Semi-automation (Make.com weekly)
   - Manual posting (Instagram app)
3. **Generate the 104 images** (I can help with this!)
4. **Set up Google Drive folder structure**
5. **Choose: Do you want me to**:
   - Expand the JSON to all 104 posts?
   - Create the CSV for Ayrshare bulk upload?
   - Build a Make.com scenario blueprint?
   - Help generate the images?

**What would you like to tackle first?**
