import os
import time
import logging
from playwright.sync_api import sync_playwright

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

OUTPUT_DIR = "docs/screenshots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

PAGES_TO_CAPTURE = [
    {"name": "Command Center", "filename": "01_command_center.png"},
    {"name": "AI Analysis", "filename": "02_ai_analysis.png"},
    {"name": "Complaint Detail", "filename": "03_investigation_console.png"},
    {"name": "Incident Clusters", "filename": "04_incident_clusters.png"},
    {"name": "Executive Intelligence", "filename": "05_executive_intelligence.png"}
]


def capture_all():
    with sync_playwright() as p:
        logger.info("Launching headless Chromium browser at 1440x900 viewport...")
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        logger.info("Navigating to http://127.0.0.1:8501 ...")
        page.goto("http://127.0.0.1:8501", wait_until="networkidle")
        time.sleep(3)

        for target in PAGES_TO_CAPTURE:
            page_name = target["name"]
            filename = target["filename"]
            save_path = os.path.join(OUTPUT_DIR, filename)

            logger.info(f"Navigating to page '{page_name}'...")
            
            # Click navigation item in Streamlit sidebar
            try:
                # Find nav link matching text
                nav_link = page.get_by_role("link", name=page_name, exact=False)
                if nav_link.count() > 0:
                    nav_link.first.click()
                    time.sleep(2.5)
                else:
                    logger.warning(f"Nav link for {page_name} not directly found by role, trying text click...")
                    page.click(f"text={page_name}")
                    time.sleep(2.5)
            except Exception as e:
                logger.error(f"Error navigating to {page_name}: {e}")

            # Wait for content & Plotly charts to stabilize
            time.sleep(1.5)

            page.screenshot(path=save_path, full_page=False)
            logger.info(f"Captured {save_path} successfully!")

        browser.close()
        logger.info("All screenshots captured cleanly!")


if __name__ == "__main__":
    capture_all()
