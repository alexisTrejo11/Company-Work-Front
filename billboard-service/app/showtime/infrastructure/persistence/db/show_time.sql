CREATE TABLE showtimes (
    id SERIAL PRIMARY KEY,
    movie_id INT NOT NULL,
    theater_id INT NOT NULL,
    start_time TIMESTAMP WITH TIME ZONE NOT NULL,
    end_time TIMESTAMP WITH TIME ZONE,
    price NUMERIC(6, 2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_movie FOREIGN KEY (movie_id) REFERENCES movies (id) ON DELETE CASCADE,
    CONSTRAINT fk_theater FOREIGN KEY (theater_id) REFERENCES theaters (id) ON DELETE CASCADE
);

CREATE INDEX idx_showtimes_movie_id ON showtimes (movie_id);
CREATE INDEX idx_showtimes_theater_id ON showtimes (theater_id);
CREATE INDEX idx_showtimes_theater_time ON showtimes (theater_id, start_time);
CREATE INDEX idx_showtimes_start_time ON showtimes (start_time);


INSERT INTO showtimes (movie_id, theater_id, start_time, end_time, price)
VALUES (1, 1, '2025-06-03 10:00:00-06', '2025-06-03 12:00:00-06', 10.50);
INSERT INTO showtimes (movie_id, theater_id, start_time, price)
VALUES (2, 2, '2025-06-03 14:30:00-06', 12.00);
INSERT INTO showtimes (movie_id, theater_id, start_time, end_time, price)
VALUES (3, 3, '2025-06-04 18:00:00-06', '2025-06-04 20:30:00-06', 9.75);
INSERT INTO showtimes (movie_id, theater_id, start_time, price)
VALUES (4, 4, '2025-06-04 21:00:00-06', 11.25);
INSERT INTO showtimes (movie_id, theater_id, start_time, end_time, price)
VALUES (5, 5, '2025-06-05 11:00:00-06', '2025-06-05 13:45:00-06', 13.00);
INSERT INTO showtimes (movie_id, theater_id, start_time, price)
VALUES (6, 6, '2025-06-05 16:00:00-06', 8.50);
INSERT INTO showtimes (movie_id, theater_id, start_time, end_time, price)
VALUES (7, 7, '2025-06-06 19:30:00-06', '2025-06-06 22:00:00-06', 10.00);
INSERT INTO showtimes (movie_id, theater_id, start_time, price)
VALUES (8, 8, '2025-06-06 20:00:00-06', 9.00);
INSERT INTO showtimes (movie_id, theater_id, start_time, end_time, price)
VALUES (9, 9, '2025-06-07 10:30:00-06', '2025-06-07 12:45:00-06', 11.50);
INSERT INTO showtimes (movie_id, theater_id, start_time, price)
VALUES (10, 10, '2025-06-07 15:00:00-06', 10.75);