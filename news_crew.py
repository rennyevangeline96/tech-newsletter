from dotenv import load_dotenv
load_dotenv()

from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool

search = SerperDevTool()

# Agent 1: can search the web
researcher = Agent(
    role="Tech News Researcher",
    goal="Find today's three most important and recent technology news stories",
    backstory=(
        "You are a sharp tech journalist who tracks the industry daily. "
        "You only trust recent, credible sources and always note what happened "
        "and why it matters, so an editor can work from your notes directly."
    ),
    tools=[search],
    verbose=True,
)

# Agent 2: no tools, only writes
writer = Agent(
    role="Newsletter Writer",
    goal="Turn research notes into a short, punchy 5-line tech newsletter",
    backstory=(
        "You are a newsletter editor who writes for busy professionals. "
        "You never invent facts. You only use the notes you are given, "
        "and you make every line clear and quick to read."
    ),
    verbose=True,
)

# Task 1: research
find = Task(
    description=(
        "Search the web for today's top 3 technology news stories. "
        "Pick stories that are recent and from credible sources."
    ),
    expected_output=(
        "Exactly 3 stories as a numbered list. For each story give: "
        "a headline, one sentence on what happened, and the source name. "
        "No extra commentary."
    ),
    agent=researcher,
)

# Task 2: write (context hands over the researcher's output)
write = Task(
    description=(
        "Using only the 3 stories from the research, write a newsletter "
        "called 'Tech in 5 lines'."
    ),
    expected_output=(
        "Exactly 5 lines, nothing more. Line 1 is the headline: 'Tech in 5 lines'. "
        "Lines 2, 3 and 4 are one short sentence each, one per story. "
        "Line 5 starts with 'Why it matters:' and gives one sentence tying the stories together."
    ),
    agent=writer,
    context=[find],
)

crew = Crew(
    agents=[researcher, writer],
    tasks=[find, write],
    process=Process.sequential,
    verbose=True,
)

print(crew.kickoff())