# Contributing

## First rule: don't guess

If you are not sure about the cause, write down the part you know and mark the part you are guessing:

> Not verified. Possibly: ...

An entry that draws a clear line between what is known and what is assumed is far more useful than one that sounds confident and is wrong. The person reading it is usually mid-incident and will act on it immediately.

## Keep real system details out

No hostnames, tenant IDs, usernames, real transport numbers. Never paste a log containing a token or session cookie.

Use placeholders instead:

```
https://<host>/sap/bc/ui5_ui5/sap/<appname>/index.html
Transport Request "<TRANSPORT>" has been determined ...
```

## Route 1 — Open an issue (no git required)

Issues tab → New issue → pick a template. Fill in what you have; a maintainer will turn it into a JSON entry.

Paste the **decisive log line verbatim**. That is the most valuable part — don't paraphrase it.

## Route 2 — Pull request

```bash
git checkout -b add-<short-description>
# create or edit issues/<id>.json
python3 scripts/build.py
git add issues/ data/issues.json
git commit -m "Add: <error title>"
git push origin add-<short-description>
```

Naming the `id` (the filename): lowercase, hyphenated, describing the symptom rather than the app it happened to.

- Good: `http-403-repository-srv`, `ladi-package-conflict`, `transport-not-modifiable`
- Bad: `zqm04-bug`, `issue-2`, `september-error`

## Route 3 — Verify an existing entry

This is the most valuable contribution in the repository.

When you have run a documented fix and it worked:

1. Change `"verified": false` to `true`
2. In the relevant `solutions[].body`, change "Not verified" to "Verified: \<date\>, \<environment\>"
3. Update `updatedAt`
4. Run `python3 scripts/build.py` and commit both files

If the fix did **not** work, that is worth just as much: record in the `body` what conditions made it fail.

## Writing each field

**`symptom`** — the decisive log line, not the whole log. For Fiori deployment failures the decisive line is almost always right after `* Updating the Application Index *` or inside the `* Operations *` block.

**`solutions`** — ordered by what to try first. Exactly one carries `recommended: true`. Every `body` needs a concrete command or transaction path; "check the configuration" helps nobody.

State the cost too: downtime, authorizations required, who else has to be involved.

**`prevention`** — what is worth changing in the process so this does not come back. If nothing comes to mind, leave it empty rather than padding it.

**`refs`** — SAP Notes, KBAs, documentation links, transaction codes. Full URLs are rendered as links on the web page.

## Review

A maintainer checks: no real system details, the `verified` flag matches the evidence given, `module` and `severity` are valid, and `data/issues.json` was rebuilt.
