# Master Record of Work — Lingbo Zeng

**What this document is.** A complete, itemised inventory of work done: systems built, decisions taken, methods used, results obtained. It is the source file that a CV, a résumé, an SOP, or an interview answer is later *cut down from*. It is not itself any of those things.

**What this document is not.** Not a personal statement. There is no narrative of growth, no motivation, no reflection on what any of it meant. Where a "why" appears it is an engineering or design rationale — why this model, why this architecture, why this interaction pattern — not a personal one.

**Working state.** Built from the CV `Lingbo_Zeng_CV_EN_drone.docx` and the 7 mentor comments in it (full text + translation: `mentor-comments-extracted.md`).

---

## §0. Conventions

Three markers are used throughout. They matter — read them before anything else.

| Marker | Meaning |
|---|---|
| **`◆ ON RECORD`** | Stated in the current CV. Carried forward verbatim or lightly re-worded. Verified against the source document. |
| **`▢ FILL`** | **Nothing has been invented here.** A slot for a fact only you hold — a model name, a number, a decision, a date. Each is written as a sharp, answerable question rather than a vague prompt. Fill or explicitly strike it. |
| **`⟡ M#n`** | Explicitly requested by mentor comment #n. These are the load-bearing gaps — the review said this material is missing and its absence is what makes the entry read as unprofessional. |

**The one rule for this file:** never fill a `▢` with something plausible. An invented embedding model or an estimated accuracy number is worse than a blank, because a blank costs you nothing at interview and an invention costs you the whole application. If you don't remember, write `UNKNOWN — need to check repo/commit history` and move on. Several `▢` items below can be answered by reading your own git log rather than from memory.

**Suggested working order.** §4.1 (NewsFlick) and §4.2 (PillWise) carry the most mentor-flagged weight and should be filled first; §10 gives the full prioritised queue.

---

## §1. Mentor review — disposition of every comment

| # | Anchor | Ask | Where handled |
|---|---|---|---|
| 0 | Coursework line | Adjust per target program | §3.3 — full course inventory kept so the line can be re-cut per application |
| 1 | Test scores | Move scores/certs to their own section | §2 — done, split out of Education |
| 2 | NewsFlick | Clustering stack · anti-hallucination · cross-source objectivity · UI transparency + card rationale · optimization | §4.1.4B, §4.1.5, §4.1.6, §4.1.7, §4.1.8 |
| 3 | NewsFlick (reply) | Show thinking → implementation → maintenance/upgrade | Structural arc applied across §4.1, §4.2, §5.1; upgrade loops at §4.1.11, §4.2.9 |
| 4 | PillWise | Retitle to Engineer · algorithm selection experiments · accuracy · front/back data flow | §4.2 header, §4.2.4, §4.2.5, §4.2.6 |
| 5 | SenseTime | Add process and results; learning↔practice loop | §4.3 |
| 6 | Interviewer Society | Tie interviewing skill to product user research | §7.4 |

Two things the mentor said that are easy to miss on a first read:

1. **"online exposure"** is mentioned for *both* NewsFlick and PillWise. Coverage, launch posts, download numbers, and public traction are treated as assets here — §4.1.12 and §4.2.10 collect them. They are currently absent from the CV entirely.
2. **PillWise is described as an embedded-systems project** (`嵌入式系统`). The current CV bullet for PillWise mentions no hardware at all. Either there is a hardware component that has been dropped from the record, or the mentor inferred it from the ESP32S3/Arduino line in Skills. Resolve this at §4.2.7 — if there is a device, it is a significant omission.

---

## §2. Credentials, scores and certifications
> ⟡ **M#1** — split into a standalone section, out from under Education.

### 2.1 Identity block
- **◆ ON RECORD** Lingbo Zeng
- **◆ ON RECORD** lbzeng@connect.ust.hk · +852-9751-9306 · Hong Kong

▢ FILL — the professional-presence set, since the mentor twice notes online exposure:
- [ ] GitHub URL, and which repos are public and presentable
- [ ] Personal site / portfolio URL
- [ ] LinkedIn
- [ ] Google Scholar or ORCID (relevant once the IROS submission resolves)
- [ ] App Store developer page (Decode: Veritas, PillWise)

### 2.2 Standardised tests
- **◆ ON RECORD** GRE: Verbal 166 (96th %ile) · Quantitative 170 (91st %ile) · Analytical Writing 4.0
- **◆ ON RECORD** TOEFL: 6.0 / 6 (new band scale) — stated as 118/120 on the legacy scale
- **◆ ON RECORD** CEFR C2

▢ FILL / verify:
- [ ] Test dates for GRE and TOEFL, and their expiry dates (both are 5-year validity — check they still cover your application cycle)
- [ ] Percentiles exactly as printed on your official score report. Percentile bands shift between reporting cohorts, so quote the report rather than a remembered figure
- [ ] The TOEFL line currently carries **two scales at once**. This is defensible while the new 1–6 band is unfamiliar to readers, but decide on one primary and confirm the mapping against the official ETS concordance rather than an estimate. If the 118/120 is a conversion rather than a score you actually received, do not present it as a score
- [ ] AW 4.0 is the one number below the rest of the profile. Decide once: report it (it will be on the official report anyway, so omission from the CV is not concealment), and if any target program publishes an AW threshold, check it

### 2.3 Certifications and other credentials
▢ FILL — collect anything not yet recorded anywhere:
- [ ] Cantonese, Mandarin, English — any formal certification behind the self-assessed levels
- [ ] Technical certifications (cloud, ML, safety, drone/UAV pilot licensing — the latter would be directly relevant to the SLAM work)
- [ ] Ethics / human-subjects research training certificates (relevant to §5.2, which ran a controlled study with human participants)

---

## §3. Education

### 3.1 Degree
- **◆ ON RECORD** Hong Kong University of Science and Technology (HKUST)
- **◆ ON RECORD** B.Sc., Integrative Systems and Design
- **◆ ON RECORD** Expected 2027

▢ FILL:
- [ ] Start date / matriculation year
- [ ] GPA and scale, plus major GPA if it is stronger; class rank or percentile band if HKUST issues one
- [ ] Any concentration, track, or minor within Integrative Systems and Design
- [ ] Exchange, visiting, or summer-school terms elsewhere
- [ ] Scholarships or admission-based awards (distinct from the competition awards in §6)
- [ ] Thesis / capstone: title, supervisor, current status

### 3.2 Program characterisation
One line is worth writing here and reusing, because "Integrative Systems and Design" does not self-explain to an overseas reader. Admissions committees outside Hong Kong will not know whether this is engineering, design, or a general studies degree.

▢ FILL:
- [ ] The one-sentence accurate description of the program's scope and its engineering content
- [ ] Which school/department it is administered under
- [ ] Core required sequence — this is what substantiates that it is a technical degree

### 3.3 Course inventory
> ⟡ **M#0** — the coursework line gets re-cut per application. That requires a complete list to cut *from*.

**◆ ON RECORD** — currently listed: Human-Robot Interaction · IoT · Rapid Prototyping · SLAM

▢ FILL — full table, every technical course taken. Keep this exhaustive even though only 4–6 ever appear on a given CV:

| Course code | Title | Term | Grade | Substantive content (2–3 keywords) | Which application profile it supports |
|---|---|---|---|---|---|
| | | | | | robotics / CV / HCI / ML / systems |

Fill particularly: mathematics (linear algebra, probability, optimisation), signals, computer vision, machine learning, embedded/real-time systems, and anything with a substantial project component. For a robotics or CV-focused application, the math and CV coursework matters more than the listed HRI/IoT courses, and the current line does not show it.

Also record, per course, any **project artefact** — several of the §6 awards and §5 projects likely originated as coursework, and that linkage is worth knowing when writing.

---

## §4. Professional work

---

### §4.1 — NewsFlick Ltd
**Co-Founder / Product & AI Engineer · 2025 – Present**
> ⟡ **M#2, M#3** — the heaviest revision target in the review. The mentor's judgement: strong project, has public exposure, but *"the actual development process is unclear and it doesn't read as professional enough."* Everything below §4.1.3 exists to fix that.

#### 4.1.1 Snapshot
- **◆ ON RECORD** AI-native news platform built on radical transparency
- **◆ ON RECORD** news-flick.com
- **◆ ON RECORD** Role: Co-Founder / Product & AI Engineer
- **◆ ON RECORD** Legal entity exists — "Ltd" — so this is an incorporated company, not a side project

▢ FILL — company facts:
- [ ] Incorporation date and jurisdiction; your equity/founder status; whether you are a director
- [ ] Team size and composition over time; how many people you worked alongside; whether anyone reported to you
- [ ] Funding status and source (see §6.4 — the HKSTP Ideation HK$100K and Dream Builder may attach here; if so, say so explicitly, because a funded company reads differently from an unfunded one)
- [ ] Current operating status: live and serving users / in beta / paused
- [ ] Launch date of the public product, distinct from the founding date

#### 4.1.2 Problem framing
> ⟡ **M#3** — the "thinking" end of the thinking→implementation→maintenance arc. This subsection is that link.

The product's stated commitment is **radical transparency**. That is a strong claim and it should be traceable to specific mechanisms in §4.1.4 through §4.1.7 — otherwise it reads as a slogan. The reader's test is: *which lines of the architecture make the word "transparency" true?*

▢ FILL:
- [ ] The specific failure of existing news products you set out to address. State it as a mechanism, not a sentiment — e.g. "readers cannot tell which claims in a story are contested and which are agreed across sources," rather than "news is biased"
- [ ] What "radical transparency" means **operationally**. Complete this sentence concretely: *"A user of NewsFlick can see X, which a user of any other news app cannot see."*
- [ ] Why an AI-native architecture is required for that, rather than editorial curation. This is the question that separates the project from a media startup with an LLM bolted on
- [ ] Target user and the evidence they exist — link forward to the interviews in §4.1.6
- [ ] What you decided **not** to build, and why. Scope negatives are strong signal and cost nothing

#### 4.1.3 Ownership boundary
State plainly which parts you personally built versus co-owned versus directed. On a co-founded project the reader silently discounts everything unless the boundary is explicit, and an honest narrow claim reads stronger than an ambiguous broad one.

▢ FILL, per component:

| Component | Sole author | Co-built (with whom) | Directed / specified only |
|---|---|---|---|
| Ingestion | | | |
| Clustering / retrieval | | | |
| Summarization | | | |
| Perspective comparison | | | |
| Frontend implementation | | | |
| UI/UX design | | | |
| Infrastructure / deploy | | | |
| Decode: Veritas | | | |

#### 4.1.4 The content pipeline
- **◆ ON RECORD** Built end-to-end LLM-powered content pipeline: **ingestion → semantic clustering → summarization → perspective comparison**, optimized for card-based, video-first delivery.

That one CV line covers four subsystems. Each is decomposed below.

---

##### A. Ingestion

*Function:* acquire source articles, normalise them into a common representation, and make them available to the clustering stage.

▢ FILL:
- [ ] **Source set.** How many sources, which ones, and by what criterion selected. This is not a trivia question — a perspective-comparison product's validity rests entirely on the spread of its sources. If sources were chosen to span political, geographic, or ownership-structure diversity, the *selection method* is itself a design contribution and should be stated
- [ ] **Acquisition mechanism.** RSS, publisher APIs, scraping, an aggregator API. Different answers imply very different engineering
- [ ] **Scheduling.** Poll cadence, and whether it is uniform or adaptive by source
- [ ] **Normalisation.** Boilerplate stripping, main-content extraction, metadata schema (publisher, author, publish timestamp, canonical URL, section)
- [ ] **Deduplication at ingest** — syndicated wire copy is the dominant duplicate source in news and will otherwise pollute clusters. How was near-duplicate detection done (hashing, shingling, embedding threshold)?
- [ ] **Language handling.** Monolingual or multilingual; if multilingual, whether translation happens before or after embedding — this materially affects clustering
- [ ] **Volume and latency.** Articles per day; median time from publication to availability in-product
- [ ] **Storage.** Database and schema; whether raw source text is retained (it must be, for the citation guarantees in §4.1.5)
- [ ] **Reliability.** Retry/backoff, dead-source detection, what happens when a source changes its HTML
- [ ] **Legal posture.** robots.txt compliance, terms-of-service position, licensing. Worth having an answer ready — an interviewer at a media-adjacent lab will ask

---

##### B. Semantic clustering
> ⟡ **M#2.1** — named explicitly: *"specify the embedding model used, the clustering algorithm, what retrieval algorithm, and how you solved streaming clustering."* Four separate answers required. This is the single most important gap in the document.

*Function:* group articles that cover the same underlying event, so that the perspective-comparison stage has a set of independent accounts of one thing to compare.

▢ FILL — **1. Embedding model:**
- [ ] Exact model name and version, embedding dimension, and where it runs (hosted API vs. local)
- [ ] What text is embedded: headline only, headline + lede, full body, or chunked-and-pooled. Full-article embeddings behave very differently from headline embeddings for event clustering — the choice is substantive
- [ ] Alternatives considered and why this one won. **The comparison is the answer the mentor wants, not the name.** Cost, latency, quality on your data, context length, multilingual support — say which criterion decided it
- [ ] Any evaluation you ran to pick it, even informal (a hand-labelled set of N article pairs is a legitimate answer and reads far better than "chose the standard one")

▢ FILL — **2. Retrieval / index:**
- [ ] **◆ ON RECORD** FAISS appears in your Skills line — confirm it is used here and say **which index type**: Flat, IVF, IVFPQ, HNSW. This distinction is the difference between a toy and a system, and the mentor is asking precisely because "we used FAISS" alone signals nothing
- [ ] Distance metric (cosine / inner product / L2) and whether vectors are normalised
- [ ] Index size — number of vectors — and query latency at that size
- [ ] Index parameters and how tuned: `nlist`/`nprobe` for IVF, `M`/`efSearch` for HNSW; recall/latency tradeoff chosen and measured
- [ ] Whether the index is rebuilt or updated incrementally, and how deletions/expiry are handled (news has a hard recency horizon — old vectors must age out or the index grows without bound)

▢ FILL — **3. Clustering algorithm:**
- [ ] Exact algorithm: HDBSCAN, agglomerative with a linkage criterion, k-means, connected-components over a similarity graph, online centroid assignment, or a custom rule
- [ ] Similarity threshold(s), and — importantly — **how the threshold was set**. Grid search against labelled pairs, manual inspection, elbow method? An arbitrary 0.8 is a red flag to a technical reader; a tuned 0.8 is a contribution
- [ ] How the number of clusters is determined, or why the method doesn't need it specified
- [ ] Minimum cluster size, and what happens to singleton articles

▢ FILL — **4. Streaming clustering** *(the mentor named this specifically — it is the hardest part and the most credit-bearing):*
- [ ] How a newly ingested article is assigned: nearest-centroid within a threshold, k-NN vote, re-clustering of a recent window?
- [ ] **Cluster birth** — when does a new article start a new cluster rather than join one?
- [ ] **Cluster death / expiry** — when does a story stop accepting new articles? News stories have a lifecycle; without an expiry rule, a long-running topic ("elections") swallows every related event
- [ ] **Cluster ID stability** — if a user has seen a story card, its identity must survive re-clustering. How is that guaranteed? This is the classic streaming-clustering failure and if you solved it, say how
- [ ] **Cluster merging and splitting** — two clusters turn out to be the same event; one cluster turns out to be two. Detected how? Handled how?
- [ ] **Drift** — do centroids update as a story develops, and does that let a cluster wander off topic over days?
- [ ] Re-clustering cadence, if any: full periodic rebuild vs. pure online
- [ ] **Cold start** — behaviour for a breaking event with one source

▢ FILL — **5. Evaluation of clustering quality** *(the part that turns all of the above from a description into an engineering claim):*
- [ ] How you know the clusters are correct. Hand-labelled evaluation set (how many articles / events)? Purity, NMI, pairwise F1, or manual audit rate?
- [ ] Measured error rate, and the direction of the errors (over-merging vs. over-splitting — these have opposite product consequences: over-merging produces a card comparing perspectives on *different events*, which is a correctness failure users will notice)
- [ ] Known failure modes, stated concretely. E.g. same entity/different event; developing stories vs. retrospectives; opinion pieces clustering with the reporting they respond to
- [ ] Whether any of the above changed after launch on real traffic — this feeds §4.1.11

---

##### C. Summarization

*Function:* produce the per-story text that appears on a card, from a cluster of source articles.

▢ FILL:
- [ ] Which LLM(s), which version, and why. If you route between models by task or cost, that routing logic is itself worth stating
- [ ] Unit of summarization: per article, per cluster, or hierarchical (summarise each article, then summarise the summaries). Hierarchical is the more defensible design at cluster scale and if you did it, say so — it also bounds context cost
- [ ] Prompt architecture: system prompt strategy, few-shot or zero-shot, whether structured output / JSON schema / tool-use is enforced
- [ ] Output contract: length limits, required fields, tone constraints, and how the format was matched to the card and video formats downstream
- [ ] Context handling: how a cluster larger than the context window is handled; how sources are ordered or selected when they must be truncated (and whether that selection introduces bias — a real concern for this product specifically)
- [ ] Determinism: temperature, seeding, and whether the same cluster produces a stable summary across runs. For a transparency-branded product, instability is a product bug, not just an engineering one
- [ ] Cost and latency per story, and what you did about them (→ §4.1.8)

---

##### D. Perspective comparison
> ⟡ **M#2.2** — *"objectivity when comparing different information sources."*

*Function:* surface how accounts of the same event differ across sources. This is the product's differentiator and therefore the component whose design must be most rigorous.

▢ FILL — **definitions first:**
- [ ] What is a "perspective" **operationally**? Source-level political lean from an external rating? A stance extracted per article by the model? A framing dimension? Fact-level disagreement? These are four different products and the reader cannot tell which one you built
- [ ] What unit is compared: whole articles, extracted claims, framing labels, or entity sentiment?
- [ ] What the user is shown: a side-by-side, a labelled spectrum, a claim-level agreement/disagreement map, a highlighted-difference view?

▢ FILL — **objectivity safeguards** (the mentor's actual concern — a system that judges bias must account for its own):
- [ ] Does the system assert *which* account is correct, or does it only map the space of accounts? The second is far more defensible and, if that was a deliberate decision, it is a genuine design contribution — state it as one
- [ ] Where do source-lean labels come from? If from an external rating body (AllSides, Ad Fontes, MBFC), name it and say what its limitations are. If from the model, that is a much stronger claim requiring validation
- [ ] The LLM carries its own priors. What was done about it? Symmetric prompting, source-blind analysis (stripping publisher identity before the model sees the text — a strong technique if you used it), label-order randomisation, self-consistency across runs?
- [ ] Validation: did you ever check whether the perspective labels were *right*? Against what? Even a small hand-audit is a real answer
- [ ] Handling of the case where sources **agree** — a comparison product must not manufacture disagreement to fill the template. If you built an explicit "sources broadly concur" state, that is a mature design decision and worth naming
- [ ] Handling of the asymmetric case: one source reports a fact no other source carries. Suppressed, flagged, or shown?

---

##### E. Delivery layer
- **◆ ON RECORD** Optimized for card-based, video-first delivery

▢ FILL:
- [ ] Whether video is generated automatically from summaries, and if so, the pipeline (TTS engine, visual assembly, rendering, cost per clip, generation latency)
- [ ] Feed construction: how stories are ranked and selected for a given user; personalised or uniform; how recency and importance are weighted
- [ ] Platform: web / iOS / Android, and what you personally built
- [ ] **◆ ON RECORD** Tech stack — Skills line lists React/Next.js and Swift/SwiftUI; specify which was used for NewsFlick vs. PillWise vs. Decode: Veritas, because as written a reader cannot attribute any of it
- [ ] Hosting, CI/CD, and how deployment works

#### 4.1.5 Hallucination control
> ⟡ **M#2.2** — *"the LLM's anti-hallucination design."* Named as a distinct requirement. For a product branded on transparency this is the central engineering claim, and its absence is conspicuous.

▢ FILL:
- [ ] **The extraction/generation boundary.** Which parts of the output are constrained to text present in sources versus freely generated? A clear boundary is the strongest single answer here
- [ ] **Attribution.** Is every claim in a summary traceable to a source article? At what granularity — story, paragraph, sentence, or span? Enforced how (post-hoc verification, structured output requiring a source ID per claim, retrieval-grounded generation)?
- [ ] **Verification pass.** Is there a second model call that checks the summary against sources? Entailment checking? Rejection and regeneration on failure?
- [ ] **Abstention.** What does the system do when it cannot summarise reliably — thin cluster, contradictory sources, paywalled bodies? A designed abstention path is a signal of maturity; if there is none, that is a known limitation worth stating honestly
- [ ] **Named entities and numbers** get special treatment in most serious pipelines because they are where hallucination is most damaging and most detectable. Did yours?
- [ ] **Measurement.** How often does it fail? Any hand-audit — even 100 summaries scored by you — produces a number, and a number is what turns this from an assertion into evidence. **If you have no measurement, say so and note it as future work rather than implying one exists**
- [ ] **Human review**: is any output reviewed before publication, and at what rate?
- [ ] **User-facing correction path** — can a reader flag an error, and what happens then? This is where §4.1.5 meets §4.1.11

#### 4.1.6 UI/UX design
- **◆ ON RECORD** Led UI/UX design for the product: interaction flows, card-based information architecture, visual interface design
- **◆ ON RECORD** Iterated based on user interviews and surveys

> ⟡ **M#2.3** — *"mention the original intent behind the card-based design — user cognition / making multi-viewpoint comparison easy."* The mentor is saying: the card format currently reads as an aesthetic choice; it needs to read as a reasoned one.

▢ FILL — **rationale for the card architecture** (answer these three and the point is made):
- [ ] What cognitive problem does a card solve here? The candidate answer, which you should confirm or replace with your actual reasoning: comparing multiple accounts of one event imposes high working-memory load; a card bounds one event into one unit so comparison happens *within* a fixed frame instead of across scrolling text
- [ ] Why cards specifically make **multi-perspective comparison** easier than an article list. What is co-visible on a card that would otherwise require the reader to hold something in memory?
- [ ] What information hierarchy is inside a card, and what was deliberately excluded from it. Exclusions demonstrate the reasoning better than inclusions

▢ FILL — **process:**
- [ ] Interaction flows designed: enumerate the actual flows (onboarding, browse feed, open story, expand perspectives, view sources, share). For each: the user's goal, the steps, and the friction removed
- [ ] Fidelity progression: sketches → wireframes → Figma prototypes → built. What survived from first design to shipped, and what didn't
- [ ] Design system: type scale, colour, spacing, components, dark mode, accessibility (contrast, dynamic type, screen-reader labels)
- [ ] Responsive/platform variants

▢ FILL — **user interviews and surveys** *(currently the vaguest claim in the entire CV — "iterated based on user interviews and surveys" with no N, no method, no finding, and no resulting change. It reads as decoration. Three numbers and one example fix it):*
- [ ] Number of interviews; participant recruitment and characteristics
- [ ] Format: structured, semi-structured, think-aloud, moderated usability test
- [ ] Survey N, instrument, and distribution channel
- [ ] **The three most important findings**, stated as findings rather than topics
- [ ] **For each finding, the design change it caused.** This is the whole value of the claim — a before/after pair is the most persuasive thing in this section
- [ ] Anything the research *disproved* — a killed feature or an assumption that turned out false is the most credible evidence that the research was real and not confirmatory
- [ ] Cross-reference §7 — the interview methodology has a provenance (⟡ M#6)

#### 4.1.7 Transparency of the AI process in the interface
> ⟡ **M#2.3** — *"did you account for the user's need for transparency into the AI's analysis process? Did you design that display step?"*

This is the mentor's sharpest question, because it tests whether "radical transparency" is a brand or an architecture. If a user cannot see anything about how the AI reached its output, the tagline is unsupported — and the reviewer will notice.

▢ FILL:
- [ ] Is there any AI-process disclosure in the UI at all? **A truthful "not yet — here is the design I specified for it and why it was deprioritised" is a strong answer.** A vague implication that transparency exists is a weak one and is easily punctured at interview
- [ ] What is exposed: source list per story, which sources contributed to which claim, why these articles were grouped together, which model produced the text, confidence or uncertainty, timestamps of analysis?
- [ ] The **cluster-explanation** question specifically: can a user see *why* these articles were treated as one story? That is the one disclosure unique to this architecture, and the hardest to communicate without exposing the machinery
- [ ] Progressive disclosure design: what is on the card by default, what is one tap away, what is buried. The interesting design work is in that gradient — full transparency shown at once is unreadable, and choosing the layering is the actual contribution
- [ ] Was AI-generated content labelled as such, and how
- [ ] Any evidence about whether users *wanted* this — did it come up unprompted in the interviews (§4.1.6)? Whether disclosure increased or decreased trust is a genuinely interesting finding either way, and directly adjacent to §5.2's research

#### 4.1.8 Optimization
> ⟡ **M#2.4** — *"you can mention optimization."* Brief in the comment, but it is where measurable engineering results live, and the entry currently contains no performance numbers at all.

▢ FILL — for each, the **before → after with a number**, which is what makes this section worth having:
- [ ] **Cost.** Cost per story or per 1k articles. Levers: model routing (cheap model for easy clusters), hierarchical summarization to bound context, caching, batch APIs, prompt compression. What did you actually do, and what did it save?
- [ ] **Latency.** Ingest→publish end to end, and per stage. What was the bottleneck, how was it found (profiling? logging?), what fixed it?
- [ ] **Embedding cost.** Batching, caching by content hash, local vs. hosted
- [ ] **Index performance.** Query latency and recall before/after parameter tuning
- [ ] **Throughput.** Articles/hour, concurrency, parallelisation, rate-limit handling
- [ ] **Frontend.** Load time, bundle size, image/video optimisation, Core Web Vitals if measured
- [ ] **The tradeoff you accepted.** Every optimisation costs something — quality, freshness, coverage. Naming what you traded away is the mark of an engineer rather than a tinkerer

#### 4.1.9 Decode: Veritas
- **◆ ON RECORD** Shipped **Decode: Veritas**, a media-literacy game on the App Store, for AI-generated-content detection

A shipped, publicly available App Store product is disproportionately strong evidence — it is verifiable by the reader in ten seconds, unlike everything else in this document. It currently gets one line.

▢ FILL — **product:**
- [ ] App Store URL, bundle ID, launch date, current version, platforms
- [ ] Downloads, ratings, retention, any featuring or editorial placement
- [ ] Free/paid; any monetisation
- [ ] Its relationship to NewsFlick: standalone product, marketing instrument, or research vehicle? Say which — the reader will wonder why a news company shipped a game

▢ FILL — **design:**
- [ ] Core loop. What does the player actually do, turn by turn?
- [ ] Content: how many items, what mix of AI-generated vs. authentic, and **how the AI-generated content was produced** (which generators, which prompts) — that provenance is itself technical work
- [ ] Difficulty progression and scoring
- [ ] The pedagogical model: what specific detection skills does it teach, and on what basis do you believe it teaches them? Any pre/post measurement of player accuracy would be a genuinely publishable result — check whether you have the data
- [ ] Whether AI is used at runtime or content is pre-generated

▢ FILL — **shipping:**
- [ ] Your role: sole developer or part of a team
- [ ] Tech stack (Swift/SwiftUI per Skills — confirm)
- [ ] App Review process, rejections and resolutions, privacy manifest/nutrition label, age rating
- [ ] Post-launch updates shipped, and what drove each (→ §4.1.11)

#### 4.1.10 Additional work not yet on record
▢ FILL — a co-founder does a great deal that never reaches a CV bullet. List anything real:
- [ ] Infrastructure, deployment, monitoring, on-call
- [ ] Analytics instrumentation
- [ ] Legal/compliance: privacy policy, GDPR/PDPO posture, content licensing, App Store compliance
- [ ] Hiring, onboarding, or managing contributors
- [ ] Fundraising, pitching, investor or accelerator relations (→ §6.4)
- [ ] Marketing, growth, content, community
- [ ] Partnerships with publishers or data providers

#### 4.1.11 Maintenance and upgrade
> ⟡ **M#3** — the explicitly requested third act: *thinking → implementation → **maintenance/upgrade***. This is the part almost every applicant omits, which is exactly why including it differentiates.

▢ FILL:
- [ ] What broke in production, and what you changed structurally as a result. One concrete incident — cause, fix, and the prevention that followed — is worth more than any list of features
- [ ] Monitoring: what is measured, what alerts, how failures surface
- [ ] How model or pipeline regressions are caught. When you swap an LLM version, what tells you quality did not drop?
- [ ] Version history: the 2–3 significant upgrades since launch, each with the evidence that triggered it (user feedback, metric, incident) and the measured result
- [ ] Feedback loop: how user input reaches the backlog and what it has changed
- [ ] Technical debt you knowingly took on, and why it was the right call at the time

#### 4.1.12 Public traction and evidence
> The mentor twice notes NewsFlick *"has online exposure"* — none of it appears in the CV.

▢ FILL:
- [ ] Press coverage, blog posts, podcasts, interviews — with links
- [ ] Social/community traction: launch post metrics, follower counts, Product Hunt or similar
- [ ] User metrics: registered users, MAU/DAU, session length, retention
- [ ] Testimonials or notable users
- [ ] Awards attributable to NewsFlick specifically (cross-check §6 — if the Techathon+ or AI Competition results were won with NewsFlick, that connection must be made explicit; awards and product currently sit in unrelated sections)

---

### §4.2 — PillWise
**Engineer · 2025 – Present**
> ⟡ **M#4** — title changed from "Product Builder" to **Engineer** as directed. Mentor's assessment: *"an excellent embedded-systems + computer-vision + interdisciplinary practical project, and it has online exposure too."* Three named gaps: algorithm selection with the comparison behind it, accuracy numbers, and front/back data flow.

#### 4.2.1 Snapshot
- **◆ ON RECORD** Medication adherence and verification product
- **◆ ON RECORD** Defined system architecture and interaction design for medication adherence and verification workflows
- **◆ ON RECORD** Built AI medication-check app: PyTorch + Transformers for pill verification, REST API backend, iOS front end (Swift/SwiftUI)
- **◆ ON RECORD** 2025 – Present

▢ FILL:
- [ ] Team size and your ownership boundary (as §4.1.3)
- [ ] Relationship to NewsFlick — parallel venture, incubator cohort project, coursework origin?
- [ ] Current status: shipped / TestFlight / prototype. If it is on the App Store, that is a second shipped product and belongs on the front line of the CV
- [ ] Product URL, App Store link, repo

#### 4.2.2 Problem framing
▢ FILL:
- [ ] The adherence problem being solved, stated specifically. Wrong-pill errors? Missed doses? Polypharmacy confusion in elderly patients? Caregiver verification at a distance? These imply different systems, and "medication adherence" alone does not tell the reader which
- [ ] Target user: patient, caregiver, or clinician. The interaction design differs completely
- [ ] Why computer vision is the right mechanism versus manual logging or smart packaging
- [ ] Safety posture. This is a medical-adjacent product and a reader **will** ask: what happens when the model is wrong? Is the output advisory or authoritative? Any regulatory consideration? Having a clear answer — including "advisory only, by design, with the following user-facing framing" — is a substantial credibility marker in this domain, and its absence is a liability

#### 4.2.3 System architecture
- **◆ ON RECORD** You defined the system architecture and the interaction design for the adherence + verification workflows

▢ FILL:
- [ ] Full component diagram: capture → preprocessing → inference → verification against prescription → logging → reminder/notification → caregiver view
- [ ] Where inference runs: on-device (Core ML) or server-side. **A significant decision with real tradeoffs** — latency, privacy of health data, model size, offline capability. If you chose deliberately, the reasoning is exactly the kind of detail the mentor is asking for
- [ ] Data model: prescriptions, doses, schedules, adherence events, users
- [ ] The **adherence** half versus the **verification** half — these are two features and the current bullets blur them

#### 4.2.4 Pill recognition — model and selection
> ⟡ **M#4.1** — *"algorithm details of pill recognition/verification. How you chose it, what comparison/experiment process."* The mentor wants the **selection experiment**, not just the final model. The comparison is the evidence of engineering judgement.

▢ FILL — **task formulation** (answer this first; everything else follows):
- [ ] What is the model actually doing? Closed-set classification over a known pill catalogue / open-set verification against an expected pill / attribute extraction (colour, shape, imprint, scoring) / imprint OCR / metric-learning similarity matching. These are fundamentally different problems and the CV does not indicate which one you solved
- [ ] Is it verification (*"is this the pill it should be?"*) or identification (*"what pill is this?"*)? The CV says "verification" — if so, say how the expected pill is known, and note that verification is the easier and more appropriate framing for safety, which is a point in your favour

▢ FILL — **architecture:**
- [ ] Exact model architecture and backbone. **◆ ON RECORD** the CV cites PyTorch + **Transformers** — clarify whether that means a vision transformer, a HuggingFace-library CNN, or a multimodal model, because "Transformers" for an image task reads ambiguously and a technical reader will flag it
- [ ] Pretrained weights used, and what was fine-tuned versus frozen
- [ ] Input resolution, preprocessing, augmentation
- [ ] Model size and inference cost

▢ FILL — **the comparison process** *(the actual ask):*
- [ ] Which alternatives you tried. Even two is enough — a CNN baseline vs. a transformer, classification vs. metric learning, with-imprint-OCR vs. without
- [ ] The evaluation protocol used to choose between them: dataset, split, metric
- [ ] The result table. **Reproduce it here in full, even the losing rows** — a table with a rejected approach in it is more convincing than a single reported number
- [ ] The criterion that decided it, especially if accuracy was not the deciding factor (latency, size, calibration, or failure mode may have been — and if a *less* accurate model won for a stated reason, that is a sophisticated result)

▢ FILL — **data:**
- [ ] Dataset: public (NIH Pill Image Recognition / RxImage), self-collected, or synthetic. Number of classes and images
- [ ] If self-collected: capture protocol, lighting/background variation, labelling process, inter-annotator checks. Self-collected data is real work and should be claimed
- [ ] Train/val/test split methodology, and specifically whether the split is **by pill instance or by image** — image-level splits leak and inflate accuracy. Getting this right is a genuine sign of rigour; getting it wrong invalidates the numbers
- [ ] Class imbalance handling
- [ ] Whether the test conditions resemble real user photos (a model evaluated only on catalogue images will not survive a kitchen table at night — if you tested under realistic conditions, that is a strength worth stating)

#### 4.2.5 Performance
> ⟡ **M#4.2** — *"performance: accuracy."* Currently the entry contains **no numbers whatsoever**. A CV claiming a shipped CV model with no metric invites the assumption that it was never measured.

▢ FILL:
- [ ] Top-1 / top-5 accuracy, with the dataset and split each was measured on
- [ ] Precision, recall, F1 — and for a medical-adjacent product, **the false-negative vs. false-positive asymmetry matters more than accuracy**. A wrong-pill-accepted error is categorically worse than a correct-pill-rejected error. If you tuned the operating threshold with that asymmetry in mind, that decision is one of the strongest single items available in this entry
- [ ] Confusion analysis: which pills get confused, and why (same colour/shape families, worn imprints)
- [ ] Calibration and confidence thresholding: does the system abstain when unsure, and at what threshold?
- [ ] Latency: on-device or round-trip, measured on which hardware
- [ ] Real-world versus benchmark performance, if you have both
- [ ] Comparison to a baseline — human accuracy, a simple colour/shape heuristic, or a prior model

#### 4.2.6 Front-end / back-end data flow
> ⟡ **M#4.3** — *"front-end/back-end data flow interaction."* Named explicitly.

- **◆ ON RECORD** REST API backend; iOS (Swift/SwiftUI) front end

▢ FILL — trace one complete transaction end to end. That single trace answers the comment in full:
- [ ] Capture on device: camera session, guidance overlay, quality gating before upload
- [ ] Client-side preprocessing: resize, compress, crop. What is sent — full image or a crop? Payload size?
- [ ] Request: endpoint, method, payload schema, auth mechanism
- [ ] Server: framework, inference serving, batching, concurrency, cold starts
- [ ] Response schema: label, confidence, alternatives, guidance
- [ ] Client handling of the response: display, confidence UI, retry path, wrong-result path
- [ ] Persistence: what is written where, and when the adherence log is updated
- [ ] Offline behaviour: queued capture, local cache, sync-on-reconnect
- [ ] Error handling across the boundary: timeouts, low-quality image, unrecognised pill, server down
- [ ] **Privacy and security of health data**: TLS, at-rest encryption, retention policy, whether images are stored after inference, PII handling. In this domain a reader treats this as non-optional, and a clear answer is a differentiator
- [ ] API versioning, and how client/server compatibility is managed

#### 4.2.7 Hardware / embedded component
> ⟡ **M#4** — the mentor characterises PillWise as an **embedded-systems** project. Nothing in the current bullets mentions hardware. Resolve this: it is either a real omission or a mischaracterisation, and the answer changes the entry substantially.

▢ FILL:
- [ ] Is there a physical device? A smart dispenser, a capture rig, a sensor-instrumented pillbox?
- [ ] **◆ ON RECORD** ESP32S3 and Arduino appear in your Skills line — is either used here? If they belong to a different project (e.g. §6.3 Robot Design Contest), the Skills line is currently creating a false association and should be re-scoped
- [ ] If hardware exists: sensors, microcontroller, firmware, power, enclosure/CAD, fabrication, device↔app communication (BLE/Wi-Fi), and how many units built
- [ ] If no hardware exists: note it explicitly here so this question is settled, and check the "IoT / embedded" framing elsewhere in the CV for consistency

#### 4.2.8 Interaction design
- **◆ ON RECORD** You defined the interaction design for the adherence and verification workflows

▢ FILL:
- [ ] The adherence flow: scheduling, reminders, snooze/skip, streaks, missed-dose recovery
- [ ] The verification flow: how a user is guided to a usable photo — this is where most CV products fail in the field, and any capture-guidance design is real HCI work
- [ ] Accessibility: this product plausibly serves elderly users with impaired vision or dexterity. If you designed for that (type size, contrast, target size, reduced-step flows), it is one of the more compelling design decisions in the whole document and it is currently invisible
- [ ] Caregiver-facing views, if any
- [ ] How a **negative** verification result is communicated — the highest-stakes screen in the product. Alarm vs. advisory; what the user is told to do next
- [ ] Any user testing done with the actual target population

#### 4.2.9 Maintenance and upgrade
> ⟡ **M#3** — applies to PillWise as well: *"the next one, PillWise, is too."*

▢ FILL:
- [ ] Model retraining: has the model been updated since first deployment, on what data, with what measured change?
- [ ] How production failures are detected — are misrecognitions captured for review?
- [ ] Version history and what drove each release
- [ ] Known limitations you are aware of and have chosen to live with

#### 4.2.10 Public traction
▢ FILL:
- [ ] The "online exposure" the mentor refers to — links, coverage, posts
- [ ] Downloads/users, ratings
- [ ] Competition results attributable to PillWise (cross-check §6)
- [ ] Any clinical, pharmacy, or institutional contact or validation

---

### §4.3 — SenseTime
**Investment Intern, AI Sector · Summer 2024**
> ⟡ **M#5** — *"add process and results. The core idea to convey is: learning leads practice, practice reinforces learning."*

- **◆ ON RECORD** Conducted investment research on AI businesses/projects: market landscape, competitive positioning, key risks
- **◆ ON RECORD** Prepared structured investment briefs for internal evaluation

#### 4.3.1 Context
▢ FILL:
- [ ] Exact dates and duration; full-time or part-time
- [ ] Which team/unit, its mandate (corporate development, strategic investment, CVC), and typical deal size or stage
- [ ] Who you reported to and team size
- [ ] Selection process and cohort size, if competitive

#### 4.3.2 Scope of work — quantified
▢ FILL — the entry currently has no scale at all:
- [ ] How many companies/projects you researched. A count converts a vague activity into work
- [ ] How many briefs you authored, and their typical length and structure
- [ ] Which sectors or technology areas you covered (specify: CV, LLM infrastructure, chips, robotics, vertical AI applications)
- [ ] Whether you worked solo on a brief or contributed sections to a team product — be precise, an intern claiming sole authorship of investment memos will be probed

#### 4.3.3 Method
> ⟡ **M#5** — *"process"* is named first in the comment. Method is what distinguishes analysis from summary.

▢ FILL:
- [ ] Your research process, step by step: sourcing → screening → deep dive → thesis → write-up
- [ ] Information sources: filings, databases (PitchBook/Crunchbase/CB Insights), expert calls, primary research, technical papers
- [ ] The **technical** dimension of your evaluation — this is the crux of the entry and the reason it belongs on a technical CV at all. As someone who builds ML systems, you could assess whether a startup's claimed technical moat was real. Did you? A concrete instance where your engineering knowledge changed an assessment is the single most valuable item in this section, and it is precisely the *"learning leads practice, practice reinforces learning"* point the mentor asked you to make. **Only claim it if it actually happened**
- [ ] Analytical frameworks used: market sizing method, competitive mapping, moat analysis, risk taxonomy
- [ ] Brief structure and standard sections

#### 4.3.4 Results
> ⟡ **M#5** — *"results."* Currently absent entirely.

▢ FILL — investment work has real confidentiality limits; describe outcomes at a level you are permitted to disclose, and say so where you cannot:
- [ ] Did any brief inform an actual decision? Even "recommendation was adopted / company advanced to the next diligence stage" is a result
- [ ] Was any output adopted as a reusable template or process improvement?
- [ ] Feedback received, or any extension/return offer
- [ ] With hindsight: did any assessment prove right or wrong? Naming a call you got wrong and why is disproportionately credible
- [ ] A specific and non-confidential example of an analysis you produced

#### 4.3.5 Transfer to engineering work
> ⟡ **M#5** — the *"practice reinforces learning"* half. Do not write this as reflection; write it as fact.

▢ FILL — concrete transfers only, each an actual event:
- [ ] Did the competitive landscape work inform how NewsFlick or PillWise was positioned or scoped?
- [ ] Did the risk analysis frameworks affect how you evaluate your own technical decisions?
- [ ] Did any specific company you researched influence a design or architectural choice?
- [ ] Conversely: did building systems make you a better evaluator of others' technical claims? A specific instance beats a general statement
- [ ] If there is no genuine transfer, say nothing here. A fabricated connection is more damaging than an unconnected internship

---

## §5. Research and technical projects

---

### §5.1 — SAH-LC: Semantic-Aware Hybrid Loop Closure for Visual SLAM
**Paper submitted to IEEE IROS 2026 — under review**

- **◆ ON RECORD** Two-stage loop closure framework for drone visual SLAM
- **◆ ON RECORD** MobileNetV3 + CBAM semantic encoder, 256-dim embeddings, FAISS retrieval
- **◆ ON RECORD** ORB + RANSAC geometric verification
- **◆ ON RECORD** Online dictionary updates
- **◆ ON RECORD** Evaluated on EuRoC MAV; average ROC-AUC **0.656** vs. NetVLAD **0.643** and ORB-only **0.546**
- **◆ ON RECORD** ~12 FPS on a laptop CPU

This is the most technically specified entry in the CV — the only one that names architectures, dimensions, baselines, and numbers. **It is the standard the other entries should be brought up to**, and it is worth noting that the mentor raised no complaint about this entry while calling the others insufficiently professional. That contrast is the clearest available guide to what the mentor wants.

#### 5.1.1 Publication status
▢ FILL:
- [ ] Submission date; venue (IROS 2026); expected decision date
- [ ] Full author list and **your author position**; who the corresponding author is
- [ ] Your specific contribution — the CRediT breakdown: conceptualisation, methodology, software, validation, writing. On a multi-author paper this must be explicit
- [ ] Advisor/PI and their affiliation
- [ ] Preprint (arXiv) — if not posted, consider whether to; an under-review paper with no readable artefact is hard for a reviewer to assess
- [ ] Code release status

#### 5.1.2 Problem
▢ FILL:
- [ ] What loop closure is failing at in the drone context specifically — viewpoint change, scale, motion blur, repetitive structure, perceptual aliasing?
- [ ] Why existing methods are inadequate here. Specifically: what does NetVLAD cost or fail at that motivated a MobileNetV3-based approach? (The likely answer is compute — a MobileNetV3 backbone with a lightweight attention module is a deliberate efficiency choice for onboard drone hardware, which frames the whole contribution)
- [ ] The constraint set: onboard compute budget, real-time requirement, memory

#### 5.1.3 Method
▢ FILL — expand each stated component into its actual design:
- [ ] **Two-stage structure**: candidate retrieval → geometric verification. What exactly does each stage accept and reject, and what is the recall/precision division of labour between them?
- [ ] **Semantic encoder**: why MobileNetV3 (efficiency), why CBAM (attention over what, and what does it buy in this setting)? Where is CBAM inserted? Pretrained or trained from scratch? If trained, on what data with what loss?
- [ ] **256-dim embeddings**: why 256? Was dimension ablated? If you tried 128/512, the ablation is a result
- [ ] **FAISS retrieval**: index type, metric, top-k, latency. (Note: this is the same technique used at NewsFlick §4.1.4B — worth being consistent about, and a legitimate cross-domain competence claim)
- [ ] **ORB + RANSAC verification**: feature count, matcher, RANSAC threshold and iteration count, inlier criterion for accepting a loop
- [ ] **Online dictionary updates** — the most distinctive element and the one most in need of expansion. What dictionary, updated with what, on what trigger, and what problem does updating solve that a static dictionary cannot? What prevents drift or unbounded growth?
- [ ] Full hyperparameter set and how each was chosen
- [ ] What is novel here relative to prior work, stated in one sentence

#### 5.1.4 Evaluation
▢ FILL:
- [ ] Which EuRoC MAV sequences were used, and whether the average is over all of them. **Report per-sequence results, not only the average** — averages hide the interesting behaviour and a reviewer will ask
- [ ] Why ROC-AUC as the metric; whether precision-recall (more standard in place recognition, and more informative under class imbalance) was also computed
- [ ] Ground-truth definition for a true loop closure — the distance/angle threshold used. This choice materially affects the numbers and must be stated
- [ ] **The margin over NetVLAD is 0.013 AUC (0.656 vs 0.643).** Be prepared to defend it: is it consistent across sequences or driven by one? Any significance testing or variance across runs? **The honest framing is likely the stronger one** — comparable-or-better accuracy at substantially lower compute is a better claim than a 2% accuracy win, and it is the claim the architecture actually supports. Check whether the paper makes the efficiency argument primary; if not, consider whether it should
- [ ] Baseline fairness: which NetVLAD implementation and weights, tuned how? A reviewer's first attack on any "we beat X" claim is that X was under-tuned
- [ ] Ablations: CBAM removed, dictionary updates disabled, geometric stage disabled, dimension varied. If these exist, they are among the strongest content available
- [ ] Failure cases

#### 5.1.5 Efficiency
▢ FILL — the efficiency claim is likely the paper's real contribution and needs full specification:
- [ ] **~12 FPS on "a laptop CPU"** — which CPU exactly, how many threads, what resolution, batch size 1? The claim is unverifiable as written and a reviewer will treat it as soft
- [ ] Per-stage timing breakdown
- [ ] Memory footprint and model size (parameters, MB)
- [ ] Comparison of compute cost against NetVLAD under identical conditions — **this is the number that carries the paper**, and if it exists it should be more prominent than the AUC
- [ ] Whether it was ever run on actual drone hardware (Jetson, RPi, or a flight controller companion computer). If yes, that is a substantially stronger claim than laptop-CPU numbers and belongs in the headline

#### 5.1.6 Implementation and process
> ⟡ **M#3** — the thinking→implementation→iteration arc applies to research too.

▢ FILL:
- [ ] Codebase: language, framework, size, whether built on an existing SLAM stack (ORB-SLAM3?) or from scratch
- [ ] Your engineering contribution versus co-authors'
- [ ] Timeline: when started, how long to first result, how many major iterations
- [ ] **What was tried and abandoned.** Research is mostly discarded approaches, and naming two or three that failed — with the reason — is the most credible evidence of genuine research work anyone can offer
- [ ] Compute resources used
- [ ] Reproducibility: seeds, config management, whether results are reproducible from the repo

---

### §5.2 — Depolarization-by-Design
**Research with Prof. RAY LC, City University of Hong Kong**

- **◆ ON RECORD** A social-media feature that turns rival fandoms into collaborators to defuse online toxicity at the group level
- **◆ ON RECORD** Grounded in in-group recategorization theory
- **◆ ON RECORD** Tested with a 3-arm controlled study

#### 5.2.1 Context
▢ FILL:
- [ ] Dates and duration; your role (RA, collaborator, project lead)
- [ ] Lab name and team size; who else was involved
- [ ] How the collaboration arose
- [ ] Output status: published, in submission, in progress, workshop paper? Target venue (CHI, CSCW)? If there is a paper, its title and authorship
- [ ] Whether this is ongoing

#### 5.2.2 Theory and design
▢ FILL:
- [ ] **In-group recategorization** (the Common In-group Identity Model — Gaertner & Dovidio) in one precise sentence, and the specific mechanism you operationalised. Name the theory precisely; an HCI reviewer will know it
- [ ] How the theory became an interface. **This translation is the actual research contribution** — what concrete feature makes two rival fandoms perceive a superordinate shared identity?
- [ ] The intervention in mechanical detail: what does a user see, what are they asked to do, what is the collaborative task, what is the reward structure?
- [ ] Why fandoms as the domain — a design decision worth justifying (high baseline group identification, naturally occurring rivalry, low political risk relative to studying partisan polarisation directly)
- [ ] Design alternatives considered and rejected
- [ ] Prototype fidelity: figma prototype, functional web app, or a real platform? Who built it, and how much of it did you build?

#### 5.2.3 Study design
▢ FILL — a 3-arm controlled study is a substantial methodological claim and needs full specification:
- [ ] **The three arms.** Name each: presumably control, a partial intervention, and the full intervention — but state exactly what distinguishes them, since the comparison logic is the design
- [ ] N total and per arm; power analysis if conducted
- [ ] Recruitment: platform (Prolific/MTurk/university pool), screening criteria, compensation
- [ ] Random assignment procedure
- [ ] **Measures**: which validated instruments (feeling thermometer, social distance scale, IOS scale, toxicity ratings) and which custom ones. Named validated instruments are what make this read as research rather than a survey
- [ ] Duration and procedure per participant
- [ ] Pre-registration status
- [ ] Ethics/IRB approval
- [ ] Analysis: statistical tests used, effect sizes, corrections for multiple comparisons

#### 5.2.4 Results
▢ FILL — **currently the CV states the study was run but reports no outcome at all**, which reads as though it did not work:
- [ ] Primary outcome: direction, magnitude, significance
- [ ] Secondary outcomes
- [ ] Whether the effect held across arms as predicted
- [ ] **A null result is a legitimate and reportable outcome** — say so plainly if that is what happened, along with what it suggests. An unreported result is worse than a null one
- [ ] Qualitative findings, if any were collected
- [ ] Limitations you would name yourself

#### 5.2.5 Your contribution
▢ FILL:
- [ ] Which of these you personally did: theory review, concept design, prototype build, study design, participant running, data analysis, writing
- [ ] The relationship to NewsFlick is worth stating explicitly — both address polarisation and information ecosystems through interface design. If one project informed the other, that is a coherent research identity rather than two unrelated items, and it materially strengthens an application for HCI or computational social science programs

---

## §6. Awards and competitive results

Each award below is currently one line. Each represents days or weeks of work with a defined output. The pattern to fill for every one: **what was built · your role · what the judges evaluated · why it won.**

### 6.1 Silver Award — HKSTP Techathon+ 2026, Trusted AI & Data Science
- **◆ ON RECORD** 1,900 participants, 470+ teams

▢ FILL:
- [ ] What you built, in technical detail. This is a "Trusted AI" track — the submission was presumably about verification, transparency, or reliability, and that is directly continuous with NewsFlick's transparency claims. **Say whether this WAS NewsFlick** — if so, the connection must be explicit, since the award and the product currently appear in unrelated sections as unrelated achievements
- [ ] Team size and your role
- [ ] Duration — hackathon-format or multi-week?
- [ ] Judging criteria and panel
- [ ] How many teams received Silver (i.e. your actual rank among 470+)
- [ ] Prize/benefits
- [ ] Demo, repo, or slides that still exist

### 6.2 Best AI Literacy Award & Top 3 — HKUST Inter-University AI Competition 2025
▢ FILL:
- [ ] What was submitted. **If this was Decode: Veritas** (a media-literacy game about detecting AI content winning a *Best AI Literacy* award is a near-certain match), say so — connecting the shipped App Store product to the award it won makes both items stronger
- [ ] Two distinct awards are listed here — clarify whether "Best AI Literacy" and "Top 3" were awarded for the same submission
- [ ] Number of participating teams and universities
- [ ] Your role and team size
- [ ] Judging criteria

### 6.3 1st Place — HKUST 15th Robot Design Contest
- **◆ ON RECORD** 100% mechanical design: CAD, fabrication, integration

▢ FILL:
- [ ] The contest task — what did the robot have to do?
- [ ] Number of competing teams; format (elimination rounds, scored runs)
- [ ] Team size, and what the other members did (since you owned mechanical entirely)
- [ ] The robot: drivetrain, mechanism, actuators, materials, dimensions, mass
- [ ] CAD tool used; number of parts designed
- [ ] Fabrication methods: 3D printing, laser cutting, machining. What you personally made
- [ ] **The key mechanical design decision** and the reasoning behind it — one well-explained mechanism is worth more than a parts list
- [ ] Iteration history: what failed in testing and what you changed. Mechanical iteration is highly legible evidence of engineering process
- [ ] Whether ESP32S3/Arduino from your Skills line belongs to this project (cross-check §4.2.7)
- [ ] Photos/video — visual evidence for a mechanical project is unusually persuasive and worth locating

### 6.4 HKSTP Ideation Programme (HK$100K seed) & HKUST Dream Builder Incubation
▢ FILL:
- [ ] **Which venture each accepted** — NewsFlick, PillWise, or both? Currently listed under Awards with no linkage to the companies in §4, which loses most of the signal
- [ ] Application and selection process; acceptance rate if known
- [ ] Programme duration and what participation involved: mentorship, milestones, deliverables
- [ ] What the HK$100K was spent on, and what it enabled
- [ ] Current status in each programme; whether milestones were met
- [ ] Note: a HK$100K seed grant is **funding**, not an award. Consider whether it belongs in the venture entry (§4.1.1) rather than under Awards — it reads as substantially more significant there

### 6.5 Unrecorded competitions and recognitions
▢ FILL:
- [ ] Any competition entered without placing, where the *work produced* was substantial. The artefact can be worth listing even without the ribbon
- [ ] Academic prizes, dean's list, departmental awards
- [ ] Hackathons, datathons, design competitions
- [ ] Scholarships and grants (distinct from §3.1)

---

## §7. Leadership — Interviewer Society, HKUST
**Vice Chairman**
> ⟡ **M#6** — *"NewsFlick and PillWise, as consumer-facing products, all require solid communication skills — interviewing / collecting market feedback, user experience, and following up on the product development process."* The instruction is to stop treating this as a detached extracurricular.

### 7.1 On record
- **◆ ON RECORD** Vice Chairman, Interviewer Society, HKUST
- **◆ ON RECORD** Led interview productions end-to-end; streamlined workflows and team coordination
- **◆ ON RECORD** Grew the society 3× to 30 members during tenure
- **◆ ON RECORD** Established a monthly interview partnership with the HKUST Business School
- **◆ ON RECORD** Launched an annual interview program with the University President

### 7.2 Operational detail
▢ FILL:
- [ ] Tenure dates; whether elected or appointed; predecessor situation
- [ ] Society size at start (10, given 3× to 30) and the growth mechanism — recruitment drive, programming change, partnerships?
- [ ] Retention, not just headcount
- [ ] Team structure under you: sub-teams, how many people you directly coordinated

▢ FILL — **"interview productions end-to-end"** unpacks into a real production pipeline; enumerate what you actually ran:
- [ ] Guest identification and outreach
- [ ] Research and question preparation
- [ ] Scheduling and logistics
- [ ] Conducting the interview — did you personally interview, or direct?
- [ ] Recording: equipment, video/audio/written
- [ ] Editing and post-production
- [ ] Publication and distribution channels
- [ ] Audience metrics — readership, views, reach
- [ ] How many interviews produced during your tenure. **A count is the single most useful number here** and is currently missing

▢ FILL — **"streamlined workflows"** is currently unsupported:
- [ ] What was inefficient before, specifically
- [ ] What process, template, or tool you introduced
- [ ] Measured effect: turnaround time, output volume, fewer dropped commitments

### 7.3 Institutional partnerships
▢ FILL — these are the two strongest items in the section and get one clause each:
- [ ] **HKUST Business School monthly partnership**: how the relationship was established, who you negotiated with, what the recurring format is, how many editions have run, and whether it outlived your tenure. Institutional durability is the real achievement
- [ ] **Annual programme with the University President**: how access at that level was obtained, what the format is, and whether it has recurred. Securing a recurring commitment from a university president as an undergraduate is a genuinely uncommon outcome and deserves more than the current half-line

### 7.4 Transfer to product research
> ⟡ **M#6** — the explicit ask. State this as fact, not as reflection.

▢ FILL — only what actually happened:
- [ ] Roughly how many interviews you have personally conducted across all contexts. This is the number that makes the connection concrete: someone who has run dozens of structured interviews is qualified to run user research, and that is a claim with evidence behind it
- [ ] Which specific interviewing techniques you carry into user research: neutral question framing, avoiding leading questions, follow-up probing, silence tolerance, structuring a guide, note-taking and synthesis
- [ ] Whether the NewsFlick user interviews (§4.1.6) used a protocol derived from this practice
- [ ] Whether any PillWise research (§4.2.8) drew on it — especially relevant if interviewing elderly or patient users, which requires more skill than average
- [ ] Stakeholder communication: managing guests, partners, and a 30-person team maps onto managing users, collaborators, and a company. If there is a specific instance, use it
- [ ] The honest framing to aim for: *interviewing is the shared method underlying both the society work and the product research*, not two separate skills that happen to coexist

---

## §8. Skills — with evidence

The CV's skills lines are unattributed, so a reader cannot tell which skill was used where. This table fixes that; it is also a self-audit — **any skill with no evidence column should come off the CV.**

### 8.1 Programming
| Skill | ◆ Listed | Evidence (fill: where actually used, at what depth) |
|---|---|---|
| Python | ✓ | ▢ — SAH-LC, PillWise training, NewsFlick backend? Specify |
| JavaScript / TypeScript | ✓ | ▢ — NewsFlick frontend? |
| React / Next.js | ✓ | ▢ — which product |
| Swift / SwiftUI | ✓ | ▢ — PillWise iOS, Decode: Veritas |
| C / C++ (embedded) | ✓ | ▢ — which project? Robot Design Contest? ESP32 firmware? **Currently unattributed anywhere** |

### 8.2 AI / ML
| Skill | ◆ Listed | Evidence |
|---|---|---|
| PyTorch | ✓ | ▢ — PillWise pill model, SAH-LC encoder |
| Transformers | ✓ | ▢ — clarify: architecture or HuggingFace library, and where (see §4.2.4) |
| API integration | ✓ | ▢ — which LLM APIs, which products |
| Prompt engineering | ✓ | ▢ — NewsFlick summarization + perspective comparison |
| OpenCV | ✓ | ▢ — PillWise preprocessing? SAH-LC ORB pipeline? |
| FAISS | ✓ | ▢ — **both** NewsFlick §4.1.4B and SAH-LC §5.1.3 — a genuine cross-domain claim, worth making explicitly |

### 8.3 Design and hardware
| Skill | ◆ Listed | Evidence |
|---|---|---|
| Figma | ✓ | ▢ — NewsFlick, PillWise |
| UI/UX prototyping | ✓ | ▢ |
| Interaction design | ✓ | ▢ — NewsFlick flows, PillWise workflows, §5.2 prototype |
| ESP32S3 | ✓ | ▢ — **which project?** (see §4.2.7) |
| Arduino | ✓ | ▢ — which project? |
| CAD | ✓ | ▢ — Robot Design Contest (100% mechanical design) |
| 3D printing | ✓ | ▢ — Robot Design Contest |

### 8.4 Languages
- **◆ ON RECORD** Mandarin Chinese (native) · English (native-level) · Cantonese (conversational)

▢ Note: "English (native-level)" is a self-assessment that CEFR C2 and the TOEFL score already substantiate. Since §2 now carries those scores in their own section, consider whether the self-assessed label adds anything or simply invites scrutiny.

### 8.5 Unrecorded skills
▢ FILL — things you have demonstrably done that appear nowhere:
- [ ] Databases (which ones — every product above implies one)
- [ ] Cloud/deployment (AWS/GCP/Vercel/Docker)
- [ ] Version control and collaboration workflow at team scale
- [ ] Web scraping / data engineering (implied by NewsFlick ingestion)
- [ ] Statistical analysis (implied by §5.2's controlled study — R? Python? SPSS?)
- [ ] Academic writing (implied by the IROS submission)
- [ ] Video production / editing (implied by §7 and NewsFlick's video-first delivery)

---

## §9. Capability map

Five capability claims are supportable from the material above. Each is listed with its independent evidence — the point being that each is demonstrated more than once, in unrelated contexts, which is what distinguishes a capability from an incident.

**1 · Retrieval and embedding systems, applied across domains**
NewsFlick semantic clustering (§4.1.4B) · SAH-LC place recognition (§5.1.3). The same technical apparatus — embeddings, FAISS, similarity thresholds — deployed once in NLP and once in computer vision. Few undergraduate profiles show the same tool used competently in two unrelated domains, and it is worth making the parallel explicit rather than leaving the reader to notice it.

**2 · Shipping to real users**
Decode: Veritas on the App Store (§4.1.9) · PillWise (§4.2) · NewsFlick live (§4.1). Verifiable, public, external. This is the strongest category of evidence in the document and it is currently under-weighted relative to the awards.

**3 · Full-stack range: hardware → model → API → interface → user research**
Mechanical CAD and fabrication (§6.3) · CV/ML models (§4.2.4, §5.1) · REST backends (§4.2.6) · iOS and web frontends · interaction design (§4.1.6) · controlled user studies (§5.2). This is the actual meaning of "Integrative Systems and Design," and demonstrating the span is more distinctive than depth in any single layer.

**4 · Research method at two levels**
Systems research with quantitative benchmarks (§5.1) · behavioural research with a controlled human-subjects study (§5.2). Competence in both algorithmic evaluation and experimental design with human participants is unusual and directly relevant to HCI and human-robot interaction programs.

**5 · Structured interviewing as a transferable method**
Interviewer Society productions (§7) · NewsFlick user interviews (§4.1.6) · PillWise research (§4.2.8). ⟡ M#6 — the mentor's point, and it holds: this is one skill applied in three places, not an extracurricular plus a product task.

---

## §10. Consolidated gap queue

Ordered by impact on the application. The top block is what the mentor review actually turns on.

### Tier 1 — blocking; the mentor's review does not close without these
| # | Item | §ref | Mentor |
|---|---|---|---|
| 1 | Embedding model + clustering algorithm + retrieval index + streaming-clustering solution | 4.1.4B | ⟡ M#2.1 |
| 2 | Pill model architecture **and the comparison experiment that selected it** | 4.2.4 | ⟡ M#4.1 |
| 3 | Pill recognition accuracy numbers | 4.2.5 | ⟡ M#4.2 |
| 4 | Anti-hallucination design | 4.1.5 | ⟡ M#2.2 |
| 5 | Cross-source objectivity safeguards | 4.1.4D | ⟡ M#2.2 |
| 6 | Card-based design rationale (cognition / comparability) | 4.1.6 | ⟡ M#2.3 |
| 7 | AI-process transparency in the UI — designed, or honestly declared absent | 4.1.7 | ⟡ M#2.3 |
| 8 | Front-end ↔ back-end data flow, traced end to end | 4.2.6 | ⟡ M#4.3 |
| 9 | Optimization work with before/after numbers | 4.1.8 | ⟡ M#2.4 |
| 10 | SenseTime process and results | 4.3.3–4.3.4 | ⟡ M#5 |
| 11 | Maintenance/upgrade arc for NewsFlick and PillWise | 4.1.11, 4.2.9 | ⟡ M#3 |
| 12 | Interviewer Society → product research linkage | 7.4 | ⟡ M#6 |

### Tier 2 — high impact, not explicitly requested
| # | Item | §ref |
|---|---|---|
| 13 | Resolve the PillWise embedded/hardware question | 4.2.7 |
| 14 | Link awards to the projects that won them (Techathon+→?, AI Competition→Decode: Veritas?, HKSTP seed→which venture) | 6.1, 6.2, 6.4 |
| 15 | User interview specifics: N, method, findings, resulting changes | 4.1.6 |
| 16 | §5.2 study results — currently no outcome reported at all | 5.2.4 |
| 17 | SAH-LC per-sequence results and CPU specification | 5.1.4, 5.1.5 |
| 18 | Public traction / online exposure for both ventures | 4.1.12, 4.2.10 |
| 19 | Ownership boundaries on co-founded and team work | 4.1.3, 5.1.1 |
| 20 | Decode: Veritas expansion — a verifiable shipped product on one line | 4.1.9 |

### Tier 3 — completeness
| # | Item | §ref |
|---|---|---|
| 21 | Full course inventory | 3.3 |
| 22 | GPA, program characterisation | 3.1, 3.2 |
| 23 | Skills evidence attribution; drop anything unattributable | 8 |
| 24 | Robot Design Contest technical detail | 6.3 |
| 25 | Interview production counts and metrics | 7.2 |
| 26 | Online presence URLs | 2.1 |
| 27 | Test score dates, validity, verified percentiles | 2.2 |
| 28 | Unrecorded skills, courses, competitions | 8.5, 6.5 |

### Structural changes already applied
- ✅ Test scores split into their own section (⟡ M#1) — §2
- ✅ "Product Builder" → "Engineer" (⟡ M#4) — §4.2
- ✅ thinking → implementation → maintenance/upgrade structure imposed on §4.1, §4.2, §5.1 (⟡ M#3)
- ✅ Coursework held as a re-cuttable inventory rather than a fixed line (⟡ M#0) — §3.3

---

## §11. Notes on filling this in

**Answer from artefacts, not memory.** Most Tier 1 items are recorded somewhere: `requirements.txt` and import statements name your models and libraries; git log dates your milestones and shows what you tried and reverted; commit messages and PR descriptions carry the reasoning; old Figma files hold the design iterations; notebooks hold the evaluation numbers. Reading your own repository will answer more of §4.1.4 and §4.2.4 in an hour than recall will.

**Numbers are the difference.** The one CV entry the mentor did not criticise (§5.1) is the one carrying architectures, dimensions, baselines, and measurements. That is not a coincidence — it is the specification for everything else here.

**Losing rows belong in the table.** For §4.2.4 in particular, the mentor asked for the *comparison process*. A result table containing an approach you rejected demonstrates engineering judgement in a way a single final number never does.

**"Not built yet" is a complete answer.** §4.1.7 and §4.1.5 may have no implementation behind them. Writing *"designed but deprioritised, for this reason"* is credible and safe. Implying a mechanism that does not exist fails at the first technical question, and this material will be read by people who ask technical questions.

**Keep this file the source of truth.** Every derived document — CV, résumé, SOP, interview prep, portfolio — gets cut down from here. When a fact changes, change it here first.
