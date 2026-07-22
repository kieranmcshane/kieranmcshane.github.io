# Kieran McShane: Notes

Source for the GitHub Pages site at <https://kieranmcshane.github.io>.

The site uses GitHub Pages, Jekyll, and the Minima theme. Long-form posts live in `_posts/`.

## Rating Lab

`/rating-lab/` is a generated, interactive comparison of Elo, Glicko-2,
Gaussian TrueSkill, and robust heavy-tail ratings for ATP tennis, European club
football, men's national-team football, and elite over-the-board chess.
The same page includes a daily, format-aware competition predictor. It covers
the five European league tables plus public football-data.org knockout fields
for the Champions League, FIFA World Cup, and European Championship. It starts
from actual results and published fixtures under each of the four rating
protocols. During live elite Lichess round-robin broadcasts it also reconstructs
the remaining all-play-all pairing set and forecasts the final chess table.

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

1. Optionally create a free football-data.org API token and add it as the
   repository secret `FOOTBALL_DATA_TOKEN` for the primary football feed.
2. To publish the completed men's World Cup 2026 player cohort, add an
   API-Football credential as `API_FOOTBALL_KEY`. The player pipeline uses one
   league-season request plus fixture-detail batches of at most 20 IDs, validates
   all 104 matches, and never exposes the credential or raw responses.
3. In **Settings → Pages**, select **GitHub Actions** as the deployment source.
4. Run **Refresh ratings and deploy Pages** once manually, or wait for the daily
   schedule. Tennis refreshes on Mondays; football and current chess refresh
   daily, while finalized Lichess archives are cached. National teams use
   Mart Jürisoo's CC0 full-international results.

For an exact local refresh and verification, run:

```sh
RATING_LAB_CACHE_DIR=.cache/rating-lab python3 scripts/refresh_ratings.py
python3 -m unittest discover -s tests -v
```

Without the football token, the script uses CC0 OpenFootball league, Champions
League, World Cup, and Euro snapshots; the predictor remains functional without
credentials. Generated JSON follows `rating_lab/schema.json`; source
adapters and rating models live in `rating_lab/`. The public manifest records
the schema and methodology versions, code revision, source freshness, and data
snapshot hash where a source is distributed as a single file.

Historical player ratings publish source and retrieval metadata per cohort.
StatsBomb raw files remain publicly reproducible. API-Football responses are
cached only during the server-side build under the provider's terms; the site
publishes derived Lineup TrueSkill/RAPM ratings, coverage gates, and a SHA-256
snapshot identifier rather than redistributing the provider feed.

The historical player lab also publishes complete league-season cohorts when
the source supplies every fixture. Premier League 2015/16 is the first men's
full-season cohort: all 380 league matches pass the lineup, minutes, integrity,
and connected-graph gates, and eligibility rises to 900 minutes and ten
appearances. The payload lists included competitions explicitly; domestic cups
and UEFA matches are not described as season-wide evidence until their complete
lineup-minute feeds are available.

Competition forecasts use 5,000 deterministic simulations per competition and
model. League forecasts publish the current table, remaining-match count, and
every team's finishing-position distribution. Knockout forecasts lock known
ties and results; when a later draw is unpublished, surviving teams are
uniformly re-drawn in each simulation. Title probabilities are withheld until
the public feed identifies a knockout field. Every forecast publishes its
fixture snapshot checksum and deterministic seed for exact reproduction.

Completed competitions replace title odds with a deterministic event replay
from the strictly pre-event rating state. Before each update, the selected
protocol records expected result score `p`; the participant residual is
`sum(actual score - p)`, and the dashboard's diverging chart standardizes it by
`sqrt(sum(p * (1 - p)))`. Wins, draws, and losses score 1, 0.5, and 0. The
published JSON retains actual score, expected score, residual, per-match
residual, variance reference, and standardized surprise for every participant.
