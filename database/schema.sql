-- ========================================
-- SISTEMA IMOBILIÁRIO IA - SCHEMA COMPLETO
-- ========================================

-- ======================
-- TABELA: TENANTS
-- ======================
CREATE TABLE IF NOT EXISTS tenants (
    id SERIAL PRIMARY KEY,
    company_name VARCHAR(100) NOT NULL,
    cnpj VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ======================
-- TABELA: USERS
-- ======================
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL,
    tenant_id INT NOT NULL,
    
    -- LGPD
    lgpd_consent BOOLEAN NOT NULL DEFAULT false,
    terms_version VARCHAR(20),
    consent_timestamp TIMESTAMP,

    -- Segurança
    refresh_token TEXT,
    last_login TIMESTAMP,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (tenant_id) REFERENCES tenants(id)
);

-- ======================
-- TABELA: PROPERTIES
-- ======================
CREATE TABLE IF NOT EXISTS properties (
    id SERIAL PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    description TEXT,
    price NUMERIC(12,2),
    address VARCHAR(200),
    city VARCHAR(100),
    status VARCHAR(50),
    tenant_id INT NOT NULL,

    -- Novos campos
    has_pet_friendly BOOLEAN DEFAULT false,
    condo_fee NUMERIC(12,2),
    total_floors INT,
    construction_year INT,
    living_rooms INT,
    kitchens INT,
    leisure_areas INT,
    balconies INT,
    accepts_swap BOOLEAN DEFAULT false,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (tenant_id) REFERENCES tenants(id)
);

-- ======================
-- TABELA: LEADS
-- ======================
CREATE TABLE IF NOT EXISTS leads (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(100),

    interest_property_id INT,
    tenant_id INT NOT NULL,

    -- LGPD
    lgpd_consent BOOLEAN NOT NULL DEFAULT false,
    terms_version VARCHAR(20),
    consent_timestamp TIMESTAMP,

    -- IA e tipo de lead
    lead_type VARCHAR(20),
    ai_summary_query TEXT,
    searched_at TIMESTAMP,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (interest_property_id) REFERENCES properties(id),
    FOREIGN KEY (tenant_id) REFERENCES tenants(id)
);

-- ======================
-- TABELA: VERIFICATION CODES
-- ======================
CREATE TABLE IF NOT EXISTS verification_codes (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    code VARCHAR(20) NOT NULL,
    type VARCHAR(50) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- ======================
-- TABELA: PROPERTY SWAPS
-- ======================
CREATE TABLE IF NOT EXISTS property_swaps (
    id SERIAL PRIMARY KEY,
    property_id_1 INT NOT NULL,
    property_id_2 INT NOT NULL,
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (property_id_1) REFERENCES properties(id),
    FOREIGN KEY (property_id_2) REFERENCES properties(id)
);
