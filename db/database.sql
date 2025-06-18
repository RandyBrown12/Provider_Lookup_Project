CREATE TABLE IF NOT EXISTS medical_providers (
    id SERIAL PRIMARY KEY,
    npi NUMERIC(10, 0) UNIQUE NOT NULL,
    phone_number VARCHAR(64),
    first_name VARCHAR(64),
    last_name VARCHAR(64),
    mailing_street VARCHAR(224),
    mailing_city VARCHAR(64),
    mailing_state VARCHAR(64),
    mailing_zip_code VARCHAR(25)
);


CREATE TABLE IF NOT EXISTS taxonomies (
    id SERIAL PRIMARY KEY,
    taxonomy_code VARCHAR(10) UNIQUE NOT NULL,
    taxonomy_specialization VARCHAR(255)
);


CREATE TABLE IF NOT EXISTS npi_to_taxonomies (
    id SERIAL PRIMARY KEY,
    npi NUMERIC(10, 0) NOT NULL,
    taxonomy_code VARCHAR(10) NOT NULL,
    CONSTRAINT unique_npi_taxonomy UNIQUE (npi, taxonomy_code),
    FOREIGN KEY (npi) REFERENCES medical_providers(npi) ON DELETE CASCADE,
    FOREIGN KEY (taxonomy_code) REFERENCES taxonomies(taxonomy_code) ON DELETE CASCADE
);
