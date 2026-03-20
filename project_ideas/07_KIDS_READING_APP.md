# Project Idea: Kids Reading App

**Status:** Backlog — captured 2026-03-20
**Type:** Standalone tool / side project
**Priority:** Medium — personal motivation, clear audience, AI-native use case

---

## Core Idea

A reading app for early readers (ages 4-8) that combines phonics, basic reading comprehension, and AI-generated stories — similar to reading.com but with the ability to generate new, original stories tailored to the child's level and interests.

Built initially for friends' kids. Could expand to a broader audience.

---

## What It Does

### 1. Phonics & Early Reading
- Letter recognition, sound-letter mapping
- Simple word building (CVC words: cat, dog, run)
- Sight word practice
- Read-aloud with word highlighting

### 2. Reading Comprehension
- Short stories with comprehension questions after
- "What happened next?" prompts
- Character and setting identification
- Simple retelling exercises

### 3. Story Generation (AI-powered)
- Generate new short stories at the right reading level
- Personalize by name, interests, favorite animals, settings
- Stories adapt to the child's current level
- Parent/teacher can set the theme or let the child pick

### 4. Original Story Library
- Curated library of original short stories
- Leveled (beginner → early reader → independent reader)
- Illustrated (simple AI-generated or hand-drawn style illustrations)

---

## Who It's For

- Ages 4-8, early readers
- Parents of young children wanting a screen-time tool that's actually educational
- Initially: friends' kids as a closed beta
- Eventually: broader audience if it works well

---

## Why It's Interesting

- reading.com is good but expensive ($20+/month) and not customizable
- AI makes personalized story generation trivially cheap — a story with the child's name, their dog's name, and their favorite color costs fractions of a cent to generate
- Most reading apps are drill-based and boring — story generation makes it feel like a new experience every time
- Parents trust recommendations from friends; organic growth through the exact network this is being built for

---

## Tech Approach

- FastAPI + Jinja2 (same stack as fullstackpm.tech) or simple Next.js frontend
- OpenAI API for story generation (GPT-4o, cheap at this length)
- Simple SQLite for progress tracking per child
- No login required for MVP — child profile stored in localStorage
- Text-to-speech for read-aloud (browser native or ElevenLabs)

---

## MVP Scope

1. 10-15 pre-written leveled stories with comprehension questions
2. AI story generator with name/interest personalization
3. Read-aloud with word highlighting (Web Speech API)
4. Simple progress indicator (stars per story completed)

---

## Open Questions

- Should stories be illustrated? (AI image generation adds cost and complexity)
- How do we handle reading level assessment — manual parent input or adaptive quiz?
- Login/profiles for multiple children on one device?
- Standalone site or a tool under fullstackpm.tech?

---

## Next Steps

1. Talk to 2-3 parents of early readers — what do they actually want?
2. Build MVP with 5 stories + AI generator
3. Test with friends' kids
4. Iterate based on what kids actually engage with
