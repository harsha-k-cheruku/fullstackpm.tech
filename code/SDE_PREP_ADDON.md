# SDE Prep Tool - Addon Integration Guide

## Overview

The SDE Prep Tool is implemented as a modular addon to fullstackpm.tech. It can be:
1. **Deployed with the main site** (current setup)
2. **Deployed as a separate service** and linked
3. **Managed as a separate git repository** for independent updates

## Current Architecture

The SDE Prep Tool is fully integrated into the main fullstackpm.tech application:

```
fullstackpm.tech/
├── app/
│   ├── models/
│   │   ├── sde_prep.py          ← SDE-specific models
│   │   └── user.py              ← User authentication
│   ├── routers/
│   │   ├── sde_prep.py          ← SDE Prep Tool routes
│   │   └── auth.py              ← Authentication routes
│   ├── templates/sde-prep/      ← SDE Prep Tool templates
│   └── seed_sde.py              ← Database seeding
├── app/static/css/sde-prep.css  ← Styling
└── fullstackpm.db               ← SQLite database
```

## API Routes

All routes are prefixed with `/tools/sde-prep` and `/api/sde-prep/`:

- **Pages**: `/tools/sde-prep/{page}` (dashboard, problems, daily-plan, system-design, behavioral, study-plan)
- **APIs**: `/api/sde-prep/{resource}` (dashboard/stats, problems, daily-tasks, system-design, behavioral)
- **Auth**: `/api/sde-prep/auth/{action}` (login, logout, current-user)

## Deployment Options

### Option 1: Unified Deployment (Current)
Deploy everything together as one application on Render:
```bash
# Single deployment
python -m uvicorn app.main:app
```
- ✅ Simple setup
- ✅ Shared database
- ✅ Single server
- ❌ Scaling requires scaling entire app

### Option 2: Separate Microservice
Deploy SDE Prep Tool as separate service:
1. Create repo: `sde-prep-tool`
2. Extract SDE-specific code
3. Deploy to separate Render instance
4. API calls from main site via HTTP

Would require:
- Separate Render instance
- API proxy/gateway
- Database migration

### Option 3: Git Submodule (Recommended for Future)
Once moved to GitHub:
```bash
# Add as submodule
git submodule add https://github.com/yourusername/sde-prep-tool.git tools/sde-prep

# Or with git subtree
git subtree add --prefix tools/sde-prep https://github.com/yourusername/sde-prep-tool.git main
```

## Pulling Latest Updates

If using git submodule:
```bash
# Update addon
git submodule update --remote

# Or with git subtree
git subtree pull --prefix tools/sde-prep <remote> main
```

## Standalone Repository

A standalone `sde-prep-tool` repository exists at:
- Local: `/Users/sidc/projects/sde-prep-tool/`
- To deploy separately: Push to GitHub and create new Render instance

## Database

SQLite database (`fullstackpm.db`) is shared with all features:
- LeetCode problems (66 items)
- System design topics (15 items)
- Behavioral stories (user-created)
- Week plans (12 items)
- Daily tasks (63 seeded items)
- User accounts (multi-user support)

To reset database:
```bash
rm fullstackpm.db
python -m app.seed_sde
```

## Environment Variables

No special environment variables needed for SDE Prep Tool. Uses same config as main app:
- `DATABASE_URL` (optional, defaults to SQLite)
- `TEMPLATES_DIR` (optional, defaults to app/templates)

## Development

To work on SDE Prep Tool:

1. **Make changes** to sde_prep files
2. **Test locally**: `python -m uvicorn app.main:app --reload`
3. **Commit** to main fullstackpm.tech repo
4. **Deploy**: Push to Render

To separate later:
1. Create separate GitHub repo
2. Copy SDE-specific files
3. Add as git submodule
4. Create separate Render deployment

## Integration Points

SDE Prep Tool integrates with main site via:

1. **Navigation**: Link in main navbar to `/tools/sde-prep`
2. **Database**: Shared SQLite with other features
3. **Static Files**: CSS/JS in main `/static/` directory
4. **Templates**: Shared Jinja2 template system
5. **Authentication**: Uses same user session system

## Monitoring

Routes:
- Main landing: `/tools/sde-prep`
- Dashboard: `/tools/sde-prep/dashboard`
- Problems: `/tools/sde-prep/problems`

APIs:
- Stats: `/api/sde-prep/dashboard/stats`
- Health check: Visit `/tools/sde-prep` and verify HTTP 200

## Future Improvements

1. **Extract to separate repo** and use git submodule
2. **Separate database** per user/tenant if scaling
3. **API documentation** via OpenAPI/Swagger
4. **Performance monitoring** via Render logs
5. **User analytics** tracking

## Support

For issues:
1. Check Render deployment logs
2. Test locally: `python -m uvicorn app.main:app --reload`
3. Verify database: `sqlite3 fullstackpm.db ".tables"`
4. Review git history: `git log --oneline app/routers/sde_prep.py`
