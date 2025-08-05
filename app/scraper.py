# 📁 File: app/scraper.py

from playwright.sync_api import sync_playwright
import psycopg2
from config import DB_NAME, DB_USER, DB_PASS, DB_HOST, DB_PORT


def init_db():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                            password=DB_PASS, host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS queries (
        id SERIAL PRIMARY KEY,
        case_type TEXT,
        case_no TEXT,
        filing_year TEXT,
        raw_response TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    conn.commit()
    conn.close()


def save_query(case_type, case_no, filing_year, raw):
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                            password=DB_PASS, host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO queries (case_type, case_no, filing_year, raw_response)
        VALUES (%s, %s, %s, %s)
    """, (case_type, case_no, filing_year, raw))
    conn.commit()
    conn.close()


def fetch_case_details(case_type, case_no, filing_year):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/114.0.0.0 Safari/537.36")
        page = context.new_page()

        result = {}
        try:
            print("📸 Navigating to Delhi High Court website...")
            page.goto("https://delhihighcourt.nic.in/case.asp")
            page.wait_for_timeout(5000)
            page.wait_for_selector("#txtcaptcha", timeout=15000)

            html = page.content()
            with open("page_dump.html", "w", encoding="utf-8") as f:
                f.write(html)
            print("🧾 HTML saved to 'page_dump.html'")

            page.screenshot(path="captcha.png")
            print("\n🛑 CAPTCHA Required. Open 'captcha.png' and type what you see.")
            captcha_text = input("Enter CAPTCHA: ")

            print("📝 Filling form")
            page.select_option("#ddlcasetype", case_type)
            page.fill("#txtcaseno", case_no)
            page.fill("#txtcyear", filing_year)
            page.fill("#txtcaptcha", captcha_text)
            page.click("#btnSearch")
            page.wait_for_timeout(5000)

            try:
                html = page.content()
            except Exception as e:
                html = "Unavailable"
                print("⚠️ Failed to get HTML content:", e)

            pdf_link = "-"
            try:
                print("📎 Scraping PDF link")
                order_link = page.query_selector("a[href*='dhcqrydisp_o.asp']")
                if order_link:
                    href = order_link.get_attribute("href")
                    order_url = f"https://delhihighcourt.nic.in/{href}"
                    new_page = context.new_page()
                    new_page.goto(order_url)
                    iframe = new_page.query_selector("iframe")
                    if iframe:
                        src = iframe.get_attribute("src")
                        if src:
                            pdf_link = f"https://delhihighcourt.nic.in/{src}"
            except Exception as e:
                print("⚠️ PDF link extraction failed:", e)

            print("✅ Done scraping — ready to close browser")
            result = {
                "parties": "Not parsed",
                "filing_date": "-",
                "hearing_date": "-",
                "pdf_link": pdf_link,
                "raw": html
            }


        except Exception as e:
            print("⚠️ Scraping exception:", e)

            result = {

                "parties": f"Scraping failed: {e}",

                "filing_date": "-",

                "hearing_date": "-",

                "pdf_link": "-",

                "raw": "See terminal log"

            }


        finally:
            print("✅ Closing browser")
            browser.close()

        return result
