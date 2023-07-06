CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) NOT NULL,
  email VARCHAR(50) NOT NULL UNIQUE,
  password VARCHAR(500) NOT NULL,
  city VARCHAR(50) NOT NULL,
  zipcode VARCHAR(50) NOT NULL
);

CREATE TABLE categories (
  id SERIAL PRIMARY KEY,
  category_name VARCHAR(1000) NOT NULL
);

CREATE TABLE user_interests (
  user_id INT NOT NULL,
  category_id INT NOT NULL,
  PRIMARY KEY (user_id, category_id),
  FOREIGN KEY (user_id) REFERENCES users (id),
  FOREIGN KEY (category_id) REFERENCES categories (id)
);

CREATE TABLE items (
  id SERIAL PRIMARY KEY,
  item_name VARCHAR(1000) NOT NULL,
  quantity INT NOT NULL,
  description VARCHAR(1000) NOT NULL,
  category_id INT NOT NULL,
  donor_id INT NOT NULL,
  img_url VARCHAR(1000),
  FOREIGN KEY (category_id) REFERENCES categories (id),
  FOREIGN KEY (donor_id) REFERENCES users (id)
);

CREATE TABLE donations (
  id SERIAL PRIMARY KEY,
  item_id INT NOT NULL,
  recipient_id INT NOT NULL,
  FOREIGN KEY (item_id) REFERENCES items (id),
  FOREIGN KEY (recipient_id) REFERENCES users (id)
);

-- Populate the users table
INSERT INTO users (name, email, password, city, zipcode)
VALUES
  ('John Doe', 'john@example.com', 'password1', 'New York', '10001'),
  ('Jane Smith', 'jane@example.com', 'password2', 'Los Angeles', '90001'),
  ('Jim Brown', 'jim@example.com', 'password3', 'Chicago', '60629'),
  ('Jill Johnson', 'jill@example.com', 'password4', 'Houston', '77036'),
  ('Joe Davis', 'joe@example.com', 'password5', 'Phoenix', '85032'),
  ('Jen Martinez', 'jen@example.com', 'password6', 'Philadelphia', '19120'),
  ('Jeff Taylor', 'jeff@example.com', 'password7', 'San Antonio', '78250'),
  ('Julie Anderson', 'julie@example.com', 'password8', 'San Diego', '92126'),
  ('Jeremy Thomas', 'jeremy@example.com', 'password9', 'Dallas', '75217'),
  ('Jessica Jackson', 'jessica@example.com', 'password10', 'San Jose', '95123');

-- Populate the categories table
INSERT INTO categories (category_name)
VALUES
  ('Books'),
  ('Electronics'),
  ('Furniture'),
  ('Toys'),
  ('Clothing'),
  ('Kitchen appliances'),
  ('Garden tools'),
  ('Sport equipment'),
  ('Musical instruments'),
  ('Art supplies');

-- Populate the user_interests table
INSERT INTO user_interests (user_id, category_id)
VALUES
  (1, 1),
  (1, 2),
  (2, 3),
  (2, 4),
  (3, 5),
  (3, 6),
  (4, 7),
  (4, 8),
  (5, 9),
  (5, 10),
  (6, 1),
  (7, 2),
  (8, 3),
  (9, 4),
  (10, 5);


-- Populate the items table
INSERT INTO items (item_name, quantity, description, category_id, donor_id, img_url)
VALUES
  ('Harry Potter Book', 1, 'First edition', 1, 1, 'https://source.unsplash.com/random/200x200?sig=1'),
  ('iPhone', 1, 'Brand new', 2, 2, 'https://source.unsplash.com/random/200x200?sig=2'),
  ('Couch', 1, 'Lightly used', 3, 3, 'https://source.unsplash.com/random/200x200?sig=3'),
  ('Lego Set', 1, 'Complete', 4, 4, 'https://source.unsplash.com/random/200x200?sig=4'),
  ('Jacket', 1, 'New', 5, 5, 'https://source.unsplash.com/random/200x200?sig=5'),
  ('Blender', 1, 'Never used', 6, 6, 'https://source.unsplash.com/random/200x200?sig=6'),
  ('Lawn Mower', 1, 'Used', 7, 7, 'https://source.unsplash.com/random/200x200?sig=7'),
  ('Bicycle', 1, 'Good condition', 8, 8, 'https://source.unsplash.com/random/200x200?sig=8'),
  ('Guitar', 1, 'Almost new', 9, 9, 'https://source.unsplash.com/random/200x200?sig=9'),
  ('Paint brushes', 1, 'Never used', 10, 10, 'https://source.unsplash.com/random/200x200?sig=10');


-- Populate the donations table
INSERT INTO donations (item_id, recipient_id)
VALUES
  (1, 10),
  (2, 9),
  (3, 8),
  (4, 7),
  (5, 6),
