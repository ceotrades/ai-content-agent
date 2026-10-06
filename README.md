# Content Control Room

A three-agent system that runs the content for a TikTok account, and the dashboard the agents report into. This repo is a frozen snapshot of the live version, safe to look at.

## The problem

Producing short-form content every day is the part that kills most accounts. The research is slow, the scripting is slow, and nobody goes back afterwards to work out which posts did anything. I had run a trading community before where this exact problem was the thing I could never keep on top of.

## What it does

Three agents, each with one job.

**Research** finds outliers. It pulls videos that have beaten their creator's own baseline by a wide margin, scores them, and works out what the pattern behind them was. The snapshot holds 17 outliers, 8 patterns and 25 creator baselines.

**Scripting** drafts from those patterns. Hooks, full scripts, and the variables worth testing between versions.

**Performance** grades what went out. Every post is measured against a 1,278-view baseline on a log scale, then graded, and the grade feeds back into what gets researched next.

The dashboard sits on top: 18 ranked ideas with the research behind each one, 67 posts tracked, 12 written learnings, and a library holding every system document the agents run on.

## What's in this repo

A read-only snapshot. The live version has database subscriptions and AI drafting tools in it; here the data is inlined, the write buttons are intercepted and the drafting is switched off. One HTML file, no build step, no backend.

## Stack

Single-file HTML, Python build script, Vercel.

## Status

The live system runs the account. This copy is the showcase version and does not update.
