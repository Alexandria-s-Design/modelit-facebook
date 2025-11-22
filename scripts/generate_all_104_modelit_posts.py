"""
Generate all 104 ModelIT Instagram posts with unique captions
"""

import json
import csv
from datetime import datetime, timedelta

# Start date: First Sunday of 2025
START_DATE = datetime(2025, 1, 5)

# Theme definitions
THEMES = {
    "Systems Thinking & Modeling": {
        "topics": [
            "What is systems thinking and why it matters",
            "Teaching interconnected concepts vs isolated facts",
            "Helping students see feedback loops in nature",
            "Making abstract concepts tangible through models",
            "Real-world applications of systems thinking",
            "Cross-curricular connections with systems",
            "Critical thinking through system analysis",
            "Problem-solving with systems approaches",
            "Environmental systems in the classroom",
            "Biological networks visualization",
            "Teaching cause and effect relationships",
            "Systems thinking in everyday life",
            "Building mental models of complex systems",
            "Identifying leverage points in systems",
            "Understanding emergence in biological systems",
            "Teaching stocks and flows concepts",
            "Circular vs linear thinking",
            "Systems thinking assessment strategies",
            "Collaborative systems exploration",
            "Systems thinking across grade levels",
            "Overcoming misconceptions about systems",
            "Visual tools for systems thinking",
            "Systems thinking in NGSS standards",
            "Student-led system investigations",
            "Making systems thinking stick",
            "Systems thinking success stories"
        ],
        "hooks": [
            "Ever notice how students memorize facts but struggle to apply them? 🤔",
            "Students seeing parts but missing the whole picture? 🧩",
            "What if your students could see how everything connects? 🌐",
            "Tired of teaching topics in isolation? 📚",
            "Want students to think like scientists, not memorizers? 🔬",
            "That moment when students finally see the big picture... ✨",
            "Struggling to teach complex concepts? 🤯",
            "Your students can list facts but can't explain why? 📝",
            "Notice how nature's lessons don't stick in isolation? 🌿",
            "What if one framework unlocked all your biology topics? 🔑",
            "Students asking 'when will we use this?' constantly? 🤷",
            "Want to teach the way scientists actually think? 🧪",
            "Tired of students compartmentalizing knowledge? 📦",
            "That 'aha!' when everything clicks together... 💡",
            "Teaching cause and effect feels impossible? ⚡",
            "Your textbook chapters feel disconnected? 📖",
            "Students struggle with real-world problem solving? 🌍",
            "Want assessment that shows actual understanding? ✅",
            "Group work falling flat? Need better collaboration? 👥",
            "Differentiation feeling overwhelming? 🎯",
            "Students can't transfer learning to new contexts? 🔄",
            "Visual learners struggling with abstract concepts? 👁️",
            "NGSS standards feeling impossible to teach? 📋",
            "Want students driving their own learning? 🚗",
            "Concepts stick for the test then disappear? ⏰",
            "Ready to see lasting transformation? 🦋"
        ],
        "values": [
            "Systems thinking transforms isolated facts into meaningful understanding.",
            "Systems thinking reveals the connections that make science come alive.",
            "Interactive models make abstract systems tangible and explorable.",
            "One framework teaches students to see patterns across all topics.",
            "Systems thinking turns passive learners into active investigators.",
            "Seeing interconnections creates those breakthrough teaching moments.",
            "Visual systems models simplify even the most complex biology.",
            "Understanding 'why' happens when students see the whole system.",
            "Biological networks show students how nature actually works.",
            "Systems frameworks work for cells, ecosystems, and everything between.",
            "When students see systems, they finally understand relevance.",
            "Real scientific thinking means seeing connections, not isolated facts.",
            "Systems thinking naturally breaks down knowledge silos.",
            "Interconnected learning creates permanent understanding.",
            "Systems models make cause-and-effect visible and manipulable.",
            "One systems approach unifies your entire curriculum.",
            "Systems thinking is how we solve real-world problems.",
            "Systems models show understanding, not just memorization.",
            "Interactive systems naturally invite collaboration and discussion.",
            "Systems thinking adapts to every learning level seamlessly.",
            "Transfer happens automatically when students see systems.",
            "Visual systems thinking reaches every learner effectively.",
            "NGSS comes alive through systems thinking approaches.",
            "Systems thinking puts students in the driver's seat.",
            "Understanding systems creates permanent schema, not temporary facts.",
            "Systems thinking doesn't just teach content—it transforms mindsets."
        ],
        "ctas": [
            "Help your students discover the connections that bring science to life.",
            "Transform your classroom into a space where learning clicks into place.",
            "Show students the beauty of interconnected thinking today.",
            "Make complex biology accessible through systems thinking.",
            "Watch engagement soar when students see the bigger picture.",
            "Create those magical teaching moments you dreamed of.",
            "Simplify your teaching while deepening student understanding.",
            "Turn 'when will we use this?' into 'I finally get it!'",
            "Bring the wonder of biological systems to your classroom.",
            "Teach once, apply everywhere—that's systems thinking.",
            "Connect learning to life and watch motivation skyrocket.",
            "Join the teachers revolutionizing science education.",
            "Break free from isolated chapters and disconnected topics.",
            "Build understanding that lasts beyond the test.",
            "Make invisible connections visible and unforgettable.",
            "Unify your teaching with one powerful approach.",
            "Prepare students for complex real-world challenges.",
            "See what students really understand, not just what they memorized.",
            "Turn your classroom into a collaborative learning community.",
            "Meet every student where they are with adaptive systems.",
            "Watch knowledge transfer happen naturally and effortlessly.",
            "Reach every student with visual systems approaches.",
            "Make standards come alive through engaging systems.",
            "Empower students to explore and discover independently.",
            "Create learning that transforms, not just informs.",
            "Experience the systems thinking revolution in your classroom."
        ],
        "hashtags": "#teachersofinstagram #scienceteacher #stemteacher #teacherresources #modelitk12 #systemsthinking #criticalthinking #problemsolving #interactivelearning #biologyclassroom #teachingtips #scienceeducation"
    },
    "Hands-On STEM Activities": {
        "topics": [
            "Interactive modeling activities for biology",
            "Quick 15-minute systems demos",
            "No-tech systems thinking activities",
            "Lab alternatives for remote learning",
            "Modeling ecosystems in the classroom",
            "Cell network interactive simulations",
            "Student-led system exploration",
            "Collaborative modeling projects",
            "Assessment through system building",
            "Differentiation with modeling tools",
            "Inquiry-based modeling lessons",
            "Station rotation with interactive models",
            "Project-based learning with systems",
            "Gamification of biological systems",
            "Virtual field trips through models",
            "Data analysis with interactive tools",
            "Student presentations using models",
            "Peer teaching with modeling tools",
            "Flipped classroom modeling activities",
            "Integration with other subjects",
            "Technology integration tips",
            "Making STEM accessible to all learners",
            "Real-time formative assessment activities",
            "Challenge-based learning with systems",
            "Student portfolios with modeling work",
            "Showcase student modeling projects"
        ],
        "hooks": [
            "Need an activity that gets EVERY student engaged? 🔬",
            "Looking for a 15-minute activity with maximum impact? ⏱️",
            "Want students exploring, not just listening? 🔍",
            "Need a lab alternative that actually works? 💻",
            "Searching for activities students can't wait to try? 🎯",
            "That lesson where 100% of students participate... 🙌",
            "No lab equipment? No problem! 🚀",
            "Remote learning got you scrambling for activities? 🏠",
            "Ecosystems too abstract for students to grasp? 🌱",
            "Cell structure putting students to sleep? 😴",
            "Want students teaching THEMSELVES? 📖",
            "Group work chaos or collaborative magic? 🤝",
            "Assessment that shows real understanding? ✨",
            "Differentiation without creating 5 lesson plans? 🎨",
            "Students asking 'can we do this again?' after class? 🤩",
            "Station rotations feeling chaotic? 🔄",
            "Project-based learning overwhelming to plan? 📊",
            "Want science to feel like a game, not a chore? 🎮",
            "Field trips impossible but need that experience? 🗺️",
            "Data analysis boring your students? 📈",
            "Student presentations falling flat? 🎤",
            "Peer teaching turning into gossip time? 👥",
            "Flipped classroom not working as planned? 🔄",
            "STEM feeling isolated from other subjects? 🔗",
            "Technology integration feeling forced? 💾",
            "Every student on a different level? Help! 📚"
        ],
        "values": [
            "Interactive modeling turns passive observers into active scientists.",
            "15 minutes of modeling beats 50 minutes of lecture every time.",
            "Systems thinking works with or without technology.",
            "Interactive models bring labs to life anywhere, anytime.",
            "Watch abstract ecosystems become concrete and manipulable.",
            "Cell networks transform from diagrams to dynamic explorations.",
            "Self-paced tools mean students drive their own discovery.",
            "Collaborative models naturally structure productive group work.",
            "Building systems reveals understanding better than any test.",
            "One model adapts to novice and expert learners seamlessly.",
            "Inquiry naturally emerges when students can manipulate systems.",
            "Interactive models make station rotations smooth and purposeful.",
            "Projects gain focus and depth with systems frameworks.",
            "When learning feels like play, engagement soars.",
            "Virtual modeling creates field trip experiences in your classroom.",
            "Interactive data makes analysis engaging and meaningful.",
            "Models give students powerful presentation tools.",
            "Modeling tools structure peer teaching for real learning.",
            "Flipped classrooms thrive with interactive exploration tools.",
            "Systems thinking naturally connects science to everything else.",
            "Good tech disappears into good learning seamlessly.",
            "Interactive systems meet students exactly where they are.",
            "Real-time interaction reveals thinking as it happens.",
            "Challenge-based learning gets structure from systems models.",
            "Digital portfolios showcase learning journeys beautifully.",
            "Student work becomes source of pride and celebration."
        ],
        "ctas": [
            "Watch your entire class lean in and discover scientific inquiry.",
            "Transform your next period with one powerful activity.",
            "Make biology hands-on without touching a single beaker.",
            "Bring the lab experience to any learning environment.",
            "See abstract concepts become concrete and clickable.",
            "Turn diagrams into explorations students control.",
            "Give students the keys to their own learning journey.",
            "Structure collaboration that actually teaches.",
            "Assess understanding in ways that inform your teaching.",
            "Differentiate effortlessly with self-adapting tools.",
            "Turn students into scientists with one simple shift.",
            "Bring order and purpose to your station rotations.",
            "Give projects the structure they need to succeed.",
            "Make science the highlight of their day.",
            "Take students anywhere without leaving your classroom.",
            "Make data analysis the part they look forward to.",
            "Equip students with tools that showcase their brilliance.",
            "Transform peer teaching from chaos to collaboration.",
            "Make flipped learning work the way it should.",
            "Show students science connects to everything they love.",
            "Integrate technology that enhances rather than distracts.",
            "Reach every single student in your classroom.",
            "See thinking happen in real-time.",
            "Challenge students in ways that excite, not overwhelm.",
            "Celebrate learning with portfolios that tell the story.",
            "Showcase the amazing work happening in your classroom."
        ],
        "hashtags": "#teachersofinstagram #STEMactivities #scienceteacher #handsonelearning #interactivelearning #middleschoolscience #teacherresources #engagingstudents #classroomactivities #scienceeducation #edtech #modelitk12"
    },
    "Teacher Time-Savers": {
        "topics": [
            "5-minute lesson prep with interactive models",
            "Reusable systems thinking frameworks",
            "Student self-directed learning tools",
            "Automated feedback through simulations",
            "Pre-built curriculum alignments",
            "Assessment shortcuts that work",
            "Classroom management with tech tools",
            "Reducing grading time with interactive labs",
            "One-and-done lesson planning",
            "Streamlined differentiation strategies",
            "Digital organization tips",
            "Efficient parent communication",
            "Batch processing lesson plans",
            "Template libraries for quick planning",
            "Automating routine tasks",
            "Finding quality resources quickly",
            "Maximizing prep periods",
            "Work-life balance strategies",
            "Sustainable teaching practices",
            "Time-blocking for teachers",
            "Delegation strategies in classroom",
            "Using student helpers effectively",
            "Planning ahead for success",
            "Recovery strategies for busy weeks",
            "Teacher wellness and time management",
            "Building a resource library"
        ],
        "hooks": [
            "Spent hours planning just to re-explain it 20 times? ⏰",
            "Sunday night lesson planning got you down? 😫",
            "Need to reclaim your evenings? 🌙",
            "Wish lesson planning didn't take all weekend? 📅",
            "Tired of reinventing the wheel every unit? 🎡",
            "5-minute prep sound impossible? Think again! ⚡",
            "Using the same lesson plan for 3 years? Same! ♻️",
            "Students need help but you're pulled 30 directions? 🤯",
            "Grading taking over your life? 📝",
            "Creating 3 versions of every lesson for differentiation? 😵",
            "Assessment prep eating all your time? ✅",
            "Classroom management stealing instructional time? 🕐",
            "Grading labs until midnight? Again? 🌃",
            "One lesson plan for every topic? Yes please! 🙏",
            "Differentiation feeling like 5 separate lessons? 📚",
            "Can't find that perfect resource you had last year? 🔍",
            "Parent emails piling up? 📧",
            "Planning 3 units ahead while teaching 2 behind? 📊",
            "Templates? What templates? You make everything from scratch? ✏️",
            "Routine tasks eating your actual teaching time? ⏳",
            "Drowning in resources but can't find what you need? 🌊",
            "Prep period? What prep period? 🤔",
            "Work-life balance feels like a myth? 🦄",
            "Burning out faster than your candle at both ends? 🕯️",
            "Time management systems failing you? ⏱️",
            "Organizing resources on 47 different platforms? 💾"
        ],
        "values": [
            "Self-paced models let students explore while you facilitate, not repeat.",
            "One framework works for every unit—plan once, use forever.",
            "Interactive tools mean students get immediate feedback automatically.",
            "Models guide exploration so students don't need constant direction.",
            "Pre-built alignments mean less planning, more teaching.",
            "Interactive assessments grade themselves while showing understanding.",
            "Self-directed tools free you to manage, not micromanage.",
            "Simulations provide detailed feedback without grading marathons.",
            "Universal design means one lesson reaches all learners.",
            "Smart organization saves hours every week.",
            "Self-directed activities free you for meaningful parent updates.",
            "Batch planning with reusable frameworks multiplies your efficiency.",
            "Quality template libraries mean quick customization, not reinvention.",
            "Automation handles routine tasks so you can actually teach.",
            "Curated resources beat endless searching every time.",
            "Structured systems maximize every precious prep minute.",
            "Sustainable practices prevent burnout and boost effectiveness.",
            "Teaching frameworks build on themselves, saving exponential time.",
            "Smart time management creates space for life outside teaching.",
            "Student-driven tools mean less teacher-intensive intervention.",
            "Systematic approaches reclaim your personal time.",
            "Preparation compounds—invest once, benefit repeatedly.",
            "Emergency flexibility comes from solid systems already in place.",
            "Wellness isn't selfish—it makes you a better teacher.",
            "Time management is really priority management.",
            "Organized resources become your teaching superpower."
        ],
        "ctas": [
            "Reclaim your time for what matters—meaningful student interactions.",
            "Spend your Sunday doing literally anything else.",
            "Give yourself permission to have evenings again.",
            "Weekend lesson planning? Make it optional, not obligatory.",
            "Build once, use forever—that's smart teaching.",
            "Prep in minutes, not hours—it's possible!",
            "Stop recreating what already works perfectly.",
            "Multiply yourself without working more hours.",
            "Leave school at school—reclaim your evenings.",
            "Differentiate smarter, not harder.",
            "Let technology handle the routine so you can teach.",
            "Free yourself from classroom management firefighting.",
            "Grade less, understand more—it's not a dream.",
            "Simplify everything and watch teaching get better.",
            "Reach every learner without multiple lesson plans.",
            "Organize once, benefit daily.",
            "Turn parent communication from burden to breeze.",
            "Plan ahead without sacrificing your present.",
            "Templates aren't cheating—they're professional tools.",
            "Automate the automatable, focus on the irreplaceable.",
            "Find what you need when you need it—finally.",
            "Make every prep minute count.",
            "Sustainable teaching isn't just survival—it's thriving.",
            "Work smarter so you can live better.",
            "Protect your time like the precious resource it is.",
            "Build systems that support you, not overwhelm you."
        ],
        "hashtags": "#teachersofinstagram #teacherlife #teachertimesavers #worksmarternotharder #teacherresources #edtech #selfpacedlearning #differentiatedinstruction #teacherwellness #teachersupport #modelitk12 #scienceteacher"
    },
    "Student Engagement Strategies": {
        "topics": [
            "Hooking reluctant learners",
            "Making science relevant to students' lives",
            "Boosting participation with hands-on tech",
            "Visual learners and modeling tools",
            "Gamification of systems thinking",
            "Student ownership of learning",
            "Collaborative exploration techniques",
            "Real-time feedback for engagement",
            "Differentiation that actually works",
            "Creating 'aha!' moments in science",
            "Building student confidence",
            "Motivating diverse learners",
            "Student choice and agency",
            "Connecting to student interests",
            "Building positive classroom culture",
            "Managing mixed-ability classrooms",
            "Re-engaging checked-out students",
            "Celebrating small wins",
            "Growth mindset in STEM",
            "Overcoming science anxiety",
            "Making thinking visible",
            "Student-driven questions",
            "Authentic assessment for engagement",
            "Building classroom community",
            "Inclusive engagement strategies",
            "Sustaining engagement long-term"
        ],
        "hooks": [
            "That moment when a struggling student suddenly gets it—magic! ✨",
            "Ever have a class where NO ONE is paying attention? 😴",
            "Want to see every hand shoot up, not just the same three? 🙋",
            "Struggling to reach your disengaged learners? 🎯",
            "What if every student felt confident in science? 💪",
            "Those students who 'aren't science people'... 🤷",
            "'When will we use this?' asked for the 47th time? 🔄",
            "Hands-on activities but half the class is lost? ✋",
            "Visual learners getting left behind? 👁️",
            "Want science to feel like their favorite game? 🎮",
            "Students controlling their learning—chaos or genius? 🚀",
            "Group work where everyone actually contributes? 🤝",
            "Feedback that students actually use to improve? 💬",
            "One lesson reaching both your struggling and gifted students? 🎯",
            "Creating those 'I finally get it!' moments? 💡",
            "Building confidence in students who've given up? 🌱",
            "Motivating 30 different personalities? 👥",
            "Student choice without losing learning targets? 🎨",
            "Making photosynthesis relevant to a 12-year-old? 🌿",
            "Culture where mistakes are celebrated? 🎉",
            "Teaching honors and intervention in one room? 📊",
            "That student who's checked out for weeks... 😞",
            "Celebrating growth, not just grades? 📈",
            "Science anxiety shutting students down? 😰",
            "Want to see what students are actually thinking? 🧠",
            "Questions from students, not just to students? ❓"
        ],
        "values": [
            "Interactive tools create breakthrough moments by making cause-effect visible.",
            "Relevance emerges when students can manipulate and explore systems.",
            "Technology that responds transforms passive watching into active doing.",
            "Visual modeling reaches learners who struggle with text and lecture.",
            "When learning feels like play, engagement becomes automatic.",
            "Control creates ownership—let students drive their exploration.",
            "Interactive tools naturally structure productive collaboration.",
            "Immediate feedback keeps students engaged and progressing.",
            "One interactive model adapts to every learning level naturally.",
            "Discovery learning creates more powerful 'aha' moments than telling.",
            "Success in small steps builds confidence for bigger challenges.",
            "Different entry points mean diverse learners all find their way in.",
            "Choice within structure gives freedom without chaos.",
            "Student interests become entry points to any science concept.",
            "Interactive exploration builds community through shared discovery.",
            "Self-paced tools let every student work at their perfect level.",
            "Models make abstract concepts concrete enough to re-engage anyone.",
            "Visible progress shows growth students can celebrate.",
            "Exploration fosters growth mindset—every attempt teaches something.",
            "Interactive models make invisible processes visible and less scary.",
            "Manipulation makes thinking visible and discussable.",
            "Student questions drive deeper learning than teacher questions.",
            "Real understanding shows in interaction, not just answers.",
            "Collaborative exploration builds connections and belonging.",
            "Multiple representations mean every learner finds their path.",
            "Sustained engagement comes from challenge without overwhelm."
        ],
        "ctas": [
            "Give every student the gift of discovery and watch understanding bloom.",
            "Transform disengagement into curiosity with one simple shift.",
            "See hands shooting up from every corner of your room.",
            "Reach that student you've been worried about.",
            "Build a classroom where everyone is a 'science person.'",
            "Turn 'when will we use this' into 'show me more!'",
            "Make hands-on learning actually accessible to all hands.",
            "Bring your visual learners into the science conversation.",
            "Turn learning into play without losing rigor.",
            "Hand students the keys to their own learning.",
            "Watch collaboration magic happen naturally.",
            "Create feedback loops that fuel growth.",
            "Meet every student exactly where they are.",
            "Multiply those magical teaching moments.",
            "Build confidence one discovery at a time.",
            "Reach every learner in your diverse classroom.",
            "Let students choose their path to the same destination.",
            "Connect abstract science to their actual lives.",
            "Create a culture where everyone belongs and grows.",
            "Challenge each student at their perfect level.",
            "Reignite curiosity in your checked-out students.",
            "Celebrate growth and watch motivation soar.",
            "Replace anxiety with excitement and possibility.",
            "See the thinking you've been guessing at.",
            "Turn students into question-askers, not just answer-givers.",
            "Build engagement that lasts all year long."
        ],
        "hashtags": "#teachersofinstagram #studentengagement #ahamoment #teacherlife #engagingstudents #interactivelearning #scienceteacher #stemteacher #teachingtips #classroomactivities #educationaltools #modelitk12 #scienceeducation"
    }
}

def get_post_date(post_num):
    """Calculate posting date for this post number"""
    # Post 1 = Week 1 Sunday, Post 2 = Week 1 Wednesday
    # Post 3 = Week 2 Sunday, Post 4 = Week 2 Wednesday
    week_num = ((post_num - 1) // 2)
    is_wednesday = (post_num % 2 == 0)

    days_offset = week_num * 7 + (3 if is_wednesday else 0)
    return START_DATE + timedelta(days=days_offset)

def generate_all_posts():
    """Generate all 104 posts"""
    posts = []

    # Theme rotation: 1, 2, 3, 4, 1, 2, 3, 4, etc.
    theme_names = list(THEMES.keys())

    for post_num in range(1, 105):
        # Determine theme (cycles through 4 themes)
        theme_index = (post_num - 1) % 4
        theme_name = theme_names[theme_index]
        theme_data = THEMES[theme_name]

        # Determine which topic within the theme (26 topics per theme)
        topic_index = ((post_num - 1) // 4) % 26

        # Get date
        post_date = get_post_date(post_num)
        day = post_date.strftime("%A")

        # Get content
        topic = theme_data["topics"][topic_index]
        hook = theme_data["hooks"][topic_index]
        value = theme_data["values"][topic_index]
        cta = theme_data["ctas"][topic_index]
        hashtags = theme_data["hashtags"]

        # Build full caption
        caption = f"{hook}\n{value}\n{cta}\n\n🔗 Explore more: modelitk12.com\n📚 Ready-to-use resources: teacherspayteachers.com/store/modelit\n\n💾 Save this for your next planning session!\n\n{hashtags}"

        # Image description
        image_desc = f"Modern minimalist Instagram image for ModelIT K12. Theme: {theme_name}. Topic: {topic}. Style: Clean, professional, scientific with deep blue #0f6de6 primary color, white background. 1080x1080px square."

        post = {
            "post_id": f"{post_num:03d}",
            "week": ((post_num - 1) // 2) + 1,
            "schedule_date": post_date.strftime("%Y-%m-%d"),
            "schedule_time": "19:00:00",
            "day": day,
            "theme": theme_name,
            "topic": topic,
            "hook": hook,
            "value": value,
            "cta": cta,
            "caption": caption,
            "hashtags": hashtags,
            "image_description": image_desc,
            "image_filename": f"Post_{post_num:03d}_Image.png",
            "image_status": "Not Generated",
            "posted": "No",
            "likes": "",
            "comments": "",
            "saves": "",
            "shares": "",
            "notes": ""
        }

        posts.append(post)

    return posts

def create_csv(posts):
    """Create CSV file"""
    output_file = r'C:\Users\MarieLexisDad\docs\ModelIT_Instagram_104_Posts_Complete.csv'

    headers = [
        "Post #",
        "Week #",
        "Post Date",
        "Post Time",
        "Day",
        "Theme",
        "Topic",
        "Hook",
        "Value",
        "CTA",
        "Full Caption",
        "Hashtags",
        "Image Description",
        "Image Filename",
        "Image Status",
        "Posted",
        "Likes",
        "Comments",
        "Saves",
        "Shares",
        "Notes"
    ]

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()

        for post in posts:
            writer.writerow({
                "Post #": post["post_id"],
                "Week #": post["week"],
                "Post Date": post["schedule_date"],
                "Post Time": post["schedule_time"],
                "Day": post["day"],
                "Theme": post["theme"],
                "Topic": post["topic"],
                "Hook": post["hook"],
                "Value": post["value"],
                "CTA": post["cta"],
                "Full Caption": post["caption"],
                "Hashtags": post["hashtags"],
                "Image Description": post["image_description"],
                "Image Filename": post["image_filename"],
                "Image Status": post["image_status"],
                "Posted": post["posted"],
                "Likes": post["likes"],
                "Comments": post["comments"],
                "Saves": post["saves"],
                "Shares": post["shares"],
                "Notes": post["notes"]
            })

    print(f"Created CSV with {len(posts)} posts")
    print(f"File: {output_file}")
    return output_file

def create_json(posts):
    """Create JSON file"""
    output_file = r'C:\Users\MarieLexisDad\docs\ModelIT_Instagram_104_Posts_Complete.json'

    data = {
        "campaign": {
            "name": "ModelIT K12 Instagram Campaign 2025-2026",
            "total_posts": 104,
            "posting_schedule": "2 posts per week (Sunday 7pm, Wednesday 7pm)",
            "duration": "52 weeks",
            "start_date": "2025-01-05",
            "end_date": posts[-1]["schedule_date"],
            "brand": {
                "website": "modelitk12.com",
                "tpt_store": "teacherspayteachers.com/store/modelit",
                "instagram": "@modelitk12",
                "primary_color": "#0f6de6",
                "hashtag": "#modelitk12"
            }
        },
        "posts": posts
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Created JSON with {len(posts)} posts")
    print(f"File: {output_file}")
    return output_file

if __name__ == "__main__":
    print("Generating all 104 ModelIT Instagram posts...")
    posts = generate_all_posts()

    csv_file = create_csv(posts)
    json_file = create_json(posts)

    print(f"\nSuccess! Created {len(posts)} unique posts")
    print(f"\nTheme breakdown:")
    for theme in THEMES.keys():
        count = sum(1 for p in posts if p['theme'] == theme)
        print(f"   {theme}: {count} posts")

    print(f"\nDate range: {posts[0]['schedule_date']} to {posts[-1]['schedule_date']}")
    print(f"\nNext step: Generate all 104 images!")
