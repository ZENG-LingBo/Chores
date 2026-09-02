# CHI 2027 PCS Submission Kit — DefuseLab Community Notes Paper

Everything needed for the PCS form (`CHI 2027 Papers`, deadline **Thu Sept 10, 2026, AoE**).
Paste-ready blocks are marked; fields the team must fill by hand are in the checklist at the end.

---

## 1. Keywords (reviewer-matching tags)

Per the form: Domain 2–6 (guidance 3–6), Method 1–2, Users 0–2 (only if a
population is the focus), Primary Contribution exactly 1. Strategy: pick the
reviewers we want, keep all domains in one AC's lane.

### Domain — select these 3 (all under *Social Computing & Online Communities*)

| Pick | Why these reviewers |
|---|---|
| **Online Communities & Social Relationships** | Sample terms literally include *fandom*. These reviewers study communities and peer dynamics and are comfortable with forum deployments and mixed methods. |
| **Content Moderation** | Platform governance / *deliberation* / community governance. They value platform-feature interventions on discourse — exactly what the note is. |
| **Online Safety & Harassment** | *Hate speech* / toxicity reviewers. They know Perspective API scoring and incivility coding, so they will be comfortable with our procedures and measures. |

**Deliberately NOT picked:**
- Any **AI & ML** domain — the paper de-centers the LLM (it's backstage by design); AI reviewers would apply model-evaluation standards the paper doesn't aim at.
- **Misinformation & Disinformation** — the feature *name* evokes it, but the paper is not about facts or corrections; fact-checking standards would hurt it.

### Method — select 2

- **Field Study** — deployment on a live forum with real community members.
- **Mixed Methods** — behavioral logs + surveys + focus groups.

(These select reviewers tolerant of small-N real-community deployments over lab-statistics purists.)

### Users — select none

Fandom members are not a listed population and no listed demographic is the
paper's focus. Tagging one (e.g., *Teens*) would invite population-specific
review standards. If the group insists on one: *General / No Specific User Group*.

### Primary Contribution — select exactly 1

- **Empirical study that tells us about how people use a system**

The claims are behavioral outcomes of people using the Community Notes feature.
Not *Artifact or System*: that tag sets technical-novelty and systems-evaluation
expectations the paper doesn't target.

---

## 2. Submission Abstract (form limit: 150 words — this is 149)

> Hostility between online communities is rooted in group identity rather than
> substantive disagreement, and interventions aimed at beliefs leave it
> untouched. Drawing on cooperative interdependence theory, we built a platform
> feature through which rival groups must co-author a single, co-signed post: a
> Community Note with one slot per group that publishes only when both sides
> have written their part. We deployed it on KFeed, a forum we built, in
> sessions where members of ARMY and BLINK, the rival fandoms of BTS and
> BLACKPINK, discussed K-pop topics, while an LLM monitored toxicity and
> published the note backstage. When the note appeared, mean message toxicity
> fell by 41%; the decline was shared across participants, and references to
> the rival fandom as "they" halved, yet attitudes toward that fandom did not
> move. We argue the note interrupts the attention escalation requires, and
> discuss conflict interventions that need not be accepted to work.

(The same text is now the abstract in `main.tex`.)

---

## 3. Alt-text for All Figures and Tables (paste-ready)

Figure 1: "Two-panel teaser. Panel A is a three-stage diagram: an escalating mixed feed of ARMY and BLINK posts, then a pinned Community Note with one contribution slot per fandom that publishes only when both sides write, then the published co-signed note carrying both fandom badges, assembled backstage by an LLM. Panel B is a bar chart: mean message toxicity 0.368 before the note versus 0.217 after it, a 41% reduction."

Figure 2: "Bar chart of mean message toxicity in nine five-minute windows across the session, with a line connecting the bar tops. Before a dashed line marking the Community Note's appearance at 15 minutes, the windows read 0.371, 0.317 and a peak of 0.395. After it they read 0.200, 0.255, 0.281, 0.229, 0.190 and 0.117. Toxicity halves across the note boundary, and no window after the note reaches even the quietest window before it."

Figure 3: "Slope chart of per-participant mean toxicity from the free phase to the note phase for the five participants who posted in both. Four lines decline; one rises slightly. The highlighted line for the most toxic participant, B1, remains the highest in the room. Annotation: paired t(4) = -3.19, p = .033, effect size d_z = 1.43."

Figure 4: "Two histograms of message toxicity, before and after the note. In the free phase, messages cluster around 0.2 to 0.3 with a tail reaching 1.0. In the note phase the mass shifts toward 0 to 0.3, and the remaining high-toxicity messages, marked with hatching, belong almost entirely to the most toxic participant, B1."

Figure 5: "Bar chart with jittered participant dots showing mean toxicity of 0.347 in the Day 1 free phase, 0.228 in the Day 1 note phase, and 0.267 on Day 2 with no feature. Day 2 sits between the two Day 1 phases; Welch tests against both are reported as not significant."

Table 1: "Session summary by phase. Free phase: 30 messages, mean toxicity 0.368, 0.50 'they' references and 0.10 'we' references per message, 'they' share of plural references 0.833. Note phase: 51 messages, mean toxicity 0.217, 0.20 'they' and 0.08 'we' per message, 'they' share 0.714."

Table 2: "Post-session survey means with standard deviations for the ten treatment-arm participants, on 1-to-5 scales: legitimacy of the note 2.20, reactance toward the note 4.25, perceived similarity to the rival fandom 3.02, perception of the rival fandom 1.95, cross-fandom contact intentions 3.02, session felt heated 4.20. Feeling thermometers, 0 to 100: own fandom 79.8, rival fandom 19.7, gap 60 points."

---

## 4. References (paste-ready, from the rendered PDF)

[1] Lisa P. Argyle, Christopher A. Bail, Ethan C. Busby, Joshua R. Gubler, Thomas Howe, Christopher Rytting, Taylor Sorensen, and David Wingate. 2023. Leveraging AI for Democratic Discourse: Chat Interventions Can Improve Online Political Conversations at Scale. Proceedings of the National Academy of Sciences 120, 41 (2023), e2311627120. https://doi.org/10.1073/pnas.2311627120
[2] Christopher A. Bail, Lisa P. Argyle, Taylor W. Brown, John P. Bumpus, Haohan Chen, M. B. Fallin Hunzaker, Jaemin Lee, Marcus Mann, Friedolin Merhout, and Alexander Volfovsky. 2018. Exposure to Opposing Views on Social Media Can Increase Political Polarization. Proceedings of the National Academy of Sciences 115, 37 (2018), 9216–9221. https://doi.org/10.1073/pnas.1804840115
[3] Nyla R. Branscombe, Naomi Ellemers, Russell Spears, and Bertjan Doosje. 1999. The Context and Content of Social Identity Threat. In Social Identity: Context, Commitment, Content, Naomi Ellemers, Russell Spears, and Bertjan Doosje (Eds.). Blackwell, Oxford, 35–58.
[4] Jack W. Brehm. 1966. A Theory of Psychological Reactance. Academic Press, New York, NY.
[5] Robert B. Cialdini, Richard J. Borden, Avril Thorne, Marcus R. Walker, Stephen Freeman, and Lloyd R. Sloan. 1976. Basking in Reflected Glory: Three (Football) Field Studies. Journal of Personality and Social Psychology 34, 3 (1976), 366–375. https://doi.org/10.1037/0022-3514.34.3.366
[6] Jamie Cleland. 2014. Racism, Football Fans, and Online Message Boards: How Social Media Has Added a New Dimension to Racist Discourse in English Football. Journal of Sport and Social Issues 38, 5 (2014), 415–431. https://doi.org/10.1177/0193723513499922
[7] Kevin Coe, Kate Kenski, and Stephen A. Rains. 2014. Online and Uncivil? Patterns and Determinants of Incivility in Newspaper Website Comments. Journal of Communication 64, 4 (2014), 658–679. https://doi.org/10.1111/jcom.12104
[8] Aidan Combs, Graham Tierney, Brian Guay, Friedolin Merhout, Christopher A. Bail, D. Sunshine Hillygus, and Alexander Volfovsky. 2023. Reducing Political Polarization in the United States with a Mobile Chat Platform. Nature Human Behaviour 7 (2023), 1454–1461. https://doi.org/10.1038/s41562023-01655-0
[9] Thomas H. Costello, Gordon Pennycook, and David G. Rand. 2024. Durably Reducing Conspiracy Beliefs Through Dialogues with AI. Science 385, 6714 (2024), eadq1814. https://doi.org/10.1126/science.adq1814
[10] Mark Duffett. 2013. Understanding Fandom: An Introduction to the Study of Media Fan Culture. Bloomsbury, New York, NY.
[11] Casey Fiesler, Shannon Morrison, and Amy S. Bruckman. 2016. An Archive of Their Own: A Case Study of Feminist HCI and Values in Design. In Proceedings of the 2016 CHI Conference on Human Factors in Computing Systems. ACM, New York, NY, 2574–2585. https://doi.org/10.1145/2858036.
[12] Samuel L. Gaertner and John F. Dovidio. 2000. Reducing Intergroup Bias: The Common Ingroup Identity Model. Psychology Press, Philadelphia, PA.
[13] Fabrizio Gilardi, Meysam Alizadeh, and Maël Kubli. 2023. ChatGPT Outperforms Crowd Workers for Text-Annotation Tasks. Proceedings of the National Academy of Sciences 120, 30 (2023), e2305016120. https://doi.org/10.1073/pnas.2305016120
[14] Andrew M. Guess, Neil Malhotra, Jennifer Pan, Pablo Barberá, Hunt Allcott, Taylor Brown, Adriana Crespo-Tenorio, Drew Dimmery, Deen Freelon, Matthew Gentzkow, et al. 2023. How Do Social Media Feed Algorithms Affect Attitudes and Behavior in an Election Campaign? Science 381, 6656 (2023), 398–404. https://doi.org/10.1126/science.abp9364
[15] Matthew J. Hornsey and Michael A. Hogg. 2000. Assimilation and Diversity: An Integrative Model of Subgroup Relations. Personality and Social Psychology Review 4, 2 (2000), 143–156. https://doi.org/10.1207/S15327957PSPR0402_03
[16] Shanto Iyengar, Yphtach Lelkes, Matthew Levendusky, Neil Malhotra, and Sean J. Westwood. 2019. The Origins and Consequences of Affective Polarization in the United States. Annual Review of Political Science 22 (2019), 129–146. https://doi.org/10.1146/annurev-polisci-051117-073034
[17] Shanto Iyengar, Gaurav Sood, and Yphtach Lelkes. 2012. Affect, Not Ideology: A Social Identity Perspective on Polarization. Public Opinion Quarterly 76, 3 (2012), 405–431. https://doi.org/10.1093/poq/nfs038
[18] Maurice Jakesch, Megan French, Xiao Ma, Jeffrey T. Hancock, and Mor Naaman. 2019. AI-Mediated Communication: How the Perception that Profile Text was Written by AI Affects Trustworthiness. In Proceedings of the 2019 CHI Conference on Human Factors in Computing Systems. ACM, New York, NY, 1–13. https://doi.org/10.1145/3290605.3300469
[19] Dal Yong Jin and Kyong Yoon. 2016. The Social Mediascape of Transnational Korean Pop Culture: Hallyu 2.0 as Spectacle. New Media & Society 18, 7 (2016), 1277–1292. https://doi.org/10.1177/1461444814554895
[20] Alyssa Lees, Vinh Q. Tran, Yi Tay, Jeffrey Sorensen, Jai Gupta, Donald Metzler, and Lucy Vasserman. 2022. A New Generation of Perspective API: Efficient Multilingual Character-Level Transformers. In Proceedings of the 28th ACM SIGKDD Conference on Knowledge Discovery and Data Mining. ACM, New York, NY, 3197–3207. https://doi.org/10.1145/3534678.3539147
[21] Mark Levine, Amy Prosser, David Evans, and Stephen Reicher. 2005. Identity and Emergency Intervention: How Social Group Membership and Inclusiveness of Group Boundaries Shape Helping Behavior. Personality and Social Psychology Bulletin 31, 4 (2005), 443–453. https://doi.org/10. 1177/0146167204271651
[22] Alice E. Marwick. 2021. Morally Motivated Networked Harassment as Normative Reinforcement. Social Media + Society 7, 2 (2021). https: //doi.org/10.1177/20563051211021378
[23] Lilliana Mason. 2018. Uncivil Agreement: How Politics Became Our Identity. University of Chicago Press, Chicago, IL.
[24] Courtney McLaren and Dal Yong Jin. 2020. “You Can’t Help But Love Them”: BTS, Transcultural Fandom, and Affective Identities. Korea Journal 60, 1 (2020), 100–127. https://doi.org/10.25024/kj.2020.60.1.100
[25] Christopher W. Moore. 2014. The Mediation Process: Practical Strategies for Resolving Conflict (4th ed.). Jossey-Bass, San Francisco, CA.
[26] Salma Mousa. 2020. Building Social Cohesion Between Christians and Muslims Through Soccer in Post-ISIS Iraq. Science 369, 6505 (2020), 866–870. https://doi.org/10.1126/science.abb3153
[27] James W. Pennebaker. 2011. The Secret Life of Pronouns: What Our Words Say About Us. Bloomsbury Press, New York, NY.
[28] Ashwin Rajadesingan, Paul Resnick, and Ceren Budak. 2020. Quick, Community-Specific Learning: How Distinctive Toxicity Norms Are Maintained in Political Subreddits. In Proceedings of the International AAAI Conference on Web and Social Media, Vol. 14. AAAI Press, Palo Alto, CA, 557–568. https://doi.org/10.1609/icwsm.v14i1.7323
[29] Steve Rathje, Jay J. Van Bavel, and Sander van der Linden. 2021. Out-group Animosity Drives Engagement on Social Media. Proceedings of the National Academy of Sciences 118, 26 (2021), e2024292118. https://doi.org/10.1073/pnas.2024292118
[30] Muzafer Sherif, O. J. Harvey, B. Jack White, William R. Hood, and Carolyn W. Sherif. 1961. Intergroup Conflict and Cooperation: The Robbers Cave Experiment. In Intergroup Conflict and Cooperation: The Robbers Cave Experiment. University Book Exchange, Norman, OK.
[31] William B. Swann, Ángel Gómez, D. Conor Seyle, J. Francisco Morales, and Carmen Huici. 2009. Identity Fusion: The Interplay of Personal and Social Identities in Extreme Group Behavior. Journal of Personality and Social Psychology 96, 5 (2009), 995–1011. https://doi.org/10.1037/a0013668
[32] William B. Swann, Jolanda Jetten, Ángel Gómez, Harvey Whitehouse, and Brock Bastian. 2012. When Group Membership Gets Personal: A Theory of Identity Fusion. Psychological Review 119, 3 (2012), 441–456. https://doi.org/10.1037/a0028589
[33] Henri Tajfel, M. G. Billig, R. P. Bundy, and Claude Flament. 1971. Social Categorization and Intergroup Behaviour. European Journal of Social Psychology 1, 2 (1971), 149–178. https://doi.org/10.1002/ejsp.2420010202
[34] Henri Tajfel and John C. Turner. 1979. An Integrative Theory of Intergroup Conflict. In The Social Psychology of Intergroup Relations, William G. Austin and Stephen Worchel (Eds.). Brooks/Cole, Monterey, CA, 33–47.
[35] Michael Henry Tessler, Michiel A. Bakker, Daniel Jarrett, Hannah Sheahan, Martin J. Chadwick, Raphael Koster, Georgina Evans, Lucy CampbellGillingham, Tantum Collins, David C. Parkes, Matthew Botvinick, and Christopher Summerfield. 2024. AI Can Help Humans Find Common Ground in Democratic Deliberation. Science 386, 6719 (2024), eadq2852. https://doi.org/10.1126/science.adq2852
[36] Petter Törnberg. 2022. How Digital Media Drive Affective Polarization Through Partisan Sorting. Proceedings of the National Academy of Sciences 119, 42 (2022), e2207159119. https://doi.org/10.1073/pnas.2207159119
[37] John C. Turner, Michael A. Hogg, Penelope J. Oakes, Stephen D. Reicher, and Margaret S. Wetherell. 1987. Rediscovering the Social Group: A Self-Categorization Theory. Basil Blackwell, Oxford.
[38] Jan G. Voelkel, Michael N. Stagnaro, James Y. Chu, Sophia L. Pink, Joseph S. Mernyk, Chrystal Redekopp, Isaias Ghezae, Matthew Cashman, Dhaval Adjodah, Levi G. Allen, et al. 2024. Megastudy Identifying Effective Interventions to Strengthen Americans’ Democratic Attitudes. Science 386, 6719 (2024), eadh4764. https://doi.org/10.1126/science.adh4764
[39] Daniel L. Wann and Nyla R. Branscombe. 1990. Die-Hard and Fair-Weather Fans: Effects of Identification on BIRGing and CORFing Tendencies. Journal of Sport and Social Issues 14, 2 (1990), 103–117. https://doi.org/10.1177/019372359001400203
[40] Daniel L. Wann and Nyla R. Branscombe. 1993. Sports Fans: Measuring Degree of Identification with Their Team. International Journal of Sport Psychology 24, 1 (1993), 1–17.
[41] Stefan Wojcik, Sophie Hilgard, Nick Judd, Delia Mocanu, Stephen Ragain, M. B. Fallin Hunzaker, Keith Coleman, and Jay Baxter. 2022. Birdwatch: Crowd Wisdom and Bridging Algorithms Can Inform Understanding and Reduce the Spread of Misinformation. arXiv preprint arXiv:2210.15723 (2022). https://doi.org/10.48550/arXiv.2210.15723
[42] Yiyi Yin. 2020. An Emergent Algorithmic Culture: The Data-ization of Online Fandom in China. International Journal of Cultural Studies 23, 4 (2020), 475–492. https://doi.org/10.1177/1367877920908269

---

## 5. Remaining form fields — fill by hand

- [ ] **Title field** — must match the PDF, Title Case: *Defusing Affective Polarization with a Co-Authored Community Note: A Field Experiment with Rival K-pop Fandoms* (update both if the group renames it).
- [ ] **Authors** — add every author in paper order, linked to PCS accounts; ORCID required for all; DBLP or "N/A"; affiliations are final at submission.
- [ ] **Paper PDF** — single-column `\documentclass[manuscript,review,anonymous]{acmart}` (already what `main.tex` uses); verify anonymization incl. PDF metadata, acknowledgments, and supplementary files.
- [ ] **Paper length** field (+ justification only if "Excessively Long").
- [ ] **Source files ZIP** (visible to chairs only; no anonymization needed).
- [ ] **Supplementary ZIP** (optional but encouraged): anonymized data + analysis script + README.md — `analysis/analyze.py` and `data/` are good candidates after anonymization review.
- [ ] **Video figure** (optional, MP4 H.264 1080p 16:9 ≤300MB) + SRT subtitles.
- [ ] **Ethics review statement** (AC-visible, non-anonymous) — state the IRB/ethics status for the human-subjects sessions; the paper's own IRB TODO must also be resolved before submission.
- [ ] **Related concurrent submissions** — list any sibling papers from the project (title, venue, difference, CHI paperID if applicable) + upload anonymized PDFs.
- [ ] **External reviewer recommendations** (optional, ≤5, no conflicts).
- [ ] **Review responsibility slots** — name 4 slots from the author list; at least one must be a senior author; every named reviewer must complete their PCS reviewer profile (volunteer, expertise, ≥10 sample papers, ORCID, DBLP).
- [ ] **Visa letter list** (optional).
- [ ] **Submitter agreement** checkboxes.
