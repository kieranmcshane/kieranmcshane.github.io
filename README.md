# Kieran McShane: Notes

Source for the GitHub Pages site at <https://kieranmcshane.github.io>.

The site uses GitHub Pages, Jekyll, and the Minima theme. Long-form posts live in `_posts/`.

## Rating Lab

`/rating-lab/` is a generated, interactive comparison of Elo, Gaussian
TrueSkill, and robust heavy-tail ratings for ATP tennis, European club
football, men's national-team football, and elite over-the-board chess.
The same page includes a daily competition predictor for the five covered
European leagues. It starts from actual results and simulates every remaining
fixture under each of the three rating protocols.

The page's protocol explorer exposes the running rules for every sport/model
pair: source identity boundary, deterministic sort order, priors, venue or
colour advantage, result likelihood, update sequence, inactivity drift,
seasonal regression, eligibility, candidate parameter grid, exact chronological
split dates, evaluation definitions, fixed numerical constants, publication
cap, and known limitations. These descriptions are generated from the same
published parameters consumed by the leaderboard rather than maintained as a
separate methodology summary.

The scheduled GitHub Actions workflow refreshes the public datasets and deploys
the complete Jekyll site as a Pages artifact. Repository setup requires:

1. Create a free football-data.org API token and add it as the repository secret
   `FOOTBALL_DATA_TOKEN`.
2. In **Settings → Pages**, select **GitHub Actions** as the deployment source.
3. Run **Refresh ratings and deploy Pages** once manually, or wait for the daily
   schedule. Tennis refreshes on Mondays; football and current chess refresh
   daily, while finalized Lichess archives are cached. National teams use
   Mart Jürisoo's CC0 full-international results.

For an exact local refresh and verification, run:

```sh
RATING_LAB_CACHE_DIR=.cache/rating-lab python3 scripts/refresh_ratings.py
python3 -m unittest discover -s tests -v
```

Without the football token, the script uses the CC0 OpenFootball feed as a
development fallback. Generated JSON follows `rating_lab/schema.json`; source
adapters and rating models live in `rating_lab/`. The public manifest records
the schema and methodology versions, code revision, source freshness, and data
snapshot hash where a source is distributed as a single file.

Competition forecasts use 5,000 deterministic season simulations per league
and model. The public football JSON records the fixture snapshot checksum,
seed, current table, remaining-match count, and every team's finishing-position
distribution, so a forecast can be audited and reproduced exactly.
