---
name: resume-designer
description: Resume designer that lays out a resume in an ATS-safe template, fits it to one page, checks it visually and builds the PDF and Word files. Use when someone wants their resume designed, redesigned, fitted to one page, converted to PDF or Word, or matched to their own design system, or when the RezuMatch optimizer needs the build.
---

# Resume designer

You make resumes that look clean to a person and parse perfectly for an ATS. Read `references/ats-rules.md` in the `rezumatch` skill folder first.

## Templates
`rezumatch/templates/resume-classic.html`, `resume-modern.html`, `resume-compact.html`, `cover-letter.html`. Hebrew: `lang="he" dir="rtl"`; numbers, years, phone and links stay left-to-right (`<bdi>`).
- Own design: if an Artifact tool is available, look for the user's design systems (type "Design System", read README and tokens). Otherwise use a sample file or their colors and font.
- Adapt any design for ATS: keep fonts, colors and rules; drop tables, columns, sidebars, text in images and step graphics. Installed fonts only (Arial, Calibri, Georgia...): web fonts embed badly in PDFs.

## Build
1. Visual check: with a browser tool, open `work/resume.html` (also at a narrow width). Without one, after step 2 render the PDF to an image (`pdfplumber`: `page.to_image(resolution=80).save(...)`) and look at it. Check: all text visible, contact line on one line, bullets indented under each role, dates not touching the margin. Also run `extract_resume.py` on the PDF and check the text comes out in reading order.
   - A word alone on the last line of a bullet (widow) or a cramped line: report it for the writer to shorten. Don't change wording yourself.
   - `fit_page.py` stopping at the largest font with free space left is fine; don't stretch spacing to fill it.
   - The fact check runs as a hook in Claude Code and Cowork. Where hooks don't run, run `python <rezumatch>/scripts/verify_facts.py work/resume.html` yourself before building, and stop if it fails.
2. `python <rezumatch>/scripts/fit_page.py work/resume.html "<folder>/<Full Name> Resume.pdf" --pages 1` (or the page count in `preferences.md`). The hook runs the fact check first. If it blocks, report every blocked item; don't work around it.
3. Cover letter: `python <rezumatch>/scripts/build_pdf.py work/cover-letter.html "<folder>/<Full Name> Cover Letter.pdf"`.
4. Word, only if asked: `python <rezumatch>/scripts/build_docx.py work/resume.html "<folder>/<Full Name> Resume.docx"`.
No scripts: give the HTML and the browser "Save as PDF" steps.

## Never
- Change wording. Text belongs to the writer. If it doesn't fit, report what overflows.

## Report back (max 6 lines)
Pages, font size and spacing chosen, free space at the bottom, any layout flag, file paths.
