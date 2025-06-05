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
    
    CONSTRAINT fk_cinema 
        FOREIGN KEY (cinema_id) 
        REFERENCES cinemas (id) ON DELETE CASCADE
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
(1, 'Room 1 - Main', 200, '2D', TRUE, FALSE),
(1, 'Room 2 - 3D', 160, '3D', TRUE, FALSE),
(2, 'Room 3 - IMAX', 300, 'IMAX', TRUE, FALSE),
(2, 'Room 4 - VIP', 50, 'V', TRUE, FALSE),
(3, 'Room 5 - 4DX', 120, '4DX', TRUE, FALSE), 
(3, 'Room 6 - Standard', 160, '2D', FALSE, TRUE), -- No Seats
(4, 'Room 7 - Premium 3D', 150, '3D', FALSE, TRUE), -- No Seats
(4, 'Room 8 - Small', 80, '2D', FALSE, TRUE),
(5, 'Room 9 - Great Format', 280, 'IMAX', FALSE, TRUE), -- No Seats
(5, 'Room 10 - Experience', 120, '4DX', FALSE, TRUE), -- No Seats
(6, 'Room 11 - Classic', 220, '2D', FALSE, TRUE), -- No Seats
(7, 'Room 12 - Comfort', 160, '3D', FALSE, TRUE), -- No Seats
(8, 'Room 13 - Exlusive', 70, 'V', FALSE, TRUE), -- No Seats
(9, 'Room 14 - Futurist', 110, '4DX', FALSE, TRUE), -- No Seats
(10, 'Room 15 - Familiar', 190, '2D', FALSE, TRUE); -- No Seats
