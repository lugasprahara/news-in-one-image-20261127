// Entry program for make.fun's news-image-20261127 bounty
// ("Sum up 27 November's world news in one image").
//
// The entry is a single 1024x1024 PNG, entry.png, drawn programmatically by
// render.py from the day's reporting and committed beside this file. The
// grading harness runs this program with no network and reads exactly one
// artifact afterwards, so the program's whole job is to place those bytes at
// the output location:
//
//   /output/entry.png            (or $MAKEFUN_OUTPUT_DIR/entry.png locally)
//
// Run it the way the kit prescribes:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");

const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outputDir, { recursive: true });

const target = join(outputDir, "entry.png");
copyFileSync(source, target);

console.log(`entry.png written to ${target} (${statSync(target).size} bytes)`);
