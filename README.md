# Two-Agent Tech Newsletter Crew

A beginner-friendly CrewAI project where two AI agents work in a line to produce a short tech newsletter. A Researcher searches the web for today's top 3 tech stories, then a Writer turns them into a 5-line newsletter.

## Overview

Yesterday's project used a single agent. This one uses a **crew of two agents** that run **sequentially**, where the second agent depends on the first agent's output.

| Agent | Role | Tools | Job |
|---|---|---|---|
| Researcher | Tech News Researcher | `SerperDevTool` (web search) | Finds today's top 3 tech stories |
| Writer | Newsletter Writer | None | Turns the stories into a 5-line newsletter |

Only the Researcher can search. The Writer has no tools on purpose: a Writer with a search tool would go and research again instead of writing from the notes it was given.

## How it works

1. **Task 1 (find):** The Researcher searches the web and returns exactly 3 stories as a numbered list, each with a headline, one sentence on what happened, and the source name.
2. **Task 2 (write):** The Writer receives that list and writes the newsletter. The hand-off happens through `context=[find]` on the Writer's task. Without it, the second task would start with no knowledge of the first.
3. **Process:** The crew runs with `Process.sequential`, so Task 1 always finishes before Task 2 starts.
4. **Verbose mode:** `verbose=True` on both agents and the crew shows the Researcher searching and the Writer drafting.

## Output format

"5 lines" is defined as a headline plus four lines:

1. Headline: `Tech in 5 lines`
2. One short sentence about story 1
3. One short sentence about story 2
4. One short sentence about story 3
5. `Why it matters:` one sentence tying the stories together

## Example output

```
Tech in 5 lines
1. <Story 1 in one short sentence>
2. <Story 2 in one short sentence>
3. <Story 3 in one short sentence>
Why it matters: <one sentence connecting the stories>
```

The stories change from day to day because the Researcher searches live.

## Tech stack

- Python 3.10 to 3.13
- CrewAI and crewai-tools
- Serper (Google search API) via `SerperDevTool`
- OpenAI API (`openai/gpt-4o-mini`)
- python-dotenv

## Project structure

```
tech-newsletter/
├── news_crew.py    # agents, tasks, crew and run logic
├── .gitignore      # ignores .env, venv/, __pycache__/
└── README.md
```

## Setup

1. Clone the repo and open the folder.
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate        # Windows
   source venv/bin/activate     # macOS / Linux
   ```
3. Install dependencies:
   ```bash
   pip install "crewai[tools]" python-dotenv
   ```
4. Get API keys:
   - OpenAI key from platform.openai.com
   - Serper key from serper.dev (free tier available)
5. Create a `.env` file in the project root:
   ```
   OPENAI_API_KEY=your-openai-key
   MODEL=openai/gpt-4o-mini
   SERPER_API_KEY=your-serper-key
   ```

## Run

```bash
python news_crew.py
```

If CrewAI asks whether to share the execution trace, type `n` and press Enter.

## Troubleshooting

| Problem | Fix |
|---|---|
| `SERPER_API_KEY` not found | Check the `.env` file name and that the key has no quotes or spaces |
| Import error for `crewai_tools` | Run `pip install "crewai[tools]"` inside the activated venv |
| Output is longer than 5 lines | Re-run, or tighten the Writer's `expected_output` |
| Same stories every run | Stories only change when the news changes. Try again on another day |

## Key learnings

- In a sequential crew, the second task does **not** automatically see the first task's output. You hand it over with `context=[...]`.
- A clear, fixed `expected_output` on the first task gives the second agent clean material to work from.
- Giving tools only to the agent that needs them keeps each agent focused on its job.

## Security

API keys are read from environment variables loaded from `.env`. The `.env` file is listed in `.gitignore`, so keys are never hard-coded or committed.