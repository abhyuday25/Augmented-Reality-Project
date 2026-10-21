import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootDir = path.resolve(__dirname, '..');
const distDir = path.resolve(rootDir, 'dist');

console.log('[Postbuild] Running asset mirroring for production deployment...');

if (!fs.existsSync(distDir)) {
  console.error('[Postbuild] Error: dist directory does not exist. Run "vite build" first.');
  process.exit(1);
}

function copyRecursive(src, dest) {
  if (!fs.existsSync(src)) return;
  fs.mkdirSync(dest, { recursive: true });
  const entries = fs.readdirSync(src, { withFileTypes: true });

  for (const entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);

    if (entry.isDirectory()) {
      copyRecursive(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

// 1. Mirror src/assets into dist/src/assets so string-based runtime asset paths resolve
const srcAssets = path.join(rootDir, 'src', 'assets');
const distSrcAssets = path.join(distDir, 'src', 'assets');
if (fs.existsSync(srcAssets)) {
  console.log('[Postbuild] Copying src/assets -> dist/src/assets');
  copyRecursive(srcAssets, distSrcAssets);
}

// 2. Mirror scripts/generated_textures into dist/scripts/generated_textures
const srcGenTex = path.join(rootDir, 'scripts', 'generated_textures');
const distGenTex = path.join(distDir, 'scripts', 'generated_textures');
if (fs.existsSync(srcGenTex)) {
  console.log('[Postbuild] Copying scripts/generated_textures -> dist/scripts/generated_textures');
  copyRecursive(srcGenTex, distGenTex);
}

// 3. Copy root 3D GLB model if present to root of dist as well
const rootGLB = path.join(rootDir, 'vit_vellore_virtual_museum.glb');
if (fs.existsSync(rootGLB)) {
  console.log('[Postbuild] Copying root vit_vellore_virtual_museum.glb -> dist/');
  fs.copyFileSync(rootGLB, path.join(distDir, 'vit_vellore_virtual_museum.glb'));
}

// 4. Generate SPA _redirects file for Netlify in dist/
const redirectsFile = path.join(distDir, '_redirects');
fs.writeFileSync(redirectsFile, '/*    /index.html   200\n', 'utf8');
console.log('[Postbuild] Created dist/_redirects for SPA routing.');

console.log('[Postbuild] Assets successfully mirrored for Netlify production.');
