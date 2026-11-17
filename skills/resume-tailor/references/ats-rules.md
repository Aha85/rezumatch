# ATS rules (what makes a resume readable by applicant tracking systems)

An ATS (applicant tracking system: Workday, Greenhouse, Lever, iCIMS, SuccessFactors, Taleo and others) parses the file into fields, then recruiters search and filter. Most do not auto-reject on a score; a recruiter decides. The goal is: parse cleanly, contain the listing's language, and read well in a 6-10 second human scan.

Avoid the myth "75% of resumes are rejected by ATS". There is no solid source for it. Don't quote it to users.

## Layout
- One column. Sidebars and two-column designs get read in the wrong order or lose the sidebar.
- No tables, text boxes, columns made of tabs, or text inside images/graphics.
- Contact details in the body, not in the page header/footer (some parsers skip them).
- Standard section headings: Summary, Skills, Experience, Projects, Education (Hebrew: תקציר, כישורים, ניסיון תעסוקתי, פרויקטים, השכלה).
- Icons are fine when the text sits next to them (the parser reads the text, ignores the icon). A link hidden behind an icon only is lost.

## File
- PDF made from text (selectable), not a scan. Check with extract_resume.py: the text must come back in order.
- Some portals prefer DOCX. Offer the DOCX only when the portal asks for it.
- Fonts: Chrome embeds web fonts and variable fonts as Type3. Text still extracts, but installed fonts (Arial, Helvetica, Calibri) are the safest. If a design-system web font is used, confirm the extracted text is clean.
- File name: "<Full Name> Resume.pdf". Nothing else in the name.

## Content
- Job titles as they were. Dates as years: "2021 - 2023". Current role: "2025 - Present" (Hebrew: "2025 - היום").
- Keywords: the listing's exact terms (both "Artificial Intelligence" and "AI" if the listing uses both), each used where it is true. No keyword lists in white text, no stuffing: recruiters see it and some ATS flag it.
- Skills section: up to ~10 items, the listing's terms that the user really has.
- Length: 1 page by default; 2 pages only for long, relevant careers and only after the user agrees.
- Every bullet: action + what + result. Numbers wherever they exist.

## Checks the scripts run
- extract_resume.py: pages, multi-column (vertical gutter), real tables, extractable text.
- ats_score.py: keywords, title, format checks, measurable results.
- fit_page.py: fills the target page count at 9.5pt-11.5pt.
