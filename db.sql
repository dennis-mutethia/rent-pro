DROP TABLE IF EXISTS packages;
CREATE TABLE IF NOT EXISTS packages (
  id TEXT PRIMARY KEY,
  name TEXT,
  amount DOUBLE PRECISION,
  pay DOUBLE PRECISION,
  description TEXT,
  offer TEXT,
  color TEXT,
  validity INT,
  created_at TIMESTAMP,
  created_by TEXT,
  updated_at TIMESTAMP,
  updated_by TEXT,
  UNIQUE (name)
);

DROP TABLE IF EXISTS licenses;
CREATE TABLE IF NOT EXISTS licenses (
  id TEXT PRIMARY KEY,
  key TEXT,
  package_id TEXT,
  expires_at TIMESTAMP,
  created_at TIMESTAMP,
  created_by TEXT,
  updated_at TIMESTAMP,
  updated_by TEXT,
  UNIQUE (key)
);

DROP TABLE IF EXISTS companies;
CREATE TABLE IF NOT EXISTS companies (
  id TEXT PRIMARY KEY,
  name TEXT,
  license_id TEXT,
  created_at TIMESTAMP,
  created_by TEXT,
  updated_at TIMESTAMP,
  updated_by TEXT
);

DROP TABLE IF EXISTS buildings;
CREATE TABLE IF NOT EXISTS buildings (
  id TEXT PRIMARY KEY,
  name TEXT,
  location TEXT,
  company_id TEXT,
  created_at TIMESTAMP,
  created_by TEXT,
  updated_at TIMESTAMP,
  updated_by TEXT,
  UNIQUE (name, company_id)
);

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