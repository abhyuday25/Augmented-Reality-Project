import { MUSEUM_EXHIBITS, INTERACTION_REGISTRY } from "../src/data/museumContent.js";
import fs from "fs";
import path from "path";

fs.writeFileSync(
  "./src/data/museumContent.json",
  JSON.stringify({ exhibits: MUSEUM_EXHIBITS, registry: INTERACTION_REGISTRY }, null, 2),
  "utf-8"
);
console.log("Successfully generated src/data/museumContent.json with " + MUSEUM_EXHIBITS.length + " exhibits.");
