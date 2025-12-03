# ModelIT K12 Instagram Campaign 2025-2026

**Complete 52-week Instagram content strategy with AI-generated images**

## Overview

This repository contains a comprehensive Instagram marketing campaign for ModelIT K12, featuring:
- **104 unique posts** (2 per week for 52 weeks)
- **104 AI-generated images** (1080x1080px, professional quality)
- **Complete automation-ready data** in JSON and CSV formats
- **Detailed implementation guides** and best practices

## Campaign Details

- **Duration**: January 5, 2025 - December 31, 2025
- **Posting Schedule**: Sundays & Wednesdays at 7:00 PM EST
- **Platform**: Instagram (@modelitk12)
- **Target Audience**: Middle & High School Science Teachers

## Content Themes

The campaign rotates through 4 strategic themes, each with 26 unique posts:

1. **Systems Thinking & Modeling** (26 posts)
   - Focus on interconnected concepts and biological networks
   - Teaching methodology and critical thinking

2. **Hands-On STEM Activities** (26 posts)
   - Interactive classroom activities
   - Engagement strategies for all learners

3. **Teacher Time-Savers** (26 posts)
   - Efficiency tips and workflow optimization
   - Work-life balance for educators

4. **Student Engagement Strategies** (26 posts)
   - Breakthrough moments and differentiation
   - Inclusive teaching practices

## Repository Structure

```
modelit-facebook/
├── data/
│   ├── ModelIT_Instagram_104_Posts_Complete.json  # Complete post data (automation-ready)
│   └── ModelIT_Instagram_104_Posts_Complete.csv   # Spreadsheet format for review
├── images/
│   └── Post_001_Image.png through Post_104_Image.png  # All 104 AI-generated images
├── scripts/
│   ├── generate_all_104_modelit_posts.py          # Post generation script
│   ├── generate_all_104_images_v2.js              # Image generation script
│   └── regenerate_post_099.js                      # Failure recovery script
├── docs/
│   ├── MODELIT-INSTAGRAM-104-POST-PLAN.md         # Complete content strategy
│   ├── MODELIT-INSTAGRAM-ENGAGEMENT-STRATEGIES-2025.md  # Instagram best practices
│   └── MODELIT-MAKECOM-AYRSHARE-AUTOMATION-GUIDE.md    # Automation implementation guide
└── README.md
```

## Quick Start

### Option 1: Manual Posting (Recommended for Testing)

1. Open `data/ModelIT_Instagram_104_Posts_Complete.csv` in Google Sheets or Excel
2. Each week, find the 2 posts scheduled for that week
3. Download the corresponding images from `images/` folder
4. Post to Instagram at scheduled times (Sun/Wed 7pm)
5. Track performance in the spreadsheet

### Option 2: Automated Posting (Advanced)

See `docs/MODELIT-MAKECOM-AYRSHARE-AUTOMATION-GUIDE.md` for:
- Make.com scenario setup
- Ayrshare API integration
- CSV bulk upload method
- Scheduling automation

## Post Format

Each post follows this proven structure:

```
[Hook] 🔬
[Value Proposition]
[Call to Action]

🔗 Explore more: modelitk12.com
📚 Ready-to-use resources: teacherspayteachers.com/store/modelit

💾 Save this for your next planning session!

#hashtags #optimized #for #engagement
```

## Image Specifications

- **Format**: PNG, 1080x1080px (Instagram square)
- **Style**: Modern minimalist design
- **Colors**: Deep blue (#0f6de6), clean white backgrounds
- **Aesthetic**: Professional, scientific, teacher-friendly
- **Generation**: OpenAI DALL-E 3, standard quality

## Instagram Best Practices (2025)

Based on current algorithm research:

- **Primary Metric**: Saves (most important algorithmic signal)
- **Optimal Hashtags**: 8-15 hashtags
- **Best Posting Times**: Sunday & Wednesday at 7pm EST
- **Engagement Strategy**: Hook-Value-CTA format
- **Content Mix**: 80% educational value, 20% promotional

## Brand Links

- **Website**: [modelitk12.com](https://modelitk12.com)
- **TPT Store**: [teacherspayteachers.com/store/modelit](https://teacherspayteachers.com/store/modelit)
- **Instagram**: [@modelitk12](https://instagram.com/modelitk12)

## Data Format

### JSON Structure

```json
{
  "campaign": {
    "name": "ModelIT K12 Instagram Campaign 2025-2026",
    "total_posts": 104,
    "posting_schedule": "2 posts per week (Sunday 7pm, Wednesday 7pm)",
    "duration": "52 weeks"
  },
  "posts": [
    {
      "post_id": "001",
      "week": 1,
      "schedule_date": "2025-01-05T19:00:00-05:00",
      "day": "Sunday",
      "theme": "Systems Thinking & Modeling",
      "topic": "What is systems thinking and why it matters",
      "hook": "Ever notice how students memorize facts but struggle to apply them? 🤔",
      "value": "Systems thinking transforms isolated facts into meaningful understanding.",
      "cta": "Help your students discover the connections that bring science to life.",
      "caption": "[Full formatted caption with links and hashtags]",
      "hashtags": ["teachersofinstagram", "scienceteacher", "stemteacher", ...],
      "image_description": "Modern minimalist design with interconnected blue nodes...",
      "image_filename": "Post_001_Image.png",
      "platforms": ["instagram"],
      "status": "draft"
    }
    // ... 103 more posts
  ]
}
```

## Performance Tracking

The CSV includes columns for tracking:
- Post Date & Time
- Likes, Comments, Saves, Shares
- Engagement Rate
- Top Comment
- Notes & Lessons Learned

## Generation Details

- **Posts Generated**: December 2024
- **Images Generated**: December 2024
- **Success Rate**: 100% (104/104 images)
- **Failed Generations**: 1 (Post 099, successfully regenerated)
- **Total Generation Time**: ~90 minutes
- **API Used**: OpenAI DALL-E 3

## Automation-Ready

All data is formatted for seamless integration with:
- **Make.com**: Workflow automation platform
- **Ayrshare**: Social media scheduling API
- **Google Sheets**: Manual tracking and review
- **Zapier**: Alternative automation platform

## Next Steps

1. **Week 0 (Before Jan 5, 2025)**
   - Review all 104 posts for accuracy
   - Verify brand links and hashtags
   - Test posting first 2-3 images manually

2. **Week 1 (Jan 5-11, 2025)**
   - Post #001 on Sunday Jan 5 at 7pm
   - Post #002 on Wednesday Jan 8 at 7pm
   - Monitor engagement and adjust

3. **Ongoing**
   - Track performance weekly
   - Engage with comments
   - Adjust posting times based on analytics
   - Refresh content as needed

## Support & Contact

For questions or issues:
- **Website**: modelitk12.com
- **Organization**: Alexandria's Design
- **Repository**: github.com/Alexandria-s-Design/modelit-facebook

## License

© 2024-2025 ModelIT K12. All rights reserved.

Content and images are proprietary to ModelIT K12 and intended for use by authorized personnel only.

---

**Last Updated**: December 2024
**Campaign Status**: Ready to Launch
**Total Assets**: 104 posts + 104 images + Complete documentation

## Status
Active

## TODO
- [ ] Schedule upcoming posts
- [ ] Update content calendar
- [ ] Analyze engagement metrics