Okay, here's a concise version of the Experimental Setup section:

**4.1. Experimental Setup**

To demonstrate our methodology, we constructed a synthetic Knowledge Graph (KG) modeling an employee domain.

*   **Schema & Instances:** The KG comprises classes `:Person`, `:Company`, `:City` and properties `:worksFor`, `:locatedIn`, `:livesIn`. It includes five instances: `Alice` (:Person), `Bob` (:Person), `CorpX` (:Company), `StartupY` (:Company), `Metroville` (:City).
*   **Induced Uncertainty:** We simulated incompleteness by omitting three facts: (1) the target of `Bob`'s `:worksFor` relation, (2) the target of `Alice`'s `:livesIn` relation, and (3) the target of `Bob`'s `:livesIn` relation.
*   **Resulting Unknowns:** This setup defines two potential unknown nodes (`un:Node1` [likely :Company], `un:Node2` [likely :City]) and three unknown edges (`un:Edge1` [`Bob`-`:worksFor`-`un:Node1`], `un:Edge2` [`Alice`-`:livesIn`-`un:Node2`], `un:Edge3` [`Bob`-`:livesIn`-???]). Consequently, the set sizes for uncertainty calculation are `|Sn|=2` (unknown nodes) and `|Se|=3` (unknown edges).


The relative weights assigned to CIR/PIR, Timeliness, and Subgraph Importance when calculating the final Imp score can be tuned based on evaluation goals; for instance, prioritizing Subgraph Importance reflects a focus on current utility, while higher Timeliness weights emphasize data freshness.
