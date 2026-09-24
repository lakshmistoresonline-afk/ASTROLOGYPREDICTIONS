import os
import shutil

pages_dir = r"D:\ASTROLOGYPREDICTIONS\frontend\src\pages"

app_path = os.path.join(pages_dir, "_app.tsx")
idx_path = os.path.join(pages_dir, "index.tsx")

if os.path.isdir(app_path):
    shutil.rmtree(app_path, ignore_errors=True)

if os.path.isdir(idx_path):
    shutil.rmtree(idx_path, ignore_errors=True)

app_content = """import type { AppProps } from 'next/app';
import '../styles/globals.css';

export default function App({ Component, pageProps }: AppProps) {
  return <Component {...pageProps} />;
}
"""

if not os.path.isfile(app_path):
    with open(app_path, "w", encoding="utf-8") as f:
        f.write(app_content)

idx_content = """import { Dashboard } from './Dashboard';

export default Dashboard;
"""

if not os.path.isfile(idx_path):
    with open(idx_path, "w", encoding="utf-8") as f:
        f.write(idx_content)

print("Created _app.tsx and index.tsx files successfully.")
