import sqlite3
import json
import os
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent / "imu_cet.db"
JSON_DIR = Path(__file__).parent / "data" / "json"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    JSON_DIR.mkdir(parents=True, exist_ok=True)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        id TEXT PRIMARY KEY,
        year INTEGER NOT NULL,
        shift TEXT,
        section TEXT NOT NULL,
        question_number INTEGER,
        question_text TEXT NOT NULL,
        option_a TEXT,
        option_b TEXT,
        option_c TEXT,
        option_d TEXT,
        correct_option TEXT,
        explanation TEXT,
        topic TEXT,
        difficulty TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)
    cursor.execute("PRAGMA table_info(questions)")
    existing_cols = [c[1] for c in cursor.fetchall()]
    if "shift" not in existing_cols:
        cursor.execute("ALTER TABLE questions ADD COLUMN shift TEXT")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_year_section ON questions(year, section)")
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

def add_question(year, section, question_text, option_a=None, option_b=None, 
                 option_c=None, option_d=None, correct_option=None, 
                 explanation=None, topic=None, difficulty=None, question_number=None, q_id=None, shift=None):
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    
    # Auto determine question number if not provided
    if question_number is None:
        if shift:
            cursor.execute("SELECT COUNT(*) FROM questions WHERE year = ? AND shift = ? AND LOWER(section) = LOWER(?)", (year, shift, section))
        else:
            cursor.execute("SELECT COUNT(*) FROM questions WHERE year = ? AND LOWER(section) = LOWER(?)", (year, section))
        question_number = cursor.fetchone()[0] + 1
        
    # Auto determine ID if not provided
    if not q_id:
        clean_section = "".join(c for c in section if c.isalnum()).upper()[:4]
        shift_tag = f"_{shift.replace(' ', '').upper()}" if shift else ""
        q_id = f"IMU_{year}{shift_tag}_{clean_section}_{question_number:03d}"
        
    created_at = datetime.utcnow().isoformat()
    
    cursor.execute("""
    INSERT OR REPLACE INTO questions (
        id, year, shift, section, question_number, question_text,
        option_a, option_b, option_c, option_d,
        correct_option, explanation, topic, difficulty, created_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        q_id, year, shift, section, question_number, question_text,
        option_a, option_b, option_c, option_d,
        correct_option, explanation, topic, difficulty, created_at
    ))
    conn.commit()
    conn.close()
    
    # Auto sync to JSON
    export_to_json(year, shift)
    return q_id

def export_to_json(year=None, shift=None):
    conn = get_connection()
    cursor = conn.cursor()
    if year:
        cursor.execute("SELECT * FROM questions WHERE year = ? ORDER BY COALESCE(shift, ''), section, question_number", (year,))
        rows = [dict(r) for r in cursor.fetchall()]
        out_file = JSON_DIR / f"imu_cet_{year}.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(rows, f, indent=2, ensure_ascii=False)
            
        # If shift is specified, also export shift-specific file
        if shift:
            shift_slug = "".join(c for c in shift if c.isalnum()).lower()
            shift_file = JSON_DIR / f"imu_cet_{year}_{shift_slug}.json"
            cursor.execute("SELECT * FROM questions WHERE year = ? AND shift = ? ORDER BY section, question_number", (year, shift))
            shift_rows = [dict(r) for r in cursor.fetchall()]
            with open(shift_file, "w", encoding="utf-8") as f:
                json.dump(shift_rows, f, indent=2, ensure_ascii=False)
    
    cursor.execute("SELECT * FROM questions ORDER BY year DESC, COALESCE(shift, ''), section, question_number")
    all_rows = [dict(r) for r in cursor.fetchall()]
    with open(JSON_DIR / "imu_cet_all.json", "w", encoding="utf-8") as f:
        json.dump(all_rows, f, indent=2, ensure_ascii=False)
        
    conn.close()
    export_to_csv(year, shift)

def export_to_csv(year=None, shift=None):
    import csv
    csv_dir = Path(__file__).parent / "data" / "csv"
    csv_dir.mkdir(parents=True, exist_ok=True)
    
    conn = get_connection()
    cursor = conn.cursor()
    
    headers = [
        "id", "year", "shift", "section", "question_number", "question_text",
        "option_a", "option_b", "option_c", "option_d",
        "correct_option", "explanation", "topic", "difficulty", "created_at"
    ]
    
    if year:
        cursor.execute("SELECT * FROM questions WHERE year = ? ORDER BY COALESCE(shift, ''), section, question_number", (year,))
        rows = cursor.fetchall()
        out_file = csv_dir / f"imu_cet_{year}.csv"
        with open(out_file, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for r in rows:
                writer.writerow([r[h] for h in headers])
                
        if shift:
            shift_slug = "".join(c for c in shift if c.isalnum()).lower()
            shift_file = csv_dir / f"imu_cet_{year}_{shift_slug}.csv"
            cursor.execute("SELECT * FROM questions WHERE year = ? AND shift = ? ORDER BY section, question_number", (year, shift))
            shift_rows = cursor.fetchall()
            with open(shift_file, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                for r in shift_rows:
                    writer.writerow([r[h] for h in headers])
                
    cursor.execute("SELECT * FROM questions ORDER BY year DESC, COALESCE(shift, ''), section, question_number")
    all_rows = cursor.fetchall()
    with open(csv_dir / "imu_cet_all.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for r in all_rows:
            writer.writerow([r[h] for h in headers])
            
    conn.close()

def get_stats():
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT year, COALESCE(shift, '-') as shift, section, COUNT(*) as count 
    FROM questions 
    GROUP BY year, shift, section 
    ORDER BY year DESC, shift, section
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

if __name__ == "__main__":
    init_db()
    print("Database manager ready.")
