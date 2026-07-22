# Contributing — Async School Management System

## Commit message format
Use conventional commits: `type(scope): short description`

Types: feat, fix, refactor, docs, test, chore
Scopes: student, class, attendance, mark, security, ci

Examples:
feat(student): add registration form validation
fix(attendance): prevent duplicate entries per session
refactor(mark): simplify grade calculation logic
docs(readme): add setup instructions

## Branching
One branch per workstream. Never commit directly to main.
Branch names: registration-a, registration-b, attendance, mark-list, security-qa

## Pull requests
- Open a PR against main when your workstream is ready for integration
- At least 1 teammate must review and approve before merge
- CI must pass (module must install cleanly) before merge
- Squash-merge preferred, keep the PR title as a conventional commit

## Before opening a PR
- Test locally: `docker compose exec odoo odoo -i school_management -d test_db --stop-after-init`
- No credentials, .env files, or private attachments in the diff
