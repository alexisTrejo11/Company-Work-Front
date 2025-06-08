CREATE TYPE cinema_status_enum AS ENUM ('OPEN', 'CLOSED', 'MAINTENANCE');
CREATE TYPE cinema_type_enum AS ENUM ('VIP', 'TRADITIONAL');
CREATE TYPE location_region_enum AS ENUM ('CDMX_SOUTH', 'CDMX_NORTH', 'CDMX_CENTER', 'CDMX_EAST', 'CDMX_WEST');

CREATE TABLE cinemas (
    id SERIAL PRIMARY KEY,
    image TEXT NOT NULL DEFAULT '',
    name VARCHAR(255) NOT NULL UNIQUE,
    tax_number VARCHAR(255) NOT NULL UNIQUE,
    is_active BOOLEAN NOT NULL DEFAULT FALSE,
    description TEXT NOT NULL DEFAULT '',
    screens INTEGER NOT NULL DEFAULT 0 CHECK (screens >= 0),

    last_renovation DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    region location_region_enum NOT NULL,
    type cinema_type_enum NOT NULL, 
    status cinema_status_enum NOT NULL, 

    -- Amenities 
    has_parking BOOLEAN NOT NULL DEFAULT FALSE,
    has_food_court BOOLEAN NOT NULL DEFAULT FALSE,
    has_coffee_station BOOLEAN NOT NULL DEFAULT FALSE,
    has_disabled_access BOOLEAN NOT NULL DEFAULT FALSE,

    -- Contact Info 
    address VARCHAR(500) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email_contact VARCHAR(255) NOT NULL UNIQUE,

    latitude DOUBLE PRECISION NOT NULL CHECK (latitude >= -90.0 AND latitude <= 90.0),
    longitude DOUBLE PRECISION NOT NULL CHECK (longitude >= -180.0 AND longitude <= 180.0),

    -- Social Media 
    facebook_url TEXT,
    instagram_url TEXT, 
    x_url TEXT,
    tik_tok_url TEXT,

    features TEXT[] NOT NULL DEFAULT '{}'
);


CREATE INDEX idx_cinemas_name ON cinemas(name);
CREATE INDEX idx_cinemas_tax_number ON cinemas(tax_number);
CREATE INDEX idx_cinemas_email_contact ON cinemas(email_contact);
CREATE INDEX idx_cinemas_status ON cinemas(status);
CREATE INDEX idx_cinemas_type ON cinemas(type);
-- Consider adding a GIST index for geographic queries if you plan to use them extensively
-- CREATE EXTENSION IF NOT EXISTS postgis; -- If using PostGIS for spatial queries
-- CREATE INDEX idx_cinemas_location ON cinemas USING GIST (ST_MakePoint(longitude, latitude));

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

INSERT INTO cinemas (
    name,
    email_contact,
    tax_number,
    is_active,
    image,
    description,
    screens,
    last_renovation,
    type,
    status,
    region,
    has_parking,
    has_food_court,
    has_coffee_station,
    has_disabled_access,
    address,
    phone,
    latitude,
    longitude,
    facebook_url,
    instagram_url,
    x_url,
    tik_tok_url,
    features
) VALUES
(
    'Cinépolis Plaza Carso',
    'atencionclientes_carso@cinepolis.com',
    'CINEP001CARSO',
    TRUE,
    'https://example.com/carso.jpg',
    'Modern cinema located in a major shopping center, known for its VIP experience.',
    10,
    '2023-01-15', -- last renovation date
    'VIP',        -- CinemaType
    'OPEN',       -- CinemaStatus
    'CDMX_CENTER', -- Location Region,
    TRUE,         -- has_parking
    TRUE,         -- has_food_court
    TRUE,         -- has_coffee_station
    TRUE,
    'Lago Zurich 245, Amp. Granada, Miguel Hidalgo, 11529 Ciudad de México, CDMX',
    '+525512345678',
    19.4398,     
    -99.1995,
    'https://www.facebook.com/cinepoliscarso',
    'https://www.instagram.com/cinepoliscarso',
    NULL,         
    NULL,
    ARRAY['3D', 'IMAX', 'VIP_SEATING']::TEXT[]
),
(
    'Cinépolis Forum Buenavista',
    'atencionclientes_buenavista@cinepolis.com',
    'CINEP002BUENA',
    TRUE,
    'https://example.com/buenavista.jpg',
    'Centrally located cinema in a bustling transport hub, offering a wide range of movies.',
    12,
    '2022-05-20',
    'TRADITIONAL',
    'OPEN',
    'CDMX_CENTER', -- Location Region,
    TRUE,
    TRUE,
    FALSE,
    TRUE,
    'Eje 1 Nte. Mosqueta 259, Buenavista, Cuauhtémoc, 06350 Ciudad de México, CDMX',
    '+525523456789',
    19.4475,
    -99.1458,
    'https://www.facebook.com/cinepolisbuenavista',
    'https://www.instagram.com/cinepolisbuenavista',
    NULL,
    NULL,
    ARRAY['2D', '3D']::TEXT[]
),
(
    'Cinépolis Perisur',
    'atencionclientes_perisur@cinepolis.com',
    'CINEP003PERI',
    TRUE,
    'https://example.com/perisur.jpg',
    'A flagship cinema in the south of the city, known for its large screens and diverse offerings.',
    15,
    '2024-02-10',
    'TRADITIONAL',
    'OPEN',
    'CDMX_SOUTH', -- Location Region,
    TRUE,
    TRUE,
    TRUE,
    TRUE,
    'Anillo Perif. Blvd. Adolfo López Mateos 4690, Jardines del Pedregal, Coyoacán, 04500 Ciudad de México, CDMX',
    '+525534567890',
    19.2987,
    -99.1834,
    'https://www.facebook.com/cinepolisperisur',
    'https://www.instagram.com/cinepolisperisur',
    'https://www.x.com/cinepolisperisur',
    NULL,
    ARRAY['2D', '3D', 'IMAX', '4D']::TEXT[]
),
(
    'Cinépolis Diana',
    'atencionclientes_diana@cinepolis.com',
    'CINEP004DIANA',
    TRUE,
    'https://example.com/diana.jpg',
    'Boutique cinema in the heart of Zona Rosa, offering a unique viewing experience.',
    6,
    '2021-11-01',
    'VIP',
    'OPEN',
    'CDMX_CENTER',
    FALSE, -- No parking
    TRUE,
    TRUE,
    TRUE,
    'Paseo de la Reforma 439, Cuauhtémoc, 06500 Ciudad de México, CDMX',
    '+525545678901',
    19.4243,
    -99.1718,
    'https://www.facebook.com/cinepolisdiana',
    NULL,
    NULL,
    NULL,
    ARRAY['VIP_SEATING', 'DOBLY_ATMOS']::TEXT[]
),
(
    'Cinépolis Universidad',
    'atencionclientes_universidad@cinepolis.com',
    'CINEP005UNIV',
    TRUE,
    'https://example.com/universidad.jpg',
    'Popular cinema near the university, frequently visited by students.',
    8,
    '2020-09-01',
    'TRADITIONAL',
    'OPEN',
    'CDMX_SOUTH',
    TRUE,
    TRUE,
    FALSE,
    TRUE,
    'Av. Universidad 1000, Xoco, Benito Juárez, 03330 Ciudad de México, CDMX',
    '+525556789012',
    19.3567,
    -99.1678,
    'https://www.facebook.com/cinepolisuniversidad',
    NULL,
    NULL,
    NULL,
    ARRAY['2D', '3D']::TEXT[]
),
(
    'Cinépolis Satélite',
    'atencionclientes_satelite@cinepolis.com',
    'CINEP006SAT',
    TRUE,
    'https://example.com/satelite.jpg',
    'Large cinema complex serving the northern suburbs.',
    14,
    '2023-08-01',
    'TRADITIONAL',
    'OPEN',
    'CDMX_WEST',
    TRUE,
    TRUE,
    TRUE,
    TRUE,
    'Circuito Centro Comercial 2251, Ciudad Satélite, Naucalpan de Juárez, 53100 Naucalpan de Juárez, Méx.',
    '+525567890123',
    19.5398,
    -99.2487,
    'https://www.facebook.com/cinepolissatelite',
    'https://www.instagram.com/cinepolissatelite',
    NULL,
    NULL,
    ARRAY['2D', '3D', 'IMAX']::TEXT[]
),
(
    'Cinépolis Santa Fe',
    'atencionclientes_santafe@cinepolis.com',
    'CINEP007SANTAFE',
    TRUE,
    'https://example.com/santafe.jpg',
    'Premium cinema offering a luxurious experience in the upscale Santa Fe district.',
    11,
    '2024-01-25',
    'VIP',
    'OPEN',
    'CDMX_WEST',
    TRUE,
    TRUE,
    TRUE,
    TRUE,
    'Av. Vasco de Quiroga 3800, Lomas de Santa Fe, Cuajimalpa de Morelos, 05348 Ciudad de México, CDMX',
    '+525578901234',
    19.3621,
    -99.2618,
    'https://www.facebook.com/cinepolissantafe',
    'https://www.instagram.com/cinepolissantafe',
    'https://www.x.com/cinepolissantafe',
    NULL,
    ARRAY['3D', 'IMAX', 'VIP_SEATING', 'DOBLY_ATMOS']::TEXT[]
),
(
    'Cinépolis Patio Universidad',
    'atencionclientes_patiouniv@cinepolis.com',
    'CINEP008PATIO',
    TRUE,
    'https://example.com/patiouniv.jpg',
    'Conveniently located cinema within a shopping mall, popular for family outings.',
    9,
    '2022-03-01',
    'TRADITIONAL',
    'OPEN',
    'CDMX_SOUTH',
    TRUE,
    TRUE,
    FALSE,
    TRUE,
    'Av. Universidad 1000, Sta Cruz Atoyac, Benito Juárez, 03310 Ciudad de México, CDMX',
    '+525589012345',
    19.3765,
    -99.1691,
    'https://www.facebook.com/cinepolispatiouniv',
    NULL,
    NULL,
    NULL,
    ARRAY['2D', '3D']::TEXT[]
),
(
    'Cinépolis Parque Delta',
    'atencionclientes_delta@cinepolis.com',
    'CINEP009DELTA',
    TRUE,
    'https://example.com/delta.jpg',
    'Modern cinema inside a popular urban shopping center.',
    10,
    '2023-07-01',
    'TRADITIONAL',
    'OPEN',
    'CDMX_WEST',
    TRUE,
    TRUE,
    TRUE,
    TRUE,
    'Av. Cuauhtémoc 462, Narvarte Poniente, Benito Juárez, 03020 Ciudad de México, CDMX',
    '+525590123456',
    19.3980,
    -99.1557,
    'https://www.facebook.com/cinepolisdeltapark',
    'https://www.instagram.com/cinepolisdeltapark',
    NULL,
    NULL,
    ARRAY['2D', '3D', '4D']::TEXT[]
),
(
    'Cinépolis Coapa',
    'atencionclientes_coapa@cinepolis.com',
    'CINEP010COAPA',
    TRUE,
    'https://example.com/coapa.jpg',
    'Community cinema serving the Coapa area, known for its family-friendly environment.',
    7,
    '2021-02-18',
    'TRADITIONAL',
    'OPEN',
    'CDMX_SOUTH',
    TRUE,
    TRUE,
    FALSE,
    TRUE,
    'Av. Canal de Miramontes 2050, Coapa, Coyoacán, 04920 Ciudad de México, CDMX',
    '+525501234567',
    19.3082,
    -99.1387,
    'https://www.facebook.com/cinepoliscoapa',
    NULL,
    NULL,
    NULL,
    ARRAY['2D', '3D']::TEXT[]
);