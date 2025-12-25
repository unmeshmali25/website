---
title: "Persona Engine"
date: 2025-12-25T00:00:00+05:30
draft: false
---

**Title:** 300+ Realistic Shopping Personas at $0 Cost

I needed realistic personas for a CVS Health retail simulation. The challenge? Generate diverse, believable shoppers at scale without breaking the bank.

---
Section 1: The Big Design Questions
Q: How on earth do you generate realistic shopping personas?
A: Great question. I explored four approaches: full LLM generation, template + LLM variation, pure randomization, and a hybrid approach. 
Here's what I found:
- Full LLM: Most realistic but would cost $50-500 for 1000 agents (yikes!)
- Template + variation: Good structure but still expensive
- Pure randomization: Free but feels fake
- My choice: Hybrid approach - Use LLM once to generate diverse archetypes, then randomly vary parameters for each agent
This gave me the best of both worlds: rich, believable personalities without the recurring cost.

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
