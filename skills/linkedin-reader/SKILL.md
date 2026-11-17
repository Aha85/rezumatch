---
name: linkedin-reader
description: Reads a LinkedIn profile for resume work. Use when a user gives a LinkedIn profile URL as their resume source, or asks to import, read or turn their LinkedIn profile into a resume.
---

# LinkedIn reader

LinkedIn blocks most automated fetching, so try the routes in this order and stop at the first that works.

## 1. A browser the user is signed in to
If a browser tool is available (Claude in Chrome, or another browser the user is signed in to):
- Open the profile URL and read the page text: headline, About, every Experience entry (title, company, dates, location, description), Education, Licenses and certifications, Skills.
- Expand "see more" sections and the full Experience list when they are collapsed.
- Only read. Never message, follow, endorse or change anything on the account.

## 2. The PDF export (most reliable)
Guide the user, one step per message:
1. Open your LinkedIn profile.
2. Click "More" (or "Resources"), then "Save to PDF".
3. Upload the file here.
Then run `extract_resume.py` on it from the resume-tailor skill.

## 3. Paste
Ask the user to copy the About and Experience sections and paste them.

## After reading
- Save the text to `work/source.txt`.
- Report counted facts only: number of entries, earliest year, current roles. Never estimate.
- Note what usually needs a fix: stale contact details, long About text, roles with no description.
