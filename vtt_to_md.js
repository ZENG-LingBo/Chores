/**
 * Converts the ISDN 4001 FYP kick-off meeting WebVTT recording into Markdown.
 *
 *   node vtt_to_md.js <input.vtt> <output.md>
 *
 * Consecutive cues from the same speaker are merged into one block so the
 * result reads as a transcript rather than as subtitles. Wording is left
 * exactly as the auto-transcription produced it; nothing is corrected or
 * paraphrased. Section headings are placed at the points where the meeting
 * visibly hands over from one speaker or segment to the next.
 */

const fs = require("fs");

const [, , IN, OUT] = process.argv;
if (!IN || !OUT) {
  console.error("usage: node vtt_to_md.js <input.vtt> <output.md>");
  process.exit(1);
}

// ---- Parse ----
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
  cues.push({ start, speaker: m ? m[1].trim() : null, text: m ? m[2].trim() : text });
}

// ---- Merge consecutive cues from one speaker ----
const blocks = [];
for (const c of cues) {
  const last = blocks[blocks.length - 1];
  if (last && last.speaker === c.speaker) last.parts.push(c.text);
  else blocks.push({ start: c.start, speaker: c.speaker, parts: [c.text] });
}

// ---- Sections, keyed by the timestamp at which each begins ----
const SECTIONS = {
  "00:07:14": "Before the meeting starts",
  "00:11:07": "Briefing — how this year's FYP is organised",
  "00:26:47": "The InnoX bootcamp, and meeting times",
  "00:30:05": "Weekly progress meetings and assessment",
  "00:31:43": "Questions from students",
  "00:37:02": "Sharing 1 — Team AWAVA (Tony / Yuming SHEN)",
  "00:48:11": "Sharing 2 — AeroRelief (Jimmy Wu / Chun Ming WU)",
  "01:01:00": "Sharing 3 — Tales9 (Jimmy Hung / Ka Hin HUNG)",
  "01:15:25": "Closing",
};

// ---- Speaker tallies for the participants table ----
// Counted over merged blocks, so "turns" means what the table says it means.
const counts = {};
for (const b of blocks) counts[b.speaker] = (counts[b.speaker] || 0) + 1;

const ROLES = {
  "Richard GU": "FYP co-coordinator; ran the briefing",
  "Chi Ying TSUI": "FYP co-coordinator (“CY”)",
  "Haochen HU": "Course staff (“Kevin” / “Keven” in the audio)",
  "Yuming SHEN": "Alumnus presenter — “Tony”, Team AWAVA",
  "Chun Ming WU": "Alumnus presenter — “Jimmy Wu”, AeroRelief",
  "Ka Hin HUNG,Jimmy": "Alumnus presenter — “Jimmy Hung”, Tales9",
  Fiona: "Student — asked about industry-initiated projects",
  Lukcy: "Student — asked about continuing a Year-3 project",
  "Audio shared by Chun Ming WU": "Audio from a video played during the AeroRelief talk",
};

const first = cues[0].start;
const last = cues[cues.length - 1].start;

// ---- Emit ----
const out = [];
out.push("# ISDN 4001 — FYP Kick-off Meeting");
out.push("");
out.push("Transcript of the recorded kick-off meeting for the 2026–27 final year project,");
out.push("HKUST Division of Integrative Systems and Design.");
out.push("");
out.push(`- **Recording spans** ${first} – ${last} (about ${Math.round((toSec(last) - toSec(first)) / 60)} minutes)`);
out.push(`- **Speakers** ${Object.keys(counts).length}`);
out.push(`- **Source** \`FYP_KickoffMeeting.vtt\` — ${cues.length} caption cues, merged into ${blocks.length} speaking turns`);
out.push("");
out.push("## Who is speaking");
out.push("");
out.push("| Speaker | Turns | Role |");
out.push("| --- | ---: | --- |");
for (const [name, n] of Object.entries(counts).sort((a, b) => b[1] - a[1])) {
  out.push(`| ${name} | ${n} | ${ROLES[name] || ""} |`);
}
out.push("");
out.push("## Contents");
out.push("");
for (const [ts, title] of Object.entries(SECTIONS)) {
  out.push(`- **${ts}** — ${title}`);
}
out.push("");
out.push("## A note on accuracy");
out.push("");
out.push("This is an automatic transcription and the wording below is left exactly as it came out,");
out.push("including its mistakes. Names and terms it repeatedly mishears:");
out.push("");
out.push("| In the transcript | Almost certainly |");
out.push("| --- | --- |");
out.push("| FIP | FYP |");
out.push("| Enox, Inoics, Shenzhen Index, Shenzhen Yunx, Shenzhen US | InnoX |");
out.push("| IDE Marketplace | Idea Marketplace |");
out.push("| Team Aviva | Team AWAVA |");
out.push("| Arrow Relief | AeroRelief |");
out.push("| Tails Night, Tails 9 | Tales9 |");
out.push("| Siwa, Siva, Chinese, God | CY (Prof. Chi Ying Tsui) |");
out.push("| Calvin, Kelvin, Catherine, Kevin | Keven (Haochen Hu) |");
out.push("| AST | HKUST |");
out.push("| “design thing” | design thinking |");
out.push("| “continuation is not really the reputation” | continuation is not repetition |");
out.push("");
out.push("---");
out.push("");
out.push("## Transcript");
out.push("");

let open = null;
for (const b of blocks) {
  if (SECTIONS[b.start] && SECTIONS[b.start] !== open) {
    open = SECTIONS[b.start];
    out.push(`### ${b.start} — ${open}`);
    out.push("");
  }
  out.push(`**[${b.start}] ${b.speaker}**`);
  out.push("");
  out.push(b.parts.join(" "));
  out.push("");
}

fs.writeFileSync(OUT, out.join("\n"));
console.log(`Wrote ${OUT} — ${blocks.length} turns, ${out.join("\n").length} chars`);

function toSec(t) {
  const [h, m, s] = t.split(":").map(Number);
  return h * 3600 + m * 60 + s;
}
