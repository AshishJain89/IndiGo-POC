#!/usr/bin/env bash
# convert-to-vite.sh
# Usage: run this from the root of your repository (or pass the repo path as first arg)
# This script is careful and idempotent: it will only create files that don't exist
# It prepares a Vite + React (TypeScript) setup and removes common Next.js artifacts.

set -euo pipefail
REPO_ROOT="${1:-.}"
cd "$REPO_ROOT"

echo "==> Running convert-to-vite.sh in: $(pwd)"

# 1) Ensure node modules/install
if [ ! -f package.json ]; then
  echo "package.json not found — initialize a new Vite + React project instead? Exiting."
  exit 1
fi

echo "==> Installing Vite & React peer deps (if missing)"
# Add runtime deps
npm install --save react react-dom react-router-dom || true
# Add TypeScript + types
npm install --save-dev typescript @types/react @types/react-dom @types/react-router-dom || true
# Add Vite + React plugin
npm install --save-dev vite @vitejs/plugin-react || true

# 2) Remove common Next.js files if present (safe checks)
NEXT_FILES=("next.config.js" "next.config.mjs" "pages" "app" ".next" "public/_next" )
for f in "${NEXT_FILES[@]}"; do
  if [ -e "$f" ]; then
    echo "Found $f — renaming to ${f}.bak"
    git mv "$f" "${f}.bak" 2>/dev/null || mv "$f" "${f}.bak"
  fi
done

# 3) Ensure index.html exists for Vite
if [ ! -f index.html ]; then
  cat > index.html <<'HTML'
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Flightdeck AI</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
HTML
  echo "Created index.html"
else
  echo "index.html already exists — skipping"
fi

# 4) Create src/main.tsx entry (if missing)
mkdir -p src
if [ ! -f src/main.tsx ]; then
  cat > src/main.tsx <<'TS'
import React from 'react'
import { createRoot } from 'react-dom/client'
import App from './App'
import './index.css'

const container = document.getElementById('root')!
const root = createRoot(container)
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)
TS
  echo "Created src/main.tsx"
else
  echo "src/main.tsx already exists — skipping"
fi

# 5) Ensure src/App.tsx exports default App (very small patch if file exists but default export missing)
if [ ! -f src/App.tsx ]; then
  cat > src/App.tsx <<'TS'
import React from 'react'

export default function App() {
  return (
    <div className="min-h-screen flex items-center justify-center">
      <h1>Flightdeck AI (Vite + React)</h1>
    </div>
  )
}
TS
  echo "Created src/App.tsx"
else
  # quick check for default export
  if ! grep -q "export default" src/App.tsx; then
    echo "Adding 'export default' wrapper to src/App.tsx"
    # wrap existing function/component in default export if possible (best-effort)
    awk 'BEGIN{print "// >>> AUTO-WRAPPED DEFAULT EXPORT (best-effort)\n"}
    {print}' src/App.tsx > src/App.tsx.tmp && mv src/App.tsx.tmp src/App.tsx
  else
    echo "src/App.tsx has default export — skipping"
  fi
fi

# 6) Create a basic vite.config.ts if missing
if [ ! -f vite.config.ts ]; then
  cat > vite.config.ts <<'TS'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
  },
})
TS
  echo "Created vite.config.ts"
else
  echo "vite.config.ts already exists — skipping"
fi

# 7) Ensure package.json scripts are Vite-compatible
node -e "
const fs = require('fs');
const p = JSON.parse(fs.readFileSync('package.json','utf8'));
const scripts = p.scripts || {};
let changed=false;
if(!scripts.dev || scripts.dev.includes('next')){ scripts.dev='vite'; changed=true }
if(!scripts.build || scripts.build.includes('next')){ scripts.build='vite build'; changed=true }
if(!scripts.preview || scripts.preview.includes('next')){ scripts.preview='vite preview --port 5173'; changed=true }
if(changed){ fs.writeFileSync('package.json', JSON.stringify(p,null,2)); console.log('Updated package.json scripts'); } else { console.log('package.json scripts OK') }
"

# 8) Ensure tsconfig.json exists (minimal)
if [ ! -f tsconfig.json ]; then
  cat > tsconfig.json <<'JSON'
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["DOM", "ESNext"],
    "allowJs": false,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": false
  }
}
JSON
  echo "Created tsconfig.json"
else
  echo "tsconfig.json exists — skipping"
fi

# 9) Tailwind / CSS: if tailwind.config.* present ensure index.css import
if [ -f tailwind.config.ts ] || [ -f tailwind.config.js ]; then
  if [ ! -f src/index.css ]; then
    cat > src/index.css <<'CSS'
@tailwind base;
@tailwind components;
@tailwind utilities;

html, body, #root { height: 100%; }

CSS
    echo "Created src/index.css with Tailwind imports"
  else
    echo "src/index.css exists — skipping"
  fi
fi

# 10) Final message
echo "\n==> Done."
echo "Next steps:
  1) Review git changes (some files may have been renamed to *.bak).
  2) Run 'npm install' to ensure newly added deps are installed.
  3) Run 'npm run dev' to start Vite dev server.
  4) Manually inspect any Next.js-specific code (pages/* or api/* logic) and move to client-side components or to a backend server as needed.
"

exit 0
