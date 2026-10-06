# @ceotalks23 Control Room — showcase snapshot

A frozen, read-only copy of the live control room that runs the three-agent content system behind
[@ceotalks23](https://www.tiktok.com/@ceotalks23). One file, no build step, no backend.

Live copy (private, Dhruv only): https://claude.ai/code/artifact/b2daa595-7e01-4415-8e67-7aa7310e2603

## What it shows

| Section | What's in it |
|---|---|
| Overview | Follower goal, catch-up rate, the three agent monitors, what needs a decision, latest weekly report |
| Agents | Each agent's job, live status protocol, run history |
| Ideas | 18 ideas ranked by opportunity score, with the full research behind each one |
| Scripts | Drafted scripts, hooks, test variables |
| Research | 17 outliers with their outlier scores, 8 content patterns, 25 creator baselines |
| Performance | 67 posts, log-scale chart against the 1,278-view baseline, grades |
| Learnings | 12 learnings, winning and losing patterns, open hypotheses |
| Library | Every system document (context, agent instructions, templates) |

Data in this snapshot was exported on the date shown in the banner. Nothing updates: the database
subscriptions are replaced by an inline copy of the data, write buttons are intercepted, and the
AI drafting tools (script generation, hook lab, screenshot reading) are switched off.

## Deploy

**Vercel, from the dashboard**
1. Push this folder to a GitHub repo.
2. vercel.com → Add New → Project → import the repo.
3. Framework preset: **Other**. Build command: leave empty. Output directory: leave empty (root).
4. Deploy. It serves `index.html` as the root.

**Vercel, from the CLI**
```bash
npm i -g vercel
cd ceotalks23-control-room
vercel          # preview
vercel --prod   # production
```

**Netlify** works the same way: drag the folder onto app.netlify.com/drop, or connect the repo with
no build command and `.` as the publish directory.

**Custom domain:** Vercel → project → Settings → Domains → add the domain, then point the DNS record
Vercel gives you at your registrar.

## Refreshing the snapshot

The data is inlined, so a refresh means rebuilding the file. In a Cowork session:

> Rebuild the control room showcase snapshot from the live database and give me the new index.html.

That re-exports every collection, rebuilds `index.html` and hands it back. Commit it, and Vercel
redeploys on push.

## Files

```
index.html    the whole thing: dashboard, inlined data, read-only shim
vercel.json   headers and clean URLs
README.md     this file
```

## How the read-only shim works

The live dashboard calls `claude.use("db")` for a realtime document store and `claude.use("sample")`
for the AI calls. In this snapshot `claude.use` returns a stub for `db` that reads from an inlined
`window.__D` object and silently swallows writes, and `null` for everything else, which the
dashboard already handles (it was written to degrade when a capability is missing). A capture-phase
click listener blocks any action that would write, and shows a notice instead. Read-only actions —
opening a record, filtering, sorting, switching tabs, copying a script — all still work.
