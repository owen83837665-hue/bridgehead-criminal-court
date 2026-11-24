#!/usr/bin/env python3
"""Inspect the public Judicial Yuan court-schedule page without submitting queries."""
from __future__ import annotations
import json
import requests
from bs4 import BeautifulSoup

URL = "https://di3.judicial.gov.tw/"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; CourtScheduleResearch/1.0)"}

def main():
    response = requests.get(URL, headers=HEADERS, timeout=30)
    response.raise_for_status()
    response.encoding = response.apparent_encoding or response.encoding
    soup = BeautifulSoup(response.text, "html.parser")

    report = {
        "url": response.url,
        "status_code": response.status_code,
        "encoding": response.encoding,
        "title": soup.title.get_text(" ", strip=True) if soup.title else "",
        "forms": [],
        "scripts": [s.get("src") for s in soup.find_all("script") if s.get("src")],
    }
    for form in soup.find_all("form"):
        item = {
            "action": form.get("action", ""),
            "method": form.get("method", "get").lower(),
            "id": form.get("id", ""),
            "name": form.get("name", ""),
            "controls": [],
        }
        for el in form.find_all(["input", "select", "textarea", "button"]):
            control = {
                "tag": el.name,
                "type": el.get("type", ""),
                "name": el.get("name", ""),
                "id": el.get("id", ""),
                "value": el.get("value", ""),
                "text": el.get_text(" ", strip=True)[:120],
            }
            if el.name == "select":
                control["options"] = [
                    {"value": opt.get("value", ""), "text": opt.get_text(" ", strip=True)}
                    for opt in el.find_all("option")
                ][:80]
            item["controls"].append(control)
        report["forms"].append(item)

    output = json.dumps(report, ensure_ascii=False, indent=2)
    print(output)
    with open("court_page_probe.json", "w", encoding="utf-8") as f:
        f.write(output)

if __name__ == "__main__":
    main()
