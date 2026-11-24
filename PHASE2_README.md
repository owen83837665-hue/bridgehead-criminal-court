# Phase 2: inspect official court schedule page

This diagnostic workflow makes a single GET request to the public Judicial Yuan schedule page and records its HTML form controls, input names, select options, and external script URLs.

It does **not** submit a search, download case data, or claim that unattended retrieval works yet.

## Add these files to the repository

- `inspect_court_page.py` (repository root)
- `.github/workflows/inspect.yml`

Then open **Actions → Inspect official court schedule page → Run workflow**.
When it finishes, download the `court-page-inspection` artifact and provide `court_page_probe.json` for analysis.

The workflow is manual-only for now. Do not add a daily schedule until the official query parameters and CSV download behavior are verified.
