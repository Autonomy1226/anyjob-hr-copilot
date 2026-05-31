"""
End-to-end pipeline test — runs without browser, using a saved HTML file.
Tests: extract → parse → matching → message → dashboard
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import requests
from bs4 import BeautifulSoup

API_BASE = "http://localhost:8000/api"

# Sample JD for matching test
SAMPLE_JD = """高级前端开发工程师
岗位要求：
- 3年以上前端开发经验
- 精通 Vue.js 或 React，熟悉 TypeScript
- 有浏览器插件开发经验优先
- 熟悉前端工程化（Webpack/Vite）
- 良好的沟通能力和团队协作精神
- 工作地点：上海"""


def extract_from_html(filepath: str) -> str:
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    for tag in soup(['script', 'style', 'nav', 'header', 'footer']):
        tag.decompose()

    body = soup.body or soup
    text = body.get_text(' ', strip=True)
    return ' '.join(text.split())


def test_health():
    print("[1/5] Health check...", end=" ")
    r = requests.get(f"{API_BASE}/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    print(f"OK (model: {data['model']})")


def test_resume_parse(raw_text: str) -> dict:
    print("[2/5] Resume parse...", end=" ")
    r = requests.post(f"{API_BASE}/resume/parse", json={
        "raw_text": raw_text,
        "source_site": "zhipin.com",
    })
    assert r.status_code == 200
    data = r.json()
    assert data.get("name"), "Name field missing"
    assert len(data.get("skills", [])) > 0, "No skills extracted"
    print(f"OK (name={data['name']}, skills={len(data['skills'])})")
    return data


def test_matching(candidate: dict) -> dict:
    print("[3/5] Candidate matching...", end=" ")
    r = requests.post(f"{API_BASE}/matching/score", json={
        "candidate": candidate,
        "jd_text": SAMPLE_JD,
    })
    assert r.status_code == 200
    data = r.json()
    assert 0 <= data.get("overall_score", -1) <= 100, "Score out of range"
    assert len(data.get("radar_dimensions", [])) > 0, "No radar dimensions"
    print(f"OK (score={data['overall_score']}, recommendation={data['recommendation']})")
    return data


def test_message(candidate: dict):
    print("[4/5] Message generation...", end=" ")
    r = requests.post(f"{API_BASE}/message/generate", json={
        "candidate": candidate,
        "jd_title": "高级前端开发工程师",
        "jd_company": "字节跳动",
        "template_type": "面试邀请",
        "custom_instruction": "",
    })
    assert r.status_code == 200
    data = r.json()
    assert len(data.get("message", "")) > 20, "Message too short"
    print(f"OK (message_len={len(data['message'])}, template={data['template_used']})")
    return data


def test_dashboard():
    print("[5/5] Dashboard stats...", end=" ")
    r = requests.get(f"{API_BASE}/dashboard/stats?days=7")
    assert r.status_code == 200
    data = r.json()
    print(f"OK (parsed={data['total_parsed']}, matched={data['total_matched']}, messages={data['total_messages']})")
    return data


def main():
    html_path = os.path.join(os.path.dirname(__file__), "test_candidate.html")
    if not os.path.exists(html_path):
        print(f"Test HTML not found: {html_path}")
        sys.exit(1)

    passed = 0
    failed = 0

    # Health
    try:
        test_health()
        passed += 1
    except Exception as e:
        failed += 1
        print(f"FAIL: {e}")

    # Extract
    raw_text = extract_from_html(html_path)
    print(f"    Extracted {len(raw_text)} chars from HTML")

    # Parse
    candidate = None
    try:
        candidate = test_resume_parse(raw_text)
        passed += 1
    except Exception as e:
        failed += 1
        print(f"FAIL: {e}")

    # Match
    match_result = None
    if candidate:
        try:
            match_result = test_matching(candidate)
            passed += 1
        except Exception as e:
            failed += 1
            print(f"FAIL: {e}")

        try:
            test_message(candidate)
            passed += 1
        except Exception as e:
            failed += 1
            print(f"FAIL: {e}")

    # Dashboard
    try:
        test_dashboard()
        passed += 1
    except Exception as e:
        failed += 1
        print(f"FAIL: {e}")

    print(f"\n{'='*60}")
    print(f"Results: {passed} passed, {failed} failed")
    if failed == 0:
        print("All pipeline tests passed!")
    else:
        print("Some tests failed — check errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
