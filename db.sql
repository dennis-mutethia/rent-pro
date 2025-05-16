
DROP TABLE IF EXISTS companies;
CREATE TABLE IF NOT EXISTS companies (
  id TEXT PRIMARY KEY,
  name TEXT,
  phone TEXT,
  created_at TIMESTAMP,
  created_by TEXT,
  updated_at TIMESTAMP,
  updated_by TEXT,
  UNIQUE (name, phone)
);

DROP TABLE IF EXISTS landlords;
CREATE TABLE IF NOT EXISTS landlords (
  id TEXT PRIMARY KEY,
  company_id TEXT,
  name TEXT,
  phone TEXT,
  created_at TIMESTAMP,
  created_by TEXT,
  updated_at TIMESTAMP,
  updated_by TEXT,
  UNIQUE (company_id, phone)
);

DROP TABLE IF EXISTS properties;
CREATE TABLE IF NOT EXISTS properties (
  id TEXT PRIMARY KEY,
  landlord_id TEXT,
  name TEXT,
  location TEXT,
  town TEXT,
  county TEXT,
  lr_no TEXT,
  image TEXT,
  created_at TIMESTAMP,
  created_by TEXT,
  updated_at TIMESTAMP,
  updated_by TEXT,
  UNIQUE (landlord_id, name)
);

DROP TABLE IF EXISTS house_types;
CREATE TABLE IF NOT EXISTS house_types (
  id TEXT PRIMARY KEY,
  company_id TEXT,
  name TEXT,
  description TEXT,
  created_at TIMESTAMP,
  created_by TEXT,
  updated_at TIMESTAMP,
  updated_by TEXT,
  UNIQUE (name, company_id)
);

DROP TABLE IF EXISTS houses;
CREATE TABLE IF NOT EXISTS houses (
  id TEXT PRIMARY KEY,
  property_id TEXT,
  house_type_id TEXT,
  name TEXT,
  rent_amount REAL DEFAULT '0',
  deposit_amount REAL DEFAULT '0',  
  created_at TIMESTAMP,
  created_by TEXT,
  updated_at TIMESTAMP,
  updated_by TEXT,
  UNIQUE (property_id, name)
);

DROP TABLE IF EXISTS tenants;
CREATE TABLE IF NOT EXISTS tenants (
  id TEXT PRIMARY KEY,
  name TEXT,
  phone TEXT,
  email TEXT,
  id_number TEXT,
  image TEXT,
  next_of_kin TEXT,
  next_of_kin_phone TEXT,
  created_at TIMESTAMP,
  created_by TEXT,
  updated_at TIMESTAMP,
  updated_by TEXT,
  UNIQUE (id_number)
);

DROP TABLE IF EXISTS tenant_houses;
CREATE TABLE IF NOT EXISTS tenant_houses (
  id TEXT PRIMARY KEY,
  tenant_id TEXT,
  house_id TEXT,
  start_date TIMESTAMP,
  end_date TIMESTAMP,
  created_at TIMESTAMP,
  created_by TEXT,
  updated_at TIMESTAMP,
  updated_by TEXT
);

DROP TABLE IF EXISTS bill_types;
CREATE TABLE IF NOT EXISTS bill_types (
  id TEXT PRIMARY KEY,
  name TEXT,
  description TEXT,
  created_at TIMESTAMP,
  created_by TEXT,
  updated_at TIMESTAMP,
  updated_by TEXT,
  UNIQUE (name)
);

DROP TABLE IF EXISTS tenant_bills;
CREATE TABLE IF NOT EXISTS tenant_bills (
  id TEXT PRIMARY KEY,
  tenant_house_id TEXT,
  bill_type TEXT,
  amount REAL DEFAULT '0',
  bill_date TIMESTAMP,
  due_date TIMESTAMP,
  created_at TIMESTAMP,
  created_by TEXT,
  updated_at TIMESTAMP,
  updated_by TEXT
);

DROP TABLE IF EXISTS payment_methods;
CREATE TABLE IF NOT EXISTS payment_methods (
  id TEXT PRIMARY KEY,
  name TEXT,
  description TEXT,
  created_at TIMESTAMP,
  created_by TEXT,
  updated_at TIMESTAMP,
  updated_by TEXT,
  UNIQUE (name)
);

DROP TABLE IF EXISTS tenant_payments;
CREATE TABLE IF NOT EXISTS tenant_payments (
  id TEXT PRIMARY KEY,
  tenant_house_id TEXT,
  amount REAL DEFAULT '0',
  payment_date TIMESTAMP,
  payment_method TEXT,
  created_at TIMESTAMP,
  created_by TEXT,
  updated_at TIMESTAMP,
  updated_by TEXT
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
  password TEXT,
  user_level_id TEXT,
  property_id TEXT,
  landlord_id TEXT,
  company_id TEXT,
  created_at TIMESTAMP,
  created_by TEXT,
  updated_at TIMESTAMP,
  updated_by TEXT,
  UNIQUE (phone)
);