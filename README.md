# Portfolio Mirror Status Monitor

Live mirror monitor for Mahendra Mali (Max) developer portfolio across distributed platforms.

| Provider | Endpoint URL | Status | Sync Mechanism |
|---|---|---|---|
| GitHub Pages | [https://ohhmax.github.io](https://ohhmax.github.io) | Live | Primary Source Branch |
| GitLab Pages | [https://ohhmax.gitlab.io](https://ohhmax.gitlab.io) | Live | Automated CI/CD Mirror |
| Codeberg Pages | [https://ohhmax.codeberg.page/](https://ohhmax.codeberg.page/) | Live | Automated CI/CD Mirror |

## Mirror Architecture

All mirrors synchronize automatically on every commit to the main branch via dedicated GitHub Actions workflows:
- Primary Host: GitHub Pages (ohhmax.github.io)
- Redundant Mirror 1: GitLab Pages (ohhmax.gitlab.io)
- Redundant Mirror 2: Codeberg Pages (ohhmax.codeberg.page)
