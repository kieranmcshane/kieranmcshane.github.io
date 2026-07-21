(function () {
  'use strict';

  var root = document.querySelector('.proof-game');
  if (!root) return;

  var storageKey = root.dataset.storageKey || 'centered-correlation-game-v1';
  var state = loadState();
  var scheduler = initializeFsrs();
  var currentMission = null;
  var currentStep = 0;
  var integrity = 3;
  var mistakes = 0;
  var checkpointResets = 0;
  var detour = null;
  var log = [];
  var returnMission = null;
  var returnAttempts = 0;
  var returnOptions = [];

  var missions = [
    {
      id: 'coordinates',
      title: 'Read the coordinates',
      short: 'Coordinates',
      objective: 'Separate local means, raw correlations, and centered correlations before using any norm.',
      target: '$C=T-rs^{\\mathsf T}$',
      facts: ['$r$ and $s$ encode the reduced states.', '$T$ contains the bipartite correlation coefficients.', 'Centering should remove only the product of the means.'],
      reward: 'You can now distinguish the four objects that the proof manipulates.',
      steps: [
        step('$r,\\ s,\\ T,\\ C$', 'The symbols have different mathematical roles.', 'Which object is the raw cross-moment?', [
          move('$T$', 'productive', 'Correct: $T$ stores the bipartite cross-moments.', 'Identify $T$ as the raw cross-moment.'),
          move('$C$', 'invalid', '$C$ is already centered; it is not the raw cross-moment.'),
          move('$r$', 'invalid', '$r$ is a local first moment, not a bipartite cross-moment.')
        ]),
        step('$T-\\square$', 'The centered matrix removes what the local means predict without genuine covariance.', 'What belongs in the empty slot?', [
          move('$rs^{\\mathsf T}$', 'productive', 'Yes. The product $rs^{\\mathsf T}$ is the cross-moment predicted by the two means.', 'Remove the product of the local means.'),
          move('$r-s$', 'invalid', 'The dimensions and the meaning are wrong: centering a cross-moment requires an outer product.'),
          move('$TT^{\\mathsf T}$', 'detour', 'This is a valid positive matrix, but it does not center $T$.', 'Explore $TT^{\\mathsf T}$ before returning.')
        ]),
        step('$C=T-rs^{\\mathsf T}$', 'This is a coefficient identity. It is not the operator identity $\\rho_{AB}-\\rho_A\\otimes\\rho_B$ without the basis factors.', 'What does an entry of $C$ represent?', [
          move('A covariance of two local basis observables', 'productive', 'Exactly. Each entry subtracts the product of the corresponding local means.', 'Interpret $C_{ij}$ as a covariance.'),
          move('A commutator', 'invalid', 'The two observables act on different subsystems; $C$ records covariance, not commutation.'),
          move('A joint probability', 'invalid', 'The coefficients can be negative and depend on the chosen traceless bases; they are not probabilities.')
        ])
      ],
      review: review('What is removed when one passes from $T$ to $C$?', [
        ['$rs^{\\mathsf T}$, the product of the local mean Bloch vectors.', true],
        ['The diagonal of $T$.', false],
        ['Every correlation produced by a separable state.', false]
      ], 'Centering removes the cross-moment predicted by the local means: $C=T-rs^{\\mathsf T}$.')
    },
    {
      id: 'product',
      title: 'Secure the product-state sector',
      short: 'Product states',
      objective: 'Recover the rank-one structure that makes the first norm computation exact.',
      target: '$\\lVert T\\rVert_*=\\lVert r\\rVert_2\\lVert s\\rVert_2$',
      facts: ['$\\rho_{AB}=\\rho_A\\otimes\\rho_B$.', 'The coefficient of $\\lambda_i\\otimes\\mu_j$ is a product of local coefficients.', 'An outer product has rank at most one.'],
      reward: 'You recovered the elementary factorization behind the separability test.',
      steps: [
        step('$\\rho_{AB}=\\rho_A\\otimes\\rho_B$', 'Expand the two local Bloch representations and inspect the mixed coefficient.', 'Which correlation matrix follows?', [
          move('$T=rs^{\\mathsf T}$', 'productive', 'Correct: every coefficient factorizes as $t_{ij}=r_i s_j$.', 'Factor the correlation matrix.'),
          move('$T=r+s$', 'invalid', 'A vector sum cannot supply a two-index correlation matrix.'),
          move('$T=sr^{\\mathsf T}$', 'detour', 'This is the transpose-sized convention. It is valid only after swapping which index belongs to which party.', 'Swap the subsystem convention, then return.')
        ]),
        step('$T=rs^{\\mathsf T}$', 'The range of this matrix is contained in the line spanned by $r$.', 'What is the strongest rank statement?', [
          move('$\\operatorname{rank}(T)\\leq1$', 'productive', 'Yes. The rank may be zero if one local Bloch vector vanishes.', 'Record the rank-one structure.'),
          move('$\\operatorname{rank}(T)=1$ always', 'invalid', 'If $r=0$ or $s=0$, then $T=0$ and its rank is zero.'),
          move('$T$ is diagonal', 'invalid', 'Rank one does not imply diagonal in the fixed Bloch bases.')
        ]),
        step('$T=rs^{\\mathsf T}$', 'A rank-one outer product has one possible nonzero singular value.', 'Which exact nuclear-norm identity holds?', [
          move('$\\lVert T\\rVert_*=\\lVert r\\rVert_2\\lVert s\\rVert_2$', 'productive', 'Correct. This is equality, not an estimate.', 'Use the rank-one norm formula.'),
          move('$\\lVert T\\rVert_*=\\lVert r\\rVert_2+\\lVert s\\rVert_2$', 'invalid', 'The singular value of an outer product is the product of the two Euclidean norms.'),
          move('$\\lVert T\\rVert_*=\\max(\\lVert r\\rVert_2,\\lVert s\\rVert_2)$', 'invalid', 'The maximum does not have the correct scaling under rescaling of one factor.')
        ])
      ],
      review: review('For a product state, why is the nuclear norm easy to compute?', [
        ['$T=rs^{\\mathsf T}$ has rank at most one, so its singular value is $\\lVert r\\rVert_2\\lVert s\\rVert_2$.', true],
        ['$T$ is always diagonal.', false],
        ['Nuclear and operator norms agree for every matrix.', false]
      ], 'The exact factorization is a rank-one statement; the later inequality appears only when several terms are added.')
    },
    {
      id: 'ensemble',
      title: 'Center one common ensemble',
      short: 'Covariance identity',
      objective: 'Use a single separable ensemble to rewrite the centered tensor as an ordinary covariance.',
      target: '$C=\\sum_k p_k(r_k-r)(s_k-s)^{\\mathsf T}$',
      facts: ['$T=\\sum_kp_kr_ks_k^{\\mathsf T}$.', '$r=\\sum_kp_kr_k$ and $s=\\sum_kp_ks_k$.', '$\\sum_kp_k=1$.'],
      reward: 'You recovered the covariance identity; its browser transitions mirror the Lean-checked theorem.',
      steps: [
        step('$C=T-rs^{\\mathsf T}$', 'Begin by exposing the separable cross-moment.', 'Which rewrite keeps the same common index $k$?', [
          move('$C=\\sum_kp_kr_ks_k^{\\mathsf T}-rs^{\\mathsf T}$', 'productive', 'Correct. The common ensemble is now visible.', 'Rewrite $T$ using the separable ensemble.'),
          move('$C=\\sum_kp_kr_k\\sum_\\ell p_\\ell s_\\ell^{\\mathsf T}$', 'invalid', 'That expression equals $rs^{\\mathsf T}$ and loses the paired cross-moment $T$.'),
          move('Choose a singular-value decomposition of $T$', 'detour', 'An SVD decomposes the matrix, but its factors need not be physical local Bloch vectors from one ensemble.', 'Inspect an algebraic decomposition, then return to the physical one.')
        ]),
        step('$C=\\sum_kp_kr_ks_k^{\\mathsf T}-rs^{\\mathsf T}$', 'To center each factor, insert terms whose weighted sums vanish.', 'Which two identities supply the zero means?', [
          move('$\\sum_kp_k(r_k-r)=0$ and $\\sum_kp_k(s_k-s)=0$', 'productive', 'Yes. They follow from the definitions of $r$ and $s$.', 'Insert the two zero-mean identities.'),
          move('$\\sum_k(r_k-r)=0$ and $\\sum_k(s_k-s)=0$', 'invalid', 'The weights $p_k$ are essential; the unweighted sums need not vanish.'),
          move('$r_k=r$ and $s_k=s$ for every $k$', 'invalid', 'That would make the state a single product point, not a general separable mixture.')
        ]),
        step('$\\sum_kp_k[r_ks_k^{\\mathsf T}-r_ks^{\\mathsf T}-rs_k^{\\mathsf T}+rs^{\\mathsf T}]$', 'The four terms have the pattern of a bilinear factorization.', 'Which expression factors this state?', [
          move('$\\sum_kp_k(r_k-r)(s_k-s)^{\\mathsf T}$', 'productive', 'Exactly. The centered matrix is the covariance of the classical ensemble of local Bloch vectors.', 'Factor the centered product.'),
          move('$\\sum_kp_k(r_k+r)(s_k+s)^{\\mathsf T}$', 'invalid', 'The signs reproduce neither the expansion nor centering.'),
          move('$\\sum_kp_k(r_k-r)(r_k-r)^{\\mathsf T}$', 'invalid', 'This is a local covariance on Alice, not the cross-covariance between Alice and Bob.')
        ])
      ],
      review: review('What makes the centered covariance identity possible?', [
        ['The same probabilities and the same index $k$ generate $r$, $s$, and $T$.', true],
        ['The optimal nuclear-norm decomposition of $T$ is unique.', false],
        ['All local Bloch vectors are mutually orthogonal.', false]
      ], 'Separability supplies one common ensemble. Expanding its centered cross-moment gives the identity.')
    },
    {
      id: 'norm',
      title: 'Pass the norm gate',
      short: 'Nuclear norm',
      objective: 'Turn the covariance decomposition into a scalar sum without silently replacing an inequality by equality.',
      target: '$\\lVert C\\rVert_*\\leq\\sum_kp_k\\lVert r_k-r\\rVert_2\\lVert s_k-s\\rVert_2$',
      facts: ['$C=\\sum_kp_ku_kv_k^{\\mathsf T}$ with $u_k=r_k-r$, $v_k=s_k-s$.', 'The nuclear norm is a norm.', '$u_kv_k^{\\mathsf T}$ has rank at most one.'],
      reward: 'You converted a matrix-valued covariance into a weighted scalar estimate.',
      steps: [
        step('$\\left\\lVert\\sum_kp_ku_kv_k^{\\mathsf T}\\right\\rVert_*$', 'Several rank-one matrices may point in incompatible singular directions.', 'Which first move is always justified?', [
          move('$\\leq\\sum_kp_k\\lVert u_kv_k^{\\mathsf T}\\rVert_*$', 'productive', 'Correct. This is the triangle inequality and is generally not equality.', 'Apply the nuclear-norm triangle inequality.'),
          move('$=\\sum_kp_k\\lVert u_kv_k^{\\mathsf T}\\rVert_*$', 'invalid', 'Equality needs special alignment and cannot be assumed for an arbitrary ensemble.'),
          move('$\\leq\\max_k\\lVert u_kv_k^{\\mathsf T}\\rVert_*$', 'invalid', 'A maximum alone does not dominate a weighted sum unless the weights are used correctly; this also discards the route to variances.')
        ]),
        step('$\\sum_kp_k\\lVert u_kv_k^{\\mathsf T}\\rVert_*$', 'Now each term has rank at most one.', 'How does each term simplify?', [
          move('$\\sum_kp_k\\lVert u_k\\rVert_2\\lVert v_k\\rVert_2$', 'productive', 'Yes. Each outer product has one nonzero singular value.', 'Use rank-one nuclear-norm factorization.'),
          move('$\\sum_kp_k(\\lVert u_k\\rVert_2+\\lVert v_k\\rVert_2)$', 'invalid', 'The singular value factorizes multiplicatively, not additively.'),
          move('$\\sum_kp_k|u_k^{\\mathsf T}v_k|$', 'detour', 'That scalar inner product is not even defined when the local Bloch dimensions differ, and it is not the nuclear norm.', 'Test a scalar contraction, then return.')
        ]),
        step('$\\lVert C\\rVert_*\\leq\\sum_kp_k\\lVert u_k\\rVert_2\\lVert v_k\\rVert_2$', 'The matrix problem has become a weighted scalar problem.', 'What mathematical tool is now prepared?', [
          move('Weighted Cauchy–Schwarz', 'productive', 'Correct. The square-root weights turn the sum into an ordinary scalar inner product.', 'Recognize the next gate.'),
          move('The spectral theorem for $C$', 'detour', 'Diagonalizing $C$ is legal, but it does not connect the right-hand side to local variance deficits.', 'Diagonalize the output matrix, then return.'),
          move('Partial transposition', 'invalid', 'PPT is a different separability test and is not used in this derivation.')
        ])
      ],
      review: review('Where does the first inequality enter the centered proof?', [
        ['At the nuclear-norm triangle inequality applied to the sum of rank-one terms.', true],
        ['At the product-state factorization $T=rs^{\\mathsf T}$.', false],
        ['At the definition $C=T-rs^{\\mathsf T}$.', false]
      ], 'Rank-one norm factorization is exact. The loss first occurs when the norm of a sum is bounded by the sum of norms.')
    },
    {
      id: 'cauchy',
      title: 'Cross the Cauchy bridge',
      short: 'Cauchy–Schwarz',
      objective: 'Convert the weighted sum of paired deviations into the product of two local root-mean-square deviations.',
      target: '$\\lVert C\\rVert_*\\leq\\sqrt{\\sum_kp_k\\lVert u_k\\rVert_2^2}\\sqrt{\\sum_kp_k\\lVert v_k\\rVert_2^2}$',
      facts: ['$u_k=r_k-r$ and $v_k=s_k-s$.', '$p_k\\geq0$ and $\\sum_kp_k=1$.', 'Cauchy–Schwarz applies to two scalar sequences.'],
      reward: 'You separated the joint covariance budget into two local fluctuation budgets.',
      steps: [
        step('$\\sum_kp_k\\lVert u_k\\rVert_2\\lVert v_k\\rVert_2$', 'The weights must be split so that their product is still $p_k$.', 'Which scalar sequences should be paired?', [
          move('$a_k=\\sqrt{p_k}\\lVert u_k\\rVert_2$, $b_k=\\sqrt{p_k}\\lVert v_k\\rVert_2$', 'productive', 'Exactly. Then $a_kb_k=p_k\\lVert u_k\\rVert_2\\lVert v_k\\rVert_2$.', 'Split each weight into two square roots.'),
          move('$a_k=p_k\\lVert u_k\\rVert_2$, $b_k=p_k\\lVert v_k\\rVert_2$', 'invalid', 'Their product contains $p_k^2$, so it is not the original sum.'),
          move('$a_k=\\lVert u_k\\rVert_2/p_k$, $b_k=\\lVert v_k\\rVert_2/p_k$', 'invalid', 'This changes the weights, can divide by zero, and does not reconstruct the target sum.')
        ]),
        step('$\\sum_ka_kb_k$', 'The two sequences now lie in an ordinary Euclidean space indexed by $k$.', 'Apply the correct inequality.', [
          move('$\\leq\\sqrt{\\sum_ka_k^2}\\sqrt{\\sum_kb_k^2}$', 'productive', 'Correct. This is the scalar Cauchy–Schwarz inequality.', 'Apply Cauchy–Schwarz.'),
          move('$\\leq\\sum_ka_k^2+\\sum_kb_k^2$', 'detour', 'A version of Young’s inequality gives a valid but weaker additive route; it loses the symmetric product needed here.', 'Follow the additive estimate, then return.'),
          move('$=\\sqrt{\\sum_ka_k^2}\\sqrt{\\sum_kb_k^2}$', 'invalid', 'Cauchy–Schwarz is an inequality unless the two scalar sequences are proportional.')
        ]),
        step('$\\sqrt{\\sum_ka_k^2}\\sqrt{\\sum_kb_k^2}$', 'Return from the auxiliary scalar sequences to the local deviations.', 'Which expression results?', [
          move('$\\sqrt{\\sum_kp_k\\lVert r_k-r\\rVert_2^2}\\sqrt{\\sum_kp_k\\lVert s_k-s\\rVert_2^2}$', 'productive', 'Yes. These are precisely the two local root-mean-square deviations.', 'Recover the two local variance sums.'),
          move('$\\sum_kp_k\\lVert r_k-r\\rVert_2\\lVert s_k-s\\rVert_2$', 'invalid', 'That is the expression before Cauchy–Schwarz, not its separated upper bound.'),
          move('$\\lVert r-s\\rVert_2$', 'invalid', 'The local vectors can even live in spaces of different dimensions; the proof uses two separate variances.')
        ])
      ],
      review: review('Why are square roots of the probabilities introduced?', [
        ['They turn the weighted sum into an ordinary inner product while leaving one factor $p_k$ in each product.', true],
        ['They make all local Bloch vectors pure.', false],
        ['They diagonalize the covariance matrix.', false]
      ], 'Set $a_k=\\sqrt{p_k}\\lVert r_k-r\\rVert_2$ and $b_k=\\sqrt{p_k}\\lVert s_k-s\\rVert_2$, then apply scalar Cauchy–Schwarz.')
    },
    {
      id: 'variance',
      title: 'Spend the variance budget',
      short: 'Variance deficit',
      objective: 'Identify each local fluctuation sum and close the marginal-dependent separability bound.',
      target: '$\\lVert C\\rVert_*\\leq\\sqrt{(R_M^2-\\lVert r\\rVert_2^2)(R_N^2-\\lVert s\\rVert_2^2)}$',
      facts: ['A separable ensemble may be refined to pure local states.', 'Pure local Bloch vectors have norm $R_M$ or $R_N$.', '$r=\\sum_kp_kr_k$ and $s=\\sum_kp_ks_k$.'],
      reward: 'You completed the centered separability bound.',
      steps: [
        step('$\\sum_kp_k\\lVert r_k-r\\rVert_2^2$', 'Expand the square and use the weighted mean identity.', 'Which variance identity is correct?', [
          move('$=\\sum_kp_k\\lVert r_k\\rVert_2^2-\\lVert r\\rVert_2^2$', 'productive', 'Correct. The cross term collapses because $r$ is the weighted mean.', 'Apply the weighted variance identity.'),
          move('$=\\sum_kp_k\\lVert r_k\\rVert_2^2+\\lVert r\\rVert_2^2$', 'invalid', 'Centering subtracts the squared mean; the sign is negative.'),
          move('$=\\lVert\\sum_kp_k(r_k-r)\\rVert_2^2$', 'invalid', 'The norm of the mean deviation is zero and is not the mean squared deviation.')
        ]),
        step('$\\sum_kp_k\\lVert r_k\\rVert_2^2-\\lVert r\\rVert_2^2$', 'Use a pure local refinement of the separable ensemble.', 'What does the first term become?', [
          move('$R_M^2$', 'productive', 'Yes. Every refined $r_k$ lies on the pure-state Bloch sphere of radius $R_M$.', 'Use the pure-state Bloch radius.'),
          move('$R_M$', 'invalid', 'The expression contains squared Euclidean norms, so the radius must be squared.'),
          move('$\\lVert r\\rVert_2^2$', 'invalid', 'That would make the variance vanish for every mixture, which is false.')
        ]),
        step('$\\lVert C\\rVert_*\\leq\\sqrt{R_M^2-\\lVert r\\rVert_2^2}\\sqrt{R_N^2-\\lVert s\\rVert_2^2}$', 'The two local variance identities close the estimate.', 'What physical feature now tightens the bound?', [
          move('A nearly pure marginal leaves a small local variance deficit', 'productive', 'Exactly. Strong local polarization leaves little room for separable covariance.', 'Interpret the marginal-dependent budget.'),
          move('A nearly pure marginal makes $C$ diagonal', 'invalid', 'Purity affects the size of the available variance budget, not the basis in which $C$ is diagonal.'),
          move('A nearly pure marginal forces the other marginal to be maximally mixed', 'invalid', 'There is no such implication for a general bipartite state.')
        ])
      ],
      review: review('What is the local fluctuation budget after a pure refinement?', [
        ['$\\sum_kp_k\\lVert r_k-r\\rVert_2^2=R_M^2-\\lVert r\\rVert_2^2$.', true],
        ['$R_M^2+\\lVert r\\rVert_2^2$.', false],
        ['$\\lVert r\\rVert_2^2$ independently of the ensemble.', false]
      ], 'The weighted variance identity subtracts the squared mean from the mean squared radius.')
    },
    {
      id: 'synthesis',
      title: 'The common-decomposition frontier',
      short: 'Synthesis',
      objective: 'Defend the exact theorem: what is equivalent bipartitely, what is stronger multipartitely, and what remains unresolved.',
      target: 'A complete, correctly qualified explanation',
      facts: ['For two Euclidean factors, projective norm = matrix nuclear norm.', 'For three or more factors, every unfolding norm is bounded by the full projective norm.', 'Separability requires one ensemble to generate all tensor orders.'],
      reward: 'Campaign complete: you can state the proof and its multipartite frontier without overclaiming.',
      steps: [
        step('$\\rho_{AB}=\\sum_kp_k\\rho_A^{(k)}\\otimes\\rho_B^{(k)}$', 'The proof begins with a physical decomposition, not an arbitrary matrix factorization.', 'Which first sentence is accurate?', [
          move('One common ensemble produces $r$, $s$, and $T$ simultaneously', 'productive', 'Correct. This common index is the structural source of the covariance identity.', 'State the ensemble structure.'),
          move('Choose independent optimal decompositions for $r$, $s$, and $T$', 'invalid', 'Independent decompositions destroy the common moment structure required by separability.'),
          move('Diagonalize every local density matrix in one basis', 'detour', 'Local diagonalizations may simplify examples, but the proof is basis-independent and does not need a common eigenbasis.', 'Try a basis reduction, then return.')
        ]),
        step('$C=T-rs^{\\mathsf T}$', 'Center the common ensemble before applying norms.', 'Which identity carries the argument?', [
          move('$C=\\sum_kp_k(r_k-r)(s_k-s)^{\\mathsf T}$', 'productive', 'Yes. This is the covariance identity.', 'Recover the centered decomposition.'),
          move('$C=\\sum_kp_kr_ks_k^{\\mathsf T}$', 'invalid', 'That is $T$, not $T-rs^{\\mathsf T}$.'),
          move('$C$ is linear in $\\rho_{AB}$', 'invalid', 'The product $rs^{\\mathsf T}$ makes the state-to-centered-tensor map nonlinear.')
        ]),
        step('$\\lVert C\\rVert_*$', 'The next three tools appear in a definite order.', 'Which chain is valid?', [
          move('Triangle inequality → rank-one norm → weighted Cauchy–Schwarz', 'productive', 'Correct. That chain separates the cross-covariance into two local variance budgets.', 'Recover the norm chain.'),
          move('PPT → spectral theorem → Jensen', 'invalid', 'Those tools do not derive this bound.'),
          move('Rank-one norm → equality for the whole sum → Cauchy–Schwarz', 'invalid', 'The norm of the whole sum is bounded by, not generally equal to, the sum of the termwise norms.')
        ]),
        step('$\\lVert C\\rVert_*\\leq\\sqrt{(R_M^2-\\lVert r\\rVert^2)(R_N^2-\\lVert s\\rVert^2)}$', 'This is a necessary condition for separability.', 'What may a violation establish?', [
          move('The state is entangled', 'productive', 'Correct. Passing the test does not prove separability.', 'Use the criterion in the valid direction.'),
          move('The state is separable', 'invalid', 'The criterion is necessary, not sufficient.'),
          move('The state is PPT in every dimension', 'invalid', 'The centered criterion and PPT are distinct tests.')
        ]),
        step('$T\\in E\\otimes F$', 'Now compare the uncentered projective-norm language with de Vicente.', 'What is genuinely equivalent in the bipartite Euclidean case?', [
          move('$\\lVert T\\rVert_{\\pi,2}=\\lVert T\\rVert_*$', 'productive', 'Exactly. A two-factor tensor is a matrix, and the Hilbertian projective norm is its nuclear norm.', 'Identify the bipartite equivalence.'),
          move('Centered criterion = de Vicente', 'invalid', 'The uncentered bipartite projective formulation is de Vicente; centering gives a stronger marginal-dependent condition.'),
          move('Projective norm = operator norm', 'invalid', 'The projective norm corresponds to the nuclear norm, not the largest singular value.')
        ]),
        step('$T\\in E_1\\otimes E_2\\otimes E_3$', 'Grouping factors produces matrix unfoldings.', 'What changes for three or more factors?', [
          move('Each unfolding nuclear norm is at most the full projective norm, and equality need not hold', 'productive', 'Correct. The full factor-by-factor projective constraint can therefore be strictly stronger.', 'State the multipartite strengthening.'),
          move('The largest unfolding norm always equals the full projective norm', 'invalid', 'A rank-one term across a grouping need not split into every individual party.'),
          move('Unfolding norms cease to be computable', 'detour', 'They remain computable matrix norms; the full tensor projective norm is the harder object.', 'Compare computational difficulty, then return.')
        ]),
        step('Subset tensors of several orders', 'Separate norm tests can all pass while describing incompatible latent ensembles.', 'What is the remaining structural question?', [
          move('Do all tensor orders arise from one common separable ensemble?', 'productive', 'Yes. This is the common-decomposition, or truncated-moment, compatibility problem.', 'Locate the research frontier.'),
          move('Can every tensor be diagonalized?', 'invalid', 'Diagonalization does not enforce compatibility across tensor orders.'),
          move('Does the top-order centered tensor determine the whole state?', 'invalid', 'Lower-order entanglement may survive even when a top-order tensor vanishes.')
        ])
      ],
      review: review('Which claim survives in the multipartite setting?', [
        ['Separate bounds on each tensor order still do not guarantee one common separable ensemble.', true],
        ['The largest unfolding norm always equals the full projective norm.', false],
        ['The centered criterion characterizes all mixed-state entanglement.', false]
      ], 'The remaining constraint is compatibility: one measure on the product Bloch bodies must generate every required moment together.')
    }
  ];

  var elements = {
    tabs: root.querySelectorAll('[data-game-view]'),
    panels: root.querySelectorAll('[data-game-panel]'),
    map: document.getElementById('game-map'),
    campaignCount: document.getElementById('game-campaign-count'),
    saveStatus: document.getElementById('game-save-status'),
    dueBadge: document.getElementById('game-due-badge'),
    missionNumber: document.getElementById('mission-number'),
    missionTitle: document.getElementById('mission-title'),
    missionObjective: document.getElementById('mission-objective'),
    missionTarget: document.getElementById('mission-target'),
    missionFacts: document.getElementById('mission-facts'),
    missionStepLabel: document.getElementById('mission-step-label'),
    missionRating: document.getElementById('mission-rating'),
    integrity: document.getElementById('integrity-meter'),
    formula: document.getElementById('proof-state-formula'),
    stateCopy: document.getElementById('proof-state-copy'),
    prompt: document.getElementById('proof-prompt'),
    tools: document.getElementById('proof-tool-buttons'),
    feedback: document.getElementById('mission-feedback'),
    log: document.getElementById('mission-log'),
    undo: document.getElementById('game-undo'),
    restart: document.getElementById('game-restart'),
    leave: document.getElementById('game-leave-mission'),
    complete: document.getElementById('mission-complete'),
    completeTitle: document.getElementById('mission-complete-title'),
    completeCopy: document.getElementById('mission-complete-copy'),
    nextMission: document.getElementById('game-next-mission'),
    returnMap: document.getElementById('game-return-map'),
    returnDue: document.getElementById('return-due-count'),
    returnNextDate: document.getElementById('return-next-date'),
    returnLabel: document.getElementById('return-mission-label'),
    returnQuestion: document.getElementById('return-question'),
    returnOptions: document.getElementById('return-options'),
    returnFeedback: document.getElementById('return-feedback'),
    returnNext: document.getElementById('return-next'),
    reset: document.getElementById('game-reset-save')
  };

  function step(formula, copy, prompt, moves) {
    return { formula: formula, copy: copy, prompt: prompt, moves: moves };
  }

  function move(label, result, feedback, logText) {
    return { label: label, result: result, feedback: feedback, log: logText || '' };
  }

  function review(question, options, explanation) {
    return { question: question, options: options, explanation: explanation };
  }

  function defaultState() {
    return { completed: {}, attempts: {}, cards: {}, view: 'campaign', lastMission: 0 };
  }

  function loadState() {
    try {
      var saved = JSON.parse(localStorage.getItem(storageKey) || '{}');
      return Object.assign(defaultState(), saved, {
        completed: saved.completed || {},
        attempts: saved.attempts || {},
        cards: saved.cards || {}
      });
    } catch (error) {
      return defaultState();
    }
  }

  function saveState() {
    try {
      localStorage.setItem(storageKey, JSON.stringify(state));
      elements.saveStatus.textContent = 'Saved on this device';
    } catch (error) {
      elements.saveStatus.textContent = 'Local save unavailable';
    }
    renderMap();
    updateReturnSummary();
  }

  function initializeFsrs() {
    if (!window.FSRS || !window.FSRS.fsrs) return null;
    return window.FSRS.fsrs({
      request_retention: 0.9,
      maximum_interval: 36500,
      enable_fuzz: true,
      enable_short_term: false
    });
  }

  function hydrateCard(raw, now) {
    if (!raw) return window.FSRS.createEmptyCard(now);
    var card = Object.assign({}, raw);
    card.due = new Date(raw.due);
    card.last_review = raw.last_review ? new Date(raw.last_review) : undefined;
    return card;
  }

  function serializeCard(card) {
    return Object.assign({}, card, {
      due: card.due.toISOString(),
      last_review: card.last_review ? card.last_review.toISOString() : null
    });
  }

  function scheduleMission(id, rating) {
    if (!scheduler) return;
    var now = new Date();
    var result = scheduler.next(hydrateCard(state.cards[id], now), now, rating);
    state.cards[id] = serializeCard(result.card);
  }

  function typeset(container) {
    if (window.MathJax && window.MathJax.typesetPromise) {
      window.MathJax.typesetPromise(container ? [container] : undefined).catch(function () {});
    }
  }

  function showView(name) {
    state.view = name;
    elements.tabs.forEach(function (tab) {
      tab.setAttribute('aria-pressed', String(tab.dataset.gameView === name));
    });
    elements.panels.forEach(function (panel) {
      panel.hidden = panel.dataset.gamePanel !== name;
    });
    if (name === 'returns') renderReturnMission();
    saveState();
  }

  function firstIncomplete() {
    for (var index = 0; index < missions.length; index += 1) {
      if (!state.completed[missions[index].id]) return index;
    }
    return missions.length - 1;
  }

  function missionUnlocked(index) {
    return index === 0 || Boolean(state.completed[missions[index - 1].id]);
  }

  function renderMap() {
    var completeCount = missions.filter(function (mission) { return Boolean(state.completed[mission.id]); }).length;
    elements.campaignCount.textContent = completeCount + ' / ' + missions.length;
    elements.map.innerHTML = missions.map(function (mission, index) {
      var complete = Boolean(state.completed[mission.id]);
      var unlocked = missionUnlocked(index);
      var status = complete ? 'Recovered' : (unlocked ? 'Available' : 'Locked');
      var className = complete ? 'is-complete' : (unlocked ? 'is-open' : 'is-locked');
      var score = complete ? '<span>' + escapeHtml(state.completed[mission.id].rating) + '</span>' : '';
      return '<li class="' + className + '">' +
        '<button type="button" data-mission-index="' + index + '" ' + (unlocked ? '' : 'disabled') + '>' +
        '<i>' + (index + 1) + '</i><span><small>' + status + '</small><strong>' + escapeHtml(mission.title) + '</strong>' + score + '</span>' +
        '</button></li>';
    }).join('');
  }

  function startMission(index) {
    if (!missionUnlocked(index)) return;
    currentMission = index;
    state.lastMission = index;
    currentStep = 0;
    integrity = 3;
    mistakes = 0;
    checkpointResets = 0;
    detour = null;
    log = [];
    elements.complete.hidden = true;
    elements.nextMission.hidden = index === missions.length - 1;
    renderMission();
    showView('mission');
  }

  function renderMission() {
    if (currentMission === null) {
      currentMission = Math.min(state.lastMission || firstIncomplete(), missions.length - 1);
    }
    var mission = missions[currentMission];
    var proofStep = mission.steps[currentStep];
    elements.missionNumber.textContent = 'Mission ' + (currentMission + 1) + ' of ' + missions.length;
    elements.missionTitle.textContent = mission.title;
    elements.missionObjective.textContent = mission.objective;
    elements.missionTarget.textContent = mission.target;
    elements.missionFacts.innerHTML = mission.facts.map(function (fact) { return '<li>' + fact + '</li>'; }).join('');
    elements.missionStepLabel.textContent = 'Decision ' + (currentStep + 1) + ' of ' + mission.steps.length;
    elements.missionRating.textContent = ratingLabel();
    renderIntegrity();
    elements.formula.textContent = detour ? detour.formula : proofStep.formula;
    elements.stateCopy.textContent = detour ? detour.copy : proofStep.copy;
    elements.prompt.textContent = detour ? 'This route does not reach the target. Undo it to continue.' : proofStep.prompt;
    elements.tools.innerHTML = detour ? '' : proofStep.moves.map(function (item, index) {
      return '<button type="button" data-move-index="' + index + '">' + item.label + '</button>';
    }).join('');
    elements.undo.disabled = !detour;
    elements.log.innerHTML = log.map(function (item) { return '<li>' + escapeHtml(item) + '</li>'; }).join('');
    typeset(document.getElementById('game-mission'));
  }

  function renderIntegrity() {
    var dots = '';
    for (var index = 0; index < 3; index += 1) dots += '<i class="' + (index < integrity ? 'is-full' : '') + '"></i>';
    elements.integrity.innerHTML = dots;
    elements.integrity.setAttribute('aria-label', integrity + ' of 3 integrity remaining');
  }

  function ratingLabel() {
    if (checkpointResets > 0) return 'Rebuilt run';
    if (mistakes > 0) return 'Recovered run';
    return 'Clean run';
  }

  function handleMove(moveIndex) {
    if (currentMission === null || detour) return;
    var mission = missions[currentMission];
    var proofStep = mission.steps[currentStep];
    var chosen = proofStep.moves[moveIndex];
    if (!chosen) return;

    if (chosen.result === 'productive') {
      log.push(chosen.log);
      elements.feedback.className = 'mission-feedback is-success';
      elements.feedback.textContent = chosen.feedback;
      currentStep += 1;
      if (currentStep >= mission.steps.length) {
        finishMission();
      } else {
        renderMission();
      }
      return;
    }

    if (chosen.result === 'detour') {
      detour = {
        formula: chosen.label,
        copy: chosen.feedback
      };
      log.push('Detour: ' + (chosen.log || chosen.label));
      elements.feedback.className = 'mission-feedback is-detour';
      elements.feedback.textContent = 'Valid detour. It does not advance the target; undo it when you are ready.';
      renderMission();
      return;
    }

    mistakes += 1;
    integrity -= 1;
    elements.feedback.className = 'mission-feedback is-error';
    elements.feedback.textContent = chosen.feedback;
    renderIntegrity();
    elements.missionRating.textContent = ratingLabel();
    if (integrity <= 0) {
      checkpointResets += 1;
      integrity = 3;
      currentStep = 0;
      log = [];
      detour = null;
      elements.feedback.textContent += ' Proof integrity reached zero: returning to this mission’s checkpoint.';
      window.setTimeout(renderMission, 900);
    }
  }

  function undoDetour() {
    if (!detour) return;
    detour = null;
    if (log.length && log[log.length - 1].indexOf('Detour:') === 0) log.pop();
    elements.feedback.className = 'mission-feedback';
    elements.feedback.textContent = 'Returned to the productive route without losing proof integrity.';
    renderMission();
  }

  function finishMission() {
    var mission = missions[currentMission];
    var rating = checkpointResets > 0 ? 'Rebuilt' : (mistakes > 0 ? 'Recovered' : 'Clean');
    state.completed[mission.id] = {
      rating: rating,
      mistakes: mistakes,
      checkpointResets: checkpointResets,
      completedAt: new Date().toISOString()
    };
    state.attempts[mission.id] = (state.attempts[mission.id] || 0) + 1;
    if (scheduler) {
      var fsrsRating = rating === 'Clean' ? window.FSRS.Rating.Good : (rating === 'Recovered' ? window.FSRS.Rating.Hard : window.FSRS.Rating.Again);
      scheduleMission(mission.id, fsrsRating);
    }
    elements.complete.hidden = false;
    elements.completeTitle.textContent = mission.title + ' recovered';
    elements.completeCopy.textContent = mission.reward + ' Run: ' + rating.toLowerCase() + '.';
    elements.nextMission.hidden = currentMission >= missions.length - 1;
    elements.tools.innerHTML = '';
    elements.prompt.textContent = 'Mission complete.';
    elements.formula.textContent = mission.target;
    elements.stateCopy.textContent = mission.reward;
    saveState();
    typeset(document.getElementById('game-mission'));
    elements.complete.scrollIntoView({ behavior: prefersReducedMotion() ? 'auto' : 'smooth', block: 'center' });
  }

  function restartMission() {
    if (currentMission === null) return;
    state.attempts[missions[currentMission].id] = (state.attempts[missions[currentMission].id] || 0) + 1;
    currentStep = 0;
    integrity = 3;
    mistakes = 0;
    checkpointResets = 0;
    detour = null;
    log = [];
    elements.complete.hidden = true;
    elements.feedback.className = 'mission-feedback';
    elements.feedback.textContent = 'Mission restarted.';
    renderMission();
  }

  function completedMissionIds() {
    return missions.filter(function (mission) { return Boolean(state.completed[mission.id]); }).map(function (mission) { return mission.id; });
  }

  function dueMissionIds(now) {
    return completedMissionIds().filter(function (id) {
      return !state.cards[id] || new Date(state.cards[id].due) <= now;
    });
  }

  function relativeDue(date, now) {
    var difference = date.getTime() - now.getTime();
    if (difference <= 60000) return 'now';
    var days = Math.round(difference / 86400000);
    if (days <= 0) return 'later today';
    if (days === 1) return 'tomorrow';
    if (days < 14) return 'in ' + days + ' days';
    return new Intl.DateTimeFormat('en', { day: 'numeric', month: 'short' }).format(date);
  }

  function updateReturnSummary() {
    var now = new Date();
    var due = dueMissionIds(now);
    elements.dueBadge.textContent = due.length;
    elements.returnDue.textContent = due.length;
    var dates = completedMissionIds().map(function (id) { return state.cards[id] ? new Date(state.cards[id].due) : now; }).sort(function (a, b) { return a - b; });
    elements.returnNextDate.textContent = due.length ? 'now' : (dates.length ? relativeDue(dates[0], now) : 'after mission 1');
  }

  function shuffled(items) {
    var copy = items.slice();
    for (var index = copy.length - 1; index > 0; index -= 1) {
      var swap = Math.floor(Math.random() * (index + 1));
      var temp = copy[index]; copy[index] = copy[swap]; copy[swap] = temp;
    }
    return copy;
  }

  function renderReturnMission() {
    updateReturnSummary();
    if (!scheduler) {
      elements.returnLabel.textContent = 'Scheduler unavailable';
      elements.returnQuestion.textContent = 'FSRS could not load. The campaign itself remains playable.';
      elements.returnOptions.innerHTML = '';
      return;
    }
    var due = dueMissionIds(new Date());
    if (!due.length) {
      returnMission = null;
      elements.returnLabel.textContent = 'No mission due';
      elements.returnQuestion.textContent = completedMissionIds().length ? 'Your next return mission will unlock when FSRS schedules it.' : 'Complete the first campaign mission to start the return schedule.';
      elements.returnOptions.innerHTML = '';
      elements.returnFeedback.textContent = '';
      elements.returnNext.hidden = true;
      return;
    }
    returnMission = due[0];
    returnAttempts = 0;
    var mission = missions.filter(function (item) { return item.id === returnMission; })[0];
    returnOptions = shuffled(mission.review.options.map(function (option) { return { text: option[0], correct: option[1] }; }));
    elements.returnLabel.textContent = 'Return mission · ' + mission.short;
    elements.returnQuestion.textContent = mission.review.question;
    elements.returnOptions.innerHTML = returnOptions.map(function (option, index) {
      return '<button type="button" data-return-option="' + index + '">' + option.text + '</button>';
    }).join('');
    elements.returnFeedback.textContent = '';
    elements.returnNext.hidden = true;
    typeset(document.getElementById('game-returns'));
  }

  function handleReturn(index) {
    if (!returnMission) return;
    var chosen = returnOptions[index];
    var button = elements.returnOptions.querySelector('[data-return-option="' + index + '"]');
    if (!chosen || !button || button.disabled) return;
    var mission = missions.filter(function (item) { return item.id === returnMission; })[0];
    if (!chosen.correct) {
      returnAttempts += 1;
      button.disabled = true;
      button.classList.add('is-wrong');
      elements.returnFeedback.textContent = 'That route does not survive. Use the remaining choices.';
      return;
    }
    button.classList.add('is-correct');
    elements.returnOptions.querySelectorAll('button').forEach(function (item) { item.disabled = true; });
    var rating = returnAttempts === 0 ? window.FSRS.Rating.Good : window.FSRS.Rating.Hard;
    scheduleMission(returnMission, rating);
    elements.returnFeedback.textContent = (returnAttempts === 0 ? 'Recovered cleanly. ' : 'Recovered after a correction. ') + mission.review.explanation;
    elements.returnNext.hidden = false;
    saveState();
    typeset(elements.returnFeedback);
  }

  function escapeHtml(value) {
    return String(value).replace(/[&<>'"]/g, function (character) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[character];
    });
  }

  function prefersReducedMotion() {
    return window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }

  elements.tabs.forEach(function (tab) {
    tab.addEventListener('click', function () {
      if (tab.dataset.gameView === 'mission') renderMission();
      showView(tab.dataset.gameView);
    });
  });
  elements.map.addEventListener('click', function (event) {
    var button = event.target.closest('[data-mission-index]');
    if (button && !button.disabled) startMission(Number(button.dataset.missionIndex));
  });
  elements.tools.addEventListener('click', function (event) {
    var button = event.target.closest('[data-move-index]');
    if (button) handleMove(Number(button.dataset.moveIndex));
  });
  elements.returnOptions.addEventListener('click', function (event) {
    var button = event.target.closest('[data-return-option]');
    if (button) handleReturn(Number(button.dataset.returnOption));
  });
  elements.undo.addEventListener('click', undoDetour);
  elements.restart.addEventListener('click', restartMission);
  elements.leave.addEventListener('click', function () { showView('campaign'); });
  elements.returnMap.addEventListener('click', function () { showView('campaign'); });
  elements.nextMission.addEventListener('click', function () { startMission(Math.min(currentMission + 1, missions.length - 1)); });
  elements.returnNext.addEventListener('click', renderReturnMission);
  elements.reset.addEventListener('click', function () {
    if (!window.confirm('Reset the entire proof campaign and its FSRS schedule on this device?')) return;
    localStorage.removeItem(storageKey);
    state = defaultState();
    currentMission = null;
    renderMap();
    showView('campaign');
  });

  renderMap();
  updateReturnSummary();
  showView(state.view === 'mission' ? 'campaign' : state.view);
})();
