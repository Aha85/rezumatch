---
name: role
description: "Build one resume for a target role, from a few job listings or a description of the role you want"
argument-hint: "[optional: the role, e.g. Customer Success Manager in B2B SaaS]"
disable-model-invocation: true
---

Use the rezumatch skill as the resume optimizer, in role mode. If the user named a role here ($ARGUMENTS), use it as the description and skip that question; otherwise ask whether they have a few listings or want to describe the role. Then run the stages in order, one question per message.
