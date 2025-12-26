import sqlite3

try:
    conn = sqlite3.connect('store.db')
    c = conn.cursor()

    # Create table
    c.execute('''CREATE TABLE IF NOT EXISTS products
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  price REAL,
                  image TEXT,
                  description TEXT)''')
                  
    # Seed data
    products = [
        # Main Collection
        ('Premium Fit', 24999.00, 'prod1.jpg', 'Experience the pinnacle of tailoring with our Premium Fit suit. Crafted from the finest Italian wool.'),
        ('Classic Look', 9999.00, 'prod2.png', 'Timeless elegance meets modern durability. The Classic Look collection is designed for the man who values style.'),
        ('Urban Style', 14999.00, 'prod3.jpg', 'Redefine street sophistication. The Urban Style line blends high-fashion aesthetics with everyday wearability.'),
        
        # Accessories
        ('Luxury Watch', 19999.00, 'https://placehold.co/600x800/1a1a1a/d4af37?text=Luxury+Watch', 'Precision engineered chronograph with gold finish and sapphire crystal glass. A statement piece for any occasion.'),
        ('Signet Ring', 4999.00, 'https://placehold.co/600x800/1a1a1a/d4af37?text=Signet+Ring', 'Minimalist solid gold signet ring. Handcrafted to perfection, offering a subtle yet powerful touch to your ensemble.'),
        ('Leather Bracelet', 2999.00, 'https://placehold.co/600x800/1a1a1a/d4af37?text=Leather+Bracelet', 'Genuine braided leather bracelet with gold clasp. The perfect balance of rugged and refined.')
    ]

    # Clear and re-seed
    c.execute('DELETE FROM products')
    c.execute("DELETE FROM sqlite_sequence WHERE name='products'")

    c.executemany('INSERT INTO products (name, price, image, description) VALUES (?,?,?,?)', products)

    conn.commit()
    print("Database updated with Accessories.")
    
except Exception as e:
    print(f"Error seeding products: {e}")
finally:
    if conn:
        conn.close()
