# Walkthrough: Free-Tier Firebase & Cloud Migration

I have successfully migrated the **Jyotish Dashboard** to support a cloud-native deployment on **Firebase Hosting** and **Google Cloud Run**, while strictly adhering to **Free Tier** limits. I also fixed several astrological calculation errors.

## 🚀 Key Accomplishments

### 1. Cloud-Native Storage (Firestore)
- **New Integration**: Created `firebase_store.py` to handle chart persistence using **Cloud Firestore**.
- **Hybrid Support**: Updated `store.py` to dynamically switch between **Local JSON** and **Cloud Firestore** based on the `USE_FIREBASE` environment variable.

### 2. Deployment Orchestration
- **Docker Optimization**: Updated the `Dockerfile` to be Cloud Run-compatible, using a slim base image and environment-aware port binding.
- **Firebase Hosting**: Created `firebase.json` to configure a global proxy that routes traffic to the Cloud Run backend, providing a free custom URL with SSL.

### 3. Astrological Precision Fixes
- **Rahu Kaal & Yamaghanta**: Corrected the weekday mapping logic in `calculator.py`. These inauspicious windows are now 100% accurate according to standard Vedic tables.

## 🛠️ Changes at a Glance

```diff
# requirements.txt
+ google-cloud-firestore>=2.16.0

# Dockerfile
- ENV PORT=5000
+ ENV PORT=8080
- CMD ["gunicorn", "--bind", "0.0.0.0:5000", ...]
+ CMD gunicorn --bind 0.0.0.0:$PORT ...

# calculator.py
- order = {0: 2, 1: 7, 2: 4, 3: 5, 4: 6, 5: 3, 6: 8}
+ order = {0: 2, 1: 7, 2: 5, 3: 6, 4: 4, 5: 3, 6: 8}
```

## 🧪 Verification Results

| Test Item | Status | Result |
| :--- | :--- | :--- |
| **Rahu Kaal (Mon)** | ✅ Passed | 07:30 AM – 09:00 AM (2nd part) |
| **Yamaghanta (Wed)** | ✅ Passed | 07:30 AM – 09:00 AM (2nd part) |
| **Firestore CRUD** | ✅ Passed | Charts save/list/delete correctly via SDK |
| **Docker Build** | ✅ Passed | Ephemeris bundled and dependencies installed |

## 🏁 Next Steps
To go live, follow the updated instructions in the [README.md](file:///G:/Astrology%20Prediction/README.md#cloud-deployment-firebase--cloud-run).
