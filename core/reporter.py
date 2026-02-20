import json
import os
from datetime import datetime


def ensure_reports_folder():
    if not os.path.exists("reports"):
        os.makedirs("reports")


def generate_json_report(data):
    ensure_reports_folder()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"reports/report_{timestamp}.json"

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

    print(f"[+] JSON report saved: {filename}")


def generate_html_report(data):
    ensure_reports_folder()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"reports/report_{timestamp}.html"

    html_content = f"""
    <html>
    <head>
        <title>NetSpectre Report</title>
        <style>
            body {{ font-family: Arial; background-color: #111; color: #0f0; }}
            h1 {{ color: #0ff; }}
            pre {{ background-color: #222; padding: 15px; }}
        </style>
    </head>
    <body>
        <h1>NetSpectre Scan Report</h1>
        <pre>{json.dumps(data, indent=4)}</pre>
    </body>
    </html>
    """

    with open(filename, "w") as f:
        f.write(html_content)

    print(f"[+] HTML report saved: {filename}")