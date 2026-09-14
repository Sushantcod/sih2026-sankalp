# Phase 9 — Multi-Label Stratified Dataset Audit Report

## 📊 Dataset Statistics
- **Total Source Images**: `10192`
- **Train Images**: `7134` (70.00%)
- **Validation Images**: `1529` (15.00%)
- **Test Images**: `1529` (15.00%)
- **Sum Verification**: `7,134 + 1,529 + 1,529 = 10,192` (`True`)
- **Cross-Split Duplicate Leakage**: `0`
- **Reproducibility Check (Seed 42)**: `PASS`

## 📋 Full 57-Class Distribution
| Class ID | Class Name | Total Instances | Train Instances (Images) | Val Instances (Images) | Test Instances (Images) | Note |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| 0 | `-Road narrows on right` | 267 | 187 (187) | 40 (40) | 40 (40) | OK |
| 1 | `50 mph speed limit` | 307 | 215 (215) | 46 (46) | 46 (46) | OK |
| 2 | `Advance Direction` | 3 | 2 (2) | 1 (1) | 0 (0) | Insufficient real samples for representation in all three splits. |
| 3 | `Attention Please-` | 590 | 413 (413) | 89 (89) | 88 (88) | OK |
| 4 | `Beware of children` | 535 | 374 (374) | 80 (80) | 81 (81) | OK |
| 5 | `Built Up Area` | 1 | 1 (1) | 0 (0) | 0 (0) | Insufficient real samples for representation in all three splits. |
| 6 | `Bullock and Hand Cart Prohibited` | 1 | 1 (1) | 0 (0) | 0 (0) | Insufficient real samples for representation in all three splits. |
| 7 | `Bus Stop` | 5 | 3 (3) | 1 (1) | 1 (1) | OK |
| 8 | `CYCLE ROUTE AHEAD WARNING` | 268 | 188 (188) | 40 (40) | 40 (40) | OK |
| 9 | `Cycle Prohibited` | 1 | 1 (1) | 0 (0) | 0 (0) | Insufficient real samples for representation in all three splits. |
| 10 | `Dangerous Left Curve Ahead` | 209 | 146 (146) | 31 (31) | 32 (32) | OK |
| 11 | `Dangerous Rright Curve Ahead` | 360 | 252 (252) | 54 (54) | 54 (54) | OK |
| 12 | `End of all speed and passing limits` | 239 | 167 (167) | 36 (36) | 36 (36) | OK |
| 13 | `Expressway Rout Marking` | 7 | 5 (5) | 1 (1) | 1 (1) | OK |
| 14 | `FS 31 Entry Ramp for Expressway` | 1 | 1 (1) | 0 (0) | 0 (0) | Insufficient real samples for representation in all three splits. |
| 15 | `Filling Station` | 15 | 10 (9) | 2 (2) | 3 (2) | OK |
| 16 | `Give Way` | 532 | 372 (372) | 80 (80) | 80 (80) | OK |
| 17 | `Go Straight or Turn Right` | 384 | 269 (269) | 57 (57) | 58 (58) | OK |
| 18 | `Go straight or turn left` | 208 | 146 (146) | 31 (31) | 31 (31) | OK |
| 19 | `Height Limit` | 4 | 3 (3) | 0 (0) | 1 (1) | Insufficient real samples for representation in all three splits. |
| 20 | `Keep-Left` | 300 | 210 (210) | 45 (45) | 45 (45) | OK |
| 21 | `Keep-Right` | 406 | 284 (284) | 61 (61) | 61 (61) | OK |
| 22 | `Left Hand Curv` | 5 | 3 (3) | 1 (1) | 1 (1) | OK |
| 23 | `Left Zig Zag Traffic` | 327 | 229 (229) | 49 (49) | 49 (49) | OK |
| 24 | `Narrow Bridge` | 2 | 1 (1) | 0 (0) | 1 (1) | Insufficient real samples for representation in all three splits. |
| 25 | `No Entry` | 415 | 290 (290) | 62 (62) | 63 (63) | OK |
| 26 | `No_Over_Taking` | 71 | 50 (50) | 10 (10) | 11 (11) | OK |
| 27 | `Object Hazard Right` | 1 | 1 (1) | 0 (0) | 0 (0) | Insufficient real samples for representation in all three splits. |
| 28 | `Overtaking by trucks is prohibited` | 238 | 167 (167) | 35 (35) | 36 (36) | OK |
| 29 | `Pedestrain Crossing` | 6 | 4 (4) | 1 (1) | 1 (1) | OK |
| 30 | `Pedestrian Crossing` | 237 | 166 (166) | 36 (36) | 35 (35) | OK |
| 31 | `Right Hand Curv` | 9 | 6 (6) | 1 (1) | 2 (2) | OK |
| 32 | `Round-About` | 359 | 251 (251) | 54 (54) | 54 (54) | OK |
| 33 | `STOP Sign` | 24 | 17 (17) | 4 (4) | 3 (3) | OK |
| 34 | `School Ahead` | 10 | 7 (6) | 2 (1) | 1 (1) | OK |
| 35 | `Side Road Right` | 9 | 6 (6) | 1 (1) | 2 (2) | OK |
| 36 | `Single Chevron` | 45 | 31 (22) | 5 (4) | 9 (5) | OK |
| 37 | `Slippery Road Ahead` | 504 | 353 (353) | 76 (76) | 75 (75) | OK |
| 38 | `Speed Limit 20 KMPh` | 209 | 146 (146) | 32 (32) | 31 (31) | OK |
| 39 | `Speed Limit 30 KMPh` | 889 | 622 (622) | 133 (133) | 134 (134) | OK |
| 40 | `Stack type Advance Direction sign` | 8 | 6 (6) | 1 (1) | 1 (1) | OK |
| 41 | `State Highway Route Marker` | 2 | 1 (1) | 1 (1) | 0 (0) | Insufficient real samples for representation in all three splits. |
| 42 | `Stop_Sign` | 153 | 107 (107) | 23 (23) | 23 (23) | OK |
| 43 | `Straight Ahead Only` | 327 | 229 (229) | 49 (49) | 49 (49) | OK |
| 44 | `Toilet` | 4 | 3 (3) | 1 (1) | 0 (0) | Insufficient real samples for representation in all three splits. |
| 45 | `Tractor Prohibited` | 1 | 1 (1) | 0 (0) | 0 (0) | Insufficient real samples for representation in all three splits. |
| 46 | `Traffic sign Not visibles` | 1 | 1 (1) | 0 (0) | 0 (0) | Insufficient real samples for representation in all three splits. |
| 47 | `Traffic_signal` | 58 | 41 (25) | 12 (6) | 5 (5) | OK |
| 48 | `Truck traffic is prohibited` | 418 | 293 (293) | 63 (63) | 62 (62) | OK |
| 49 | `Turn left ahead` | 417 | 292 (292) | 62 (62) | 63 (63) | OK |
| 50 | `Turn right ahead` | 406 | 284 (284) | 61 (61) | 61 (61) | OK |
| 51 | `Two Wheeler Prohibited` | 1 | 1 (1) | 0 (0) | 0 (0) | Insufficient real samples for representation in all three splits. |
| 52 | `Uneven Road` | 389 | 272 (272) | 59 (59) | 58 (58) | OK |
| 53 | `other` | 10 | 8 (5) | 1 (1) | 1 (1) | OK |
| 54 | `speed limit` | 41 | 29 (28) | 6 (6) | 6 (6) | OK |
| 55 | `speed limit 20` | 8 | 6 (6) | 1 (1) | 1 (1) | OK |
| 56 | `speed limit 80` | 7 | 5 (5) | 1 (1) | 1 (1) | OK |
