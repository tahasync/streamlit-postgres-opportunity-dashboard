CREATE TABLE IF NOT EXISTS opportunities (
    opportunity_id SERIAL PRIMARY KEY,
    company_name   VARCHAR(100)  NOT NULL,
    job_title      VARCHAR(150)  NOT NULL,
    category       VARCHAR(50)   NOT NULL,
    city           VARCHAR(80),
    country        VARCHAR(80),
    work_mode      VARCHAR(30)   CHECK (work_mode IN ('Remote', 'Onsite', 'Hybrid')),
    required_skills TEXT         NOT NULL,
    salary_min     NUMERIC(10,2),
    salary_max     NUMERIC(10,2),
    currency       VARCHAR(10)   DEFAULT 'PKR',
    experience_level VARCHAR(50),
    application_deadline DATE,
    status         VARCHAR(30)   DEFAULT 'Open'
                               CHECK (status IN ('Open', 'Closed', 'Expired', 'Shortlisted')),
    source_link    TEXT,
    created_at     TIMESTAMP     DEFAULT CURRENT_TIMESTAMP
);
