-- Table structure for transactions
CREATE TABLE IF NOT EXISTS transactions (
  id TEXT PRIMARY KEY,
  subscriber_id TEXT,
  amount INT DEFAULT 0,
  payment_method TEXT,
  payment_account TEXT,
  confirmation_code TEXT,
  status BOOLEAN DEFAULT FALSE,
  created_by TEXT,
  created_at TIMESTAMP,
  updated_by TEXT,
  updated_at TIMESTAMP
);
