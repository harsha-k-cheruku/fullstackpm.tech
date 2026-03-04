---
title: "What Is an AI Agent, Really?"
date: 2026-02-28
tags: [ai, product-management, ai-native-pm, agents, building-in-public]
excerpt: "Everyone's building 'AI agents.' Most of them are just prompts with a loop. Here's what actually makes something an agent — and a walkthrough of how a prompt graduates into one."
author: "Harsha Cheruku"
---

The word "agent" is everywhere. Every AI startup has one. Every dev tool is shipping one. Every LinkedIn post is about building one.

But most things called "agents" aren't agents. They're prompts. Or scripts. Or automations with an AI step bolted on.

So what actually makes something an agent?

The answer is older than AI. And once you see it, you can't unsee it.

---

## The Word Itself

"Agent" comes from Latin *agere* — **to act.**

A real estate agent acts on your behalf to sell your house. A travel agent acts on your behalf to book your trip. You don't tell the real estate agent which words to say in every conversation. You say "sell my house for at least $500K" and they figure out the steps.

That's the core idea: **you delegate a goal, and the agent figures out how to achieve it.**

A tool does what you tell it. An agent does what you *need* — and decides the steps itself.

---

## The Spectrum: Tool → Instruction Set → Agent

These aren't three separate categories. They're a spectrum of increasing autonomy.

### Tool: Zero autonomy

A calculator. You press buttons, it computes. A SQL query. You write it, the database returns results. `git push`. You say push, it pushes.

You decide what to do. It executes exactly that.

### Instruction Set: Guided autonomy

A recipe. The cook follows steps in order. A deployment checklist. The engineer runs through it item by item. A structured prompt. The LLM follows the defined process.

You define the process. It follows the steps. It can make small decisions within each step — how to phrase something, which example to pick — but the overall flow is predetermined.

**Key property:** you could hand this to a different LLM (or a human) and get roughly the same process. The intelligence is in the document, not the executor.

### Agent: Real autonomy

A senior employee. You say "increase retention by 10%." They decide: analyze churn data, identify levers, run experiments, report back. If the data is inconclusive, they dig deeper. If one approach fails, they try another.

You define the goal. It figures out the steps.

---

## What Makes an Agent an Agent?

Four properties. Without all four, you have something less than an agent — which is often fine, but call it what it is.

### 1. Goal-directed (not step-directed)

An instruction set says: "Do step 1, then step 2, then step 3."

An agent says: "Achieve this outcome. Figure out how."

The agent might do steps 1, 2, 3. Or it might skip step 2 because it's not needed. Or it might do step 4 that nobody anticipated. The goal is fixed. The path is flexible.

**Test:** If you removed the step-by-step instructions and just gave it the goal, could it still get there?

### 2. Autonomous decision-making

An instruction set follows a predetermined flow. An agent makes decisions during execution:

- "This search returned nothing. Let me try a different query."
- "The user's answer is ambiguous. Let me ask a follow-up."
- "This approach isn't working. Let me try an alternative."

**Test:** Does it adapt its behavior based on what it encounters?

### 3. Tool use

An agent can interact with the outside world — not just think, but *act*:

- Read files, search the web, call APIs
- Write code, execute commands
- Send messages, create documents

An instruction set might *describe* using tools. An agent actually *decides when and which* tools to use based on what it needs.

**Test:** Does it choose which tools to use and when?

### 4. Feedback loops

An agent observes the results of its actions and adjusts:

- "I ran the tests. 3 failed. Let me read the errors and fix the code."
- "The API returned a 404. The endpoint might have changed. Let me check the docs."
- "My first draft was rejected. Let me revise based on the feedback."

This is the **sense → think → act → sense** loop. It doesn't just act once and stop. It acts, observes, and acts again.

**Test:** Does it adjust its approach based on the results of its own actions?

---

## A Walkthrough: From Prompt to Agent

Let's make this concrete. Say you want to build something that researches a product's technical architecture for a blog post.

### Level 1: A Prompt (Tool)

```
"Tell me how Google Maps calculates ETA."
```

You ask. It answers. One shot. If the answer is wrong or incomplete, you ask again manually. The intelligence is in your question.

### Level 2: An Instruction Set

```
You are a Product Researcher. Follow these steps:

Step 1: Clarify the scope (which product, which feature)
Step 2: Map the user-visible flow (what the user sees)
Step 3: Break down the technical architecture (what's behind the scenes)
Step 4: Identify the D/P chain (which steps are deterministic, which probabilistic)
Step 5: Surface the PM decisions (what trade-offs did they make)
Step 6: Compile the research output
```

Now there's structure. The LLM follows steps 1 through 6 in order. The output is consistent. But if step 3 hits a dead end — say there's no public information about the architecture — it doesn't adapt. It just does its best within step 3 and moves on.

The process is smarter. The executor is still a follower.

### Level 3: An Agent

```
Goal: Produce a deep technical + product breakdown of Google Maps ETA prediction.

Tools available: web search, read URLs, file read/write

Constraints: Ground everything in public sources. Flag inferences.
```

Now it's different. The agent:

1. **Decides** to start by searching for Google engineering blog posts about Maps
2. **Finds** a 2019 DeepMind paper on traffic prediction → reads it
3. **Decides** that's not enough on the routing side → searches for "Google Maps routing architecture"
4. **Finds** a GCP blog post about graph optimization → reads it
5. **Realizes** there's a gap in how ETA confidence intervals are displayed → searches specifically for that
6. **Comes up empty** on confidence intervals → flags it as "likely hidden from users, inference based on UX patterns"
7. **Synthesizes** everything into the breakdown format
8. **Reviews** its own output → notices it missed the real-time update mechanism → goes back and researches that
9. **Produces** the final output

Same goal as the instruction set. Completely different path. The agent encountered dead ends, changed strategy, went back to fill gaps, and reviewed its own work. No one told it to do steps 1-9 — it figured out the sequence based on what it found.

**The difference in one line:** The instruction set follows a script. The agent pursues a goal.

---

## Why Most "Agents" Aren't Agents

Here's an honest assessment of what people are actually building:

| What they call it | What it actually is | Why |
|---|---|---|
| "AI agent that writes emails" | Prompt with a template | No tool use, no feedback loops, no adaptation |
| "Customer support agent" | Instruction set with branching | Follows decision tree, doesn't pursue goals |
| "Coding agent" (Copilot) | Tool with suggestions | You decide what to accept, it doesn't pursue goals |
| "Coding agent" (Claude Code, Devin) | Closer to real agent | Goal-directed, uses tools, has feedback loops |
| "Research agent" | Depends | If it just summarizes search results = tool. If it iterates based on findings = agent |

The label doesn't matter. The properties do. Goal-directed? Autonomous decisions? Tool use? Feedback loops? Count the properties and you know what you're dealing with.

---

## The Graduation Path

You don't build an agent on day one. You graduate toward one:

```
Instruction Set (static process)
    + Tool Access         → Can interact with the world
    + Decision Logic      → Can choose what to do next
    + Memory              → Can remember across interactions
    + Feedback Loops      → Can observe results and adapt
    = Agent (dynamic, goal-directed system)
```

Each addition is independent. You can add tools without memory. You can add decision logic without feedback loops. But a true agent has all four properties working together.

**Start with an instruction set.** Get the process right. Make the output consistent. Then ask: "Where does this break down because it can't adapt?" That's where you add the next layer of autonomy.

This is how I'm building my own [7-agent SDLC chain](https://fullstackpm.tech) — starting as structured instruction sets, graduating to true agents as each one proves its process works.

---

## The Honest State of AI Agents (March 2026)

LLMs are excellent instruction followers. They're getting better at tool use. Feedback loops work when the loop is short (write code → run test → see error → fix).

Where they still struggle:

- **Long-horizon goal pursuit** — they lose track, go in circles, or get stuck after 10+ steps
- **Knowing when to stop** — agents that keep "improving" past the point of usefulness
- **Knowing when to ask for help** — instead of confidently going down the wrong path
- **Strategic pivots** — recognizing "this entire approach is wrong, let me try something fundamentally different"

The gap is in the decision-making layer. LLMs can execute individual steps well. The hard part is: which step should I do next? When should I stop? When should I change approach entirely?

That's why the instruction set → agent graduation path matters. You're providing the decision-making scaffolding that LLMs are weakest at, then gradually removing it as the technology improves.

---

## What This Means for PMs

If you're a PM working with AI, three things matter:

**1. Know what you're actually building.** When someone says "we're building an agent," ask: is it goal-directed? Does it use tools? Does it have feedback loops? Or is it a prompt with a fancy wrapper?

**2. The autonomy dial is a product decision.** More autonomy = more capable but less predictable. Less autonomy = more reliable but more limited. Where you set that dial depends on the cost of error in your domain.

**3. Instruction sets first, agents later.** Get the process right before you add autonomy. A bad process with full autonomy is an agent that confidently does the wrong thing.

---

## What's Next

Understanding agents is one lens. But there's a deeper question beneath all of this: in any AI-powered workflow, which steps are deterministic (same input → same output) and which are probabilistic (same input → different output)?

That distinction — **D vs. P** — turns out to be the most useful framework I've found for thinking about AI products, agent design, and even career strategy.

That's what I'll break down next.

---

*Building in public at [fullstackpm.tech](https://fullstackpm.tech). Follow along on [X @fullstackpmtech](https://x.com/fullstackpmtech).*
