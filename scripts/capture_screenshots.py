import os
import time
import logging
from playwright.sync_api import sync_playwright

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

OUTPUT_DIR = "docs/screenshots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

PAGES_TO_VERIFY = [
    "Command Center",
    "Submit Complaint",
    "Complaint Queue",
    "Human Review Queue",
    "SLA Monitor",
    "AI Analysis",
    "Incident Clusters",
    "Train Intelligence",
    "Station Intelligence",
    "Executive Intelligence",
    "Complaint Detail"
]

SHOWCASE_CAPURES = [
    {"name": "Command Center", "filename": "01_command_center.png"},
    {"name": "AI Analysis", "filename": "02_ai_analysis.png"},
    {"name": "Complaint Detail", "filename": "03_investigation_console.png"},
    {"name": "Incident Clusters", "filename": "04_incident_clusters.png"},
    {"name": "Executive Intelligence", "filename": "05_executive_intelligence.png"}
]

EXCEPTION_SIGNATURES = [
    "ImportError",
    "ModuleNotFoundError",
    "Traceback (most recent call last)",
    "SyntaxError",
    "NameError",
    "AttributeError",
    "StreamlitAPIException",
    "StreamlitSetPageConfigMustBeFirstCommandError",
]


def run_verification_and_capture():
    with sync_playwright() as p:
        logger.info("Launching headless Chromium browser at 1440x900 viewport...")
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        logger.info("Navigating to http://127.0.0.1:8501 ...")
        page.goto("http://127.0.0.1:8501", wait_until="networkidle")
        time.sleep(3)

        # 1. Verify ALL 11 registered pages
        logger.info("--- VERIFYING ALL 11 STREAMLIT PAGES ---")
        failed_pages = []
        for p_name in PAGES_TO_VERIFY:
            try:
                nav_link = page.get_by_role("link", name=p_name, exact=False)
                if nav_link.count() > 0:
                    nav_link.first.click()
                else:
                    page.click(f"text={p_name}")
                time.sleep(2)

                # Robust Exception Detection: DOM selector + specific exception signatures
                exception_elements = page.locator(".stException, [data-testid='stException']")
                has_dom_exception = exception_elements.count() > 0

                content = page.content()
                has_text_exception = any(sig in content for sig in EXCEPTION_SIGNATURES)

                if has_dom_exception or has_text_exception:
                    logger.error(f"  ❌ FAIL: {p_name} contains runtime exception or traceback!")
                    failed_pages.append(p_name)
                else:
                    logger.info(f"  ✅ PASS: {p_name} loaded cleanly with zero errors.")
            except Exception as e:
                logger.error(f"  ❌ FAIL: Exception navigating to {p_name}: {e}")
                failed_pages.append(p_name)

        if failed_pages:
            logger.error(f"Page verification failed for: {failed_pages}")
            browser.close()
            raise RuntimeError(f"Streamlit pages failed verification: {failed_pages}")

        logger.info("All 11 Streamlit pages verified PASS cleanly with 0 errors!")

        # 2. Capture the 5 Showcase Screenshots
        logger.info("--- CAPTURING 5 PORTFOLIO SHOWCASE SCREENSHOTS ---")
        for target in SHOWCASE_CAPURES:
            p_name = target["name"]
            filename = target["filename"]
            save_path = os.path.join(OUTPUT_DIR, filename)

            nav_link = page.get_by_role("link", name=p_name, exact=False)
            if nav_link.count() > 0:
                nav_link.first.click()
            else:
                page.click(f"text={p_name}")
            time.sleep(3)

            # Special action for AI Analysis to populate live demo output
            if p_name == "AI Analysis":
                try:
                    text_area = page.get_by_role("textbox")
                    if text_area.count() > 0:
                        text_area.first.fill("AC is not cooling in coach B4 seat 21 on train 12951 since Pune.")
                        analyze_btn = page.get_by_role("button", name="Run Unified AI Pipeline")
                        if analyze_btn.count() > 0:
                            analyze_btn.first.click()
                            time.sleep(3)
                except Exception as e:
                    logger.warning(f"Could not submit AI analysis demo text: {e}")

            time.sleep(2)
            page.screenshot(path=save_path, full_page=False)
            logger.info(f"  📸 Captured {save_path} (1440x900 PNG)")

        browser.close()
        logger.info("All 5 showcase screenshots captured successfully!")


if __name__ == "__main__":
    run_verification_and_capture()
