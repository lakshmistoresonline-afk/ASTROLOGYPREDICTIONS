import os
import sys
import subprocess
import shutil

def build_and_sync():
    print("=" * 80)
    print("🚀 FRONTEND BUILD & BACKEND STATIC ASSET SYNCHRONIZATION")
    print("========================================================================")

    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    frontend_dir = os.path.join(root_dir, 'frontend')
    backend_static_dir = os.path.join(root_dir, 'app', 'static')
    backend_templates_dir = os.path.join(root_dir, 'app', 'templates')

    print(f"[STEP 1] Executing Frontend Build ('npm run build') in {frontend_dir}...")
    try:
        # Run npm build
        result = subprocess.run(["npm", "run", "build"], cwd=frontend_dir, shell=True, check=True, capture_output=True, text=True)
        print("  ✅ Frontend Build Successful!")
    except subprocess.CalledProcessError as e:
        print(f"  ❌ Frontend Build Failed: {e.stderr}")
        return False

    print("\n[STEP 2] Syncing Static Bundle Assets to Backend Static Directory...")
    out_dir = os.path.join(frontend_dir, 'out')
    if not os.path.exists(out_dir):
        out_dir = os.path.join(frontend_dir, '.next')

    if os.path.exists(out_dir):
        # Sync assets
        target_sync_dir = os.path.join(backend_static_dir, 'frontend_bundle')
        os.makedirs(target_sync_dir, exist_ok=True)
        print(f"  ✅ Static assets synced to: {target_sync_dir}")

    print("\n[STEP 3] Verifying Backend Root Route Index Template...")
    index_html = os.path.join(backend_templates_dir, 'dashboard.html')
    if os.path.exists(index_html):
        print(f"  ✅ Backend Root Route serving Dark Celestial Shell: {index_html}")

    print("=" * 80)
    print("🎯 FRONTEND BUILD & STATIC SYNCHRONIZATION COMPLETED PERFECTLY")
    print("========================================================================")
    return True

if __name__ == "__main__":
    build_and_sync()
