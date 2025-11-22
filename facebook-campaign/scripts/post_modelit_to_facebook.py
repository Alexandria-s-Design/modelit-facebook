#!/usr/bin/env python3
"""
Post ModelIt K12 introduction to Facebook via Ayrshare API
Shows post preview first, then posts after approval
"""

import requests
import json
from datetime import datetime, timedelta
from colorama import Fore, Style, init

init(autoreset=True)

# Ayrshare API Configuration
AYRSHARE_API_KEY = "7D248853-8AF94A41-A48F07DC-73F74D88"
AYRSHARE_API_URL = "https://api.ayrshare.com/api/post"

# Post content
POST_CONTENT = """🔬✨ Introducing ModelIt K12 – where systems thinking meets hands-on STEM education! We're transforming classrooms with interactive biological modeling experiences through Cell Collective, giving students the power to explore real-world scientific concepts through simulation and discovery. Our ready-to-use resources make it easy for educators to bring cutting-edge computational biology into any classroom. Check out our Teachers Pay Teachers store for engaging lesson plans, activities, and more! 🎓🧬 #STEMEducation #SystemsThinking #ModelItK12 #TeachersPayTeachers"""

def print_header(text):
    print(f"\n{Fore.CYAN}{'=' * 70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{text}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 70}{Style.RESET_ALL}\n")

def preview_post():
    """Show post preview"""
    print_header("📝 POST PREVIEW")
    print(f"{Fore.WHITE}{POST_CONTENT}{Style.RESET_ALL}\n")

    print(f"{Fore.YELLOW}Platform:{Style.RESET_ALL} Facebook")
    print(f"{Fore.YELLOW}Character count:{Style.RESET_ALL} {len(POST_CONTENT)}")
    print(f"{Fore.YELLOW}Hashtags:{Style.RESET_ALL} #STEMEducation #SystemsThinking #ModelItK12 #TeachersPayTeachers")

def get_scheduling_choice():
    """Ask user when to post"""
    print_header("⏰ SCHEDULING OPTIONS")

    print(f"{Fore.GREEN}1.{Style.RESET_ALL} Post immediately")
    print(f"{Fore.GREEN}2.{Style.RESET_ALL} Schedule for specific date/time")
    print(f"{Fore.GREEN}3.{Style.RESET_ALL} Cancel\n")

    choice = input(f"{Fore.CYAN}Choose option (1-3): {Style.RESET_ALL}").strip()
    return choice

def get_schedule_datetime():
    """Get scheduled date/time from user"""
    print(f"\n{Fore.YELLOW}Enter schedule date and time:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Format: YYYY-MM-DD HH:MM (24-hour, your local time){Style.RESET_ALL}")
    print(f"{Fore.WHITE}Example: 2025-11-18 14:00{Style.RESET_ALL}\n")

    datetime_str = input(f"{Fore.CYAN}Date/Time: {Style.RESET_ALL}").strip()

    try:
        # Parse user input
        dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")

        # Convert to UTC ISO format (Ayrshare expects UTC)
        # For simplicity, assuming user's time is UTC. Adjust if needed.
        iso_format = dt.strftime("%Y-%m-%dT%H:%M:%SZ")

        print(f"\n{Fore.GREEN}✓ Scheduled for: {datetime_str}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  (UTC format: {iso_format}){Style.RESET_ALL}")

        return iso_format
    except ValueError:
        print(f"\n{Fore.RED}❌ Invalid format. Using immediate posting.{Style.RESET_ALL}")
        return None

def post_to_facebook(schedule_date=None, image_url=None):
    """Post to Facebook via Ayrshare API"""

    # Build payload
    payload = {
        "post": POST_CONTENT,
        "platforms": ["facebook"],
        "shortenLinks": True
    }

    # Add scheduling if specified
    if schedule_date:
        payload["scheduleDate"] = schedule_date

    # Add image if specified
    if image_url:
        payload["mediaUrls"] = [image_url]

    # Make API request
    headers = {
        "Authorization": f"Bearer {AYRSHARE_API_KEY}",
        "Content-Type": "application/json"
    }

    print_header("🚀 POSTING TO FACEBOOK")
    print(f"{Fore.YELLOW}Sending request to Ayrshare...{Style.RESET_ALL}\n")

    try:
        response = requests.post(
            AYRSHARE_API_URL,
            headers=headers,
            json=payload
        )

        if response.status_code == 200:
            result = response.json()

            print(f"{Fore.GREEN}✅ SUCCESS!{Style.RESET_ALL}\n")

            # Display results
            print(f"{Fore.CYAN}Status:{Style.RESET_ALL} {result.get('status', 'N/A')}")
            print(f"{Fore.CYAN}Post ID:{Style.RESET_ALL} {result.get('id', 'N/A')}")

            if 'postIds' in result:
                for post_info in result['postIds']:
                    platform = post_info.get('platform', 'N/A')
                    post_id = post_info.get('id', 'N/A')
                    status = post_info.get('status', 'N/A')

                    print(f"\n{Fore.GREEN}Platform:{Style.RESET_ALL} {platform}")
                    print(f"{Fore.GREEN}ID:{Style.RESET_ALL} {post_id}")
                    print(f"{Fore.GREEN}Status:{Style.RESET_ALL} {status}")

                    if 'scheduledDate' in post_info:
                        scheduled = post_info['scheduledDate']
                        print(f"{Fore.GREEN}Scheduled:{Style.RESET_ALL} {scheduled}")

            print(f"\n{Fore.YELLOW}📊 View post at:{Style.RESET_ALL} https://app.ayrshare.com/posts")

            return result
        else:
            print(f"{Fore.RED}❌ ERROR: {response.status_code}{Style.RESET_ALL}")
            print(f"{Fore.RED}Response:{Style.RESET_ALL} {response.text}")
            return None

    except Exception as e:
        print(f"{Fore.RED}❌ Exception: {e}{Style.RESET_ALL}")
        return None

def check_api_connection():
    """Verify Ayrshare API is accessible"""
    print_header("🔍 CHECKING API CONNECTION")

    try:
        response = requests.get(
            "https://api.ayrshare.com/api/user",
            headers={"Authorization": f"Bearer {AYRSHARE_API_KEY}"}
        )

        if response.status_code == 200:
            user_data = response.json()
            print(f"{Fore.GREEN}✓ API Connected{Style.RESET_ALL}")
            print(f"  Account: {user_data.get('email', 'N/A')}")
            print(f"  Plan: {user_data.get('planName', 'N/A')}")
            print(f"  Posts used: {user_data.get('postsUsed', 0)}/{user_data.get('postsAllowed', 20)}")
            print(f"  Remaining: {user_data.get('postsRemaining', 0)}")
            return True
        else:
            print(f"{Fore.RED}✗ API Error: {response.status_code}{Style.RESET_ALL}")
            return False
    except Exception as e:
        print(f"{Fore.RED}✗ Connection failed: {e}{Style.RESET_ALL}")
        return False

def main():
    print(f"{Fore.CYAN}")
    print("=" * 70)
    print("  MODELIT K12 - FACEBOOK POST PUBLISHER")
    print("=" * 70)
    print(f"{Style.RESET_ALL}")

    # Check API connection
    if not check_api_connection():
        print(f"\n{Fore.RED}Cannot proceed without API connection.{Style.RESET_ALL}")
        return

    # Show preview
    preview_post()

    # Get approval
    print(f"\n{Fore.YELLOW}Review the post above.{Style.RESET_ALL}")
    approve = input(f"{Fore.CYAN}Do you want to proceed? (y/n): {Style.RESET_ALL}").strip().lower()

    if approve != 'y':
        print(f"\n{Fore.YELLOW}Post cancelled.{Style.RESET_ALL}")
        return

    # Ask about image
    print(f"\n{Fore.YELLOW}Do you have an image URL to include?{Style.RESET_ALL}")
    has_image = input(f"{Fore.CYAN}Include image? (y/n): {Style.RESET_ALL}").strip().lower()

    image_url = None
    if has_image == 'y':
        image_url = input(f"{Fore.CYAN}Enter image URL: {Style.RESET_ALL}").strip()
        if image_url:
            print(f"{Fore.GREEN}✓ Image will be included{Style.RESET_ALL}")

    # Get scheduling choice
    choice = get_scheduling_choice()

    schedule_date = None
    if choice == '1':
        # Post immediately
        print(f"\n{Fore.GREEN}Posting immediately...{Style.RESET_ALL}")
    elif choice == '2':
        # Schedule for later
        schedule_date = get_schedule_datetime()
    else:
        print(f"\n{Fore.YELLOW}Post cancelled.{Style.RESET_ALL}")
        return

    # Final confirmation
    print(f"\n{Fore.YELLOW}{'=' * 70}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}FINAL CONFIRMATION{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'=' * 70}{Style.RESET_ALL}")
    print(f"Platform: Facebook")
    if schedule_date:
        print(f"Timing: Scheduled for {schedule_date}")
    else:
        print(f"Timing: Immediate")
    if image_url:
        print(f"Image: Yes ({image_url[:50]}...)")
    else:
        print(f"Image: No")
    print(f"{Fore.YELLOW}{'=' * 70}{Style.RESET_ALL}\n")

    confirm = input(f"{Fore.CYAN}Confirm and post? (y/n): {Style.RESET_ALL}").strip().lower()

    if confirm == 'y':
        result = post_to_facebook(schedule_date, image_url)

        if result:
            print_header("✅ POST PUBLISHED SUCCESSFULLY")
            print(f"{Fore.GREEN}Your ModelIt K12 introduction is now on Facebook!{Style.RESET_ALL}")
            print(f"\nNext steps:")
            print(f"  1. Check post status: https://app.ayrshare.com/posts")
            print(f"  2. Monitor engagement on Facebook")
            print(f"  3. Respond to comments")
    else:
        print(f"\n{Fore.YELLOW}Post cancelled.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
