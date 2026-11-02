# Unpublished articles

These six articles stay in the repository so they can be rewritten and republished later. Jekyll does not publish files in `_drafts/` unless the build is run with `--drafts`.

The Pages workflow in `.github/workflows/refresh-and-deploy.yml` builds with `actions/jekyll-build-pages` and does not pass `--drafts`. The same is true of the visual-regression workflow. These files are therefore left out of the public site, the home-page post list, the Atom feed, and the sitemap.

Referenced images, diagrams, and PDFs stay under `assets/` so a later rewrite can keep using them.

To republish an article, move it back to `_posts/` (for example with `git mv`).
