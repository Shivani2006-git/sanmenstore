import sqlite3

try:
    conn = sqlite3.connect('store.db')
    c = conn.cursor()
    # Check if exists first
    c.execute("SELECT * FROM users WHERE email='sangetha2017@gmail.com'")
    if c.fetchone():
        print("User already exists")
    else:
        c.execute("INSERT INTO users (email, password, name) VALUES ('sangetha2017@gmail.com', '123456', 'Sangetha')")
        conn.commit()
        print("User created successfully with password '123456'")
except Exception as e:
    print(f"Error: {e}")
finally:
    conn.close()
