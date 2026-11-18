# RezuMatch

A free Claude plugin that fits your resume to one specific job listing, step by step.

- **Estimated ATS score** before and after, with the keywords you're missing
- **A coach, not a form:** one question at a time, with clear choices
- **Never invents facts:** every number, title and claim comes from you, and a built-in check blocks anything that doesn't
- **Ready-to-send files:** a one-page PDF resume, a matching cover letter, and a Word version if a portal asks for one
- **Your design:** clean built-in templates, or your own Claude design system
- **English and Hebrew** (full right-to-left support)

**Step-by-step guide for everyone: [dannyshaket.com/en/creations/rezumatch](https://www.dannyshaket.com/en/creations/rezumatch)**

[עברית](README.he.md)

## What you need
- Claude: Claude Code, the Claude desktop app, or claude.ai
- Your resume (PDF, Word, pasted text or a LinkedIn profile), or no resume at all: it can build one with you
- The job listing (text or link)
- For the automatic checks and PDF export on your computer (Claude Code or the desktop app):
  - Google Chrome or Microsoft Edge (you probably have one already)
  - Python 3 ([python.org/downloads](https://www.python.org/downloads/)). Claude installs the few Python packages it needs and tells you first.

No Python? It still works: Claude scores by hand and gives you the resume as a web page you save as PDF in two clicks.

## Install

### Claude Code and the Claude desktop app
```
/plugin marketplace add Aha85/rezumatch
/plugin install rezumatch@rezumatch
```
Then type `/tailor` (or just say "help me fit my resume to this job").

### claude.ai or the Claude app
1. Download `rezumatch-plugin.zip` from [the RezuMatch page](https://www.dannyshaket.com/en/creations/rezumatch).
2. Click Customize on the left, open the Plugins tab, then + Add, Upload plugin, and choose the file.
3. Start a chat: "Help me fit my resume to this job".

On claude.ai the two automatic checks (invented facts, file names) don't run as hooks. Claude still follows the same rules from the skill.

## Commands
- `/tailor [job link]`: the full process, from your resume to files ready to send
- `/score [job link]`: only the estimated score and what's missing

## How it works (11 steps)
1. Language
2. Your resume
3. The job listing
4. How you'll apply
5. Baseline score and the 3 biggest problems
6. What your experience already proves, then questions only about real gaps
7. Structure and draft, for your approval
8. Design
9. Build the PDF and rescore
10. Cover letter or other files
11. Hand-over, with a 3-item checklist

## Privacy
Your files stay in a folder on your computer (Claude Code and the desktop app). Your resume and answers are sent to Claude to do the work, like any message you send Claude. Nothing is sent anywhere else.

## About the score
The score is an estimate built from the listing's keywords, title match, format checks and measurable results. Real ATS products differ, and most leave the decision to a recruiter. Use it to find gaps, not as a promise.

## Troubleshooting
- **"PDF rendering failed" or no PDF:** install Chrome or Edge, or open the HTML file Claude gives you, press Ctrl+P (Cmd+P on Mac) and choose "Save as PDF".
- **The PDF is open and can't be replaced:** close it in your PDF viewer. Claude saves a copy with "(new)" in the meantime.
- **Claude stops and asks about a fact:** that's the anti-invention check. Answer the question, or tell Claude to remove the line.
- **Something else:** [open an issue](https://github.com/Aha85/rezumatch/issues) with what you did and what you saw. Please don't attach your real resume.

## Disclaimer
RezuMatch gives writing and formatting help, not professional career, legal or immigration advice. You are responsible for checking that everything in your resume and letters is true before you send them.

## License
MIT. Made by [Danny Shaket](https://www.dannyshaket.com).
