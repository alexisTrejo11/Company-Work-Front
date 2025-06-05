
CREATE TABLE showtime_seats(
    id SERIAL PRIMARY KEY,
    showtime_id INT NOT NULL,
    theater_seat_id INT NOT NULL,

    taken_at TIMESTAMP,
    taken_at TIMESTAMP WITH TIME ZONE,
    transation_id INT,
    user_id INT,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP

    CONSTRAINT pk_showtime FOREIGN KEY showtime_id REFERENCES showtimes(id) ON DELETE NULL,
    CONSTRAINT pk_theater_seat FOREIGN KEY theater_seat_id REFERENCES theater_seats(id) ON DELETE NULL
);