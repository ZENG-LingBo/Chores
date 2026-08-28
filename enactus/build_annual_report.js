/**
 * Enactus_Annual_Report_Draft.docx — pages 1–3 of the four-page Annual
 * Report (page 4 is Enactus_Impact_Page.docx). Drafted from the team's
 * current Fliq positioning, compressed to Enactus weighting: realized
 * impact first, innovation in service of it. Purple [BRACKETS] are
 * numbers to fill; red guidance boxes are internal and must be deleted
 * before print.
 */
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  WidthType, ShadingType, AlignmentType, BorderStyle, ImageRun, PageBreak,
  VerticalAlign, LevelFormat, convertInchesToTwip,
} = require("docx");
const fs = require("fs");

const PURPLE = "800080", NAVY = "11256A", PLUM = "352E4A", MUTED = "6E6787",
      LAV = "EFE9FF", SKY = "E7F1FD", PINK = "FDF0FD", LIME = "C9FA85",
      RULE = "D8D0E8", WHITE = "FFFFFF", RED = "B03020";
const HEAD = "Space Grotesk", BODY = "Inter";
const SZ = 19; // 9.5pt body

const t = (text, o = {}) => new TextRun({ text, font: BODY, size: SZ, color: PLUM, ...o });
const ph = (text) => t(text, { color: PURPLE, bold: true });
const p = (children, o = {}) => new Paragraph({ children, spacing: { after: 90, line: 252 }, ...o });

const h1 = (text) =>
  new Paragraph({
    spacing: { before: 60, after: 100 },
    children: [t(text, { font: HEAD, bold: true, size: 32, color: NAVY })],
  });
const h2 = (text) =>
  new Paragraph({
    spacing: { before: 140, after: 70 },
    children: [t(text.toUpperCase(), { font: HEAD, bold: true, size: 20, color: PURPLE })],
  });

const bullet = (runs) =>
  new Paragraph({
    numbering: { reference: "b", level: 0 },
    spacing: { after: 50, line: 248 },
    children: runs,
  });

const guidance = (text) =>
  new Table({
    width: { size: 10466, type: WidthType.DXA },
    columnWidths: [10466],
    rows: [new TableRow({ children: [new TableCell({
      width: { size: 10466, type: WidthType.DXA },
      shading: { type: ShadingType.CLEAR, fill: "FFF4F2" },
      borders: {
        top: { style: BorderStyle.SINGLE, size: 4, color: RED },
        bottom: { style: BorderStyle.SINGLE, size: 4, color: RED },
        left: { style: BorderStyle.SINGLE, size: 12, color: RED },
        right: { style: BorderStyle.SINGLE, size: 4, color: RED },
      },
      margins: { top: 60, bottom: 60, left: 110, right: 110 },
      children: [new Paragraph({ spacing: { after: 0 }, children: [
        t("GUIDANCE (delete before print) — ", { bold: true, color: RED, size: 17 }),
        t(text, { color: RED, size: 17, italics: true }),
      ]})],
    })]})],
  });

const statTable = (cells) => {
  const w = Math.floor(10466 / cells.length);
  const ws = cells.map((_, i) => (i === cells.length - 1 ? 10466 - w * (cells.length - 1) : w));
  return new Table({
    width: { size: 10466, type: WidthType.DXA },
    columnWidths: ws,
    rows: [new TableRow({ children: cells.map(([big, small, fill], i) => new TableCell({
      width: { size: ws[i], type: WidthType.DXA },
      shading: { type: ShadingType.CLEAR, fill },
      borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE },
                 left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE } },
      margins: { top: 90, bottom: 90, left: 110, right: 110 },
      verticalAlign: VerticalAlign.TOP,
      children: [
        new Paragraph({ spacing: { after: 20 }, children: [t(big, { font: HEAD, bold: true, size: 30, color: NAVY })] }),
        new Paragraph({ spacing: { after: 0 }, children: [t(small, { size: 17, color: PLUM })] }),
      ],
    }))})],
  });
};

const logo = fs.readFileSync("/home/user/Chores/assets/fliq-logo-purple.png");

const children = [
  // ============================ PAGE 1 ============================
  new Paragraph({
    spacing: { after: 60 },
    children: [
      new ImageRun({ type: "png", data: logo, transformation: { width: 95, height: 35 } }),
      t("   ", {}),
      t("ENACTUS HKUST · ANNUAL REPORT ", { font: HEAD, bold: true, size: 19, color: NAVY }),
      ph("[year]"),
    ],
  }),
  h1("Information is abundant. Understanding is not."),
  p([
    t("Young people want to stay informed, but the way news is delivered pushes them away. "),
    t("42% of 18–24-year-olds now avoid news, only 37% trust it", { bold: true }),
    t(", and young people are three times more likely than older audiences to say they avoid news because it is "),
    t("difficult to understand", { italics: true }),
    t(" (Reuters Institute, 2025). A global study of more than 66,000 people found Gen Z is the worst generation at telling real headlines from fake ones — and the most aware of that vulnerability."),
  ]),
  p([
    t("The problem is not access to information. Young people already have more information than they can process. The problem is understanding what happened, knowing what to trust, and separating the facts of an event from the noise around it. Traditional news interfaces mix three different things together — "),
    t("what happened, how we know, and how people are interpreting it", { italics: true }),
    t(" — and leave readers to untangle facts, claims, uncertainty, sources, opinions, and social reaction themselves."),
  ]),
  h2("We measured the need ourselves"),
  statTable([
    ["79%", "rank trust — knowing a story is accurate — as their #1 priority in news (our 100-response study)", LAV],
    ["52%", "would read news more often if they could trust it more", SKY],
    ["43%", "say they simply cannot tell what is true", PINK],
  ]),
  p([
    t("Before writing a line of code we ran our own needs assessment with the audience we serve: a 100-response study recruited via Prolific (18–34), an earlier 18-response study, roughly 30 interviews, and an 86-participant A/B test of the trust features — "),
    t("~85% said they would switch to the transparent version", { bold: true }),
    t("."),
  ], { spacing: { before: 90, after: 90 } }),
  h2("Entrepreneurial leadership"),
  p([
    t("We did not wait for permission to act on what we found. As a two-person student team we incorporated "),
    t("NewsFlick Limited", { bold: true }),
    t(", closed a small angel and family round, won Silver in Trusted AI & Data Science at HKUST Techathon+ 2026, became IET Young Professionals Undergraduate Champion and Enactus Hong Kong Regional Champion, and were admitted to HKUST InnoBay, the HKSTP Ideation programme, Dream Builder and AWS Activate. The team owns and operates every part of the product — research, design, engineering, and the business — with faculty advisors at HKUST supporting AI and product development."),
  ]),
  p([
    t("This report covers two initiatives: "),
    t("Fliq", { bold: true, color: PURPLE }),
    t(", a mobile news platform that redesigns news around understanding and verification, and "),
    t("Decode: Veritas", { bold: true, color: PURPLE }),
    t(", our media-literacy programme in Hong Kong classrooms. All impact figures cover the official reporting period "),
    ph("[1 Sep 2026 – 31 Aug 2027]"),
    t(" and follow the Enactus impact definitions; earlier work appears only as context."),
  ]),
  guidance("Judges read page 1 for the needs assessment and your ownership of the project. Keep partner contributions clearly separate from team-led work — Enactus evaluates only what the team itself did."),
  new Paragraph({ children: [new PageBreak()] }),

  // ============================ PAGE 2 ============================
  h1("What we built"),
  h2("Fliq — news redesigned around understanding"),
  p([
    t("Fliq transforms coverage from many sources into visual, structured stories that separate "),
    t("what happened", { bold: true }),
    t(" (adaptive story cards with expandable Deep Dives), "),
    t("how we know", { bold: true }),
    t(" (every claim labeled confirmed, disputed, developing, or analysis, with its evidence attached and traced to origin — fifty outlets republishing the same wire copy count as one source, not fifty), and "),
    t("how people are interpreting it", { bold: true }),
    t(" (a Social Layer organizing official, expert, media, creator, and public perspectives, with Temperature separating emotional reaction from factual certainty). A finite, personalized feed gives readers a clear point at which they are caught up."),
  ]),
  bullet([t("Story Cards & Deep Dives — ", { bold: true }), t("focused visual cards that expand in place into context and a “How we know” section.")]),
  bullet([t("Confidence Signal — ", { bold: true }), t("how well supported a story currently is, inspectable down to individual sources, their track record and leaning.")]),
  bullet([t("Three voices — ", { bold: true }), t("Smart Friend, Traditional, Easy: the same verified facts adapt to the reader; facts and scores never change.")]),
  bullet([t("Finite Feed — ", { bold: true }), t("Morning Brief plus Essential, Yours, Blindspot, and Wildcard, with visible progress instead of infinite scroll.")]),
  p([
    t("Under the hood, “what do we actually know” is a computed, checkable property rather than a model's assertion: an incremental three-layer clustering pipeline gives each story a stable identity; each verification state carries its own evidence requirement built into the extraction schema (a claim marked confirmed needs two or more independent sources, or it is dropped); and a metered verification pass is spent only on borderline cases, tuned to require genuine cross-source agreement rather than volume."),
  ]),
  p([
    t("In the reporting period the public beta reached "),
    ph("[N]"), t(" readers. Of these, "), ph("[N]"),
    t(" completed our in-app comprehension instrument at onboarding and again at "),
    ph("[4–8]"), t(" weeks, improving their news-comprehension scores by "),
    ph("[X]%"), t(" on average — the measured change behind the Direct Impact column on page 4."),
  ]),
  h2("Decode: Veritas — media literacy in the classroom"),
  p([
    t("The same verification thinking, taught directly. In "),
    ph("[N]"), t(" Hong Kong schools we ran "),
    ph("[N]"), t(" workshop sessions teaching "),
    ph("[N]"), t(" students to separate claims from evidence, spot manufactured certainty, and read a confidence signal critically. Every participant took an identical media-literacy test before the first and after the final workshop; scores improved by "),
    ph("[X]%"), t(" on average, and "),
    ph("[N]"), t(" students reported sharing what they learned at home."),
  ]),
  p([
    t("“", { color: MUTED, italics: true }),
    ph("[One-sentence quote from a named student or teacher — ask permission first]"),
    t("”", { color: MUTED, italics: true }),
    t("  — ", { color: MUTED }),
    ph("[Name, school]"),
  ]),
  guidance("This page carries the criterion's Innovation weight, but the two [measured change] paragraphs are what score. Downloads and waitlist are Reach — never present them as impact. The named beneficiary story is what judges remember; get consent early."),
  new Paragraph({ children: [new PageBreak()] }),

  // ============================ PAGE 3 ============================
  h1("A business built to sustain the impact"),
  h2("Business model"),
  p([
    t("Fliq pairs a "),
    t("low-priced subscription with advertising", { bold: true }),
    t(" — a model chosen from our own study data (43% would pay $0 for a perfect news product; only 6% would pay more than $5/month), not from hope. The core news experience stays free; revenue scales with readership while costs are held down by the finite feed, a lean card count per story, and licensed-pool sourcing that scales by adding pools rather than re-architecting. Decode: Veritas is offered to schools at "),
    ph("[fee / free]"),
    t(", covering delivery cost while feeding the product real classroom evidence."),
  ]),
  h2("Financials in the reporting period"),
  bullet([t("Income/Revenue: ", { bold: true }), t("$"), ph("[N]"), t(" — subscriptions $"), ph("[N]"), t(", school programme fees $"), ph("[N]"), t(", grants $"), ph("[N]"), t(". Equity investment is excluded (not sales, grant, sponsorship, or donation)."), ]),
  bullet([t("Expenses: ", { bold: true }), t("$"), ph("[N]"), t(" — infrastructure and licensed sourcing run at low, predictable cost (order of hundreds of USD per month pre-launch).")]),
  bullet([t("Profit/Surplus: ", { bold: true }), t("$"), ph("[N]"), t(", reinvested into ingestion breadth and school delivery.")]),
  h2("Our role, and our partners'"),
  p([
    t("Everything reported here was designed, built, and delivered by the student team: the pipeline, the app, the research instruments, and the classroom teaching. Partners — "),
    ph("[schools, licensed content vendors, programme sponsors]"),
    t(" — provided access and materials; the measured change is attributable to the team's own intervention."),
  ]),
  h2("The next twelve months"),
  bullet([t("Readers: ", { bold: true }), t("grow measured-impact readers (both quizzes completed) to "), ph("[N]"), t(" and paying subscribers to "), ph("[N]"), t(" by "), ph("[month year]"), t(".")]),
  bullet([t("Schools: ", { bold: true }), t("expand Decode: Veritas to "), ph("[N]"), t(" schools; train "), ph("[N]"), t(" teachers so delivery scales beyond the founding team.")]),
  bullet([t("Product: ", { bold: true }), t("official launch, provisional patent filed, regression suite guarding the verification pipeline on every release.")]),
  p([
    t("Trust in news is not rebuilt by another publisher asking to be believed. It is rebuilt by giving a generation the means to examine why something should be believed — and measuring, reader by reader and classroom by classroom, that they can.", { italics: true, color: NAVY }),
  ], { spacing: { before: 120 } }),
  guidance("Keep every number here identical to page 4 and to the presentation script — after the Impact & Financial Review, numbers freeze; a mismatch on stage means disqualification. Page 4 of this report must be the Standardized Impact Page (Enactus_Impact_Page.docx)."),
];

const doc = new Document({
  numbering: {
    config: [{
      reference: "b",
      levels: [{
        level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 300, hanging: 180 } } },
      }],
    }],
  },
  styles: { default: { document: { run: { font: BODY, size: SZ, color: PLUM } } } },
  sections: [{
    properties: { page: { margin: { top: 620, bottom: 560, left: 720, right: 720 } } },
    children,
  }],
});

Packer.toBuffer(doc).then((b) => {
  fs.writeFileSync(__dirname + "/Enactus_Annual_Report_Draft.docx", b);
  console.log("Wrote Enactus_Annual_Report_Draft.docx");
});
