+++
title = "Rethinking my AI Coding Workflow"
date = 2026-01-07T00:00:00-05:00
draft = false
tags = ["essay"]
+++

## Why Git Worktrees may not be as useful as I initially thought when it comes to coding with AI agents. 

My previous/current AI workflow :
- Start local project
- Enable git (git init)
- Build a simple working version and test it in main branch (mostly with Anthropic's Claude Code tool)
- For advanced features, I would create n number of worktrees (n = number of coding agents)
- Get each of the AI coding agents to work on a feature/functionality of the project independently (e.g. Claude Code, Opencode coding agent with GLM 4.7 model, Gemini GLI from Google)
- Test each worktree locally independently and whichever is the best implementation - merge that one to main.

I am quitting this workflow now. Because managing multiple agents is a lot of work. Especially during the planning phase and when debugging. 
I use the `AskUserQuestion` tool on Claude Code - this tool triggers an interview where Claude Code asks me 15-25 questions about the new feature. 
Reading those, thinking about them, and answering/choosing the right option is satisfying but exhaustive.
Other coding tools will also adopt this feature (check my last post about my ai_workflow) soon and I'll end up duplicating the same process over and over. 
No thank you! 
Also
Getting each of the coding tools (and their LLMs) to do the same thing burns through tokens like Confettu at New Year's Eve on NYC Times Square.
And not all LLMs or agents are good at every step of the process - each of them shine while doing different things (Claude Opus 4.5 shines with planning,  Gemini 3 Pro on UI/UX, GLM 4.7 on general Python)- much like us mortal humans.


New workflow :
- Maintain a directory that is agnostic of the coding tool or LLM being used.
- This is slightly difficult to get every LLM to obey - so it will need system prompting each of my favorite LLMs individually to obey this above directory.
- Planning and ToDos : Anthropic's Claude Opus 4.5 Model used via <Claude Code>
  - ToDos : Separate into frontend (F1, F2, ..), Backend (B1, B2, ..), and Database (DB1, DB2, ..)
- Z_ai's GLM 4.7 via <opencode> to work on Backend tasks.
- Google Gemini 2.5 pro via <cursor> to work on Frontend tasks.
- OpenAi's ChatGPT 5 via <kilocode> to work on DB tasks (being extra careful here - I have a set of rules while working with DB which I'll write about some other time)
- Claude Sonnet 4.5 via <Claude Code> to write tests and get feedback on connecting all 3 pieces.

This is mostly conceptual for now. I may even discard this new approach after building more products and learning something even better. 
We live in exciting times. The possibilities are endless. So why should our workflows be? 
 
