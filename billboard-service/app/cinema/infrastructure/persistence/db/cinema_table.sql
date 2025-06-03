CREATE TABLE cinemas (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    email_contact VARCHAR(255) NOT NULL,
    tax_number VARCHAR(20) NOT NULL UNIQUE,
    is_active BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE index idx_cinemas_name_id on cinemas(id);
CREATE index idx_cinemas_name_name on cinemas(name);
CREATE index idx_cinemas_name_email on cinemas(email_contact);


CREATE OR REPLACE FUNCTION update_updated_at_column() 
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_cinemas_updated_at
BEFORE UPDATE ON cinemas
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();


INSERT INTO cinemas (name, email_contact, tax_number, is_active) VALUES
('Cinépolis Plaza Carso', 'atencionclientes@cinepolis.com', 'CINEP001CARSO', TRUE),
('Cinépolis Forum Buenavista', 'atencionclientes@cinepolis.com', 'CINEP002BUENA', TRUE),
('Cinépolis Perisur', 'atencionclientes@cinepolis.com', 'CINEP003PERI', TRUE),
('Cinépolis Diana', 'atencionclientes@cinepolis.com', 'CINEP004DIANA', TRUE),
('Cinépolis Universidad', 'atencionclientes@cinepolis.com', 'CINEP005UNIV', TRUE),
('Cinépolis Satélite', 'atencionclientes@cinepolis.com', 'CINEP006SAT', TRUE),
('Cinépolis Santa Fe', 'atencionclientes@cinepolis.com', 'CINEP007SANTAFE', TRUE),
('Cinépolis Patio Universidad', 'atencionclientes@cinepolis.com', 'CINEP008PATIO', TRUE),
('Cinépolis Parque Delta', 'atencionclientes@cinepolis.com', 'CINEP009DELTA', TRUE),
('Cinépolis Coapa', 'atencionclientes@cinepolis.com', 'CINEP010COAPA', TRUE);