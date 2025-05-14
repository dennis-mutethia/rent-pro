DROP TABLE IF EXISTS user_levels;
CREATE TABLE IF NOT EXISTS user_levels (
  id TEXT PRIMARY KEY,
  name TEXT,
  level INT DEFAULT '0',
  description TEXT,
  created_at TIMESTAMP,
  created_by TEXT,
  updated_at TIMESTAMP,
  updated_by TEXT,
  UNIQUE (name)
);

DROP TABLE IF EXISTS users;
CREATE TABLE IF NOT EXISTS users (
  id TEXT PRIMARY KEY,
  name TEXT,
  phone TEXT,
  building_id TEXT,
  user_level_id TEXT,
  password TEXT,
  created_at TIMESTAMP,
  created_by TEXT,
  updated_at TIMESTAMP,
  updated_by TEXT,
  UNIQUE (phone)
);