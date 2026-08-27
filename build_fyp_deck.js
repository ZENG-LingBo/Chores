/**
 * Builds Fliq_FYP_Proposal.pptx — the ISDN 4001 FYP proposal deck.
 *
 * Design system, geometry, palette and type are taken from the team's own
 * Enactus SLEEP 2026 regional-final deck so this reads as the same product.
 *   Headings  Space Grotesk bold, 11256A
 *   Body      Inter, 352E4A
 *   Accent    800080 purple, C9FA85 lime
 *
 * Every figure is drawn from the ISDN 3002 final report or the ISDN 4001
 * kick-off deck; nothing here is estimated.
 */

const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

const OUT = path.join(__dirname, "Fliq_FYP_Proposal.pptx");
const ASSETS = path.join(__dirname, "assets");

const img = (f) =>
  "image/png;base64," + fs.readFileSync(path.join(ASSETS, f)).toString("base64");
const LOGO_PURPLE = img("fliq-logo-purple.png");
const LOGO_WHITE = img("fliq-logo-white.png");
const MARK_WHITE = img("fliq-mark.png");

// ---- Brand palette (sampled from the Enactus deck) ----
const PURPLE = "800080";
const NAVY = "11256A";
const PLUM = "352E4A";
const MUTED = "6E6787";
const SLATE = "3A466E";
const LIME = "C9FA85";
const LAVENDER = "D3CAFF";
const SKY = "CEE7FD";
const PINK = "FDE1FD";
const TINT = "F5F2FF";
const RULE = "E2DBF0";
const PERI = "667DFF";
const OFFWHITE = "FFF9FF";
const WHITE = "FFFFFF";
const GHOST = "C7D1FF";

const HEAD = "Space Grotesk";
const BODY = "Inter";

// ---- Grid (matches the source deck exactly) ----
const SW = 13.333;
const L = 0.55; // content left
const R = 12.78; // content right
const CW = R - L; // 12.23
const BAND_H = 2.07; // header band height
const TOP = 2.3; // content top
const BOT = 6.82; // content bottom (footer rule sits at 6.98)

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.author = "Victor Nesteruk and Ling Bo Zeng";
pres.company = "NewsFlick Limited";
pres.title = "Fliq — ISDN 4001 FYP Proposal";

const META = "ISDN 4001 · FYP PROPOSAL · 28 AUGUST 2026";
const FOOT = "Fliq: News That Moves Like You Do";

const shadow = () => ({
  type: "outer",
  angle: 90,
  blur: 10,
  offset: 2,
  color: "352E4A",
  opacity: 0.13,
});

let pageNo = 0;

/** Standard content slide: tinted header band, logo, eyebrow, title, footer. */
function slide(o) {
  const s = pres.addSlide();
  s.background = { color: WHITE };
  pageNo += 1;

  s.addShape(pres.ShapeType.rect, {
    x: -0.02,
    y: -0.02,
    w: 13.38,
    h: BAND_H,
    fill: { color: o.tint || SKY },
    line: { type: "none" },
  });
  s.addImage({ data: LOGO_PURPLE, x: 0.47, y: 0.24, w: 1.25, h: 0.46 });
  s.addText(META, {
    x: 7.4,
    y: 0.37,
    w: 5.38,
    h: 0.3,
    isTextBox: true,
    margin: 0,
    align: "right",
    fontFace: BODY,
    fontSize: 9,
    color: SLATE,
  });
  s.addText(o.eyebrow.toUpperCase(), {
    x: L,
    y: 0.88,
    w: CW,
    h: 0.32,
    isTextBox: true,
    margin: 0,
    fontFace: BODY,
    fontSize: 10.5,
    bold: true,
    color: PURPLE,
  });
  s.addText(o.title, {
    x: L,
    y: o.titleY || 1.17,
    w: CW,
    h: o.titleH || 0.85,
    isTextBox: true,
    margin: 0,
    fontFace: HEAD,
    fontSize: o.titleSize || 33,
    bold: true,
    color: NAVY,
    valign: "top",
  });

  s.addShape(pres.ShapeType.rect, {
    x: L,
    y: 6.98,
    w: CW,
    h: 0.012,
    fill: { color: RULE },
    line: { type: "none" },
  });
  s.addText(FOOT, {
    x: L,
    y: 7.04,
    w: 10.5,
    h: 0.3,
    isTextBox: true,
    margin: 0,
    fontFace: BODY,
    fontSize: 9,
    color: MUTED,
  });
  s.addText(String(pageNo), {
    x: 11.9,
    y: 7.04,
    w: 0.88,
    h: 0.3,
    isTextBox: true,
    margin: 0,
    align: "right",
    fontFace: BODY,
    fontSize: 9.5,
    color: MUTED,
  });
  return s;
}

/** Pastel card with a Space Grotesk heading and an Inter body. */
function card(s, o) {
  s.addShape(pres.ShapeType.roundRect, {
    x: o.x,
    y: o.y,
    w: o.w,
    h: o.h,
    rectRadius: 0.08,
    fill: { color: o.fill || TINT },
    line: { type: "none" },
    shadow: shadow(),
  });
  const pad = o.pad || 0.3;
  if (o.label) {
    s.addText(o.label.toUpperCase(), {
      x: o.x + pad,
      y: o.y + 0.22,
      w: o.w - 2 * pad,
      h: 0.26,
      isTextBox: true,
      margin: 0,
      fontFace: BODY,
      fontSize: 9.5,
      bold: true,
      color: PURPLE,
    });
  }
  const hy = o.y + (o.label ? 0.54 : 0.26);
  s.addText(o.heading, {
    x: o.x + pad,
    y: hy,
    w: o.w - 2 * pad,
    h: o.headH || 0.34,
    isTextBox: true,
    margin: 0,
    fontFace: HEAD,
    fontSize: o.headSize || 16,
    bold: true,
    color: NAVY,
    valign: "top",
    lineSpacingMultiple: 1.05,
  });
  if (o.body) {
    const by = hy + (o.headH || 0.34) + 0.1;
    s.addText(o.body, {
      x: o.x + pad,
      y: by,
      w: o.w - 2 * pad,
      h: o.y + o.h - by - 0.2,
      isTextBox: true,
      margin: 0,
      fontFace: BODY,
      fontSize: o.bodySize || 13,
      color: PLUM,
      valign: "top",
      lineSpacingMultiple: 1.16,
    });
  }
}

/* ================================================================== *
 * 1 — Title
 * ================================================================== */
{
  const s = pres.addSlide();
  s.background = { color: PURPLE };
  s.addShape(pres.ShapeType.rect, {
    x: 0,
    y: 0,
    w: 0.85,
    h: 0.1,
    fill: { color: LIME },
    line: { type: "none" },
  });
  s.addImage({ data: MARK_WHITE, x: 8.6, y: 1.91, w: 4.78, h: 4.69 });
  s.addImage({ data: LOGO_WHITE, x: 0.44, y: 0.42, w: 1.956, h: 0.72 });

  s.addText("ISDN 4001 · FINAL YEAR PROJECT · PROPOSAL TO CONTINUE", {
    x: 0.7,
    y: 2.35,
    w: 8.6,
    h: 0.4,
    isTextBox: true,
    margin: 0,
    fontFace: BODY,
    fontSize: 14,
    bold: true,
    color: LIME,
  });
  s.addText(
    [
      { text: "We would like to build", options: { color: OFFWHITE, breakLine: true } },
      { text: "Fliq for Year 4.", options: { color: LIME } },
    ],
    {
      x: 0.7,
      y: 2.85,
      w: 8.9,
      h: 1.9,
      isTextBox: true,
      margin: 0,
      fontFace: HEAD,
      fontSize: 54,
      bold: true,
      lineSpacingMultiple: 1.12,
    }
  );
  s.addText(
    [
      {
        text: "A request to carry our Year-3 project into ISDN 4001.",
        options: { bold: true, color: WHITE, breakLine: true },
      },
      {
        text: "Two years of research, an incorporated company, and an app in build.",
        options: { color: LAVENDER },
      },
    ],
    {
      x: 0.7,
      y: 4.95,
      w: 8.6,
      h: 0.95,
      isTextBox: true,
      margin: 0,
      fontFace: BODY,
      fontSize: 18,
      lineSpacingMultiple: 1.2,
    }
  );
  s.addShape(pres.ShapeType.rect, {
    x: 0.7,
    y: 6.42,
    w: 8.66,
    h: 0.014,
    fill: { color: LIME },
    line: { type: "none" },
  });
  s.addText(
    [
      { text: "Victor Nesteruk · Ling Bo Zeng", options: { bold: true, color: OFFWHITE } },
      { text: "     |     HKUST ISDN, Year 4     |     ", options: { color: "E8E2FF" } },
      { text: "For Prof. Chi Ying Tsui · Prof. Hongri Gu", options: { color: "E8E2FF" } },
    ],
    {
      x: 0.7,
      y: 6.6,
      w: 9.4,
      h: 0.3,
      isTextBox: true,
      margin: 0,
      fontFace: BODY,
      fontSize: 13,
    }
  );

  s.addNotes(
`SCRIPT — VICTOR  (about 60 seconds)

"Good morning, and thank you both for making the time before term starts. Professor Tsui, thank you for moving this to Friday to fit us in.

I'm Victor, this is Adam. We're both Year 4 in ISD.

Professor Tsui — we first met you in ISDN 1001, and again at the HKUST-HSBC Social Entrepreneurship Competition last November.

We're here for one reason. We'd like to ask whether we can carry the project we've been building for the last two years into ISDN 4001 as our final year project.

One quick note on the name. In our email we called it NewsFlick. That's still the company — NewsFlick Limited. The product now ships as Fliq. Same project.

We'll take about fifteen minutes, and then we'd really like to hear what you think."

NOTE: Warm, unhurried. Don't rush into the pitch — the two of them agreeing to meet in August is a favour, so acknowledge it properly.`
  );
}

/* ================================================================== *
 * 2 — The ask
 * ================================================================== */
{
  const s = slide({
    tint: LAVENDER,
    eyebrow: "The ask · why we asked to meet",
    title: "May we bring Fliq into ISDN 4001?",
  });

  s.addShape(pres.ShapeType.roundRect, {
    x: L,
    y: TOP,
    w: CW,
    h: 1.2,
    rectRadius: 0.08,
    fill: { color: NAVY },
    line: { type: "none" },
  });
  s.addText(
    "We would like to register Fliq — the project we built through ISDN 3001 and 3002, and have kept building since — as our own-idea FYP topic.",
    {
      x: L + 0.42,
      y: TOP,
      w: CW - 0.84,
      h: 1.2,
      isTextBox: true,
      margin: 0,
      fontFace: HEAD,
      fontSize: 19,
      bold: true,
      color: WHITE,
      valign: "middle",
      lineSpacingMultiple: 1.16,
    }
  );

  const cards = [
    {
      fill: LAVENDER,
      label: "We are not assuming",
      heading: "We know this is unusual",
      body:
        "As far as we know, nobody has carried a Year-3 project straight into Year 4 this way. We did not want to assume it is allowed, which is why we asked to speak with you before term starts.",
    },
    {
      fill: SKY,
      label: "What we would bring",
      heading: "It is already real",
      body:
        "Two years of user research, a validated pre-launch MVP, an incorporated company, and an application already in development.",
    },
    {
      fill: PINK,
      label: "What we are asking",
      heading: "Your read on it",
      body:
        "Whether this is a project the Division would want as an FYP — and if it is, what it would need to look like.",
    },
  ];
  cards.forEach((c, i) => {
    card(s, {
      x: L + i * 4.12,
      y: 3.72,
      w: 3.7,
      h: 3.0,
      fill: c.fill,
      label: c.label,
      heading: c.heading,
      body: c.body,
    });
  });

  s.addNotes(
`SCRIPT — VICTOR  (about 60 seconds)

"So here's the ask, straight away, so nothing is ambiguous.

We'd like to register Fliq as our own-idea FYP topic — the project we've been building through 3001 and 3002.

And we want to say up front that we know this is an unusual thing to ask. As far as we know, nobody has carried a project from Year 3 straight into Year 4 like this. The kick-off mentioned bringing your own idea as one of the ways to start, but we didn't want to assume that stretches to something we've already been building for two years. That's exactly why we wanted to speak to you before term starts, rather than just registering it and hoping it was fine.

What we'd bring to it isn't a concept. It's two years of user research, a validated MVP, an incorporated company, and an app that's in build right now.

And what we're really asking for is your read — whether this is something the Division would want as an FYP, and if it is, what it would need to look like."

NOTE: This slide sets the tone for the whole meeting. We are asking, not claiming a right. Because nobody has done this before, the professors get to shape what it becomes — so invite that rather than presenting it as settled. Don't oversell; the evidence is on slides 3 to 7.`
  );
}

/* ================================================================== *
 * 3 — What Fliq is
 * ================================================================== */
{
  const s = slide({
    tint: SKY,
    eyebrow: "The project · what we are building",
    title: "The scarce resource in news is not information. It is trust.",
    titleSize: 29,
    titleH: 1.0,
  });

  s.addText("WHAT OUR OWN RESEARCH FOUND", {
    x: L,
    y: TOP,
    w: 5.5,
    h: 0.3,
    isTextBox: true,
    margin: 0,
    fontFace: BODY,
    fontSize: 11,
    bold: true,
    color: PURPLE,
  });

  const stats = [
    ["79%", NAVY, "rank trust — knowing a story is accurate — as their number-one priority in news"],
    ["52%", PERI, "would read news more often if they could trust it more"],
    ["43%", PURPLE, "say they simply cannot tell what is true"],
  ];
  stats.forEach((st, i) => {
    const y = 2.78 + i * 1.24;
    s.addText(st[0], {
      x: L,
      y,
      w: 1.55,
      h: 0.72,
      isTextBox: true,
      margin: 0,
      fontFace: HEAD,
      fontSize: 40,
      bold: true,
      color: st[1],
      valign: "middle",
    });
    s.addText(st[2], {
      x: L + 1.65,
      y,
      w: 3.9,
      h: 0.8,
      isTextBox: true,
      margin: 0,
      fontFace: BODY,
      fontSize: 13,
      color: PLUM,
      valign: "middle",
      lineSpacingMultiple: 1.14,
    });
  });
  s.addText(
    "Our own 100-response study, recruited via Prolific, skewed to the 18–34 audience.",
    {
      x: L,
      y: 6.4,
      w: 5.6,
      h: 0.38,
      isTextBox: true,
      margin: 0,
      fontFace: BODY,
      fontSize: 10,
      color: MUTED,
    }
  );

  const feats = [
    [LAVENDER, "A confidence signal", "A glanceable Low / Medium / High level and a lifecycle state — never a false-precision percentage."],
    [SKY, "Claim-level transparency", "Each claim is tagged Confirmed, Developing, Disputed or Analysis, and expands in place to show its evidence."],
    [PINK, "Primary-source grounding", "“Two pools, one gate” ingestion makes legality structural and anchors confidence in original evidence."],
    [TINT, "A finite card feed", "Bounded sessions rather than infinite scroll — built for a Gen-Z audience, against doomscroll."],
  ];
  feats.forEach((f, i) => {
    const y = TOP + i * 1.12;
    s.addShape(pres.ShapeType.roundRect, {
      x: 6.5,
      y,
      w: 6.28,
      h: 1.0,
      rectRadius: 0.08,
      fill: { color: f[0] },
      line: { type: "none" },
      shadow: shadow(),
    });
    s.addText(f[1], {
      x: 6.78,
      y: y + 0.12,
      w: 5.72,
      h: 0.32,
      isTextBox: true,
      margin: 0,
      fontFace: HEAD,
      fontSize: 15,
      bold: true,
      color: NAVY,
    });
    s.addText(f[2], {
      x: 6.78,
      y: y + 0.46,
      w: 5.72,
      h: 0.46,
      isTextBox: true,
      margin: 0,
      fontFace: BODY,
      fontSize: 12,
      color: PLUM,
      lineSpacingMultiple: 1.1,
    });
  });

  s.addNotes(
`SCRIPT — VICTOR  (about 70 seconds)

"Very quickly, what it actually is.

We started from one observation: young readers aren't short of news. They're unsure what to believe.

We didn't assume that — we measured it. In our own hundred-response study, seventy-nine percent ranked trust, knowing a story is accurate, as their number-one priority. Ahead of speed, ahead of clarity. Fifty-two percent told us they'd read more news if they could trust it more. And forty-three percent said they simply can't tell what's true.

So we built against that.

Every story carries a confidence signal — Low, Medium or High, plus where the story is in its lifecycle. Deliberately not a percentage.

Inside a story, every individual claim is tagged: Confirmed, Developing, Disputed, or Analysis. You can tap any one of them and see who confirmed it, and why.

Underneath, we ground stories in primary evidence through an ingestion model we call two pools, one gate.

And the feed is finite. It ends. That's a deliberate choice for a Gen-Z audience."

IF ASKED why no single trust score: our interviews killed it. People asked "a percentage out of what?" A bare number felt precise but told them nothing, so we show the evidence rather than averaging it away.`
  );
}

/* ================================================================== *
 * 4 — Year 3
 * ================================================================== */
{
  const s = slide({
    tint: SKY,
    eyebrow: "Year 3 · ISDN 3001 and 3002",
    title: "Five design generations, each one driven by evidence",
  });

  const gens = [
    ["G1", "Explorations", "Established the card-and-feed metaphor, and that transparency belongs on the surface."],
    ["G2", "Research-led reframe", "User landscape, journey, persona. The design stopped being aesthetic-led; the goal became trust."],
    ["G3", "Card-and-arc library", "Scattered mockups became one versioned, maintainable component system."],
    ["G4", "The confidence Engine", "Ten directions explored. We dropped the numeric score — against a raw user preference."],
    ["G5", "Inline transparency", "From a colour “rainbow” to status icons and keyword highlights, so the tags are discoverable."],
  ];
  const tints = [LAVENDER, SKY, PINK, LAVENDER, SKY];
  gens.forEach((g, i) => {
    const x = L + i * 2.45;
    const w = 2.25;
    s.addShape(pres.ShapeType.roundRect, {
      x,
      y: TOP,
      w,
      h: 2.9,
      rectRadius: 0.08,
      fill: { color: tints[i] },
      line: { type: "none" },
      shadow: shadow(),
    });
    s.addText(g[0], {
      x: x + 0.26,
      y: TOP + 0.22,
      w: 1.7,
      h: 0.36,
      isTextBox: true,
      margin: 0,
      fontFace: HEAD,
      fontSize: 20,
      bold: true,
      color: PURPLE,
    });
    s.addText(g[1], {
      x: x + 0.26,
      y: TOP + 0.66,
      w: 1.75,
      h: 0.6,
      isTextBox: true,
      margin: 0,
      fontFace: HEAD,
      fontSize: 14,
      bold: true,
      color: NAVY,
      valign: "top",
      lineSpacingMultiple: 1.05,
    });
    s.addText(g[2], {
      x: x + 0.26,
      y: TOP + 1.3,
      w: 1.75,
      h: 1.4,
      isTextBox: true,
      margin: 0,
      fontFace: BODY,
      fontSize: 11,
      color: PLUM,
      valign: "top",
      lineSpacingMultiple: 1.14,
    });
  });

  s.addShape(pres.ShapeType.roundRect, {
    x: L,
    y: 5.5,
    w: CW,
    h: 1.24,
    rectRadius: 0.08,
    fill: { color: NAVY },
    line: { type: "none" },
  });
  s.addText(
    [
      { text: "Grounded in primary research: ", options: { bold: true, color: WHITE } },
      {
        text:
          "an 18-response study, a 100-response Prolific study, roughly 30 interviews and an 86-participant A/B test.",
        options: { color: "E8E2FF", breakLine: true },
      },
      { text: "Advised by ", options: { color: "E8E2FF" } },
      { text: "Prof. Ajay Joneja", options: { bold: true, color: LIME } },
      { text: " on product development and ", options: { color: "E8E2FF" } },
      { text: "Prof. Erwin Huang", options: { bold: true, color: LIME } },
      { text: " on AI and retrieval-augmented generation.", options: { color: "E8E2FF" } },
    ],
    {
      x: L + 0.4,
      y: 5.5,
      w: CW - 0.8,
      h: 1.24,
      isTextBox: true,
      margin: 0,
      fontFace: BODY,
      fontSize: 12.5,
      valign: "middle",
      lineSpacingMultiple: 1.3,
    }
  );

  s.addNotes(
`SCRIPT — VICTOR  (about 60 seconds)

"This is last year, across ISDN 3001 and 3002, under Professor Joneja and Professor Huang.

We didn't design it once. We went through five generations, and each one was pushed by evidence rather than by our own taste.

G1 established the card and feed metaphor. G2 is where it stopped being aesthetic-led — we did the user landscape, the journey, the persona, and the research told us the job of this product is trust, not speed. That reframed everything after it.

G3 turned scattered mockups into one versioned component library, so the design and the generation pipeline share a single source of truth.

G4 is the one I'd point at. We explored ten directions for the confidence signal. In our A/B test, people actually preferred a numeric score — but the interviews told us that number was meaningless to them. So we dropped it. We followed the deeper evidence against a surface preference.

G5 made the claim tags legible and discoverable, after testing showed people didn't realise they were tappable.

Underneath all of it: two questionnaires, about thirty interviews, and an eighty-six person A/B test."

NOTE: Credit Prof. Joneja and Prof. Huang out loud, not just on the slide. G4 is the story that shows judgement — take your time on it.`
  );
}

/* ================================================================== *
 * 5 — Validation
 * ================================================================== */
{
  const s = slide({
    tint: SKY,
    eyebrow: "Evidence · engineering validation",
    title: "It is validated, not just demonstrated",
  });
  s.addText(
    "Four documented stress-test passes over the pipeline in June, plus a controlled A/B test of the trust features.",
    {
      x: L,
      y: TOP,
      w: CW,
      h: 0.34,
      isTextBox: true,
      margin: 0,
      fontFace: BODY,
      fontSize: 13,
      color: PLUM,
    }
  );

  const cells = [
    ["~85%", NAVY, LAVENDER, "would switch to the transparent version — 73 of 86 A/B participants"],
    ["~88%", PURPLE, SKY, "rated a visibly shown trust indicator as important"],
    ["22 → 11", PERI, PINK, "story arcs: the taxonomy converged and stabilised, with no loss of coverage"],
    ["17.8", NAVY, SKY, "out of 20 on card quality, against a clarity, structure and completeness rubric"],
    ["PASS", PURPLE, PINK, "lifecycle and hallucination resistance — it reports “no developments” rather than inventing them"],
    ["PASS", PERI, LAVENDER, "voice layer across 144 renderings, with the facts preserved verbatim"],
  ];
  cells.forEach((c, i) => {
    const col = i % 3;
    const row = Math.floor(i / 3);
    const x = L + col * 4.12;
    const y = 2.82 + row * 1.86;
    s.addShape(pres.ShapeType.roundRect, {
      x,
      y,
      w: 3.7,
      h: 1.66,
      rectRadius: 0.08,
      fill: { color: c[2] },
      line: { type: "none" },
      shadow: shadow(),
    });
    s.addText(c[0], {
      x: x + 0.3,
      y: y + 0.16,
      w: 3.1,
      h: 0.62,
      isTextBox: true,
      margin: 0,
      fontFace: HEAD,
      fontSize: 32,
      bold: true,
      color: c[1],
      valign: "middle",
    });
    s.addText(c[3], {
      x: x + 0.3,
      y: y + 0.84,
      w: 3.1,
      h: 0.68,
      isTextBox: true,
      margin: 0,
      fontFace: BODY,
      fontSize: 11.5,
      color: PLUM,
      valign: "top",
      lineSpacingMultiple: 1.12,
    });
  });

  s.addText(
    "Reported honestly: the card-quality figure is a best-and-worst-per-arc sample scored by the model itself, and the lifecycle pass rests on three tracked stories. They are directional baselines and regression bars, not exhaustive proof.",
    {
      x: L,
      y: 6.5,
      w: CW,
      h: 0.34,
      isTextBox: true,
      margin: 0,
      fontFace: BODY,
      fontSize: 10,
      color: MUTED,
    }
  );

  s.addNotes(
`SCRIPT — ADAM  (about 75 seconds)

"I'll take this one, since it's the engineering side.

The thing that matters here is that we treated the pipeline as a system to be validated, not demonstrated.

On the product bet: across eighty-six A/B participants, around eighty-five percent said they'd switch to the transparent version — that's seventy-three of eighty-six — and around eighty-eight percent rated a visibly shown trust indicator as important.

On the pipeline itself, we ran four documented passes in June.

The arc taxonomy converged from twenty-two arcs down to eleven with no loss of coverage, which tells us the abstraction actually holds as the corpus grows.

Card quality scored about seventeen-point-eight out of twenty against a clarity, structure and completeness rubric.

The lifecycle and hallucination-resistance pass came back clean. On a quiet day the system reports 'no relevant developments' rather than inventing movement — that one is load-bearing, because a single confident unsupported claim would undermine the whole confidence signal.

And the voice layer passed across a hundred and forty-four renderings with the facts preserved verbatim.

I want to be straight about the limits, because they're in our report too. The card-quality number is a best-and-worst-per-arc sample scored by the model itself, and the lifecycle pass rests on three tracked stories. These are directional baselines and regression bars. They aren't exhaustive proof."

NOTE: Say the caveat even if they don't ask. Volunteering the limits is far stronger than being caught by them, and it's what makes the other numbers credible.`
  );
}

/* ================================================================== *
 * 6 — Outside the classroom
 * ================================================================== */
{
  const s = slide({
    tint: SKY,
    eyebrow: "Traction · judged outside HKUST",
    title: "Tested well beyond the coursework",
  });

  const items = [
    ["Techathon+ 2026", "Silver Award — Trusted AI and Data Science", LAVENDER],
    ["NewsFlick Limited", "Incorporated", SKY],
    ["Angel / family round", "Closed", PINK],
    ["HKUST InnoBay", "2026/27 cohort", TINT],
    ["HKSTP Ideation", "Programme completed", SKY],
    ["HKUST Dream Builder", "Programme completed", PINK],
    ["AWS Activate", "Admitted", TINT],
    ["Provisional patent", "In preparation", LAVENDER],
  ];
  items.forEach((it, i) => {
    const col = i % 4;
    const row = Math.floor(i / 4);
    const x = L + col * 3.09;
    const y = TOP + row * 1.86;
    s.addShape(pres.ShapeType.roundRect, {
      x,
      y,
      w: 2.79,
      h: 1.6,
      rectRadius: 0.08,
      fill: { color: it[2] },
      line: { type: "none" },
      shadow: shadow(),
    });
    s.addText(it[0], {
      x: x + 0.28,
      y: y + 0.3,
      w: 2.23,
      h: 0.56,
      isTextBox: true,
      margin: 0,
      fontFace: HEAD,
      fontSize: 14,
      bold: true,
      color: NAVY,
      valign: "top",
      lineSpacingMultiple: 1.05,
    });
    s.addText(it[1], {
      x: x + 0.28,
      y: y + 0.92,
      w: 2.23,
      h: 0.5,
      isTextBox: true,
      margin: 0,
      fontFace: BODY,
      fontSize: 11.5,
      color: PLUM,
      valign: "top",
      lineSpacingMultiple: 1.1,
    });
  });

  s.addText(
    "Before all of this, our team won the HKUST-HSBC Social Entrepreneurship Competition in November 2025, with the pill dispenser we designed.",
    {
      x: L,
      y: 6.34,
      w: CW,
      h: 0.4,
      isTextBox: true,
      margin: 0,
      fontFace: BODY,
      fontSize: 11.5,
      color: MUTED,
    }
  );

  s.addNotes(
`SCRIPT — ADAM  (about 45 seconds)

"Alongside the coursework we took it outside the classroom, and it's had to survive judging by people who don't know us.

Silver at Techathon+ this year, in Trusted AI and Data Science.

We incorporated as NewsFlick Limited. We closed a small angel and family round — and I want to be precise about that: it's angel and family, not institutional investment.

We're in the InnoBay twenty-six twenty-seven cohort. We completed HKSTP Ideation and Dream Builder. We're on AWS Activate. And a provisional patent is in preparation.

Professor Tsui — the HKUST-HSBC competition we mentioned earlier, the pill dispenser, was where we last saw you."

NOTE: Don't read the grid item by item, let them scan it. The one sentence that matters is that outsiders keep backing it. Be scrupulous about the funding wording — overstating it is the fastest way to lose them.`
  );
}

/* ================================================================== *
 * 7 — Summer momentum
 * ================================================================== */
{
  const s = slide({
    tint: LAVENDER,
    eyebrow: "Since the Year-3 report · summer 2026",
    title: "We did not stop when the course ended",
  });
  s.addText("The three months since ISDN 3002 was submitted and graded.", {
    x: L,
    y: TOP,
    w: CW,
    h: 0.34,
    isTextBox: true,
    margin: 0,
    fontFace: BODY,
    fontSize: 13,
    color: PLUM,
  });

  const wins = [
    {
      label: "Summer 2026",
      heading: "IET Young Professionals",
      body: "Exhibition and Competition — Undergraduate Champion.",
      fill: SKY,
    },
    {
      label: "Summer 2026",
      heading: "Enactus Hong Kong",
      body: "Regional Champion.",
      fill: SKY,
    },
    {
      label: "In progress now",
      heading: "The app is in build",
      body:
        "We are building the application itself — the step from a validated design to something real readers can open.",
      fill: LIME,
    },
  ];
  wins.forEach((w, i) => {
    card(s, {
      x: L + i * 4.12,
      y: 2.86,
      w: 3.7,
      h: 2.5,
      fill: w.fill,
      label: w.label,
      heading: w.heading,
      headSize: 19,
      headH: 0.78,
      body: w.body,
      bodySize: 13,
    });
  });

  s.addShape(pres.ShapeType.roundRect, {
    x: L,
    y: 5.62,
    w: CW,
    h: 1.1,
    rectRadius: 0.08,
    fill: { color: NAVY },
    line: { type: "none" },
  });
  s.addText(
    "This is a live venture with momentum — not a finished piece of coursework we are asking to hand in twice.",
    {
      x: L + 0.42,
      y: 5.62,
      w: CW - 0.84,
      h: 1.1,
      isTextBox: true,
      margin: 0,
      fontFace: HEAD,
      fontSize: 17,
      bold: true,
      color: LIME,
      valign: "middle",
    }
  );

  s.addNotes(
`SCRIPT — VICTOR  (about 45 seconds)

"This is the part we most wanted to show you, because all of it happened after the course ended, and nobody asked us to do any of it.

Over the summer we won the IET Young Professionals Exhibition and Competition as Undergraduate Champion. And we were Regional Champion at Enactus Hong Kong.

And right now we're building the app itself. That's the step from a validated design to something a real reader can actually open.

Which is the honest reason we're sitting here. This is a live venture with momentum. It isn't a finished piece of coursework we're asking to hand in twice."

NOTE: This slide is the whole argument in miniature. Energy, but no boasting — the facts do the work. Let the last line land, then move on.`
  );
}

/* ================================================================== *
 * 8 — Fits the FYP's goals
 * ================================================================== */
{
  const s = slide({
    tint: LAVENDER,
    eyebrow: "Alignment · the four outcomes you set out",
    title: "Where we think we stand",
  });

  const goals = [
    [
      "A STRONG PROTOTYPE",
      "An AI-native pipeline with a frozen system specification and four documented test passes behind it — a system, not a demo.",
      NAVY,
    ],
    [
      "A CONVINCING STORY",
      "Trust is the scarce resource in news. We measured that ourselves rather than borrowing it from a market report.",
      PURPLE,
    ],
    [
      "EVIDENCE OF SOLVING A MEANINGFUL PROBLEM",
      "Our research reframed the problem from information overload to trust, and the whole product follows from that finding.",
      NAVY,
    ],
    [
      "SOMETHING TO SHOW AFTER GRADUATION",
      "An incorporated company, an application heading for public beta, and a provisional patent in preparation.",
      PURPLE,
    ],
  ];
  goals.forEach((g, i) => {
    const y = TOP + i * 1.06;
    s.addShape(pres.ShapeType.roundRect, {
      x: L + 1.05,
      y,
      w: CW - 1.05,
      h: 0.96,
      rectRadius: 0.08,
      fill: { color: TINT },
      line: { type: "none" },
      shadow: shadow(),
    });
    s.addShape(pres.ShapeType.roundRect, {
      x: L,
      y,
      w: 1.0,
      h: 0.96,
      rectRadius: 0.08,
      fill: { color: g[2] },
      line: { type: "none" },
    });
    s.addText(String(i + 1), {
      x: L,
      y,
      w: 1.0,
      h: 0.96,
      isTextBox: true,
      margin: 0,
      align: "center",
      valign: "middle",
      fontFace: HEAD,
      fontSize: 30,
      bold: true,
      color: WHITE,
    });
    s.addText(g[0], {
      x: L + 1.35,
      y: y + 0.16,
      w: 4.4,
      h: 0.7,
      isTextBox: true,
      margin: 0,
      fontFace: BODY,
      fontSize: 12,
      bold: true,
      color: NAVY,
      valign: "middle",
      lineSpacingMultiple: 1.05,
    });
    s.addText(g[1], {
      x: L + 5.95,
      y: y + 0.14,
      w: 6.0,
      h: 0.74,
      isTextBox: true,
      margin: 0,
      fontFace: BODY,
      fontSize: 12,
      color: PLUM,
      valign: "middle",
      lineSpacingMultiple: 1.14,
    });
  });

  s.addText(
    "The four outcomes set out at the ISDN 4001 kick-off meeting.",
    {
      x: L,
      y: 6.56,
      w: CW,
      h: 0.28,
      isTextBox: true,
      margin: 0,
      fontFace: BODY,
      fontSize: 10,
      color: MUTED,
    }
  );

  s.addNotes(
`SCRIPT — VICTOR  (about 40 seconds)

"We looked at the four things the kick-off set out for the year, and tried to be honest with ourselves about where we actually are against each.

A strong prototype — we have a pipeline with a frozen specification and four documented test passes behind it. A system, not a demo.

A convincing story — trust as the scarce resource in news, and we measured that ourselves.

Evidence of defining and solving a meaningful problem — our research reframed it from information overload to trust, and the whole product follows from that.

And something you can show after graduation — a company, an app going to beta, and a patent in preparation.

That last one is honestly a large part of why this matters to us."

NOTE: Keep this brisk — it's a checkpoint, not an argument. Point four is usually the one professors care about most.`
  );
}

/* ================================================================== *
 * 9 — Track
 * ================================================================== */
{
  const s = slide({
    tint: LAVENDER,
    eyebrow: "Track · which of the three we would declare",
    title: "Entrepreneurship and Venture",
  });
  s.addText(
    "The three deliverables set for this track, and what we can already put against each.",
    {
      x: L,
      y: TOP,
      w: CW,
      h: 0.34,
      isTextBox: true,
      margin: 0,
      fontFace: BODY,
      fontSize: 13,
      color: PLUM,
    }
  );

  const track = [
    [
      "Market / value contribution",
      "An incorporated company, a subscription-plus-advertising model built on what people told us they would actually pay, and a closed angel round.",
      LAVENDER,
    ],
    [
      "MVP / business concept",
      "A pre-launch MVP with a frozen specification and an architecture that scales by adding licensed source pools — now moving into app development.",
      SKY,
    ],
    [
      "Pitch / customer validation",
      "An 86-participant A/B test, roughly 30 interviews, two questionnaires, and four competitions judged by panels outside the university.",
      PINK,
    ],
  ];
  track.forEach((t, i) => {
    card(s, {
      x: L + i * 4.12,
      y: 2.86,
      w: 3.7,
      h: 2.5,
      fill: t[2],
      heading: t[0],
      headSize: 16,
      headH: 0.66,
      body: t[1],
      bodySize: 12.5,
    });
  });

  s.addShape(pres.ShapeType.roundRect, {
    x: L,
    y: 5.62,
    w: CW,
    h: 1.1,
    rectRadius: 0.08,
    fill: { color: TINT },
    line: { type: "none" },
  });
  s.addText(
    [
      { text: "We would bring Research and Technology depth into the track as well — ", options: { color: PLUM } },
      {
        text: "the AI-native pipeline, the two-pools-one-gate ingestion architecture, and the four stress-test passes that keep the confidence signal defensible.",
        options: { color: PLUM },
      },
    ],
    {
      x: L + 0.42,
      y: 5.62,
      w: CW - 0.84,
      h: 1.1,
      isTextBox: true,
      margin: 0,
      fontFace: BODY,
      fontSize: 12.5,
      valign: "middle",
      lineSpacingMultiple: 1.2,
    }
  );

  s.addNotes(
`SCRIPT — ADAM  (about 45 seconds)

"On tracks — we'd declare Entrepreneurship and Venture.

Against the three deliverables you set for it:

Market and value contribution — we have the incorporated company, a subscription-plus-advertising model built on what people actually told us they'd pay, and the closed round.

MVP and business concept — a pre-launch MVP with a frozen specification and an architecture that scales by adding licensed source pools, now moving into app development.

Pitch and customer validation — the eighty-six person A/B test, the interviews, the questionnaires, and four competitions judged by panels outside the university.

We'd also bring research and technology depth into the track — the AI pipeline, the ingestion architecture, the stress tests.

And if you think the Research and Technology track serves the project better, we'd genuinely like your view on that. We're not attached to the label."

NOTE: If they push toward Research and Technology, take it seriously rather than defending. Asking their advice here costs nothing and shows we're coachable.`
  );
}

/* ================================================================== *
 * 10 — Continuation is not repetition
 * ================================================================== */
{
  const s = slide({
    tint: LAVENDER,
    eyebrow: "The new contribution · continuation is not repetition",
    title: "What Year 4 adds that Year 3 did not",
  });

  s.addShape(pres.ShapeType.roundRect, {
    x: L,
    y: TOP,
    w: 5.9,
    h: 3.5,
    rectRadius: 0.08,
    fill: { color: TINT },
    line: { type: "none" },
    shadow: shadow(),
  });
  s.addText("YEAR 3 — ALREADY DONE", {
    x: L + 0.36,
    y: TOP + 0.26,
    w: 5.18,
    h: 0.28,
    isTextBox: true,
    margin: 0,
    fontFace: BODY,
    fontSize: 10.5,
    bold: true,
    color: MUTED,
  });
  s.addText(
    [
      { text: "The problem defined and measured", options: { bullet: true, breakLine: true } },
      { text: "Five design generations, user-tested", options: { bullet: true, breakLine: true } },
      { text: "A decided confidence-signal design", options: { bullet: true, breakLine: true } },
      { text: "Four documented stress-test passes", options: { bullet: true, breakLine: true } },
      { text: "A pre-launch MVP that has never met a real reader", options: { bullet: true } },
    ],
    {
      x: L + 0.36,
      y: TOP + 0.7,
      w: 5.18,
      h: 2.6,
      isTextBox: true,
      margin: 0,
      fontFace: BODY,
      fontSize: 13,
      color: PLUM,
      paraSpaceAfter: 10,
    }
  );

  s.addShape(pres.ShapeType.roundRect, {
    x: 6.88,
    y: TOP,
    w: 5.9,
    h: 3.5,
    rectRadius: 0.08,
    fill: { color: NAVY },
    line: { type: "none" },
  });
  s.addText("YEAR 4 — THE NEW CONTRIBUTION", {
    x: 7.24,
    y: TOP + 0.26,
    w: 5.18,
    h: 0.28,
    isTextBox: true,
    margin: 0,
    fontFace: BODY,
    fontSize: 10.5,
    bold: true,
    color: LIME,
  });
  s.addText(
    [
      { text: "Ship it — a public beta on real, live news", options: { bullet: true, breakLine: true } },
      { text: "Real readers in real sessions, measured", options: { bullet: true, breakLine: true } },
      { text: "First paying users, and the pricing tested", options: { bullet: true, breakLine: true } },
      { text: "The stress tests automated as a regression suite", options: { bullet: true, breakLine: true } },
      { text: "The provisional patent filed", options: { bullet: true } },
    ],
    {
      x: 7.24,
      y: TOP + 0.7,
      w: 5.18,
      h: 2.6,
      isTextBox: true,
      margin: 0,
      fontFace: BODY,
      fontSize: 13,
      color: WHITE,
      paraSpaceAfter: 10,
    }
  );

  s.addShape(pres.ShapeType.roundRect, {
    x: L,
    y: 6.02,
    w: CW,
    h: 0.72,
    rectRadius: 0.08,
    fill: { color: LIME },
    line: { type: "none" },
  });
  s.addText(
    "Year 3 showed that people want this. Year 4 has to show that they will use it, and pay for it.",
    {
      x: L + 0.42,
      y: 6.02,
      w: CW - 0.84,
      h: 0.72,
      isTextBox: true,
      margin: 0,
      fontFace: HEAD,
      fontSize: 16,
      bold: true,
      color: NAVY,
      valign: "middle",
    }
  );

  s.addNotes(
`SCRIPT — VICTOR  (about 60 seconds)

"Now the objection we'd rather raise ourselves, because it's the obvious one. Continuation is not repetition. So what's actually new?

Here's the honest answer.

Year 3 defined and measured the problem, ran five design generations, settled the confidence-signal design, and produced four documented test passes. And it produced a pre-launch MVP that has never met a real reader. Everything we've measured so far, we measured on prototypes and mockups.

Year 4 is where it ships. A public beta on real, live news. Real readers in real sessions, measured. First paying users, with the pricing actually tested rather than surveyed. The stress tests automated into a regression suite, so every future version of the pipeline is measured rather than eyeballed. And the provisional patent filed.

Year 3 showed that people want this. Year 4 has to show that they'll use it, and pay for it."

NOTE: This is the strongest objection to what we're asking, so own it before they raise it. "Has never met a real reader" is the admission that makes the rest credible. End on the lime line and stop.`
  );
}

/* ================================================================== *
 * 11 — Timeline
 * ================================================================== */
{
  const s = slide({
    tint: GHOST,
    eyebrow: "Plan · the next ten months",
    title: "How Year 4 runs on the FYP calendar",
  });

  const steps = [
    ["SEP 2026", "Lock and pitch", "Confirm topic, advisor and track. InnoX bootcamp, 19–20 September: two rounds of pitching.", LIME],
    ["OCT 2026", "Plan and prove", "Detailed project plan and feasibility: ingestion breadth, cost model, and the scope of the beta.", PURPLE],
    ["NOV – DEC 2026", "Build and launch", "Ship the public beta. First real readers on real news, alongside the mid-term deliverables.", NAVY],
    ["JAN – MAY 2027", "Live iteration", "User testing on genuine sessions, commercial validation, first paying users, patent filed.", PERI],
    ["JUN 2027", "Final demo", "A live product with real users and traction data behind it.", PURPLE],
  ];
  // Connector runs behind the nodes, so it is drawn before the loop.
  s.addShape(pres.ShapeType.rect, {
    x: L + 0.6,
    y: 5.365,
    w: CW - 1.2,
    h: 0.03,
    fill: { color: RULE },
    line: { type: "none" },
  });
  steps.forEach((st, i) => {
    const x = L + i * 2.45;
    const w = 2.25;
    s.addShape(pres.ShapeType.roundRect, {
      x,
      y: TOP,
      w,
      h: 2.72,
      rectRadius: 0.08,
      fill: { color: i === 0 ? LAVENDER : TINT },
      line: { type: "none" },
      shadow: shadow(),
    });
    s.addShape(pres.ShapeType.rect, {
      x: x + 0.02,
      y: TOP,
      w: w - 0.04,
      h: 0.08,
      fill: { color: st[3] },
      line: { type: "none" },
    });
    s.addText(st[0], {
      x: x + 0.24,
      y: TOP + 0.24,
      w: 1.8,
      h: 0.26,
      isTextBox: true,
      margin: 0,
      fontFace: BODY,
      fontSize: 10.5,
      bold: true,
      color: PURPLE,
    });
    s.addText(st[1], {
      x: x + 0.24,
      y: TOP + 0.56,
      w: 1.8,
      h: 0.36,
      isTextBox: true,
      margin: 0,
      fontFace: HEAD,
      fontSize: 15,
      bold: true,
      color: NAVY,
    });
    s.addText(st[2], {
      x: x + 0.24,
      y: TOP + 1.0,
      w: 1.8,
      h: 1.5,
      isTextBox: true,
      margin: 0,
      fontFace: BODY,
      fontSize: 11,
      color: PLUM,
      valign: "top",
      lineSpacingMultiple: 1.14,
    });
    // timeline node
    s.addShape(pres.ShapeType.ellipse, {
      x: x + w / 2 - 0.1,
      y: 5.28,
      w: 0.2,
      h: 0.2,
      fill: { color: st[3] },
      line: { color: WHITE, width: 1.5 },
    });
  });

  s.addShape(pres.ShapeType.roundRect, {
    x: L,
    y: 5.82,
    w: CW,
    h: 0.9,
    rectRadius: 0.08,
    fill: { color: TINT },
    line: { type: "none" },
  });
  s.addText(
    [
      { text: "ON INNOX:  ", options: { bold: true, color: PURPLE } },
      {
        text:
          "the bootcamp lands at a useful moment for us. We would use its two pitching rounds to pressure-test the scope of the beta, not to look for a topic.",
        options: { color: PLUM },
      },
    ],
    {
      x: L + 0.42,
      y: 5.82,
      w: CW - 0.84,
      h: 0.9,
      isTextBox: true,
      margin: 0,
      fontFace: BODY,
      fontSize: 12.5,
      valign: "middle",
    }
  );

  s.addNotes(
`SCRIPT — ADAM  (about 55 seconds)

"Here's how that sits on your calendar.

September: lock the topic, confirm advisor and track, and the InnoX bootcamp on the nineteenth and twentieth. We've both reserved those dates already.

And on InnoX — we don't want to treat it as a formality just because we're arriving with an idea. We'd use the two pitching rounds to pressure-test the scope of the beta. What goes in and what doesn't is a genuinely open question for us.

October: the detailed plan and feasibility work — ingestion breadth, the cost model, and the scope of the beta.

November and December: build and launch the public beta, alongside the mid-term deliverables. First real readers.

January to May: live iteration on genuine sessions, commercial validation, first paying users, and the patent filed.

And June twenty twenty-seven: the final demo is a live product with real users and traction data behind it. Not a prototype."

NOTE: The InnoX point pre-empts a fair worry — that a team arriving with a finished idea will coast through the bootcamp. Say it before they think it.`
  );
}

/* ================================================================== *
 * 12 — Team
 * ================================================================== */
{
  const s = slide({
    tint: GHOST,
    eyebrow: "Team · and an honest word on team size",
    title: "The two of us",
  });

  const people = [
    [
      "Victor Nesteruk",
      "Co-founder / CEO — product, design and research",
      "Product direction and the positioning around radical transparency; the design-thinking process across generations; user research and competitive analysis; the card-and-arc and confidence-signal design.",
      LAVENDER,
    ],
    [
      "Ling Bo “Adam” Zeng",
      "Co-founder — engineering and business",
      "Technical co-lead: the two-pools-one-gate ingestion architecture, the generation and analysis pipeline, MVP implementation, the four-pass stress-test programme, and the commercial model.",
      SKY,
    ],
  ];
  people.forEach((p, i) => {
    const x = L + i * 6.33;
    s.addShape(pres.ShapeType.roundRect, {
      x,
      y: TOP,
      w: 5.9,
      h: 2.0,
      rectRadius: 0.08,
      fill: { color: p[3] },
      line: { type: "none" },
      shadow: shadow(),
    });
    s.addText(p[0], {
      x: x + 0.32,
      y: TOP + 0.2,
      w: 5.26,
      h: 0.34,
      isTextBox: true,
      margin: 0,
      fontFace: HEAD,
      fontSize: 17,
      bold: true,
      color: NAVY,
    });
    s.addText(p[1], {
      x: x + 0.32,
      y: TOP + 0.56,
      w: 5.26,
      h: 0.26,
      isTextBox: true,
      margin: 0,
      fontFace: BODY,
      fontSize: 11,
      bold: true,
      color: PURPLE,
    });
    s.addText(p[2], {
      x: x + 0.32,
      y: TOP + 0.9,
      w: 5.26,
      h: 1.0,
      isTextBox: true,
      margin: 0,
      fontFace: BODY,
      fontSize: 11.5,
      color: PLUM,
      valign: "top",
      lineSpacingMultiple: 1.14,
    });
  });

  s.addShape(pres.ShapeType.roundRect, {
    x: L,
    y: 4.5,
    w: CW,
    h: 2.32,
    rectRadius: 0.08,
    fill: { color: NAVY },
    line: { type: "none" },
  });
  s.addText("ON THE TEAM-SIZE GUIDELINE", {
    x: L + 0.42,
    y: 4.72,
    w: CW - 0.84,
    h: 0.28,
    isTextBox: true,
    margin: 0,
    fontFace: BODY,
    fontSize: 10.5,
    bold: true,
    color: LIME,
  });
  s.addText(
    "We know a pair is provisional. We would like to make the case for the two of us.",
    {
      x: L + 0.42,
      y: 5.02,
      w: CW - 0.84,
      h: 0.4,
      isTextBox: true,
      margin: 0,
      fontFace: HEAD,
      fontSize: 16,
      bold: true,
      color: WHITE,
    }
  );
  const reasons = [
    "Everything on the previous slides was delivered by these two, alongside a full course load.",
    "The company is incorporated, with roles and equity already settled between us.",
    "Two faculty advisors are already engaged with the project and know its history.",
  ];
  reasons.forEach((r, i) => {
    const y = 5.5 + i * 0.34;
    s.addShape(pres.ShapeType.ellipse, {
      x: L + 0.44,
      y: y + 0.1,
      w: 0.1,
      h: 0.1,
      fill: { color: LIME },
      line: { type: "none" },
    });
    s.addText(r, {
      x: L + 0.7,
      y,
      w: CW - 1.2,
      h: 0.3,
      isTextBox: true,
      margin: 0,
      fontFace: BODY,
      fontSize: 12,
      color: "E8E2FF",
      valign: "middle",
    });
  });
  s.addText(
    "If the Division would prefer a larger team, we would welcome your guidance on how to bring people in well.",
    {
      x: L + 0.42,
      y: 6.5,
      w: CW - 0.84,
      h: 0.28,
      isTextBox: true,
      margin: 0,
      fontFace: BODY,
      fontSize: 11,
      color: LAVENDER,
    }
  );

  s.addNotes(
`SCRIPT — ADAM  (about 55 seconds)

"On the team.

It's the two of us. Victor leads product, design and research. I lead engineering and the business side — the ingestion architecture, the generation pipeline, the MVP, the stress-test programme and the commercial model.

And we want to raise team size ourselves rather than wait for you to ask. We know the kick-off deck asks for three to five, and that a pair is provisional.

We'd like to make the case for the two of us. Everything on the last ten slides was delivered by these two people, alongside a full course load. The company is incorporated, with roles and equity already settled between us. And we already have two faculty advisors engaged who know the project's history.

But if the Division would rather we were a larger team, we'd genuinely welcome your guidance on how to bring people in well. That's a harder question than it looks, because of the company structure, and we'd rather get it right than guess."

NOTE: Then stop and listen. Do not argue this point in the room — if they want a larger team, take the guidance and work out the details afterwards. Fighting it here is the one thing that could sour the meeting.`
  );
}

/* ================================================================== *
 * 13 — Asks and thanks
 * ================================================================== */
{
  const s = pres.addSlide();
  s.background = { color: PURPLE };
  s.addShape(pres.ShapeType.rect, {
    x: 0,
    y: 0,
    w: 0.85,
    h: 0.1,
    fill: { color: LIME },
    line: { type: "none" },
  });
  s.addImage({ data: MARK_WHITE, x: 9.3, y: 2.75, w: 4.0, h: 3.92 });
  s.addImage({ data: LOGO_WHITE, x: 0.44, y: 0.42, w: 1.956, h: 0.72 });

  s.addText("THREE THINGS WE WOULD LIKE TO ASK YOU", {
    x: 0.7,
    y: 1.72,
    w: 8.6,
    h: 0.34,
    isTextBox: true,
    margin: 0,
    fontFace: BODY,
    fontSize: 13,
    bold: true,
    color: LIME,
  });

  const asks = [
    "May we register Fliq as our FYP topic, under the Entrepreneurship and Venture track?",
    "How would you advise us on advisor arrangements for the year ahead?",
    "What would you like to see from us before the first class on 3 September, and before InnoX?",
  ];
  asks.forEach((a, i) => {
    const y = 2.3 + i * 1.02;
    s.addShape(pres.ShapeType.roundRect, {
      x: 0.7,
      y,
      w: 8.3,
      h: 0.86,
      rectRadius: 0.08,
      fill: { color: "8F1A8F" },
      line: { type: "none" },
    });
    s.addText(String(i + 1), {
      x: 0.94,
      y: y + 0.19,
      w: 0.48,
      h: 0.48,
      isTextBox: true,
      margin: 0,
      align: "center",
      valign: "middle",
      fontFace: HEAD,
      fontSize: 19,
      bold: true,
      color: LIME,
    });
    s.addText(a, {
      x: 1.56,
      y,
      w: 7.2,
      h: 0.86,
      isTextBox: true,
      margin: 0,
      fontFace: BODY,
      fontSize: 13.5,
      color: WHITE,
      valign: "middle",
      lineSpacingMultiple: 1.1,
    });
  });

  s.addText("Thank you for making the time before term begins.", {
    x: 0.7,
    y: 5.62,
    w: 8.6,
    h: 0.44,
    isTextBox: true,
    margin: 0,
    fontFace: HEAD,
    fontSize: 22,
    bold: true,
    color: OFFWHITE,
  });
  s.addShape(pres.ShapeType.rect, {
    x: 0.7,
    y: 6.55,
    w: 8.66,
    h: 0.014,
    fill: { color: LIME },
    line: { type: "none" },
  });
  s.addText(
    [
      { text: "Victor Nesteruk · Ling Bo Zeng", options: { bold: true, color: OFFWHITE } },
      { text: "     |     HKUST ISDN, Year 4     |     ", options: { color: "E8E2FF" } },
      { text: "NewsFlick Limited     |     fliq.news", options: { color: "E8E2FF" } },
    ],
    {
      x: 0.7,
      y: 6.72,
      w: 9.8,
      h: 0.32,
      isTextBox: true,
      margin: 0,
      fontFace: BODY,
      fontSize: 13,
    }
  );

  s.addNotes(
`SCRIPT — VICTOR  (about 35 seconds)

"So — three things we'd like to ask you.

First: may we register Fliq as our FYP topic, under the Entrepreneurship and Venture track?

Second: how would you advise us on advisor arrangements for the year ahead?

And third: what would you like to see from us before the first class on the third of September, and before the InnoX bootcamp?

Thank you again for making the time before term begins. We're very happy to send you the ISDN 3002 report and the stress-test evidence afterwards, if that would be useful."

NOTE: Ask all three, then stop talking and let the silence sit. Question two matters practically — Prof. Tsui suggested Prof. Gu and Prof. Song meet us first, so the advisor arrangement is genuinely open. Don't assume who our advisor would be.

IF THEY SAY YES: don't celebrate and leave. Ask what they need from us to make it official, and when.
IF THEY HESITATE: ask what would make them comfortable, and offer to come back with it before the third.`
  );
}

pres
  .writeFile({ fileName: OUT })
  .then(() => console.log("Wrote " + OUT))
  .catch((e) => {
    console.error(e);
    process.exit(1);
  });
