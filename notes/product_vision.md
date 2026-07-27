
# Product Vision

## First Usable Website Milestone

The first useful Poolside website milestone is a simple pool care log.

The home page should become the working screen for one pool. It should let a user record the latest maintenance check and see what needs attention next.

## Core Workflow

1. Open the home page.
2. Enter today's pool readings and maintenance notes.
3. Mark routine tasks complete.
4. See the latest saved check at the top of the page.

## Minimum Data Model

Start with browser-local data for one pool:

- Check date.
- Free chlorine.
- pH.
- Water temperature.
- Filter pressure.
- Tasks completed.
- Notes.

Keep the first version local and plain. Do not add accounts, multiple pools, cloud sync, photos, chemical dosing recommendations, or external integrations yet.

## Website vs Notes Boundary

Website:

- Current pool care entries.
- Simple task completion state.
- The latest operational snapshot.

Obsidian notes:

- Project decisions.
- Architecture notes.
- Backlog history.
- Workflow lessons.

The website should not become the project notebook. The notes vault should not become the operational pool log.
