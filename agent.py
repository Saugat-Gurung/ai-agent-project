import os
import sys
from pathlib import Path
import datetime

from dotenv import load_dotenv
from google.adk.agents import Agent, LoopAgent
from google.adk.tools import agent_tool

# 1. Configuration
# This explicitly loads the GOOGLE_API_KEY from your .env file
load_dotenv() 

model_name = os.getenv("MODEL_NAME", "gemini-flash-latest")

# 2. Phase 1: The Planner Sub-System
blog_planner = Agent(
    name="blog_planner",
    model=model_name,
    description="Takes a topic and turns it into a structured outline.",
    instruction="""Create a markdown outline with:
    1. A title
    2. A short introduction
    3. 4 to 6 sections with bullet points
    4. A conclusion.""",
    output_key="blog_outline" 
)

print("Phase 1: Blog Planner successfully initialized.")

# ---------------------------------------------------------
# Phase 2: The Planner's Safety Net
# ---------------------------------------------------------

# 1. The Planner's Validation Checker Class
class OutlineValidationChecker(Agent):
    def __init__(self):
        super().__init__(
            name="OutlineValidationChecker",
            model=model_name,
            description="Validates that the outline is usable.",
            instruction="""
            Check the outline in state `blog_outline`. If it has a title, intro, 
            4-6 sections, and a conclusion, respond exactly "ok". 
            Otherwise respond exactly "retry" and list missing pieces.
            """,
            output_key="validation_result",
        )

# 2. The Robust Planner Loop
robust_blog_planner = LoopAgent(
    name="RobustBlogPlanner",
    description="Retries planning if validation fails.",
    sub_agents=[blog_planner, OutlineValidationChecker()],
    max_iterations=3,
)

print("Phase 2: Validation Checker Class and Loop Agent initialized.")

# ---------------------------------------------------------
# Phase 3: The Writer Sub-System
# ---------------------------------------------------------

# 1. The Writer Sub-Agent
blog_writer = Agent(
    name="BlogWriter",
    model=model_name,
    description="Writes a technical blog post from the outline.",
    instruction="""
    Write a complete Markdown article from the outline in `blog_outline`.

    Guidelines:
    - Audience: software engineers; skip basics and focus on practical insight.
    - Explain both the 'how' and 'why'.
    - Include concise code snippets when helpful.
    - Follow the outline's structure (H2/H3).
    - Output only the final article in Markdown (no fence around the whole post).
    """,
    output_key="blog_post",
)

# 2. The Writer's Validation Checker Class
class BlogPostValidationChecker(Agent):
    def __init__(self):
        super().__init__(
            name="BlogPostValidationChecker",
            model=model_name,
            description="Validates the final post.",
            instruction="""
            Check `blog_post` for: intro, clear sections matching the outline, conclusion, and technical clarity.
            If passes, respond "ok". Else respond "retry" with the specific fixes.
            """,
            output_key="validation_result",
        )

# 3. The Robust Writer Loop
robust_blog_writer = LoopAgent(
    name="RobustBlogWriter",
    description="Retries writing if validation fails.",
    sub_agents=[blog_writer, BlogPostValidationChecker()],
    max_iterations=3,
)

print("Phase 3: Blog Writer and Validation Loop initialized.")

# ---------------------------------------------------------
# Phase 4: The Master Controller (Root Agent)
# ---------------------------------------------------------

# 1. Expose planner and writer loops as tools
planner_tool = agent_tool.AgentTool(agent=blog_planner)
writer_tool = agent_tool.AgentTool(agent=blog_writer)

# 2. The Root Agent
root_agent = Agent(
    name="Blogger",
    model=model_name,
    description="Minimal multi-agent blogger that plans and writes.",
    instruction=f"""
    If the user gives a topic:
    1) Call the planner tool to generate the outline.
    2) Call the writer tool to produce the full draft.
    3) End with 3 alternate titles and 2 tweet-length hooks.

    Date: {datetime.datetime.now().strftime("%Y-%m-%d")}
    """,
    tools=[
        planner_tool, # calls RobustBlogPlanner
        writer_tool,  # calls RobustBlogWriter
    ],
)

print("Phase 4: Root Agent initialized! The system is complete.")