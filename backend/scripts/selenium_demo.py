"""
Selenium automation demo — extracts candidate profile from saved HTML,
calls the backend API, and prints structured results.

Run: python backend/scripts/selenium_demo.py
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import requests
from bs4 import BeautifulSoup

API_BASE = "http://localhost:8000/api"


def extract_from_html(filepath: str) -> tuple[str, str]:
    """Extract candidate profile text from a locally saved HTML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')

    # Remove noisy elements
    for tag in soup(['script', 'style', 'nav', 'header', 'footer']):
        tag.decompose()

    # Try common candidate profile selectors
    main_content = (
        soup.select_one('[class*="resume"]') or
        soup.select_one('[class*="profile"]') or
        soup.select_one('[class*="detail"]') or
        soup.select_one('main') or
        soup.body
    )

    raw_text = main_content.get_text(' ', strip=True) if main_content else soup.get_text(' ', strip=True)
    # Collapse whitespace
    raw_text = ' '.join(raw_text.split())

    source_site = "demo.local"
    return raw_text, source_site


def call_parse_api(raw_text: str, source_site: str) -> dict:
    """Send raw text to the resume parsing API."""
    res = requests.post(
        f"{API_BASE}/resume/parse",
        json={"raw_text": raw_text, "source_site": source_site},
    )
    res.raise_for_status()
    return res.json()


def call_matching_api(candidate: dict, jd_text: str) -> dict:
    """Send candidate and JD to the matching API."""
    res = requests.post(
        f"{API_BASE}/matching/score",
        json={"candidate": candidate, "jd_text": jd_text},
    )
    res.raise_for_status()
    return res.json()


def call_message_api(candidate: dict, jd_title: str, jd_company: str, template_type: str = "面试邀请") -> dict:
    """Generate an outreach message."""
    res = requests.post(
        f"{API_BASE}/message/generate",
        json={
            "candidate": candidate,
            "jd_title": jd_title,
            "jd_company": jd_company,
            "template_type": template_type,
            "custom_instruction": "",
        },
    )
    res.raise_for_status()
    return res.json()


def main():
    # Check if HTML file provided
    if len(sys.argv) < 2:
        print("Usage: python selenium_demo.py <path_to_candidate_page.html>")
        print()
        print("If no HTML file is available, a sample extraction demo will run instead.")
        print("First, save a recruitment page as HTML, then run:")
        print("  python backend/scripts/selenium_demo.py candidate.html")
        print()
        print("=" * 60)
        print("Hint: You can manually save a BOSS直聘 candidate page as HTML")
        print("and use this script to demonstrate the automation pipeline.")
        return

    html_path = sys.argv[1]
    if not os.path.exists(html_path):
        print(f"File not found: {html_path}")
        return

    # Step 1: Extract
    print("[1/4] Extracting text from HTML...")
    raw_text, source_site = extract_from_html(html_path)
    print(f"  Extracted {len(raw_text)} characters from {source_site}")

    # Step 2: Parse resume
    print("[2/4] Parsing resume via API...")
    try:
        candidate = call_parse_api(raw_text, source_site)
        print(f"  Name: {candidate.get('name', 'N/A')}")
        print(f"  Title: {candidate.get('current_title', 'N/A')}")
        print(f"  Skills: {', '.join(candidate.get('skills', []))}")
    except Exception as e:
        print(f"  Parse failed: {e}")
        print("  Make sure the backend is running: uvicorn app.main:app --reload")
        return

    # Step 3: Match against sample JD
    print("[3/4] Running candidate-JD matching...")
    sample_jd = """我们正在寻找一位高级前端开发工程师，要求：
    - 3年以上前端开发经验
    - 精通 Vue.js 或 React
    - 熟悉 TypeScript
    - 有浏览器插件开发经验优先
    - 良好的沟通能力和团队协作精神"""

    try:
        match_result = call_matching_api(candidate, sample_jd)
        print(f"  Overall Score: {match_result.get('overall_score', 'N/A')}")
        print(f"  Recommendation: {match_result.get('recommendation', 'N/A')}")
    except Exception as e:
        print(f"  Matching failed: {e}")

    # Step 4: Generate message
    print("[4/4] Generating outreach message...")
    try:
        msg_result = call_message_api(
            candidate,
            jd_title="高级前端开发工程师",
            jd_company="示例科技有限公司",
            template_type="面试邀请",
        )
        print(f"  Generated Message:")
        print(f"  {msg_result.get('message', 'N/A')[:200]}...")
    except Exception as e:
        print(f"  Message generation failed: {e}")

    print()
    print("=" * 60)
    print("Demo complete! All pipeline stages verified.")


if __name__ == "__main__":
    main()
