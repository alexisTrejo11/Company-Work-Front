DO $$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'theater_type_enum') THEN
        CREATE TYPE theater_type_enum AS ENUM ('2D', '3D', 'IMAX', '4DX', 'V');
    END IF;
END $$;

CREATE TABLE theaters (
    id SERIAL PRIMARY KEY,
    cinema_id INT NOT NULL,
    name VARCHAR(50) NOT NULL,
    capacity INT NOT NULL CHECK (capacity > 0),
    theater_type theater_type_enum NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    maintenance_mode BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_cinema FOREIGN KEY (cinema_id) REFERENCES cinemas (id) ON DELETE CASCADE
);

CREATE INDEX idx_theaters_cinema_id ON theaters (cinema_id);
CREATE INDEX idx_theaters_type ON theaters (theater_type);
CREATE INDEX idx_theaters_active_cinema_type ON theaters (cinema_id, theater_type, is_active);

CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_theaters_updated_at
BEFORE UPDATE ON theaters
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();

INSERT INTO theaters (cinema_id, name, capacity, theater_type, is_active, maintenance_mode)
VALUES
(1, 'Sala 1 - Principal', 250, '2D', TRUE, FALSE),
(1, 'Sala 2 - 3D', 180, '3D', TRUE, FALSE),
(2, 'Sala 3 - IMAX', 300, 'IMAX', TRUE, FALSE),
(2, 'Sala 4 - VIP', 50, 'V', TRUE, FALSE),
(3, 'Sala 5 - 4DX', 100, '4DX', TRUE, FALSE),
(3, 'Sala 6 - Estándar', 200, '2D', TRUE, FALSE),
(4, 'Sala 7 - Premium 3D', 150, '3D', TRUE, FALSE),
(4, 'Sala 8 - Pequeña', 80, '2D', TRUE, TRUE),
(5, 'Sala 9 - Gran Formato', 280, 'IMAX', FALSE, FALSE),
(5, 'Sala 10 - Experiencia', 120, '4DX', TRUE, FALSE),
(6, 'Sala 11 - Clásica', 220, '2D', TRUE, FALSE),
(7, 'Sala 12 - Confort', 160, '3D', TRUE, FALSE),
(8, 'Sala 13 - Exclusiva', 70, 'V', TRUE, FALSE),
(9, 'Sala 14 - Futurista', 110, '4DX', TRUE, FALSE),
(10, 'Sala 15 - Familiar', 190, '2D', TRUE, FALSE);