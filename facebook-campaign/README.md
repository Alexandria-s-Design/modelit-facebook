# ModelIT K12 Facebook Campaign 2025-2026

**Complete 52-week Facebook content strategy with AI-generated images**

## Overview

This repository contains a comprehensive Facebook marketing campaign for ModelIT K12, featuring:
- **104 unique posts** (2 per week for 52 weeks)
- **104 AI-generated images** (1200x628px, Facebook-optimized)
- **Complete automation-ready data** in Google Sheets
- **Detailed implementation guides** and best practices

## Campaign Details

- **Duration**: December 2, 2025 - November 27, 2026
- **Posting Schedule**: Mondays & Fridays at 7:00 PM EST
- **Platform**: Facebook (@modelitk12)
- **Target Audience**: Middle & High School Science Teachers

## Content Themes

The campaign features 39 unique themes covering:

1. **Teaching Strategies** - Quick assessments, differentiation, engagement
2. **Systems Thinking** - Complex systems, feedback loops, modeling
3. **Classroom Management** - Time-saving tips, efficiency strategies
4. **Student Success** - Breakthrough moments, student-driven learning
5. **Professional Development** - ModelIT workshops, community insights
6. **Technology Integration** - Remote learning, virtual labs, seamless tech
7. **NGSS Alignment** - Standards-based teaching and assessment
8. **Biological Modeling** - Disease models, gene regulation, ecosystems

## Repository Structure

```
facebook-campaign/
├── images/
│   └── post_001_*.png through post_104_*.png  # All 104 AI-generated images (1200x628px)
├── data/
│   └── all_images_complete.json                # Image manifest with metadata
├── docs/
│   ├── FINAL_STATUS_AND_NEXT_STEPS.md         # Campaign completion status
│   ├── manual_upload_solution.md               # Google Drive upload guide
│   ├── update_sheet_urls.gs                    # Apps Script for automation
│   └── image_upload_template.csv               # CSV template for imports
└── scripts/
    ├── generate_104_modelit_facebook_posts.py  # Post generation script
    ├── create_modelit_facebook_campaign.py     # Campaign creation script
    └── post_modelit_to_facebook.py             # Posting automation script
```

## Image Specifications

- **Format**: PNG
- **Dimensions**: 1200x628px (Facebook optimal ratio)
- **Size Range**: 926 KB - 1576 KB
- **Total Size**: ~137 MB
- **AI Model**: Nano Banana (Google Gemini 2.5 Flash Image)

## Google Sheet Integration

All campaign data is stored in Google Sheets:
- **Sheet ID**: `1pjJl8yxdVi-HwdkFxuu5Uq2qPklYAicX67sLz8qHCV0`
- **Drive Folder**: `1JAEQPbWPEQKb3oU3BvN7bRGwT0ZrgW5I`

### Sheet Structure (14 columns):
- A: post_number (1-104)
- B: scheduled_date
- C: post_type (punchy/detailed)
- D: theme
- E: post_text
- F: character_count
- G: ayrshare_json (automation payload)
- H: image_url (requires manual upload)
- I: image_filename
- J-N: Additional metadata

## Implementation Status

### ✅ Completed
- All 104 post texts generated
- All 104 images generated
- Google Sheet populated with content
- Ayrshare JSON payloads ready
- Documentation complete

### ⚠️ Pending
- **Image Upload**: Images need to be uploaded to Google Drive
- **Sheet Update**: Column H (image_url) needs to be populated

See `docs/FINAL_STATUS_AND_NEXT_STEPS.md` for detailed completion instructions.

## Manual Upload Guide

Due to OAuth authentication expiration, images require manual upload:

1. **Upload to Google Drive**:
   - Drag all images from `images/` to Drive folder
   - Set sharing to "Anyone with the link"

2. **Update Google Sheet**:
   - Use Apps Script: `docs/update_sheet_urls.gs`
   - Or CSV Import: `docs/image_upload_template.csv`

Complete instructions in `docs/manual_upload_solution.md`.

## Automation with Ayrshare

Once image URLs are in the Sheet, posts can be scheduled via Ayrshare API using the JSON payloads in column G.

## Content Quality

- **35 punchy posts** (280-350 characters) - Quick engagement
- **69 detailed posts** (400-600 characters) - Deep insights
- Strategic mix optimized for Facebook algorithm
- Character counts optimized for mobile viewing

## Related Campaigns

This repository also contains an Instagram campaign:
- 104 posts for Instagram (@modelitk12)
- 1080x1080px images
- Sundays & Wednesdays schedule
- See root directory for Instagram campaign files

## License

All content and images © 2025 ModelIT K12. All rights reserved.

## Contact

For questions about this campaign, contact the ModelIT K12 team.
