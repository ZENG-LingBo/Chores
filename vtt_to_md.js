/**
 * Converts the ISDN 4001 FYP kick-off meeting WebVTT recording into Markdown.
 *
 *   node vtt_to_md.js <input.vtt> <output.md> [--verbatim]
 *
 * Consecutive cues from the same speaker are merged into one turn, so the
 * result reads as a transcript rather than as subtitles.
 *
 * By default the text is lightly edited for readability: mis-transcribed
 * names and terms are corrected, stutters and filler words are trimmed, and
 * long monologues are broken into paragraphs. No sentence is reworded and
 * nothing is summarised — every claim stays as its speaker made it.
 * Pass --verbatim to emit the raw transcription instead, with the
 * corrections listed in a glossary rather than applied.
 *
 * The .vtt file remains the authoritative record either way.
 */

const fs = require("fs");

const args = process.argv.slice(2);
const VERBATIM = args.includes("--verbatim");
const [IN, OUT] = args.filter((a) => !a.startsWith("--"));
if (!IN || !OUT) {
  console.error("usage: node vtt_to_md.js <input.vtt> <output.md> [--verbatim]");
  process.exit(1);
}

// ---------------------------------------------------------------- parse ----
const raw = fs.readFileSync(IN, "utf8").replace(/^﻿/, "").replace(/\r\n/g, "\n");
const cues = [];
for (const block of raw.split("\n\n")) {
  const lines = block.trim().split("\n").filter((l) => l.trim());
  if (!lines.length || lines[0].startsWith("WEBVTT")) continue;
  const tsIdx = lines.findIndex((l) => l.includes("-->"));
  if (tsIdx === -1) continue;
  const start = lines[tsIdx].split("-->")[0].trim().split(".")[0];
  const text = lines.slice(tsIdx + 1).join(" ").trim();
  const m = text.match(/^([^:]{1,40}):\s*(.*)$/);
  cues.push({ start, speaker: m ? m[1].trim() : "Unknown", text: m ? m[2].trim() : text });
}

const blocks = [];
for (const c of cues) {
  const last = blocks[blocks.length - 1];
  if (last && last.speaker === c.speaker) last.parts.push(c.text);
  else blocks.push({ start: c.start, speaker: c.speaker, parts: [c.text] });
}

// ------------------------------------------------------------ corrections --
// Words the auto-transcription reliably gets wrong. Applied in order.
const TERMS = [
  [/\bFIP\b/g, "FYP"],
  [/\bF-shaped\b/g, "fuzzy"],
  [/\bShenzhen (?:Inoics|Index|Yunx|US|Innoics)\b/g, "Shenzhen InnoX"],
  [/\b(?:Enox|Inoics|Innoics)\b/g, "InnoX"],
  [/\bIDE Marketplace\b/g, "Idea Marketplace"],
  [/\bIDEA Marketplace\b/g, "Idea Marketplace"],
  [/\bTeam Aviva\b/g, "Team AWAVA"],
  [/\bArrow Relief\b/g, "AeroRelief"],
  [/\berror relief\b/gi, "AeroRelief"],
  [/\bTails Night\b/g, "Tales9"],
  [/\bTails 9\b/g, "Tales9"],
  [/\bTales 9\b/g, "Tales9"],
  [/\bSUP board\b/g, "SUP board"],
  [/\bStand Up Pedal Board\b/g, "stand-up paddleboard"],
  [/\bStand Up for, Stand Up Pedal Board\b/g, "stand-up paddleboard"],
  [/\bdesign thing\b/g, "design thinking"],
  [/\bcontinuation is not really the reputation\b/g, "continuation is not repetition"],
  [/\bAST or HKUST\b/g, "HKUST"],
  [/\bHJUSD\b/g, "HKUST"],
  [/\bUSD stresses\b/g, "HKUST stresses"],
  [/\bIC signature\b/g, "ISD signature"],
  [/\bISDR\b/g, "ISD students"],
  [/\bEFC going to be year 4\b/g, "soon-to-be Year 4"],
  [/\bBarco\b/g, "Barcode"],
  [/\bBarcoat\b/g, "Barcode"],
  [/\bhome written card\b/g, "home return permit"],
  [/\bcross control\b/g, "cruise control"],
  [/\bactive throttle-based\b/g, "active thrust-based"],
  [/\bpast, planning algorithm\b/g, "path planning algorithms"],
  [/\bLOM AI agent\b/g, "LLM AI agent"],
  [/\bwarrantin\b/gi, "iterations"],
  [/\bAI slope\b/g, "AI slop"],
  [/\bholistic\b/g, "hallucinated"],
  // People
  [/\bChi Ying TSUI\b/g, "Chi Ying TSUI"],
  [/\b(?:Siwa|Siva)\b/g, "CY"],
  [/\bthank, thank all three\b/g, "thank all three"],
  [/\bKelvin\b/g, "Keven"],
  [/\bCalvin\b/g, "Keven"],
  [/\bKevin\b/g, "Keven"],
  [/\bJimmy Hong\b/g, "Jimmy Hung"],
];

// Disfluencies. Only patterns that carry no meaning are removed.
// The "…" a speaker uses to restart a sentence is KEPT — deleting it welds
// two false starts into one broken sentence, which reads worse than the mark.
const FILLER = [
  [/,?\s*\byou know,\s*/g, " "],
  [/,?\s*\bI mean,\s*/g, " "],
  [/,\s*like,\s*/g, ", "],
  [/\blike,\s+like,\s*/g, "like "],
  [/\bsort of,\s*/g, ""],
  [/\bso,\s+so,\s*/gi, "So "],
];

// Run last, after every other rule has had a chance to create new duplicates.
const TIDY = [
  [/\b(\w+),(?:\s+\1,){2,}\s+/gi, "$1, "], // yeah, yeah, yeah, yeah -> yeah,
  [/\b(\w+),\s+\1,\s+\1\b/gi, "$1"], // yeah, yeah, yeah -> yeah
  [/\b(\w+)\s+\1\b(?=[\s,.?!])/gi, "$1"], // "the the" / "or or" -> one
  [/\b(\w+\s+\w+)\s+\1\b/gi, "$1"], // "I will I will" / "as a as a" -> one
  [/\b(\w+),\s+\1\b(?=\s)/gi, "$1"], // "and, and" -> "and"
  [/([a-z]),?\.\s+([a-z])/g, "$1 $2"], // stray full stop mid-clause
  [/\s*…\s*/g, "… "],
  [/\s+([,.?!])/g, "$1"],
  [/,{2,}/g, ","],
  [/,\s*\./g, "."],
  [/\s{2,}/g, " "],
];

function clean(t) {
  let s = t;
  for (const [re, to] of TERMS) s = s.replace(re, to);
  for (const [re, to] of FILLER) s = s.replace(re, to);
  for (const [re, to] of TIDY) s = s.replace(re, to);
  s = s.replace(/^\s*[,.]\s*/, "").trim();
  return s.charAt(0).toUpperCase() + s.slice(1);
}

/** Split a long turn into paragraphs of roughly three sentences. */
function paragraphs(text) {
  // "…" marks hesitation, not a sentence end, so it must not split a paragraph.
  const sentences = text.match(/[^.?!]+(?:[.?!]+|$)/g) || [text];
  const out = [];
  let buf = [];
  let chars = 0;
  for (const s of sentences) {
    buf.push(s.trim());
    chars += s.length;
    if (buf.length >= 3 && chars > 320) {
      out.push(buf.join(" "));
      buf = [];
      chars = 0;
    }
  }
  if (buf.length) out.push(buf.join(" "));
  return out;
}

// --------------------------------------------------------------- sections --
const SECTIONS = {
  "00:07:14": "Waiting to start",
  "00:11:07": "Briefing — how this year's FYP works",
  "00:26:47": "InnoX bootcamp and meeting times",
  "00:30:05": "Weekly meetings and assessment",
  "00:31:43": "Student questions",
  "00:37:02": "Talk 1 — Team AWAVA (Tony Shen)",
  "00:48:11": "Talk 2 — AeroRelief (Jimmy Wu)",
  "01:01:00": "Talk 3 — Tales9 (Jimmy Hung)",
  "01:15:25": "Closing",
};

const ROLES = {
  "Richard GU": "FYP co-coordinator; gave the briefing",
  "Chi Ying TSUI": "FYP co-coordinator (“CY”)",
  "Haochen HU": "Course staff (“Keven”)",
  "Yuming SHEN": "Alumnus — “Tony”, Team AWAVA",
  "Chun Ming WU": "Alumnus — “Jimmy Wu”, AeroRelief",
  "Ka Hin HUNG,Jimmy": "Alumnus — “Jimmy Hung”, Tales9",
  Fiona: "Student — asked about industry projects",
  Lukcy: "Student — asked about continuing a Year-3 project",
  "Audio shared by Chun Ming WU": "Audio from a video played during the talk",
};

const DISPLAY = { "Ka Hin HUNG,Jimmy": "Jimmy HUNG (Ka Hin)" };

const counts = {};
for (const b of blocks) counts[b.speaker] = (counts[b.speaker] || 0) + 1;

const toSec = (t) => t.split(":").reduce((a, v) => a * 60 + Number(v), 0);
const first = cues[0].start;
const last = cues[cues.length - 1].start;

// ------------------------------------------------------------------ emit --
const o = [];
o.push("# ISDN 4001 — FYP Kick-off Meeting");
o.push("");
o.push("Kick-off for the 2026–27 final year project, HKUST Division of Integrative Systems and Design.");
o.push("");
o.push(`**Recording** ${first}–${last} (${Math.round((toSec(last) - toSec(first)) / 60)} min) · `
  + `**Speakers** ${Object.keys(counts).length} · **Turns** ${blocks.length}`);
o.push("");

if (!VERBATIM) {
  o.push("> **On this text.** Lightly edited from the automatic captions for readability:");
  o.push("> mis-transcribed names and terms corrected, stutters and filler trimmed, long");
  o.push("> monologues broken into paragraphs. Nothing is reworded or summarised, and no");
  o.push("> point is added or dropped. `FYP_KickoffMeeting.vtt` remains the actual record —");
  o.push("> quote from that, not from here.");
  o.push("");
}

o.push("## Jump to");
o.push("");
for (const [ts, title] of Object.entries(SECTIONS)) {
  o.push(`- \`${ts}\` — ${title}`);
}
o.push("");
o.push("## Who speaks");
o.push("");
o.push("| Speaker | Turns | |");
o.push("| --- | ---: | --- |");
for (const [name, n] of Object.entries(counts).sort((a, b) => b[1] - a[1])) {
  o.push(`| **${DISPLAY[name] || name}** | ${n} | ${ROLES[name] || ""} |`);
}
o.push("");

if (VERBATIM) {
  o.push("## Terms the transcription gets wrong");
  o.push("");
  o.push("| In the text | Means |");
  o.push("| --- | --- |");
  o.push("| FIP | FYP |");
  o.push("| Enox, Inoics, Shenzhen Index | InnoX |");
  o.push("| IDE Marketplace | Idea Marketplace |");
  o.push("| Team Aviva | Team AWAVA |");
  o.push("| Arrow Relief | AeroRelief |");
  o.push("| Tails Night | Tales9 |");
  o.push("| Siwa, Siva | CY (Prof. Chi Ying Tsui) |");
  o.push("| Calvin, Kelvin, Kevin | Keven (Haochen Hu) |");
  o.push("");
}

o.push("---");
o.push("");

let open = null;
for (const b of blocks) {
  if (SECTIONS[b.start] && SECTIONS[b.start] !== open) {
    open = SECTIONS[b.start];
    o.push(`## ${open}`);
    o.push("");
    o.push(`<sub>from ${b.start}</sub>`);
    o.push("");
  }
  const joined = b.parts.join(" ");
  const text = VERBATIM ? joined : clean(joined);
  const name = DISPLAY[b.speaker] || b.speaker;
  const paras = VERBATIM ? [text] : paragraphs(text);

  o.push(`**${name}** &nbsp;<sub>${b.start}</sub>`);
  o.push("");
  for (const p of paras) {
    o.push(p);
    o.push("");
  }
}

fs.writeFileSync(OUT, o.join("\n"));
console.log(
  `Wrote ${OUT} — ${blocks.length} turns, ${VERBATIM ? "verbatim" : "readability-edited"}, ${o.join("\n").length} chars`
);
