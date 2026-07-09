CREATE TABLE companies
(
    id         SERIAL PRIMARY KEY,
    name       TEXT NOT NULL UNIQUE,
    website    TEXT,
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE applications
(
    id           SERIAL PRIMARY KEY,
    company_id   INTEGER NOT NULL REFERENCES companies (id) ON DELETE CASCADE,
    position     TEXT    NOT NULL,
    status       TEXT    NOT NULL DEFAULT 'applied'
        CHECK (status IN ('applied', 'screening', 'interview', 'offer', 'rejected')),
    applied_date DATE    NOT NULL DEFAULT CURRENT_DATE,
    notes        TEXT
);

CREATE TABLE audit_log
(
    id             SERIAL PRIMARY KEY,
    application_id INTEGER REFERENCES applications (id) ON DELETE SET NULL,
    action         TEXT    NOT NULL,
    old_status     TEXT,
    new_status     TEXT,
    created_at     TIMESTAMP DEFAULT now()
);