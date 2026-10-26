CREATE TABLE IF NOT EXISTS orders(id integer PRIMARY KEY, item text NOT NULL);
INSERT INTO orders VALUES (1,'book'),(2,'keyboard') ON CONFLICT DO NOTHING;
