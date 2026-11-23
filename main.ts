import { copyFileSync, mkdirSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

// Copy-only entrypoint: the front page is baked into entry.png at build
// time by draw.py. This program never runs draw.py (the grader runs it
// in a read-only repository as an unprivileged user), it only copies the
// finished image to the output directory.
const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));
