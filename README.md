# Kieran McShane: Notes

Source for the GitHub Pages site at <https://kieranmcshane.github.io>.

The site uses GitHub Pages, Jekyll, and the Minima theme. Long-form posts live in `_posts/`.

## Rating Lab

`/rating-lab/` is a generated, interactive comparison of Elo, Gaussian
TrueSkill, and robust heavy-tail ratings for ATP tennis, European football,
and elite over-the-board chess.

The scheduled GitHub Actions workflow refreshes the public datasets and deploys
the complete Jekyll site as a Pages artifact. Repository setup requires:

1. Create a free football-data.org API token and add it as the repository secret
   `FOOTBALL_DATA_TOKEN`.
2. In **Settings → Pages**, select **GitHub Actions** as the deployment source.
3. Run **Refresh ratings and deploy Pages** once manually, or wait for the daily
   schedule. Tennis refreshes on Mondays; football and current chess refresh
   daily, while finalized Lichess archives are cached.

For a local refresh, run `python3 scripts/refresh_ratings.py`. Without the
football token, the script uses the CC0 OpenFootball feed as a development
fallback. Generated JSON follows `rating_lab/schema.json`; source adapters and
rating models live in `rating_lab/`.
