---
title: "Persona Engine"
date: 2025-12-25T00:00:00+05:30
draft: false
---

### 300+ Realistic Shopping Personas at $0 Cost

I have built a retail shopping app to gain hands-on experience in full-stack development. I built and deployed the app and "convinced" 7 friends to sign up for it and play with it. I realized finding users, convincing them to use your app, and get them to play with it for data collection is a hard problem. 
Enter AI. 
I used the hallucinating properties of LLMs (along with temperature control, and prompt engineering techniques) to generate 300+ diverse, believable shopper personas. Since this is just a micro-blog on how I generated personas - stay tuned for the next ones where I actually put these 300+ agents to use/interact with the app and give me copius amounts of data to play with (albeit synthetic) AND more importantly it gives me the much needed experience of playing and building with AI Agents (primarily Langgraph). Stay tuned! 

---
Section 1: The Big Design Questions
Q: How on earth do you generate realistic shopping personas?
A: I evaluated four options: full LLM (too pricey at $50-500/1000), templates (still costly), pure random (unrealistic), and hybrid winner—LLM for archetypes once. 
I tested with free-tier LLMs on OpenRouter. It was Christmas of 2025 and many models were avaialble for free. I leveraged the Minimax M2.1 - recently released open source model (for free) to generate all these personas. I made sure to use LLMs from diverse research labs, and different time releases to even out any biases. 
And ofcouse a detailed prompt to make the API call. 

---
Section 2: What Makes a Persona "Real"?
Q: What exactly defines a shopper's behavior?
A: When I started, I thought just age and income would do. But quickly realized that's like judging a book by its cover.
I ended up with 20+ attributes across five categories:
Demographics: Age, income, location, household size (the basics)
Behavioral traits: The juicy stuff - price sensitivity (0-1 scale), brand loyalty, impulsivity, how tech-savvy they are. This is where personas start feeling like real people.
Shopping preferences: Which categories they care about, their weekly budget, how often they shop.
Temporal patterns: Weekday vs weekend shopper? Morning or evening person?
Coupon behavior: Do they clip coupons obsessively, or barely glance at deals?
Each attribute tells part of the story. Together, they create a 3D picture of someone you could actually meet in a CVS aisle.

---
Section 3: Making It Realistic, Not Random
Q: How do you avoid just randomizing everything and getting unrealistic personas?
A: Randomness alone creates caricatures, not characters. I needed patterns that mirror real life.
For category preferences, I went with demographic-based rules plus an 80/20 power law:
- 18-24 year olds gravitate toward beauty, snacks, electronics
- 35-54 year olds lean toward vitamins, skincare, household items  
- 55+ shoppers prioritize healthcare, wellness
Then I apply the 80/20 rule: 20% of shoppers are category enthusiasts (5+ interests), while 80% have focused preferences (1-3 categories).
This reflects reality - most people know what they like, while a few are browsing everything.
I am hoping that using 20+ attributes, randomizing with context (gender, age etc.) and LLMs bias and hallucinations will get me personas as closers to real-life as possible. 

---
Section 4: The Technical Magic
Q: So how did you actually build this?
A: Three core components:
1. Multi-provider LLM Client: I support OpenRouter, OpenAI, and Claude APIs through a unified interface. If one model hits a rate limit, it automatically falls back to the next model. It's like having backup generators ready to kick in.
2. Sophisticated Prompts: I crafted CVS Health-specific prompts with built-in diversity guidance. For example: "Create a male caregiver (age 30-55) shopping for aging parents, focused on medications and healthcare essentials." These notes rotate through 10 predefined archetypes, ensuring gender balance and variety.
3. Validation Layer: Pydantic models enforce structure, but I added custom validation - age should match age_group, weekly budget should align with income_bracket. The generator catches inconsistencies before they make it into the dataset.
Q: What about when things go wrong?
A: Two key safeguards:
Retry with exponential backoff: If an API call fails, I wait 2 seconds, then 4, then 8, retrying up to 5 times. This handles temporary hiccups gracefully.
Cancel-safe incremental export: I save progress after each batch. If generation gets interrupted at agent273, you can resume from there instead of starting over at agent001.

---
Section 5: The Numbers (Results)
Q: So what's the verdict? How did it perform?
A: Here's what I achieved:
- 300+ personas generated with full 20+ attribute profiles
- $0 total cost using free-tier OpenRouter models (GLM-4.5-Air, minimax-m2.1, NVIDIA Nemotron)
- ~3 seconds per persona average generation time
- Multi-sheet Excel output with Summary, All Attributes, Backstories, Behavioral Profile, and Shopping Patterns sheets
- Zero validation failures - internal consistency built into every persona

---
Section 6: Lessons Learned
Q: What would you do differently next time?
A: Three things stand out:
1. Plan for diversity upfront: Initially I got gender imbalance (more female shoppers). Adding explicit diversity notes fixed this, but planning diversity from day one would have been better.
2. Free tiers have limits: Rate limits on free models forced me to implement retry logic and fallback cascades. Paid models would be faster, but my approach works for 90% of use cases at zero cost.
3. Validation is your friend: Age groups not matching ages. Budgets that don't align with income. These inconsistencies happen more than you'd expect. Investing in validation early saves cleanup time later.

---

These personas are will now drive real simulations, test offer optimization, and shape customer experience decisions. 
The engine continues to generate, scale, and adapt - proving that thoughtful design and free-tier models can create enterprise-quality datasets.
