/**
 * Enactus_Impact_Page.docx — the Standardized Impact Page (page 4 of the
 * Annual Report), in the exact section order and table format Enactus
 * requires. Purple [BRACKETED] placeholders mark every number that must be
 * filled from the evidence tracker before submission. All text >= 9pt.
 */
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  WidthType, ShadingType, AlignmentType, BorderStyle, LevelFormat, VerticalAlign,
} = require("docx");
const fs = require("fs");

const PURPLE = "800080", NAVY = "11256A", PLUM = "352E4A", MUTED = "6E6787",
      LAV = "EFE9FF", SKY = "E7F1FD", RULE = "D8D0E8", WHITE = "FFFFFF";
const HEAD = "Space Grotesk", BODY = "Inter";

const t = (text, o = {}) => new TextRun({ text, font: BODY, size: 18, color: PLUM, ...o });
const ph = (text) => t(text, { color: PURPLE, bold: true });          // placeholder
const p = (children, o = {}) => new Paragraph({ children, spacing: { after: 60 }, ...o });

const borders = () => ({
  top: { style: BorderStyle.SINGLE, size: 4, color: RULE },
  bottom: { style: BorderStyle.SINGLE, size: 4, color: RULE },
  left: { style: BorderStyle.SINGLE, size: 4, color: RULE },
  right: { style: BorderStyle.SINGLE, size: 4, color: RULE },
});

function cell(children, { w, fill = WHITE, header = false } = {}) {
  return new TableCell({
    width: { size: w, type: WidthType.DXA },
    shading: { type: ShadingType.CLEAR, fill },
    borders: borders(),
    verticalAlign: VerticalAlign.CENTER,
    margins: { top: 60, bottom: 60, left: 80, right: 80 },
    children: children.map((runs) =>
      new Paragraph({ children: runs, spacing: { after: 20 } })
    ),
  });
}
const hcell = (label, w) =>
  cell([[t(label, { bold: true, color: WHITE, size: 18, font: HEAD })]], { w, fill: NAVY, header: true });

// ---- Section heading pill ----
const secHead = (label) =>
  new Paragraph({
    spacing: { before: 160, after: 100 },
    shading: { type: ShadingType.CLEAR, fill: LAV },
    children: [t("  " + label + "  ", { bold: true, color: NAVY, size: 22, font: HEAD })],
  });

// ---- Impact Overview Table ----
const W = [1310, 1540, 1300, 1180, 1180, 1150, 1220, 1586]; // sums to 10466
const overview = new Table({
  width: { size: 10466, type: WidthType.DXA },
  columnWidths: W,
  rows: [
    new TableRow({
      tableHeader: true,
      children: [
        hcell("Project Name", W[0]), hcell("Direct Impact (people)", W[1]),
        hcell("Indirect Impact (people)", W[2]), hcell("Reach (people)", W[3]),
        hcell("Income/ Revenue (USD)", W[4]), hcell("Profit/ Surplus (USD)", W[5]),
        hcell("Planet Impact", W[6]), hcell("Projections (next 12 months)", W[7]),
      ],
    }),
    new TableRow({
      children: [
        cell([[t("Decode: Veritas", { bold: true, color: NAVY })]], { w: W[0], fill: LAV }),
        cell([[ph("[N]"), t(" students improved media-literacy scores by "), ph("[X]%"), t(" (pre/post test)")]], { w: W[1] }),
        cell([[ph("[N]"), t(" family members of trained students")]], { w: W[2] }),
        cell([[ph("[N]"), t(" people via school talks & campaigns")]], { w: W[3] }),
        cell([[t("$"), ph("[N]"), t(" school programme fees")]], { w: W[4] }),
        cell([[t("$"), ph("[N]")]], { w: W[5] }),
        cell([[t("N/A")]], { w: W[6] }),
        cell([[t("Expand to "), ph("[N]"), t(" schools by "), ph("[month year]")]], { w: W[7] }),
      ],
    }),
    new TableRow({
      children: [
        cell([[t("Fliq", { bold: true, color: NAVY })]], { w: W[0], fill: SKY }),
        cell([[ph("[N]"), t(" beta readers improved news-comprehension scores by "), ph("[X]%"), t(" (in-app pre/post)")]], { w: W[1] }),
        cell([[ph("[N]"), t(" household members of measured readers")]], { w: W[2] }),
        cell([[ph("[N]"), t(" downloads, waitlist & media exposure")]], { w: W[3] }),
        cell([[t("$"), ph("[N]"), t(" subscriptions + grants")]], { w: W[4] }),
        cell([[t("$"), ph("[N]")]], { w: W[5] }),
        cell([[t("N/A")]], { w: W[6] }),
        cell([[ph("[N]"), t(" paying users by "), ph("[month year]")]], { w: W[7] }),
      ],
    }),
    new TableRow({
      children: [
        cell([[t("Other Projects", { bold: true, color: NAVY })]], { w: W[0] }),
        cell([[ph("[N]"), t(" people")]], { w: W[1] }),
        cell([[ph("[N]"), t(" people")]], { w: W[2] }),
        cell([[ph("[N]"), t(" people")]], { w: W[3] }),
        cell([[t("$"), ph("[N]")]], { w: W[4] }),
        cell([[t("$"), ph("[N]")]], { w: W[5] }),
        cell([[t("N/A")]], { w: W[6] }),
        cell([[t("")]], { w: W[7] }),
      ],
    }),
    new TableRow({
      children: [
        cell([[t("Total", { bold: true, color: WHITE })]], { w: W[0], fill: PURPLE }),
        cell([[ph("[N]"), t(" people", { bold: true })]], { w: W[1], fill: LAV }),
        cell([[ph("[N]"), t(" people", { bold: true })]], { w: W[2], fill: LAV }),
        cell([[ph("[N]"), t(" people", { bold: true })]], { w: W[3], fill: LAV }),
        cell([[t("$", { bold: true }), ph("[N]")]], { w: W[4], fill: LAV }),
        cell([[t("$", { bold: true }), ph("[N]")]], { w: W[5], fill: LAV }),
        cell([[t("")]], { w: W[6], fill: LAV }),
        cell([[t("")]], { w: W[7], fill: LAV }),
      ],
    }),
  ],
});

// ---- Impact Measurement table ----
const MW = [1666, 4400, 4400];
const mrow = (label, dv, fq, fill) =>
  new TableRow({
    children: [
      cell([[t(label, { bold: true, color: NAVY })]], { w: MW[0], fill: LAV }),
      cell(dv, { w: MW[1], fill }),
      cell(fq, { w: MW[2], fill }),
    ],
  });

const dash = "– ";
const measurement = new Table({
  width: { size: 10466, type: WidthType.DXA },
  columnWidths: MW,
  rows: [
    new TableRow({
      tableHeader: true,
      children: [
        hcell("", MW[0]),
        hcell("Decode: Veritas", MW[1]),
        hcell("Fliq", MW[2]),
      ],
    }),
    mrow("Tools & Methods",
      [
        [t(dash + "Direct impact: identical media-literacy test before the first and after the final workshop; attendance registers per session.")],
        [t(dash + "Reach: school assembly headcounts and campaign sign-in sheets.")],
        [t(dash + "Income: school programme invoices and receipts.")],
      ],
      [
        [t(dash + "Direct impact: in-app news-comprehension quiz at onboarding, repeated at "), ph("[4–8]"), t(" weeks; only readers who completed both are counted.")],
        [t(dash + "Reach: app-store download counts, waitlist entries, media coverage.")],
        [t(dash + "Income: subscription statements; grant award letters.")],
      ],
      WHITE),
    mrow("Time period & Sample",
      [
        [t("Workshops run "), ph("[Sep 2026 – May 2027]"), t(". All "), ph("[N]"), t(" participants across "), ph("[N]"), t(" schools tested pre and post; "), ph("[N]"), t(" completed both tests.")],
      ],
      [
        [t("Public beta live from "), ph("[month 2026]"), t(". Of "), ph("[N]"), t(" onboarded readers, "), ph("[N]"), t(" completed the follow-up quiz ("), ph("[X]%"), t(" response rate).")],
      ],
      "FAFAFF"),
    mrow("Estimates & Assumptions",
      [
        [t("Indirect impact assumes each trained student shares learning with "), ph("[2]"), t(" family members, per exit-survey self-reports.")],
      ],
      [
        [t("Indirect impact assumes "), ph("[1]"), t(" household member per measured reader, per onboarding survey. Equity investment is excluded from Income/Revenue (not sales, grant, sponsorship, or donation).")],
      ],
      WHITE),
  ],
});

const doc = new Document({
  styles: { default: { document: { run: { font: BODY, size: 18, color: PLUM } } } },
  sections: [{
    properties: {
      page: { margin: { top: 620, bottom: 560, left: 720, right: 720 } },
    },
    children: [
      p([t("FLIQ · ENACTUS ", { bold: true, color: PURPLE, size: 18, font: HEAD }),
         t("HKUST — ANNUAL REPORT · PAGE 4", { color: MUTED, size: 18, font: HEAD })],
        { spacing: { after: 40 } }),
      secHead("Impact Overview Table"),
      overview,
      secHead("Impact Measurement"),
      measurement,
      p([t("Impact window: ", { bold: true, color: NAVY, size: 18 }),
         ph("[1 Sep 2026 – 31 Aug 2027 — confirm exact dates with Enactus Hong Kong]"),
         t("  ·  All terms per official Enactus impact definitions.", { color: MUTED, size: 18 })],
        { spacing: { before: 100 } }),
      p([t("INTERNAL DRAFT — every [bracket] must be replaced with a verified number from the evidence tracker before the Impact & Financial Reporting Review; numbers freeze one month before the World Cup. Delete this line before printing.",
          { color: "B03020", size: 18, italics: true })],
        { spacing: { before: 40 } }),
    ],
  }],
});

Packer.toBuffer(doc).then((b) => {
  fs.writeFileSync(__dirname + "/Enactus_Impact_Page.docx", b);
  console.log("Wrote Enactus_Impact_Page.docx");
});
