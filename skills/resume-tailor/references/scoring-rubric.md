# Scoring rubric (estimated match, 0-100)

Always call it an estimated score. Real ATS products rank differently and most leave the decision to a recruiter.

| Part | Points | Measured by |
|---|---|---|
| Keywords from the listing | 40 | ats_score.py, from work/jd_keywords.json |
| Job title alignment | 15 | ats_score.py (exact title 15, partial by words) |
| Experience and seniority | 15 | Claude's judgment, work/judgment.json |
| Soft skills | 10 | Claude's judgment, work/judgment.json |
| Format and parseability | 15 | ats_score.py format checks |
| Measurable results | 5 | ats_score.py (share of lines with numbers) |

## Writing work/jd_keywords.json
- 15-30 terms from the listing: tools, methods, domain words, responsibilities.
- weight 2: in the requirements, or repeated. weight 1: mentioned once.
- aliases: other forms of the same thing ("APIs" / "API", "JavaScript" / "JS").
- title: the exact job title from the listing.

## Writing work/judgment.json
- experience (0-15): years and scope versus the level the listing asks for. Director-level scope without the title still counts.
- soft (0-10): evidence of the listed soft skills (communication, ownership, problem solving) in real examples.
- Be honest and consistent: don't raise judgment parts to make the number look good.

## Showing the score
- A small table: part, before, after.
- After every later change, rerun and explain small moves in one line ("+1: 'prompts' is back in the MBA line").
- Above ~85 is a very strong match. Say what still holds it back, and which gaps are not closable without inventing.
