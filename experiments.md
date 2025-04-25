Okay, here's how the previous explanation and table could be framed within the **Experiments** section of a research paper focused on KG evaluation, specifically demonstrating the calculation and utility of the importance-weighted I-Score.

---

**4. Experiments**

**4.1. Experimental Setup**

To evaluate the proposed importance metrics and their integration into an uncertainty measure, we conducted experiments on a synthetically generated, illustrative Knowledge Graph (KG). The goal is to demonstrate how our multi-faceted importance assessment provides a more nuanced understanding of KG uncertainty compared to simpler approaches.

*   **KG Domain:** We instantiated a small KG representing a common enterprise scenario involving employees, companies, and locations.
*   **Schema:** The KG utilizes three classes: `:Person`, `:Company`, `:City`, and three properties: `:worksFor` (Domain: `:Person`, Range: `:Company`), `:locatedIn` (Domain: `:Company`, Range: `:City`), and `:livesIn` (Domain: `:Person`, Range: `:City`).
*   **Instance Data & Uncertainty:** The KG was populated with five instances: `Alice` (:Person), `Bob` (:Person), `CorpX` (:Company), `StartupY` (:Company), and `Metroville` (:City). To simulate real-world incompleteness, we introduced specific points of uncertainty:
    *   The `:worksFor` relationship for `Bob` is unknown, implying a missing edge and potentially an unknown `:Company` instance.
    *   The `:livesIn` relationship for `Alice` is unknown, implying a missing edge and potentially an unknown `:City` instance.
    *   The `:livesIn` relationship for `Bob` is unknown.
    For the purpose of this experiment, we denote the potential unknown company as `un:Node1`, the potential unknown city as `un:Node2`, and the missing edges as `un:Edge1` (`Bob` `:worksFor` `un:Node1`), `un:Edge2` (`Alice` `:livesIn` `un:Node2`), and `un:Edge3` (`Bob` `:livesIn` ???). This setup yields `|Sn|=2` unknown nodes and `|Se|=3` unknown edges.

**4.2. Importance Metric Application**

We applied the proposed importance factors—Class Instantiation Ratio (CIR), Property Instantiation Ratio (PIR), Timeliness, and Subgraph Importance (estimated via query frequency)—to the entities and relations within our experimental KG.

*   **Metric Estimation:** For this illustrative experiment, metric values were assigned based on plausible scenarios (e.g., `:Person` having higher CIR and Subgraph Importance than `:City`; `:worksFor` having higher PIR and Subgraph Importance than `:livesIn`). Timeliness was assigned per instance. All metrics were normalized to a [0, 1] scale, where higher values indicate greater importance or relevance.
*   **Node/Edge Importance (`Imp`) Score:** A synthesized Importance Score (`Imp`) was derived for each known class, property, and instance, reflecting its overall significance based on the contributing metrics. Crucially, `Imp` scores were also *estimated* for the unknown nodes and edges based on their expected type and context (e.g., the `Imp` for `un:Node1` was based on the expected importance of a `:Company` instance needed to resolve a `:worksFor` link for an important `:Person`).
*   **Results Summary:** The calculated and estimated importance scores are detailed in Table 1. As expected, core entities like `:Person` instances (`Alice`, `Bob`) and structural relationships like `:worksFor` received high `Imp` scores, while peripheral entities like `:City` and optional relationships like `:livesIn` received lower scores. The estimated importance for unknowns reflects this; `un:Node1` and `un:Edge1` (related to Bob's employment) were estimated as highly important, while `un:Node2`, `un:Edge2`, and `un:Edge3` (related to living locations) were deemed less critical.

**(Table 1 would be inserted here - identical to the table in the previous response)**

**4.3. Uncertainty Quantification: Adapted I-Score**

We utilized the calculated importance scores to compute the Adapted I-Score, our proposed measure of importance-weighted KG uncertainty. Following the formulation presented in Section X [Reference to where the formula is formally defined earlier in the paper], and assuming uniform probabilities for unknowns (`pi = 1/|Sn|`, `qj = 1/|Se|`) for simplicity in this demonstration:

`I_Score_adapted = log(|Sn|) * Avg(Imp_unknown_nodes) + log(|Se|) * Avg(Imp_unknown_edges)`

*   **Calculation Steps:**
    1.  Identify unknowns: `|Sn| = 2`, `|Se| = 3`.
    2.  Calculate average importance of unknowns from Table 1:
        *   `Avg(Imp_unknown_nodes)` = (`Imp(un:Node1)` + `Imp(un:Node2)`) / 2 = (0.75 + 0.50) / 2 = 0.625
        *   `Avg(Imp_unknown_edges)` = (`Imp(un:Edge1)` + `Imp(un:Edge2)` + `Imp(un:Edge3)`) / 3 = (0.80 + 0.55 + 0.50) / 3 ≈ 0.617
    3.  Calculate log terms (base 2): `log2(2) = 1`, `log2(3) ≈ 1.585`.
    4.  Compute final score: `I_Score_adapted = (1 * 0.625) + (1.585 * 0.617) ≈ 1.603`.

**4.4. Baseline Comparison and Discussion**

To contextualize the result, we compare the `I_Score_adapted` to the original I-Score formulation (Dou et al., 2023) which uses constant weights (`cn`, `ce`) for node and edge importance. Using the example weights `cn = ce = 0.5`:

`I_Score_original = log2(2) * 0.5 + log2(3) * 0.5 = (1 * 0.5) + (1.585 * 0.5) ≈ 1.293`.

*   **Interpretation:** The `I_Score_adapted` (1.603) is significantly higher than the baseline `I_Score_original` (1.293). This difference arises because the average estimated importance of the unknown elements in our KG (`Avg(Imp_nodes)`=0.625, `Avg(Imp_edges)`=0.617) exceeds the baseline assumption of 0.5. Our method correctly identifies that the specific missing information (particularly Bob's employment details, driving up the average importance) represents a higher degree of *valuable* uncertainty than would be assumed by an unweighted model.
*   **Conclusion:** This experiment demonstrates that the Adapted I-Score, informed by multi-faceted node and edge importance metrics, provides a more sensitive and representative measure of KG uncertainty. It moves beyond merely quantifying the *amount* of missing information to reflecting the *potential impact or value* of resolving that uncertainty, thereby offering a more actionable metric for guiding KG completion, refinement, and quality assessment efforts. Priority can be given to resolving unknowns with higher estimated importance scores, which contribute more significantly to the overall `I_Score_adapted`.

---
