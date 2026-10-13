# 🚢 IMU CET Question Bank Database

Structured repository of previous year IMU CET (Indian Maritime University Common Entrance Test) examination papers.

---

## 📊 Database Status

### 🏆 IMU CET 2024 — Complete Paper (200 / 200 Questions) ✅

| Section | Subject / Area | Questions | Q. Numbers | ID Format | Status |
| :---: | :--- | :---: | :---: | :--- | :---: |
| **Section 1** | **English Language & Vocabulary** | **40** | Q01 – Q40 | `IMU_2024_ENG_001` – `040` | ✅ Complete |
| **Section 2** | **General Aptitude, Reasoning & GK** | **40** | Q41 – Q80 | `IMU_2024_GA_041` – `080` | ✅ Complete |
| **Section 3** | **Mathematics** | **50** | Q81 – Q130 | `IMU_2024_MATH_081` – `130` | ✅ Complete |
| **Section 4** | **Physics** | **50** | Q131 – Q180 | `IMU_2024_PHY_131` – `180` | ✅ Complete |
| **Section 5** | **Chemistry** | **20** | Q181 – Q200 | `IMU_2024_CHEM_181` – `200` | ✅ Complete |
| **Total** | **Full 2024 Paper** | **200** | **Q01 – Q200** | | 🚀 **100% Synced** |

---

## 📁 Storage Formats & Files

1. **SQLite Database**: `imu_cet.db`
   - Indexed on `(year, section)` for sub-millisecond retrieval.
2. **JSON Data**:
   - `data/json/imu_cet_2024.json`: Complete 2024 paper (200 questions).
   - `data/json/imu_cet_all.json`: Master question bank across all years.
3. **Excel / CSV Data**:
   - `data/csv/imu_cet_2024.csv`: Spreadsheet format with UTF-8 BOM encoding for direct opening in Excel or Google Sheets.
   - `data/csv/imu_cet_all.csv`: Master CSV file.

---

## 🛠️ Schema Details

Each question is structured with:
- `id`: Unique identifier (e.g., `IMU_2024_MATH_085`)
- `year`: Exam year (e.g., 2024)
- `section`: Section name (English, General Aptitude, Mathematics, Physics, Chemistry)
- `question_number`: Sequential question number in paper (1 to 200)
- `question_text`: Complete problem statement with LaTeX / formula formatting
- `option_a`, `option_b`, `option_c`, `option_d`: Multiple choice options
- `correct_option`: Correct key (`A`, `B`, `C`, or `D`)
- `explanation`: In-depth step-by-step solution / scientific reason
- `topic`: Specific topic / syllabus classification
- `difficulty`: Easy / Medium / Hard
