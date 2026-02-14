---
title: "Why I'm Building in Public as a Product Manager"
date: 2026-02-15
tags: [ai, building-in-public, product-management]
excerpt: "What changed when I started sharing my roadmap, experiments, and trade-offs in the open."
author: "Harsha Cheruku"
---
Building in public started as a curiosity and turned into a strategy. When I shared the first prototype of a PM tool on LinkedIn, I expected a few likes. Instead, I got real feedback from product leaders who cared about the same bottlenecks I was seeing: slow research cycles, shallow customer insights, and roadmaps that were always one quarter behind reality.

## The Feedback Loop That Changed Everything

The practice creates a feedback loop that a private roadmap can’t match. Every post forces me to clarify the **problem**, **hypothesis**, and **metric** before I ship. When your stakeholders can see what you’re trying to learn, you build trust and recruit collaborators who want to help you test faster.

> “Visibility doesn’t just increase accountability — it shortens the distance between insight and iteration.”

From a tactical perspective, it’s also a sharp way to validate AI workflows. I can share a prompt experiment, measure the response quality, and refine the scaffolding in the open. That transparency has made my work more robust and less tied to a single tool or vendor.

Here’s the basic structure I follow for every experiment:

```python
from dataclasses import dataclass

@dataclass
class Experiment:
    hypothesis: str
    metric: str
    iteration: int

experiment = Experiment(
    hypothesis="Structured prompts reduce ambiguity in PRD drafts",
    metric="Time to publish a customer-ready draft",
    iteration=3,
)
print(experiment)
```

If you’re curious about the tools I’m using, check out the [projects page](/projects) and the evolving [design system](/about). I also draw a lot of inspiration from the open-source community — here’s a great primer on [building in public](https://www.swyx.io/building-in-public/).

The bigger lesson: shipping publicly forces a product manager to act like a maker. You still align stakeholders and refine strategy, but you also own the surface area of the outcome. That mindset change is why I’m investing in full-stack PM skills and why I keep posting the messy in-between. The roadmap isn’t perfect, but it’s finally visible.
