---
name: score
description: "Get an estimated ATS match score for your resume against a job listing, without rewriting it"
argument-hint: "[optional: job listing link]"
disable-model-invocation: true
---

Run only the ATS specialist (the ats-specialist skill, or its agent). Get the resume and the job listing ($ARGUMENTS if given), one question per message. Show the score table, the missing keywords and the 3 biggest problems. Then ask one question: do they want the full RezuMatch team to tailor the resume?
