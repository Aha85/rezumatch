# RezuMatch

A free Claude plugin: a team of expert agents that fits your resume to one specific job listing, so it gets through the first ATS screening.

- **Estimated ATS score** before and after, with the keywords you're missing
- **An expert team, not one prompt:** an ATS specialist, a career consultant, a resume writer, a recruiter, a designer and a senior headhunter, each in its own context, led by a resume optimizer
- **Checked in loops:** every draft is scored and reviewed 2-3 times before you get it
- **One question at a time,** with clear choices
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
2. Click Customize on the left, open the Plugins tab, then + Add, Upload plugin.
3. Drop the zip into "Plugin file" and click Upload.
4. Start a chat: "Help me fit my resume to this job".

On claude.ai chat, hooks and subagents may not run yet (Anthropic: they run in Cowork and Claude Code). Then one Claude plays each expert in turn and still follows the same rules.

## Commands
- `/tailor [job link]`: the full process, from your resume to files ready to send
- `/score [job link]`: only the ATS specialist: estimated score and what's missing
- `/cover-letter [job link]`: only the writer: a cover letter
- `/review [job link]`: the recruiter and the senior headhunter review your resume

## How it works: the team
| Expert | Job |
|---|---|
| Resume optimizer | Runs the team, talks to you, settles disagreements in one line |
| ATS specialist | Analyzes the listing, scores the resume 4 times |
| Career consultant | Finds your proof, interviews you one question at a time |
| Resume writer | Writes the resume and cover letter from your facts only |
| Recruiter | Reads the draft like a hiring manager |
| Designer | One-page PDF, cover letter, Word |
| Senior headhunter | Fresh-eyes final review before you send |

Stages: 1) intake 2) analysis (ATS specialist and career consultant in parallel) 3) your story, one question at a time 4) draft, reviewed 2-3 rounds 5) design and cover letter in parallel 6) final headhunter review, 2-3 rounds, then hand-over.

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
