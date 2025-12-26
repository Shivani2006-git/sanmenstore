import sqlite3
import os

db_file = 'store.db'

if not os.path.exists(db_file):
    print(f"Error: {db_file} not found. Run start_server.bat first!")
else:
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        
        print(f"\nConnected to {db_file}")
        print("-" * 30)
        
        print("USERS TABLE:")
        print(f"{'ID':<5} {'Name':<20} {'Email':<30}")
        print("-" * 60)
        
        cursor = c.execute("SELECT id, name, email FROM users")
        rows = cursor.fetchall()
        
        if not rows:
            print("(No users found)")
        else:
            for row in rows:
                # Handle potential None values safely
                uid = str(row[0])
                name = str(row[1]) if row[1] else "Unknown"
                email = str(row[2]) if row[2] else "No Email"
                print(f"{uid:<5} {name:<20} {email:<30}")
                
        conn.close()
    except Exception as e:
        print(f"Error reading database: {e}")

print("\n" + "-" * 30)
input("Press Enter to close...")
