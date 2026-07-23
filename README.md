# Kieran McShane: Notes

Source for the GitHub Pages site at <https://kieranmcshane.github.io>.

The site uses GitHub Pages, Jekyll, and the Minima theme. Long-form posts live in `_posts/`.

## Rating Lab

`/rating-lab/` is a generated, interactive comparison of Elo, Glicko-2,
Gaussian TrueSkill, and robust heavy-tail ratings for ATP tennis, European club
football, men's national-team football, and elite over-the-board chess.
The same page includes a daily, format-aware competition predictor. A single
public state machine applies to leagues, qualifying rounds, cups, knockout
tournaments, chess tournaments, and official ATP draws: **Upcoming** publishes
prior-heavy expected outcomes; **Live** locks the current score, table, or draw
and publishes conditional progression probabilities; **Finished** replaces
forecast odds with protocol performance ratings and an actual-versus-expected
outperformer/underperformer graph. ATP draws preserve every published path and
bye, use the declared surface-aware probability for each unplayed match, and
publish direct-match, round-progression, and title probabilities. During elite
Lichess round-robin broadcasts it reconstructs the remaining all-play-all
pairing set and forecasts the final chess table; recently finished events stay
visible for retrospective performance analysis.

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
2. To publish candidate recent men's league seasons or the completed men's
   World Cup 2026 player cohort, add an API-Football credential as
   `API_FOOTBALL_KEY`. Premier League 2022/23 through 2025/26 are checked
   independently for all 380 fixtures; World Cup 2026 requires all 104 matches.
   Fixture details are requested in batches of at most 20 IDs, keeping the first
   complete expansion below 100 requests. Cohorts that the configured plan
   cannot access remain explicitly withheld. The credential and raw responses
   are never exposed.
3. In **Settings → Pages**, select **GitHub Actions** as the deployment source.
4. Run **Refresh ratings and deploy Pages** once manually, or wait for the daily
   schedule. Tennis, football, national-team football, and current chess refresh
   daily, while finalized Lichess archives are cached. National teams use
   Mart Jürisoo's CC0 full-international results.

For an exact local refresh and verification, run:

```sh
RATING_LAB_CACHE_DIR=.cache/rating-lab python3 scripts/refresh_ratings.py
python3 -m unittest discover -s tests -v
```

Install `requirements-rating-lab.txt` first so the refresh can extract the
public ATP ProTennisLive draw PDFs. The draw PDF is the bracket authority;
ManTennisData supplies stable ATP identifiers and the result cross-check.

Without the football token, the script uses CC0 OpenFootball league, Champions
League, World Cup, and Euro snapshots; the predictor remains functional without
credentials. Generated JSON follows `rating_lab/schema.json`; source
adapters and rating models live in `rating_lab/`. The public manifest records
the schema and methodology versions, code revision, source freshness, and data
snapshot hash where a source is distributed as a single file.

Historical player ratings publish source and retrieval metadata per cohort.
StatsBomb raw files remain publicly reproducible. API-Football responses are
cached only during the server-side build under the provider's terms; the site
publishes derived Lineup TrueSkill, RAPM, experimental pairwise-chemistry,
team-specific HAPM, and team-specific LAPM
ratings, coverage gates, and a SHA-256
snapshot identifier rather than redistributing the provider feed.
An unavailable optional commercial cohort cannot block or replace validated
public-data cohorts. The payload records whether each candidate recent Premier
League season and World Cup 2026 is published, not configured, or withheld,
together with a sanitized reason and check time.

The Pages workflow always runs the historical player pipeline before Jekyll so
a restored fallback can never silently replace the checked-in player schema.
Push deployments refresh the player payload needed by the changed interface;
scheduled and manual runs refresh the sport feeds first and then the player
payload. The event-aware source cache restores the previous public-data cache
on its first run and is saved under a new version only after validation.

The historical player lab also publishes complete league-season cohorts when
the source supplies every fixture. Premier League 2015/16 is the first men's
full-season cohort: all 380 league matches pass the lineup, minutes, integrity,
and connected-graph gates, and eligibility rises to 900 minutes and ten
appearances. Premier League 2022/23 through 2025/26 are candidate API-Football
cohorts and are published independently only after all 380 matches pass the
same stable-ID, lineup, substitution, minute, goal-event and score-reproduction
gates. The payload lists included competitions explicitly; domestic cups and
UEFA matches are not described as season-wide evidence until their complete
lineup-minute feeds are available.

Lineup TrueSkill and RAPM remain the primary player-comparison baselines. Their
additivity assumption is explicit, but strong regularization makes them more
stable and interpretable when football lineup combinations are sparse. Broad
rankings and over- or under-performance claims should begin with both baselines,
their agreement, minutes, and uncertainty. Interaction models answer narrower
partnership or lineup questions and do not become replacements merely because
they are more flexible.

Pairwise chemistry is a non-additive residual lens rather than a replacement
for the two additive baselines. Exact teammate overlap minutes define the pair
features; a ridge model is fitted only to the goal difference RAPM did not
explain, with shrinkage selected on the chronological final quarter. Each
cohort publishes the interaction layer's held-out RMSE beside the RAPM baseline
and marks it descriptive-only when validation does not support predictive use.

HAPM is a separate dependency-aware lens based on Josephs et al.'s extended
hypergraph incidence construction. Within each team, supported players, pairs,
trios, quartets, and full observed constant lineups become weighted regression
rows while players remain the columns. This bounded-order adaptation avoids
materializing all 2,047 non-empty subsets of every 11-player lineup. Ridge
strength is selected on the chronological final quarter; the public payload
reports HAPM's held-out stint RMSE beside a full-lineup APM baseline and counts
how many teams beat that simpler baseline. HAPM remains experimental regardless
of an individual team's result; its player coefficients also remain additive.
Pairwise chemistry remains the explicit residual interaction model.

LAPM is a separate descriptive dependency lens based on Josephs et al.'s
line-graph APM construction. Exact substitution intervals split matches into
constant-lineup stints; event goals must reproduce the final score. Within each
team, singleton players, supported pairs, and full observed lineups become
nodes. Non-zero player overlap creates Jaccard-weighted edges, and a Laplacian
penalty smooths the fitted goal-difference values across similar combinations.
The public payload records the retained orders, thresholds, node and edge
counts, solver diagnostics, paper DOI, and reference implementation. LAPM
values are never ranked across teams because those graphs do not share a
common fitted scale.

Competition forecasts use 5,000 deterministic simulations per competition and
model. Tennis forecasts lock official ProTennisLive draw slots, results, and
byes, then use the selected global-plus-surface belief for every unplayed
singles match. League forecasts publish the current table, remaining-match
count, and every team's finishing-position distribution; before the first
result those distributions are explicitly labeled as priors. Knockout and
qualifying forecasts lock known aggregate scores and results, publish the
current tie beside conditional advancement chances, and never infer an
unpublished field. When a later cup draw is unpublished, surviving teams are
uniformly re-drawn in each simulation only where the competition protocol
permits it. Title probabilities are withheld until the public feed identifies
a knockout field. Every forecast publishes its lifecycle state, state
definition, fixture snapshot checksum, and deterministic seed for exact
reproduction.

Completed competitions replace title odds with a deterministic event replay
from the strictly pre-event rating state. Before each update, the selected
protocol records expected result score `p`; the participant residual is
`sum(actual score - p)`, and the dashboard's diverging chart standardizes it by
`sqrt(sum(p * (1 - p)))`. Wins, draws, and losses score 1, 0.5, and 0. The
published JSON retains actual score, expected score, residual, per-match
residual, variance reference, and standardized surprise for every participant.

Eligible Polymarket and Kalshi winner fields are retained as dated benchmark
snapshots rather than overwritten on the next refresh. Each capture freezes
the normalized market field and all four Rating Lab title forecasts on the
same participant identities, including an explicit `Other` remainder when the
market field is incomplete. After the official winner is known, the unchanged
snapshots receive categorical log-loss and multiclass Brier scores. The public
JSON retains the quote date, source hash, forecasts, resolution, and
per-forecaster scores; lower is better and market data never enter a model.
Competitions without a conservative season-and-identity match publish an
explicit `no eligible market found` state.
