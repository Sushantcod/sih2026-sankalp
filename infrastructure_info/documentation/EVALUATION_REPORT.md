# Phase 9 — Final Model Evaluation & Benchmark Report

## 🎯 Overall Held-out Test Metrics (1,529 Test Images)
- **Precision**: `0.7966`
- **Recall**: `0.6791`
- **mAP@50**: `0.6925`
- **mAP@50-95**: `0.5628`

## 📋 Full 57-Class Per-Class Benchmark
| Class ID | Class Name | Test Instances | Precision | Recall | mAP50 | mAP50-95 | Status |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| 0 | `-Road narrows on right` | 40 | 0.9934 | 1.0 | 0.995 | 0.879 | Evaluated |
| 1 | `50 mph speed limit` | 46 | 0.9779 | 0.9602 | 0.9923 | 0.7831 | Evaluated |
| 2 | `Advance Direction` | 0 | N/A | N/A | N/A | N/A | No test instances — unevaluable |
| 3 | `Attention Please-` | 88 | 1.0 | 0.9883 | 0.995 | 0.84 | Evaluated |
| 4 | `Beware of children` | 81 | 0.997 | 1.0 | 0.995 | 0.8805 | Evaluated |
| 5 | `Built Up Area` | 0 | N/A | N/A | N/A | N/A | No test instances — unevaluable |
| 6 | `Bullock and Hand Cart Prohibited` | 0 | N/A | N/A | N/A | N/A | No test instances — unevaluable |
| 7 | `Bus Stop` | 1 | 1.0 | 0.0 | 0.1421 | 0.0853 | Evaluated |
| 8 | `CYCLE ROUTE AHEAD WARNING` | 40 | 0.993 | 1.0 | 0.995 | 0.8504 | Evaluated |
| 9 | `Cycle Prohibited` | 0 | N/A | N/A | N/A | N/A | No test instances — unevaluable |
| 10 | `Dangerous Left Curve Ahead` | 32 | 1.0 | 0.9805 | 0.995 | 0.8444 | Evaluated |
| 11 | `Dangerous Rright Curve Ahead` | 54 | 0.976 | 1.0 | 0.995 | 0.8347 | Evaluated |
| 12 | `End of all speed and passing limits` | 36 | 0.9948 | 1.0 | 0.995 | 0.8145 | Evaluated |
| 13 | `Expressway Rout Marking` | 1 | 0.0 | 0.0 | 0.0 | 0.0 | Evaluated |
| 14 | `FS 31 Entry Ramp for Expressway` | 0 | N/A | N/A | N/A | N/A | No test instances — unevaluable |
| 15 | `Filling Station` | 3 | 0.0 | 0.0 | 0.0829 | 0.0415 | Evaluated |
| 16 | `Give Way` | 80 | 0.9978 | 1.0 | 0.995 | 0.8097 | Evaluated |
| 17 | `Go Straight or Turn Right` | 58 | 0.9965 | 1.0 | 0.995 | 0.8488 | Evaluated |
| 18 | `Go straight or turn left` | 31 | 0.993 | 1.0 | 0.995 | 0.875 | Evaluated |
| 19 | `Height Limit` | 1 | 1.0 | 0.0 | 0.0398 | 0.0199 | Evaluated |
| 20 | `Keep-Left` | 45 | 0.9821 | 1.0 | 0.995 | 0.875 | Evaluated |
| 21 | `Keep-Right` | 61 | 1.0 | 0.9911 | 0.995 | 0.803 | Evaluated |
| 22 | `Left Hand Curv` | 1 | 1.0 | 0.0 | 0.1106 | 0.0221 | Evaluated |
| 23 | `Left Zig Zag Traffic` | 49 | 0.9982 | 1.0 | 0.995 | 0.8483 | Evaluated |
| 24 | `Narrow Bridge` | 1 | 0.0 | 0.0 | 0.0 | 0.0 | Evaluated |
| 25 | `No Entry` | 63 | 0.9971 | 1.0 | 0.995 | 0.7936 | Evaluated |
| 26 | `No_Over_Taking` | 11 | 0.9773 | 1.0 | 0.995 | 0.8729 | Evaluated |
| 27 | `Object Hazard Right` | 0 | N/A | N/A | N/A | N/A | No test instances — unevaluable |
| 28 | `Overtaking by trucks is prohibited` | 36 | 0.9942 | 1.0 | 0.995 | 0.7958 | Evaluated |
| 29 | `Pedestrain Crossing` | 1 | 0.0 | 0.0 | 0.0524 | 0.0262 | Evaluated |
| 30 | `Pedestrian Crossing` | 35 | 0.9891 | 1.0 | 0.995 | 0.847 | Evaluated |
| 31 | `Right Hand Curv` | 2 | 1.0 | 0.0 | 0.2487 | 0.1492 | Evaluated |
| 32 | `Round-About` | 54 | 0.9962 | 1.0 | 0.995 | 0.8762 | Evaluated |
| 33 | `STOP Sign` | 3 | 0.2984 | 1.0 | 0.83 | 0.3765 | Evaluated |
| 34 | `School Ahead` | 1 | 1.0 | 0.0 | 0.4975 | 0.4477 | Evaluated |
| 35 | `Side Road Right` | 2 | 0.0 | 0.0 | 0.1138 | 0.0243 | Evaluated |
| 36 | `Single Chevron` | 9 | 0.272 | 0.2222 | 0.164 | 0.085 | Evaluated |
| 37 | `Slippery Road Ahead` | 75 | 0.9969 | 1.0 | 0.995 | 0.8926 | Evaluated |
| 38 | `Speed Limit 20 KMPh` | 31 | 1.0 | 0.988 | 0.995 | 0.8464 | Evaluated |
| 39 | `Speed Limit 30 KMPh` | 134 | 0.9843 | 0.9851 | 0.9944 | 0.8408 | Evaluated |
| 40 | `Stack type Advance Direction sign` | 1 | 0.1974 | 1.0 | 0.199 | 0.0574 | Evaluated |
| 41 | `State Highway Route Marker` | 0 | N/A | N/A | N/A | N/A | No test instances — unevaluable |
| 42 | `Stop_Sign` | 23 | 0.9878 | 1.0 | 0.995 | 0.8597 | Evaluated |
| 43 | `Straight Ahead Only` | 49 | 0.9951 | 1.0 | 0.995 | 0.823 | Evaluated |
| 44 | `Toilet` | 0 | N/A | N/A | N/A | N/A | No test instances — unevaluable |
| 45 | `Tractor Prohibited` | 0 | N/A | N/A | N/A | N/A | No test instances — unevaluable |
| 46 | `Traffic sign Not visibles` | 0 | N/A | N/A | N/A | N/A | No test instances — unevaluable |
| 47 | `Traffic_signal` | 5 | 0.3389 | 0.8 | 0.6753 | 0.4032 | Evaluated |
| 48 | `Truck traffic is prohibited` | 62 | 0.9963 | 1.0 | 0.995 | 0.8496 | Evaluated |
| 49 | `Turn left ahead` | 63 | 0.9765 | 1.0 | 0.995 | 0.8322 | Evaluated |
| 50 | `Turn right ahead` | 61 | 1.0 | 0.989 | 0.995 | 0.8555 | Evaluated |
| 51 | `Two Wheeler Prohibited` | 0 | N/A | N/A | N/A | N/A | No test instances — unevaluable |
| 52 | `Uneven Road` | 58 | 0.995 | 1.0 | 0.995 | 0.8716 | Evaluated |
| 53 | `other` | 1 | 0.0 | 0.0 | 0.0 | 0.0 | Evaluated |
| 54 | `speed limit` | 6 | 0.7515 | 0.3333 | 0.4092 | 0.2475 | Evaluated |
| 55 | `speed limit 20` | 1 | 1.0 | 0.0 | 0.3317 | 0.199 | Evaluated |
| 56 | `speed limit 80` | 1 | 1.0 | 0.0 | 0.0995 | 0.0597 | Evaluated |
