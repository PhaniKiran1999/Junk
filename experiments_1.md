Okay, here's a concise version of the Experimental Setup section:

**4.1. Experimental Setup**

To demonstrate our methodology, we constructed a synthetic Knowledge Graph (KG) modeling an employee domain.

*   **Schema & Instances:** The KG comprises classes `:Person`, `:Company`, `:City` and properties `:worksFor`, `:locatedIn`, `:livesIn`. It includes five instances: `Alice` (:Person), `Bob` (:Person), `CorpX` (:Company), `StartupY` (:Company), `Metroville` (:City).
*   **Induced Uncertainty:** We simulated incompleteness by omitting three facts: (1) the target of `Bob`'s `:worksFor` relation, (2) the target of `Alice`'s `:livesIn` relation, and (3) the target of `Bob`'s `:livesIn` relation.
*   **Resulting Unknowns:** This setup defines two potential unknown nodes (`un:Node1` [likely :Company], `un:Node2` [likely :City]) and three unknown edges (`un:Edge1` [`Bob`-`:worksFor`-`un:Node1`], `un:Edge2` [`Alice`-`:livesIn`-`un:Node2`], `un:Edge3` [`Bob`-`:livesIn`-???]). Consequently, the set sizes for uncertainty calculation are `|Sn|=2` (unknown nodes) and `|Se|=3` (unknown edges).

**** weights importance
The relative weights assigned to CIR/PIR, Timeliness, and Subgraph Importance when calculating the final Imp score can be tuned based on evaluation goals; for instance, prioritizing Subgraph Importance reflects a focus on current utility, while higher Timeliness weights emphasize data freshness.


4.2. Importance Metric Application
We applied our multi-faceted importance metrics (CIR, PIR, Timeliness, Subgraph Importance) to all KG elements. Values were estimated based on plausible domain roles (e.g., :Person having high CIR/Subgraph Importance). A synthesized Importance Score (Imp, normalized 0-1) was derived for each known entity/relation and estimated for unknown elements based on their expected type and context.
Detailed Imp scores are presented in Table 1. Notably, core elements like :Person instances and the :worksFor property received high scores, while peripheral elements like :City and :livesIn scored lower. This pattern extended to unknowns: the uncertainty surrounding Bob's employment (un:Node1, un:Edge1) was estimated as highly important (Imp ≈ 0.75-0.80), whereas location uncertainties (un:Node2, un:Edge2, un:Edge3) yielded lower estimated importance (Imp ≈ 0.50-0.55).
4.3. Uncertainty Quantification: Adapted I-Score
We calculated the Adapted I-Score using the estimated importance (Imp) scores of unknown elements, quantifying importance-weighted uncertainty. Using the simplified formula with uniform probabilities:
I_Score_adapted = log(|Sn|) * Avg(Imp_unknown_nodes) + log(|Se|) * Avg(Imp_unknown_edges)
With |Sn|=2, |Se|=3, Avg(Imp_unknown_nodes)=0.625, and Avg(Imp_unknown_edges)≈0.617 (derived from Table 1), the calculation is:
I_Score_adapted = (log2(2) * 0.625) + (log2(3) * 0.617) ≈ (1 * 0.625) + (1.585 * 0.617) ≈ 1.603.
This score represents the total uncertainty, weighted by the average estimated importance of the missing nodes and edges.
