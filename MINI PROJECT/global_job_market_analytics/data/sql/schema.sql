-- ============================================================
-- Global Job Market Analysis System — Database Schema
-- Engine: SQLite (dev) / PostgreSQL (production)
-- ============================================================

PRAGMA foreign_keys = ON;

-- Countries
CREATE TABLE IF NOT EXISTS countries (
    code         TEXT PRIMARY KEY,
    name         TEXT NOT NULL UNIQUE,
    region       TEXT NOT NULL,
    currency     TEXT NOT NULL,
    gdp_per_capita REAL,
    population   INTEGER,
    created_at   TEXT DEFAULT (datetime('now'))
);

-- Job Roles
CREATE TABLE IF NOT EXISTS job_roles (
    id               INTEGER PRIMARY KEY,
    title            TEXT NOT NULL UNIQUE,
    category         TEXT NOT NULL,
    experience_level TEXT,
    avg_years_exp    INTEGER,
    created_at       TEXT DEFAULT (datetime('now'))
);

-- Salary Data (current snapshot)
CREATE TABLE IF NOT EXISTS salary_data (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    country_code    TEXT NOT NULL REFERENCES countries(code),
    role_id         INTEGER NOT NULL REFERENCES job_roles(id),
    work_mode       TEXT NOT NULL CHECK(work_mode IN ('Onsite','Hybrid','Remote')),
    avg_salary_usd  REAL NOT NULL,
    min_salary_usd  REAL,
    max_salary_usd  REAL,
    avg_bonus_usd   REAL,
    created_at      TEXT DEFAULT (datetime('now')),
    UNIQUE(country_code, role_id, work_mode)
);

-- Salary Trends (year-wise)
CREATE TABLE IF NOT EXISTS salary_trends (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    country_code    TEXT NOT NULL REFERENCES countries(code),
    role_id         INTEGER NOT NULL REFERENCES job_roles(id),
    year            INTEGER NOT NULL,
    avg_salary_usd  REAL NOT NULL,
    q3_salary_usd   REAL,
    q1_salary_usd   REAL,
    UNIQUE(country_code, role_id, year)
);

-- Demand Trends (year-wise)
CREATE TABLE IF NOT EXISTS demand_trends (
    id                       INTEGER PRIMARY KEY AUTOINCREMENT,
    country_code             TEXT NOT NULL REFERENCES countries(code),
    role_id                  INTEGER NOT NULL REFERENCES job_roles(id),
    year                     INTEGER NOT NULL,
    demand_index             REAL NOT NULL,
    job_postings_thousands   REAL,
    remote_postings_thousands REAL,
    UNIQUE(country_code, role_id, year)
);

-- Skills per Role
CREATE TABLE IF NOT EXISTS skills (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    role_id     INTEGER NOT NULL REFERENCES job_roles(id),
    skill_name  TEXT NOT NULL,
    skill_type  TEXT NOT NULL CHECK(skill_type IN ('Technical','Soft')),
    percentage  REAL NOT NULL,
    UNIQUE(role_id, skill_name)
);

-- Job Postings (individual listings)
CREATE TABLE IF NOT EXISTS job_postings (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    company          TEXT,
    country_code     TEXT REFERENCES countries(code),
    role_id          INTEGER REFERENCES job_roles(id),
    work_mode        TEXT,
    salary_usd       REAL,
    experience_level TEXT,
    posted_date      TEXT,
    applicants       INTEGER,
    created_at       TEXT DEFAULT (datetime('now'))
);

-- Cost of Living
CREATE TABLE IF NOT EXISTS cost_of_living (
    country_code        TEXT PRIMARY KEY REFERENCES countries(code),
    col_index           REAL,
    avg_rent_usd        REAL,
    meal_cost_usd       REAL,
    transport_monthly_usd REAL,
    income_tax_rate     REAL
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_salary_country   ON salary_data(country_code);
CREATE INDEX IF NOT EXISTS idx_salary_role      ON salary_data(role_id);
CREATE INDEX IF NOT EXISTS idx_salary_mode      ON salary_data(work_mode);
CREATE INDEX IF NOT EXISTS idx_trend_year       ON salary_trends(year);
CREATE INDEX IF NOT EXISTS idx_demand_year      ON demand_trends(year);
CREATE INDEX IF NOT EXISTS idx_postings_date    ON job_postings(posted_date);
CREATE INDEX IF NOT EXISTS idx_postings_country ON job_postings(country_code);
