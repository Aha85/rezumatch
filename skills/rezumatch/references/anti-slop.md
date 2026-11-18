# Anti-slop: resumes and letters that sound like a person wrote them

Recruiters now spot AI text in seconds, and many reject it on sight. Every resume line, summary, cover letter, email and "why us" answer passes this check. Hebrew gets the same rules, plus its own list below, because translated-sounding Hebrew is the most common giveaway.

`scripts/slop_check.py` catches the mechanical patterns and blocks the build. It can't judge meaning, so the writer and the senior headhunter also read every line against the three tests.

## Three tests for every line
1. **Could someone disagree?** "Passionate about delivering value" can't be disagreed with, so it says nothing. Replace it with a claim or a fact.
2. **Would a person say it out loud,** to a recruiter on the phone, in these words? If not, it's translated or templated.
3. **Is there a name, a number or a specific moment?** If the line could sit in anyone's resume, rewrite or cut it.

## Patterns (English)
1. **X-versus-Y punchlines:** "Not just a manager, a leader." "Not a tool demo. A strategy." "It's not about X, it's about Y."
2. **Aphorisms:** "Data tells a story." "People are the product."
3. **Perfect triplets:** "strategic, hands-on and results-driven", "Plan. Build. Scale." Real people list two things, or four, or one.
4. **Stock AI words:** leverage, spearhead, synergy, cutting-edge, passionate, dynamic, results-driven, seamless, robust, delve, tapestry, testament, transformative, innovative, visionary, holistic, empower, elevate, foster, navigate (figurative), landscape, journey, realm, unlock, harness, game-changer, thrive, proven track record, go-getter, wear many hats, think outside the box.
5. **Empty openers and closers:** "I am writing to express my interest", "I am excited to apply", "I believe I would be a great fit", "Thank you for considering my application" as the whole close.
6. **Em dashes and en dashes in sentences.** Use a comma, a period or a colon. (A dash between years, "2021 - 2024", is fine.)
7. **Inflated scope:** "transformed", "revolutionized", "world-class" with nothing measured behind it.
8. **Nobody's there:** no names, no numbers, no moments. Generic enough to fit any candidate.

## דפוסים בעברית
1. **ניגוד מוכן מראש:** "לא רק מנהלת, מובילה", "זה לא עניין של X, זה עניין של Y".
2. **עברית מתורגמת:** "לייצר ערך", "להניע תהליכים", "ליצור תוצרים", "בעל יכולת הובלה מוכחת", "מוכוון תוצאות", "עם דגש על", "ברמה הגבוהה ביותר", "לקחת חלק פעיל ב...", "אחראי על הנעת". אף ישראלי לא אומר את זה בטלפון למגייסת.
3. **מילות באזז:** "חדשני", "פורץ דרך", "סינרגיה", "תשוקה", "יוצא דופן", "ראש גדול", "ראייה רחבה", "יכולות בין-אישיות מעולות", "יכולת למידה עצמית גבוהה", "מוטיבציה גבוהה", "עבודה בסביבה דינמית", "חשיבה מחוץ לקופסה", "שחקן/ית צוות".
4. **שלשות מושלמות:** "יצירתי, יסודי ומחויב", "לתכנן, לבנות, להצמיח".
5. **פתיחה וסגירה ריקות:** "ברצוני להגיש מועמדות", "אשמח להזדמנות להוכיח את עצמי", "אודה על התייחסותכם".
6. **מקפים ארוכים באמצע משפט.** פסיק, נקודה או נקודתיים. (מקף בין שנים, "2021 - 2024", בסדר.)
7. **לשון זכר כברירת מחדל כשהמועמדת אישה,** או "בעל/ת" בקורות חיים של אדם אחד. כותבים בלשון של המועמד/ת עצמו/ה.

## How to fix
- Replace the adjective with the fact that earned it: "results-driven" → "raised retention from 86% to 93%".
- Replace the punchline with the plain claim: "Not just support, partnership" → "Ran quarterly reviews with the managers of 15 accounts".
- Cut a line that has nothing behind it. Shorter beats padded.
- Keep the user's own words, even plain ones. Flag only real slop in their text, and suggest; never force.
- Never invent a moment, name or number to make a line concrete. Ask the user.
