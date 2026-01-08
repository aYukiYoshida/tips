import fs from "node:fs";
import path from "node:path";
import { Command } from "commander";

const defaultAssets = ["images"];

const srcDir = path.resolve("src");
const outDir = path.resolve("out");
const log = (message) => {
  console.log("[assets]", message);
};

const copy = (from, to) => {
  fs.mkdirSync(to, { recursive: true });
  fs.cpSync(from, to, { recursive: true });
  log(`copied: ${from} -> ${to}`);
};

/**
 * 指定したディレクトリ直下のディレクトリ一覧を取得する
 */
const getTopLevelDirectories = (dir=srcDir) => {
  if (!fs.existsSync(dir)) return [];

  return fs
    .readdirSync(dir, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .map((entry) => entry.name);
};

const copyAssets = (assets) => {
  const topLevelDirectories = getTopLevelDirectories(srcDir);
  for (const topLevelDirectory of topLevelDirectories) {
    for (const asset of assets) {
      const from = path.resolve(srcDir, topLevelDirectory, asset);
      const to = path.resolve(outDir, topLevelDirectory, asset);

      if (!fs.existsSync(from)) {
        log(`skip: not found: ${from}`);
        continue;
      }

      copy(from, to);
    }
  }
};

const main = () => {
  const program = new Command();
  program
    .description("Copy static assets from each directory under src/ to directories with the same name under out/")
    .argument("[assets...]", "Asset directory names under each directory", defaultAssets)
    .action((assets) => {
      copyAssets(assets);
    });

  program.parse(process.argv);
};

main();
