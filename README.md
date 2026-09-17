# SAP Error Codex

A searchable reference of **SAP Fiori / UI5, ABAP extensibility, transport and integration** deployment errors — indexed by **message ID**, not by title.

When you hit an error, what you actually have in front of you is `/UI2/UI5_REP_LOAD-039` or `HTTP 403`, not a sentence describing it. This reference is indexed on that.

**Browse:** https://stormshynn.github.io/sap-error-codex/

---

## What's in it

| Area | Entries |
|---|---|
| SAP Fiori / UI5 | 12 |
| Basis / Auth | 5 |
| Transport & Release | 2 |
| Integration / OData | 2 |
| ABAP / Extensibility | 1 |
| **Total** | **22** |

A few representative entries:

- `ladi-package-conflict` — *SAPUI5 application can only be deployed to the previous package*. The conflict is on the LADI, not the package; changing `package` in the yaml does nothing.
- `http-403-repository-srv` — 403 because `/UI5/ABAP_REPOSITORY_SRV` is not activated, which looks exactly like an authorization failure but isn't.
- `testmode-pass-deploy-fail` — why `--testMode` reports success and the real deploy still fails.
- `unknown-file-type-upload` — files silently skipped at upload (`.Ui5RepositoryTextFiles`).
- `self-signed-cert-deploy` — `unable to get local issuer certificate`.

---

## The `verified` flag

Every entry carries a `verified` field:

| Value | Meaning |
|---|---|
| `true` | The fix was executed on a real system and it worked. Someone watched it happen. |
| `false` | Written from documentation, blog posts, or general experience — **check it before you apply it** |

**4 of 22** entries are currently `true`. That number matters more than the total: a reference with 200 entries of unknown reliability is useless at the moment you actually need it.

Individual fixes say so too — each `body` opens with "Verified" or "Not verified".

---

## How the data is organised

The source of truth is `issues/` — one JSON file per error. `data/issues.json` is a generated bundle used by the web page.

```
issues/<id>.json     <- edit here
data/issues.json     <- generated, do not hand-edit
index.html           <- static reference page
scripts/build.py     <- merges issues/ into data/issues.json, validates schema
```

### Entry schema

```json
{
  "title": "Short line naming what the person actually sees",
  "module": "SAP Fiori / UI5",
  "severity": "Blocker | High | Medium | Low",
  "status": "Open | Investigating | Resolved",
  "verified": false,
  "msgKeys": ["/UI2/UI5_REP_LOAD-039", "HTTP 400"],
  "symptom": "The log line that decides it, verbatim. That is what the next person searches for.",
  "rootCause": "Why it happens. If you are not sure, say 'Not verified' and give the possibilities.",
  "solutions": [
    { "label": "Name of the fix", "body": "Concrete steps", "recommended": true }
  ],
  "prevention": "What to change so this does not recur",
  "refs": ["SAP Note 1797736", "https://..."],
  "createdAt": "2026-09-17T10:00:00.000Z",
  "updatedAt": "2026-09-17T10:00:00.000Z"
}
```

`module` must be one of: `SAP Fiori / UI5`, `ABAP / Extensibility`, `Transport & Release`, `Integration / OData`, `Power BI`, `Microsoft Fabric`, `Basis / Auth`.

---

## Running it locally

```bash
python3 scripts/build.py     # merge issues/ -> data/issues.json
python3 -m http.server 8000  # open http://localhost:8000
```

Opening `index.html` straight from disk over `file://` will not work — browsers block `fetch` on that scheme.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Three routes, lightest first:

1. **Open an issue** — use a template, no git needed
2. **Send a pull request** — add or edit a file in `issues/`, run `scripts/build.py`, commit both
3. **Flip a `verified` flag** — when you have run a fix and it worked, set `verified` to `true` and update `updatedAt`

The most valuable contribution is not a new entry. It is verifying one that already exists.

---

## Known limits

- Most official SAP documentation (help.sap.com, launchpad.support.sap.com) blocks automated access, so this content is assembled from real deployment logs, SAP's own open samples repositories, and SAP Community threads. Always check the original SAP Note before applying anything to production.
- The Power BI and Microsoft Fabric areas are empty so far. The schema is ready for them.
- No system-specific information is stored here: no hostnames, tenant IDs, usernames, or real transport numbers. Keep it that way when contributing.

---

## Licence

MIT — see [LICENSE](LICENSE).
