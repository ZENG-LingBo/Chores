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
> feature through which rival groups must co-author a single co-signed post: a
> Community Note with one slot per group that publishes only when both sides
> have written. We deployed it on KFeed, our forum, in five two-day
> sessions where members of ARMY and BLINK, rival fandoms of BTS and
> BLACKPINK, discussed K-pop; matched control sessions received an inert
> feature at the same trigger. Control sessions escalated after the trigger;
> note sessions did not, a 25.3-point difference that held in every session
> and persisted the next day without the feature. The calm came from the
> periphery: the heaviest posters grew hotter. We argue the note interrupts
> the attention escalation requires, and discuss interventions that need not
> be accepted to work.

(The same text is the abstract in `main.tex`; the 25.3 comes from `stats.tex`.)

---

## 3. Alt-text for All Figures and Tables (paste-ready)

Figure 1: "Two-panel teaser. Panel A is a three-stage diagram: an escalating mixed feed of ARMY and BLINK posts, then a pinned Community Note with one contribution slot per fandom that publishes only when both sides write, then the published co-signed note carrying both fandom badges, assembled backstage by an LLM. Panel B shows one Day-1 session in both arms as two stacked timelines, six participant rows each, one square per message shaded from calm to toxic, with a dashed line at 35 minutes marking the feature. In the Community Note arm the squares after the line are mostly light; in the control arm they are mostly dark."

Figure 2: "Two bar charts with participant dots. Left, Day 1 mean toxicity before and after the feature: Community Note arm 45.9 then 44.2, control arm 46.9 then 68.8, with each participant's two means connected; most note-arm lines fall and five thick lines, the heaviest posters, rise; almost every control-arm line rises. The difference-in-differences over sessions is 25.3 points, t(4) = 10.57, p < .001. Right, mean change per participant: note-arm periphery minus 18.2 with 24 dots mostly below zero, note-arm heaviest posters plus 14.1 with all five above zero, control periphery plus 21.4, control heaviest posters plus 23.3."

Figure 3: "Two paired histograms of message toxicity by arm, share of each arm's messages per 10-point bin. Before the feature, the Community Note arm (mean 45.9) and control arm (mean 46.9) follow the same hump centred near 45. After the feature, control bars pile up between 60 and 100 (mean 68.8, 77% of messages at 60 or above), while note-arm bars spread across the whole range (mean 44.2, 37% at 60 or above), with mass both at 0 to 30 and at 60 to 80."

Figure 4: "Two line charts of mean toxicity per five-minute window, five sessions pooled in bold with each session faint. Day 1: both arms rise together from about 30 to about 65 by minute 35, marked by a dashed line; after it the control line continues to 61, 73, 68, 70 and 76 while the Community Note line falls to 47 and 32, then rises to 36, 45 and 58. Day 2, no feature: the control line runs between 67 and 76 from the first window; the note line runs between 38 and 52."

Figure 5: "Six bars of session-level mean toxicity with the five sessions as connected dots. Community Note arm: 46.1 before the feature on Day 1, 43.8 after it, 44.5 on Day 2, with a bracket marked not significant, p = 0.78, between the last two. Control arm: 45.8, 68.8, 71.6, with a bracket marked not significant, p = 0.17. A bracket across the two Day 2 bars is marked three stars, p = 0.0008."

Figure 6: "Left: three bars on a 0 to 100 feeling thermometer, own fandom 80, K-pop overall 88, and rival fandom 20, with the 60-point own-rival gap marked. Right: horizontal bars for seven agreement items on a 1 to 5 scale: rival fans are intelligent 2.20, rival fans are moral 1.70, we share values 2.90, would share their post 2.50, would discuss K-pop with them 2.80, would work with them 2.90, and could be friends in real life 3.90, the only bar past the midpoint line at 3, highlighted. Pilot cohorts, n = 10."

Table 1: "Day 1 by arm and phase. Community Note arm before the feature: 272 messages, mean toxicity 45.9 (SD 20.1), 29% scoring 60 or above, 1.55 messages per minute, 0.42 'they' and 0.11 named references to the rival fandom per message, no note-task messages; after: 192 messages, 44.2 (25.7), 37%, 1.54 per minute, 0.19 'they', 0.29 named, 32% about the note task. Control arm before: 259 messages, 46.9 (20.2), 30%, 1.48 per minute, 0.48 'they', 0.12 named, none; after: 177 messages, 68.8 (17.9), 77%, 1.42 per minute, 0.44 'they', 0.12 named, 10% about the note task."

Table 2: "Robustness of the condition-by-phase difference. All 60 participants: note arm 46.1 to 43.8, control 45.8 to 68.8, difference-in-differences 25.3 points, t(4) = 10.57, p < .001. At least six messages, 56 participants: 24.8 points, t = 11.19. At least ten messages, 44 participants: 23.1 points, t = 8.64. Heaviest poster of each session excluded, 50 participants: note arm 44.8 to 26.9, control 46.9 to 69.5, 40.4 points, t = 10.52; all p < .001."

Table 3: "Post-session survey means with standard deviations for the ten treatment-arm participants of the pilot cohorts, on 1-to-5 scales: legitimacy of the note 2.20, reactance toward the note 4.25, perceived similarity to the rival fandom 3.02, perception of the rival fandom 1.95, cross-fandom contact intentions 3.02, session felt heated 4.20. Feeling thermometers, 0 to 100: own fandom 79.8, rival fandom 19.7, gap 60 points."

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
