import sqlite3

def cleanup():
    conn = sqlite3.connect('D:/ASTROLOGYPREDICTIONS/data/app.db')
    c = conn.cursor()
    # Delete non-showcase test profiles that aren't the user's
    c.execute("DELETE FROM charts WHERE id='78e009b2'")
    c.execute("DELETE FROM charts WHERE id='test-v317'")
    c.execute("DELETE FROM charts WHERE id='test-v318'")

    # Keep only the latest Subramanian profile
    c.execute("SELECT id FROM charts WHERE name='Subramanian T S' ORDER BY saved_at DESC")
    rows = c.fetchall()
    if len(rows) > 1:
        for r in rows[1:]:
            c.execute("DELETE FROM charts WHERE id=?", (r[0],))

    conn.commit()
    conn.close()
    print("Cleanup complete.")

if __name__ == "__main__":
    cleanup()
