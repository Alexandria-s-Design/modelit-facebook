#!/usr/bin/env python3
"""
ModelIT K12 Facebook Campaign Generator
Generates 104 optimized Facebook posts with Nano Banana images
"""

import os
import sys
import json
import requests
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
import io
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables with override to ensure fresh keys
load_dotenv(Path(__file__).parent.parent / '.env', override=True)

# Configuration
TPT_URL = "https://www.teacherspayteachers.com/store/modelit"
MODELIT_URL = "modelitk12.com"
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY not found in .env file")

# Google API Scopes
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.file'
]

# Content themes
CONTENT_THEMES = {
    "tpt_resources": [
        "Digital Breakout Activities",
        "Systems Thinking Worksheets",
        "Interactive Modeling Lessons",
        "NGSS-Aligned Resources",
        "Brain Break Science Activities",
        "Cell Collective Lesson Plans",
        "Foldable Templates",
        "Coloring & Puzzles"
    ],
    "problem_solving": [
        "Meeting NGSS Standards Easily",
        "Boosting Student Engagement",
        "Time-Saving Lesson Prep",
        "Differentiation Made Simple",
        "Quick Assessment Strategies",
        "Remote Learning Solutions",
        "Classroom Management Tips"
    ],
    "systems_thinking": [
        "Understanding Feedback Loops",
        "Interconnected Biological Systems",
        "Multi-Scale Modeling",
        "Cause and Effect in Biology",
        "Systems Diagrams",
        "Pattern Recognition Skills",
        "Dynamic Biological Processes"
    ],
    "community": [
        "Teacher Appreciation",
        "Classroom Victory Celebrations",
        "Friday Wins",
        "Monday Motivation",
        "Relatable Teaching Moments",
        "Student Breakthroughs"
    ],
    "student_success": [
        "Student Model Discoveries",
        "Aha Moments in Biology",
        "Student-Created Networks",
        "STEM Career Connections",
        "Critical Thinking Growth"
    ],
    "professional_dev": [
        "Research Updates",
        "New Teaching Strategies",
        "Cell Collective Features",
        "Computational Biology Basics",
        "STEM Education Trends"
    ]
}

# Hashtag sets (1-2 per post)
HASHTAG_OPTIONS = [
    "#STEMEducation #TeachersOfFacebook",
    "#SystemsThinking #ScienceTeachers",
    "#NGSSStandards #MiddleSchool",
    "#TeacherResources #BiologyTeacher",
    "#ClassroomIdeas #STEMActivities",
]

def get_google_credentials():
    """Get Google API credentials"""
    creds = None
    token_path = os.path.expanduser('~/.config/gcloud/application_default_credentials.json')

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

    return creds

def generate_posting_schedule(start_date=None):
    """Generate optimal posting schedule: 2-3x/week for ~1 year"""
    if not start_date:
        start_date = datetime.now() + timedelta(days=1)

    schedule = []
    current_date = start_date

    # Mon (weekday 0), Wed (2), Thu (3)
    # Optimal times: 10 AM Wed/Thu, 9 AM Mon
    posting_days = [
        (0, "09:00"),  # Monday 9 AM
        (2, "10:00"),  # Wednesday 10 AM
        (3, "10:00"),  # Thursday 10 AM
    ]

    pattern_index = 0
    while len(schedule) < 104:
        target_day, time = posting_days[pattern_index]

        # Find next occurrence
        days_ahead = target_day - current_date.weekday()
        if days_ahead <= 0:
            days_ahead += 7

        post_date = current_date + timedelta(days=days_ahead)
        schedule.append({
            "date": post_date.strftime("%Y-%m-%d"),
            "time": time,
            "iso": f"{post_date.strftime('%Y-%m-%d')}T{time}:00-08:00"
        })

        current_date = post_date
        pattern_index = (pattern_index + 1) % len(posting_days)

    return schedule[:104]

def generate_nano_banana_image(prompt, output_path):
    """Generate image using Nano Banana via OpenRouter"""
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://modelitk12.com",
        "X-Title": "ModelIt K12 Facebook Campaign"
    }

    payload = {
        "model": "google/gemini-2.5-flash-image",
        "modalities": ["image", "text"],
        "messages": [{
            "role": "user",
            "content": prompt
        }]
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        response.raise_for_status()

        result = response.json()

        # Extract image from nested structure (correct format for Nano Banana)
        images = result['choices'][0]['message'].get('images', [])

        if not images:
            print(f"Warning: No images in response for {output_path}")
            return False

        # Get first image
        img_data = images[0]

        # Handle nested dictionary structure
        if isinstance(img_data, dict):
            if 'image_url' in img_data:
                img_url = img_data['image_url'].get('url', '')
            else:
                img_url = img_data.get('url', '')

            if img_url and img_url.startswith('data:image'):
                # Extract base64 data
                base64_data = img_url.split(',')[1]

                # Decode and save
                img_bytes = base64.b64decode(base64_data)

                with open(output_path, 'wb') as f:
                    f.write(img_bytes)

                return True

        print(f"Warning: No valid image data for {output_path}")
        return False

    except Exception as e:
        print(f"Error generating image: {e}")
        return False

def upload_to_drive(creds, file_path, folder_id):
    """Upload file to Google Drive and return shareable link"""
    try:
        drive_service = build('drive', 'v3', credentials=creds)

        file_metadata = {
            'name': os.path.basename(file_path),
            'parents': [folder_id]
        }

        from googleapiclient.http import MediaFileUpload
        media = MediaFileUpload(file_path, resumable=True)

        file = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        file_id = file.get('id')

        # Make publicly accessible
        drive_service.permissions().create(
            fileId=file_id,
            body={'type': 'anyone', 'role': 'reader'}
        ).execute()

        # Get shareable link
        shareable_link = f"https://drive.google.com/uc?id={file_id}"

        return shareable_link

    except Exception as e:
        print(f"Error uploading to Drive: {e}")
        return None

def generate_post_content(post_num, theme, post_type):
    """Generate post text based on theme and type"""

    punchy_templates = [
        "Ready to transform your biology classroom? 🔬",
        "What if your students could actually SEE how systems work?",
        "Struggling to meet NGSS standards? We can help. 💡",
        "Your next great lesson is waiting. Are you ready? ⏱️",
        "What's your biggest classroom challenge this week? 🤔",
        "Biology doesn't have to be boring. Promise. 🧬",
        "Ever wish you could model real biological processes? Now you can.",
        "Question: What makes learning stick? Answer: Systems thinking.",
        "Time-saving tip: Let students build their own models. 🎯",
        "Your students deserve to see the connections. Show them. 🌟"
    ]

    detailed_templates = {
        "tpt_resources": "Looking for ready-to-use {topic}? Our TPT store has NGSS-aligned resources that save you hours of prep time. Students love the interactive approach, and you'll love how easy implementation is. What topic would you model first?",
        "problem_solving": "Struggling with {topic}? ModelIT K12 brings university-level Cell Collective modeling to your classroom with zero learning curve. Teachers report 30% higher engagement when students build their own biological networks. Ready to try?",
        "systems_thinking": "{topic} can be tricky to teach. But when students can manipulate and visualize feedback loops in real-time, those 'aha moments' happen naturally. Want to see it in action?",
        "community": "{topic}: We see you, teachers! Every small win matters. Share yours below—what made you smile in class this week? Let's celebrate together! 🎉",
        "student_success": "Teacher Win Alert! One of our educators reported {topic} when students discovered enzyme regulation patterns they built themselves. This is why we do what we do. What breakthroughs have you seen lately?",
        "professional_dev": "New research shows {topic} significantly improves student understanding of complex systems. ModelIT K12 makes implementing these findings simple. Want the study details?"
    }

    if post_type == "punchy":
        import random
        return random.choice(punchy_templates)
    else:
        # Detailed post
        theme_category = None
        for category, topics in CONTENT_THEMES.items():
            if theme in topics:
                theme_category = category
                break

        if theme_category and theme_category in detailed_templates:
            return detailed_templates[theme_category].format(topic=theme.lower())
        else:
            # Fallback
            return f"Discover how {theme.lower()} transforms middle school science education. ModelIT K12 provides interactive biological modeling tools that meet NGSS standards while keeping students engaged. Ready to revolutionize your classroom?"

def create_first_comment(theme):
    """Generate first comment with links"""
    comments = [
        f"Explore interactive biological modeling at {MODELIT_URL} and get ready-to-use lessons at {TPT_URL} ✨ Save hours of prep time!",
        f"Learn more at {MODELIT_URL} | Find classroom resources at {TPT_URL} | Transform your teaching today!",
        f"Discover the full platform at {MODELIT_URL} and browse our TPT store at {TPT_URL} for instant downloads! 🎓",
        f"Visit {MODELIT_URL} for interactive demos | Shop ready-made lessons at {TPT_URL} | Make systems thinking simple!",
    ]

    import random
    return random.choice(comments)

def create_ayrshare_json(post_data):
    """Create Ayrshare JSON payload"""
    return json.dumps({
        "post": f"{post_data['post_text']}\n\n{post_data['hashtags']}",
        "platforms": ["facebook"],
        "mediaUrls": [post_data['image_url']] if post_data['image_url'] else [],
        "scheduleDate": post_data['post_iso']
    })

def generate_image_prompt(theme, post_num):
    """Generate Nano Banana image prompt"""
    base_style = "Professional educational illustration, 1200x628 pixels, modern clean design, blue and green color scheme (#0F6ACE, #48d2fc), less than 20% text overlay"

    prompts = {
        "Digital Breakout Activities": f"{base_style}. Show diverse middle school students (ages 11-14) collaborating around a laptop, working on a digital escape room with biological puzzle elements. Excited expressions, colorful interface visible on screen.",
        "Systems Thinking Worksheets": f"{base_style}. Professional worksheet mockup showing systems diagrams with feedback loops, arrows connecting biological components, clean infographic style.",
        "Interactive Modeling Lessons": f"{base_style}. Split screen: left shows teacher presenting, right shows students at computers building biological network models, drag-and-drop interface visible.",
        "NGSS-Aligned Resources": f"{base_style}. Modern classroom with diverse students, NGSS standards poster visible on wall, students engaged with tablets showing biological simulations.",
        "Brain Break Science Activities": f"{base_style}. Students laughing and moving, incorporating science concepts into physical activities, energetic and fun atmosphere.",
        "Cell Collective Lesson Plans": f"{base_style}. Computer screen showing Cell Collective interface with biological network diagram, clean professional UI, student hands visible interacting with touchscreen.",
        "Foldable Templates": f"{base_style}. Colorful paper foldables showing biological systems, hands folding interactive learning tools, 3D paper models on desk.",
        "Coloring & Puzzles": f"{base_style}. Educational coloring sheets featuring cells and molecules, colored pencils, partially colored scientific diagrams.",
        "default": f"{base_style}. Diverse middle school students collaborating on biological modeling project, computer screens showing network diagrams, warm classroom environment, engaged learners."
    }

    return prompts.get(theme, prompts["default"])

def main():
    print("ModelIT K12 Facebook Campaign Generator")
    print("=" * 70)
    print("Generating 104 optimized Facebook posts with Nano Banana images\n")

    # Get Google credentials
    print("Authenticating with Google...")
    creds = get_google_credentials()
    sheets_service = build('sheets', 'v4', credentials=creds)
    drive_service = build('drive', 'v3', credentials=creds)

    # Create Drive folder
    print("Creating Google Drive folder...")
    folder_metadata = {
        'name': 'ModelIT K12 Facebook Campaign',
        'mimeType': 'application/vnd.google-apps.folder'
    }
    folder = drive_service.files().create(body=folder_metadata, fields='id').execute()
    main_folder_id = folder.get('id')

    images_folder_metadata = {
        'name': 'Images',
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [main_folder_id]
    }
    images_folder = drive_service.files().create(body=images_folder_metadata, fields='id').execute()
    images_folder_id = images_folder.get('id')

    print(f"[OK] Created folder ID: {main_folder_id}")

    # Create Google Sheet
    print("Creating Google Sheet...")
    spreadsheet = {
        'properties': {'title': 'ModelIT K12 - 104 Facebook Posts'},
        'sheets': [{'properties': {'title': 'Facebook Posts', 'gridProperties': {'frozenRowCount': 1}}}]
    }
    result = sheets_service.spreadsheets().create(body=spreadsheet).execute()
    spreadsheet_id = result['spreadsheetId']

    # Add headers
    headers = [
        ["post_number", "post_date", "post_time", "theme", "post_text",
         "first_comment", "hashtags", "image_url", "image_filename",
         "engagement_question", "post_type", "character_count",
         "status", "ayrshare_json"]
    ]

    sheets_service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range="A1:N1",
        valueInputOption="RAW",
        body={"values": headers}
    ).execute()

    print(f"[OK] Created sheet ID: {spreadsheet_id}")

    # Generate schedule
    print("Generating posting schedule...")
    schedule = generate_posting_schedule()

    # Generate all content
    print(f"\nGenerating 104 posts...")
    print(f"{'='*70}")

    all_rows = []

    # Distribution: 35 punchy, 69 detailed
    post_types = ["punchy"] * 35 + ["detailed"] * 69

    # Distribute themes
    all_themes = []
    for theme_cat, themes in CONTENT_THEMES.items():
        all_themes.extend(themes)

    # Cycle through themes until we have 104
    import random
    random.shuffle(all_themes)

    # Repeat themes to reach 104 posts
    while len(all_themes) < 104:
        all_themes.extend(all_themes[:104 - len(all_themes)])

    all_themes = all_themes[:104]

    for i in range(104):
        post_num = i + 1
        post_data = schedule[i]
        theme = all_themes[i]
        post_type = post_types[i]
        hashtags = random.choice(HASHTAG_OPTIONS)

        print(f"\nPost {post_num}/104: {theme} ({post_type})")

        # Generate post text
        post_text = generate_post_content(post_num, theme, post_type)
        char_count = len(post_text)

        # Generate first comment
        first_comment = create_first_comment(theme)

        # Generate engagement question
        engagement_q = post_text if "?" in post_text else "What do you think?"

        # Generate image
        print(f"  [IMG] Generating image...")
        image_filename = f"modelit_post_{post_num:03d}.png"
        temp_dir = os.path.join(os.path.expanduser("~"), "temp")
        os.makedirs(temp_dir, exist_ok=True)
        temp_image_path = os.path.join(temp_dir, image_filename)

        image_prompt = generate_image_prompt(theme, post_num)
        image_generated = generate_nano_banana_image(image_prompt, temp_image_path)

        # Upload to Drive
        image_url = ""
        if image_generated and os.path.exists(temp_image_path):
            print(f"  [UPLOAD] Uploading to Drive...")
            image_url = upload_to_drive(creds, temp_image_path, images_folder_id)
            if image_url:
                print(f"  [OK] Image uploaded")

        # Create Ayrshare JSON
        row_data = {
            'post_text': post_text,
            'hashtags': hashtags,
            'image_url': image_url or "pending",
            'post_iso': post_data['iso']
        }
        ayrshare_json = create_ayrshare_json(row_data)

        # Build row
        row = [
            post_num,
            post_data['date'],
            post_data['time'],
            theme,
            post_text,
            first_comment,
            hashtags,
            image_url or "pending",
            image_filename,
            engagement_q,
            post_type,
            char_count,
            "draft",
            ayrshare_json
        ]

        all_rows.append(row)
        print(f"  [OK] Post {post_num} complete ({char_count} chars)")

    # Batch update sheet
    print(f"\nPopulating Google Sheet with all {len(all_rows)} rows...")
    sheets_service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=f"A2:N{len(all_rows)+1}",
        valueInputOption="RAW",
        body={"values": all_rows}
    ).execute()

    sheet_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit"

    print(f"\n{'='*70}")
    print("[SUCCESS] Campaign Generated Successfully!")
    print(f"{'='*70}")
    print(f"\nGoogle Sheet: {sheet_url}")
    print(f"Drive Folder ID: {main_folder_id}")
    print(f"\nStats:")
    print(f"   - Total posts: 104")
    print(f"   - Punchy posts: 35")
    print(f"   - Detailed posts: 69")
    print(f"   - Posting frequency: 2-3x/week")
    print(f"   - Duration: ~1 year")
    print(f"\nNext: Review posts and update status to 'ready' to activate posting!")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    if not OPENROUTER_API_KEY:
        print("ERROR: OPENROUTER_API_KEY not found in environment")
        sys.exit(1)

    main()
