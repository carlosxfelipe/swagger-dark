// To run this script with Deno, use:
// deno run --allow-read --allow-write --allow-net minify.ts
import * as esbuild from "npm:esbuild@0.20.2";

async function minifyCss() {
  console.log("Minifying CSS...");
  try {
    await esbuild.build({
      entryPoints: ["static/swagger/swagger-dark.css"],
      bundle: true,
      minify: true,
      outfile: "static/swagger/swagger-dark.min.css",
    });
    console.log(
      "✅ CSS minified successfully! Saved as static/swagger/swagger-dark.min.css",
    );
  } catch (error) {
    console.error("❌ Error minifying CSS:", error);
  } finally {
    // Esbuild leaves processes running by default, so we need to stop them
    esbuild.stop();
  }
}

minifyCss();
