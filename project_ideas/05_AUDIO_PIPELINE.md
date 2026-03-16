# Audio Pipeline: Listen to Blog Posts

**Status:** Backlog — captured 2026-03-11
**Type:** Site feature
**Priority:** Medium — nice differentiator for content, low complexity to POC

---

## Core Idea

Add audio versions of blog articles so readers can listen instead of read.
Podcast-style consumption of the same content — no separate RSS feed or platform needed, just a player embedded in the blog post.

---

## How It Works

**Content generation:**
1. Take finished article markdown
2. Run through ElevenLabs TTS (text-to-speech) API
3. Generate MP3 audio file
4. Save to `code/app/static/audio/{slug}.mp3`

**Surfacing it on the site:**
1. Add optional `audio` field to article frontmatter:
   ```yaml
   audio: "/static/audio/the-speed-drug.mp3"
   ```
2. `blog/detail.html` checks if `post.audio` exists
3. If yes, renders a minimal audio player above the article body

**Player UI:**
- Simple HTML5 `<audio>` element with custom styling
- Play/pause, progress bar, time remaining
- "Listen to this article (~8 min)" label
- No external dependencies

---

## POC Plan

Start with one article — **Productivity Paradox** or **Speed Drug** as the first test.

1. Generate audio via ElevenLabs
2. Save MP3 to `static/audio/`
3. Add `audio` field to that post's frontmatter
4. Build the player partial in `detail.html`
5. Ship and see how it feels

If it works well, add audio to all future articles as part of the publishing workflow.

---

## ElevenLabs Notes

- API: straightforward REST call with text input → MP3 output
- Voice: pick one consistent voice for the brand (not switching per article)
- Cost: ~$0.30 per article at typical length (~2,000 words ≈ 12-15 min audio)
- Files: MP3s are ~10-15MB each — fine for static hosting on Render

---

## Future Extension

Once audio exists per article, a natural next step is an **RSS audio feed** (`/podcast.xml`) which makes the content discoverable on Apple Podcasts, Spotify, etc. without any additional recording work. The audio files already exist — just need a feed wrapper.

That turns the blog into a podcast automatically.

---

## Open Questions

- Which ElevenLabs voice fits the brand? (needs a listen test)
- Do we generate audio for all existing articles retroactively, or just new ones going forward?
- Player design — minimal (just play/pause) or show waveform?
- Should the audio player be above or below the article header?
