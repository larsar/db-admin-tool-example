CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public; -- To generate UUIDs
CREATE SCHEMA sec; -- To prevent mixing everything into one big pile called 'public'

CREATE TABLE sec.repos (
  id      UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name    TEXT NOT NULL UNIQUE,
  git_url TEXT UNIQUE
);