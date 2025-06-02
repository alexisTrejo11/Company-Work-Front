CREATE TYPE movie_genre AS ENUM  ('action', 'comedy', 'drama', 'romance', 'thriller', 'sci-fi');
CREATE TYPE movie_rating AS ENUM ('G', 'PG', 'PG-13', 'R', 'NC-17');

CREATE TABLE movies (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    original_title VARCHAR(200),
    minute_duration INTEGER NOT NULL,
    release_date DATE NOT NULL,
    end_date DATE NOT NULL,
    description TEXT NOT NULL,
    genre movie_genre NOT NULL,
    rating movie_rating NOT NULL,
    poster_url TEXT,
    trailer_url TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_movies_title ON movies(title);
CREATE INDEX idx_movies_dates ON movies(release_date, end_date);
CREATE INDEX idx_movies_active ON movies(is_active) WHERE is_active = TRUE;
CREATE INDEX idx_movies_genre ON movies(genre);
CREATE INDEX idx_movies_genre_active_dates ON movies(genre, is_active, release_date);

CREATE OR REPLACE FUNCTION update_updated_at_column() 
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_movies_updated_at
BEFORE UPDATE ON movies
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Sample 1: Action movie
INSERT INTO movies (title, original_title, minute_duration, release_date, end_date, description, genre, rating, poster_url, trailer_url, is_active)
VALUES ('The Dark Knight', 'The Dark Knight', 152, '2008-07-18', '2008-10-18', 'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.', 'action', 'PG-13', 'https://example.com/posters/darkknight.jpg', 'https://youtube.com/thedarkknight', true);
-- Sample 2: Comedy
INSERT INTO movies (title, original_title, minute_duration, release_date, end_date, description, genre, rating, poster_url, trailer_url, is_active)
VALUES ('Superbad', 'Superbad', 113, '2007-08-17', '2007-11-17', 'Two co-dependent high school seniors are forced to deal with separation anxiety after their plan to stage a booze-soaked party goes awry.', 'comedy', 'R', 'https://example.com/posters/superbad.jpg', 'https://youtube.com/superbad', true);
-- Sample 3: Drama
INSERT INTO movies (title, original_title, minute_duration, release_date, end_date, description, genre, rating, poster_url, trailer_url, is_active)
VALUES ('The Shawshank Redemption', 'The Shawshank Redemption', 142, '1994-09-23', '1995-01-23', 'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.', 'drama', 'R', 'https://example.com/posters/shawshank.jpg', 'https://youtube.com/shawshank', true);
-- Sample 4: Romance
INSERT INTO movies (title, original_title, minute_duration, release_date, end_date, description, genre, rating, poster_url, trailer_url, is_active)
VALUES ('The Notebook', 'The Notebook', 123, '2004-06-25', '2004-09-25', 'A poor yet passionate young man falls in love with a rich young woman, giving her a sense of freedom, but they are soon separated because of their social differences.', 'romance', 'PG-13', 'https://example.com/posters/notebook.jpg', 'https://youtube.com/thenotebook', true);
-- Sample 5: Sci-Fi
INSERT INTO movies (title, original_title, minute_duration, release_date, end_date, description, genre, rating, poster_url, trailer_url, is_active)
VALUES ('Inception', 'Inception', 148, '2010-07-16', '2010-10-16', 'A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.', 'sci-fi', 'PG-13', 'https://example.com/posters/inception.jpg', 'https://youtube.com/inception', true);
-- Sample 6: Thriller
INSERT INTO movies (title, original_title, minute_duration, release_date, end_date, description, genre, rating, poster_url, trailer_url, is_active)
VALUES ('Gone Girl', 'Gone Girl', 149, '2014-10-03', '2015-01-03', 'With his wife''s disappearance having become the focus of an intense media circus, a man sees the spotlight turned on him when it''s suspected that he may not be innocent.', 'thriller', 'R', 'https://example.com/posters/gonegirl.jpg', 'https://youtube.com/gonegirl', true);
-- Sample 7: Action with different original title
INSERT INTO movies (title, original_title, minute_duration, release_date, end_date, description, genre, rating, poster_url, trailer_url, is_active)
VALUES ('Hero', 'Ying xiong', 99, '2004-08-27', '2004-11-27', 'A defense officer, Nameless, was summoned by the King of Qin regarding his success of terminating three warriors.', 'action', 'PG-13', 'https://example.com/posters/hero.jpg', 'https://youtube.com/hero', false);
-- Sample 8: Comedy
INSERT INTO movies (title, original_title, minute_duration, release_date, end_date, description, genre, rating, poster_url, trailer_url, is_active)
VALUES ('Bridesmaids', 'Bridesmaids', 125, '2011-05-13', '2011-08-13', 'Competition between the maid of honor and a bridesmaid, over who is the bride''s best friend, threatens to upend the life of an out-of-work pastry chef.', 'comedy', 'R', 'https://example.com/posters/bridesmaids.jpg', 'https://youtube.com/bridesmaids', true);
-- Sample 9: Drama (Oscar winner)
INSERT INTO movies (title, original_title, minute_duration, release_date, end_date, description, genre, rating, poster_url, trailer_url, is_active)
VALUES ('Parasite', 'Gisaengchung', 132, '2019-10-11', '2020-01-11', 'Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.', 'drama', 'R', 'https://example.com/posters/parasite.jpg', 'https://youtube.com/parasite', true);
-- Sample 10: Romance (classic)
INSERT INTO movies (title, original_title, minute_duration, release_date, end_date, description, genre, rating, poster_url, trailer_url, is_active)
VALUES ('Casablanca', 'Casablanca', 102, '1942-11-26', '1943-03-26', 'A cynical expatriate American cafe owner struggles to decide whether or not to help his former lover and her fugitive husband escape the Nazis in French Morocco.', 'romance', 'PG', 'https://example.com/posters/casablanca.jpg', 'https://youtube.com/casablanca', true);
-- Sample 11: Sci-Fi (recent)
INSERT INTO movies (title, original_title, minute_duration, release_date, end_date, description, genre, rating, poster_url, trailer_url, is_active)
VALUES ('Dune', 'Dune', 155, '2021-10-22', '2022-01-22', 'Feature adaptation of Frank Herbert''s science fiction novel about the son of a noble family entrusted with the protection of the most valuable asset in the galaxy.', 'sci-fi', 'PG-13', 'https://example.com/posters/dune.jpg', 'https://youtube.com/dune', true);
-- Sample 12: Thriller (Hitchcock classic)
INSERT INTO movies (title, original_title, minute_duration, release_date, end_date, description, genre, rating, poster_url, trailer_url, is_active)
VALUES ('Psycho', 'Psycho', 109, '1960-06-16', '1960-09-16', 'A Phoenix secretary embezzles $40,000 from her employer''s client, goes on the run, and checks into a remote motel run by a young man under the domination of his mother.', 'thriller', 'R', 'https://example.com/posters/psycho.jpg', 'https://youtube.com/psycho', true);
-- Sample 13: Action (superhero)
INSERT INTO movies (title, original_title, minute_duration, release_date, end_date, description, genre, rating, poster_url, trailer_url, is_active)
VALUES ('Black Panther', 'Black Panther', 134, '2018-02-16', '2018-05-16', 'T''Challa, heir to the hidden but advanced kingdom of Wakanda, must step forward to lead his people into a new future and must confront a challenger from his country''s past.', 'action', 'PG-13', 'https://example.com/posters/blackpanther.jpg', 'https://youtube.com/blackpanther', true);
-- Sample 14: Comedy (animated)
INSERT INTO movies (title, original_title, minute_duration, release_date, end_date, description, genre, rating, poster_url, trailer_url, is_active)
VALUES ('The Lego Movie', 'The Lego Movie', 100, '2014-02-07', '2014-05-07', 'An ordinary LEGO construction worker, thought to be the prophesied "Special", is recruited to join a quest to stop an evil tyrant from gluing the LEGO universe into eternal stasis.', 'comedy', 'PG', 'https://example.com/posters/legomovie.jpg', 'https://youtube.com/legomovie', false);
-- Sample 15: Drama (biographical)
INSERT INTO movies (title, original_title, minute_duration, release_date, end_date, description, genre, rating, poster_url, trailer_url, is_active)
VALUES ('The Social Network', 'The Social Network', 120, '2010-10-01', '2011-01-01', 'As Harvard student Mark Zuckerberg creates the social networking site that would become known as Facebook, he is sued by the twins who claimed he stole their idea, and by the co-founder who was later squeezed out of the business.', 'drama', 'PG-13', 'https://example.com/posters/socialnetwork.jpg', 'https://youtube.com/socialnetwork', true);
-- Sample 16: Romance (musical)
INSERT INTO movies (title, original_title, minute_duration, release_date, end_date, description, genre, rating, poster_url, trailer_url, is_active)
VALUES ('La La Land', 'La La Land', 128, '2016-12-09', '2017-03-09', 'While navigating their careers in Los Angeles, a pianist and an actress fall in love while attempting to reconcile their aspirations for the future.', 'romance', 'PG-13', 'https://example.com/posters/lalaland.jpg', 'https://youtube.com/lalaland', true);
-- Sample 17: Sci-Fi (cyberpunk)
INSERT INTO movies (title, original_title, minute_duration, release_date, end_date, description, genre, rating, poster_url, trailer_url, is_active)
VALUES ('Blade Runner 2049', 'Blade Runner 2049', 164, '2017-10-06', '2018-01-06', 'A young blade runner''s discovery of a long-buried secret leads him to track down former blade runner Rick Deckard, who''s been missing for thirty years.', 'sci-fi', 'R', 'https://example.com/posters/bladerunner.jpg', 'https://youtube.com/bladerunner', true);
-- Sample 18: Thriller (crime)
INSERT INTO movies (title, original_title, minute_duration, release_date, end_date, description, genre, rating, poster_url, trailer_url, is_active)
VALUES ('The Silence of the Lambs', 'The Silence of the Lambs', 118, '1991-02-14', '1991-05-14', 'A young F.B.I. cadet must receive the help of an incarcerated and manipulative cannibal killer to help catch another serial killer, a madman who skins his victims.', 'thriller', 'R', 'https://example.com/posters/silence.jpg', 'https://youtube.com/silence', true);
-- Sample 19: Action (spy)
INSERT INTO movies (title, original_title, minute_duration, release_date, end_date, description, genre, rating, poster_url, trailer_url, is_active)
VALUES ('Mission: Impossible - Fallout', 'Mission: Impossible - Fallout', 147, '2018-07-27', '2018-10-27', 'Ethan Hunt and his IMF team, along with some familiar allies, race against time after a mission gone wrong.', 'action', 'PG-13', 'https://example.com/posters/missionimpossible.jpg', 'https://youtube.com/missionimpossible', false);
-- Sample 20: Comedy (satire)
INSERT INTO movies (title, original_title, minute_duration, release_date, end_date, description, genre, rating, poster_url, trailer_url, is_active)
VALUES ('Dr. Strangelove', 'Dr. Strangelove or: How I Learned to Stop Worrying and Love the Bomb', 95, '1964-01-29', '1964-04-29', 'An insane general triggers a path to nuclear holocaust that a war room full of politicians and generals frantically tries to stop.', 'comedy', 'PG', 'https://example.com/posters/strangelove.jpg', 'https://youtube.com/strangelove', true);
-- Sample 21: Sci-Fi Classic
INSERT INTO movies (title, original_title, minute_duration, release_date, end_date, description, genre, rating, poster_url, trailer_url, is_active)
VALUES ('2001: A Space Odyssey', '2001: A Space Odyssey', 149, '1968-04-03', '1968-07-03', 'After discovering a mysterious artifact buried beneath the Lunar surface, mankind sets off on a quest to find its origins with help from intelligent supercomputer HAL 9000.', 'sci-fi', 'G', 'https://example.com/posters/2001.jpg', 'https://youtube.com/2001space', true);
-- Sample 22: Romantic Comedy
INSERT INTO movies (title, original_title, minute_duration, release_date, end_date, description, genre, rating, poster_url, trailer_url, is_active)
VALUES ('When Harry Met Sally', 'When Harry Met Sally', 95, '1989-07-21', '1989-10-21', 'Harry and Sally have known each other for years, and are very good friends, but they fear sex would ruin the friendship.', 'romance', 'R', 'https://example.com/posters/harrysally.jpg', 'https://youtube.com/harrysally', true);
-- Sample 23: Psychological Thriller
INSERT INTO movies (title, original_title, minute_duration, release_date, end_date, description, genre, rating, poster_url, trailer_url, is_active)
VALUES ('Black Swan', 'Black Swan', 108, '2010-12-03', '2011-03-03', 'A committed dancer struggles to maintain her sanity after winning the lead role in a production of Tchaikovsky''s "Swan Lake".', 'thriller', 'R', 'https://example.com/posters/blackswan.jpg', 'https://youtube.com/blackswan', false);
-- Sample 24: Animated Adventure
INSERT INTO movies (title, original_title, minute_duration, release_date, end_date, description, genre, rating, poster_url, trailer_url, is_active)
VALUES ('Spider-Man: Into the Spider-Verse', 'Spider-Man: Into the Spider-Verse', 117, '2018-12-14', '2019-03-14', 'Teen Miles Morales becomes the Spider-Man of his universe and must join with five spider-powered individuals from other dimensions to stop a threat for all realities.', 'action', 'PG', 'https://example.com/posters/spiderverse.jpg', 'https://youtube.com/spiderverse', true);
-- Sample 25: Historical Drama
INSERT INTO movies (title, original_title, minute_duration, release_date, end_date, description, genre, rating, poster_url, trailer_url, is_active)
VALUES ('Schindler''s List', 'Schindler''s List', 195, '1993-12-15', '1994-03-15', 'In German-occupied Poland during World War II, industrialist Oskar Schindler gradually becomes concerned for his Jewish workforce after witnessing their persecution by the Nazis.', 'drama', 'R', 'https://example.com/posters/schindler.jpg', 'https://youtube.com/schindler', true);
-- Sample 26: Action Comedy
INSERT INTO movies (title, original_title, minute_duration, release_date, end_date, description, genre, rating, poster_url, trailer_url, is_active)
VALUES ('Deadpool', 'Deadpool', 108, '2016-02-12', '2016-05-12', 'A wisecracking mercenary gets experimented on and becomes immortal but ugly, and sets out to track down the man who ruined his looks.', 'action', 'R', 'https://example.com/posters/deadpool.jpg', 'https://youtube.com/deadpool', true);
-- Sample 27: Fantasy Adventure
INSERT INTO movies (title, original_title, minute_duration, release_date, end_date, description, genre, rating, poster_url, trailer_url, is_active)
VALUES ('The Lord of the Rings: The Fellowship of the Ring', 'The Lord of the Rings: The Fellowship of the Ring', 178, '2001-12-19', '2002-03-19', 'A meek Hobbit from the Shire and eight companions set out on a journey to destroy the powerful One Ring and save Middle-earth from the Dark Lord Sauron.', 'action', 'PG-13', 'https://example.com/posters/fellowship.jpg', 'https://youtube.com/fellowship', true);
-- Sample 28: Dark Comedy
INSERT INTO movies (title, original_title, minute_duration, release_date, end_date, description, genre, rating, poster_url, trailer_url, is_active)
VALUES ('Fargo', 'Fargo', 98, '1996-03-08', '1996-06-08', 'Jerry Lundegaard''s inept crime falls apart due to his and his henchmen''s bungling and the persistent police work of the quite pregnant Marge Gunderson.', 'comedy', 'R', 'https://example.com/posters/fargo.jpg', 'https://youtube.com/fargo', false);
-- Sample 29: Musical Drama
INSERT INTO movies (title, original_title, minute_duration, release_date, end_date, description, genre, rating, poster_url, trailer_url, is_active)
VALUES ('Whiplash', 'Whiplash', 106, '2014-10-10', '2015-01-10', 'A promising young drummer enrolls at a cut-throat music conservatory where his dreams of greatness are mentored by an instructor who will stop at nothing to realize a student''s potential.', 'drama', 'R', 'https://example.com/posters/whiplash.jpg', 'https://youtube.com/whiplash', true);
-- Sample 30: Superhero Action
INSERT INTO movies (title, original_title, minute_duration, release_date, end_date, description, genre, rating, poster_url, trailer_url, is_active)
VALUES ('Avengers: Endgame', 'Avengers: Endgame', 181, '2019-04-26', '2019-07-26', 'After the devastating events of Avengers: Infinity War, the universe is in ruins. With the help of remaining allies, the Avengers assemble once more in order to reverse Thanos'' actions and restore balance to the universe.', 'action', 'PG-13', 'https://example.com/posters/endgame.jpg', 'https://youtube.com/endgame', true);
-- Sample 31: Crime Thriller
INSERT INTO movies (title, original_title, minute_duration, release_date, end_date, description, genre, rating, poster_url, trailer_url, is_active)
VALUES ('The Departed', 'The Departed', 151, '2006-10-06', '2007-01-06', 'An undercover cop and a mole in the police attempt to identify each other while infiltrating an Irish gang in South Boston.', 'thriller', 'R', 'https://example.com/posters/departed.jpg', 'https://youtube.com/departed', true);
-- Sample 32: Animated Fantasy
INSERT INTO movies (title, original_title, minute_duration, release_date, end_date, description, genre, rating, poster_url, trailer_url, is_active)
VALUES ('Spirited Away', 'Sen to Chihiro no kamikakushi', 125, '2001-07-20', '2001-10-20', 'During her family''s move to the suburbs, a sullen 10-year-old girl wanders into a world ruled by gods, witches, and spirits, and where humans are changed into beasts.', 'drama', 'PG', 'https://example.com/posters/spirited.jpg', 'https://youtube.com/spirited', true);
-- Sample 33: Sci-Fi Horror
INSERT INTO movies (title, original_title, minute_duration, release_date, end_date, description, genre, rating, poster_url, trailer_url, is_active)
VALUES ('Alien', 'Alien', 117, '1979-05-25', '1979-08-25', 'After a space merchant vessel receives an unknown transmission as a distress call, one of the crew is attacked by a mysterious life form and they soon realize that its life cycle has merely begun.', 'sci-fi', 'R', 'https://example.com/posters/alien.jpg', 'https://youtube.com/alien', true);
-- Sample 34: Coming-of-Age Drama
INSERT INTO movies (title, original_title, minute_duration, release_date, end_date, description, genre, rating, poster_url, trailer_url, is_active)
VALUES ('Lady Bird', 'Lady Bird', 94, '2017-11-03', '2018-02-03', 'In the early 2000s, an artistically inclined seventeen-year-old girl comes of age in Sacramento, California.', 'drama', 'R', 'https://example.com/posters/ladybird.jpg', 'https://youtube.com/ladybird', false);
-- Sample 35: Action Spy
INSERT INTO movies (title, original_title, minute_duration, release_date, end_date, description, genre, rating, poster_url, trailer_url, is_active)
VALUES ('Kingsman: The Secret Service', 'Kingsman: The Secret Service', 129, '2014-12-13', '2015-03-13', 'A spy organization recruits an unrefined but promising street kid into the agency''s ultra-competitive training program just as a global threat emerges from a twisted tech genius.', 'action', 'R', 'https://example.com/posters/kingsman.jpg', 'https://youtube.com/kingsman', true);
-- Sample 36: Satirical Comedy
INSERT INTO movies (title, original_title, minute_duration, release_date, end_date, description, genre, rating, poster_url, trailer_url, is_active)
VALUES ('The Grand Budapest Hotel', 'The Grand Budapest Hotel', 99, '2014-03-28', '2014-06-28', 'The adventures of Gustave H, a legendary concierge at a famous hotel from the fictional Republic of Zubrowka between the first and second World Wars, and Zero Moustafa, the lobby boy who becomes his most trusted friend.', 'comedy', 'R', 'https://example.com/posters/budapest.jpg', 'https://youtube.com/budapest', true);
-- Sample 37: Sports Drama
INSERT INTO movies (title, original_title, minute_duration, release_date, end_date, description, genre, rating, poster_url, trailer_url, is_active)
VALUES ('Rocky', 'Rocky', 120, '1976-11-21', '1977-02-21', 'A small-time Philadelphia boxer gets a supremely rare chance to fight the world heavyweight champion in a bout in which he strives to go the distance for his self-respect.', 'drama', 'PG', 'https://example.com/posters/rocky.jpg', 'https://youtube.com/rocky', true);
-- Sample 38: Cyberpunk Action
INSERT INTO movies (title, original_title, minute_duration, release_date, end_date, description, genre, rating, poster_url, trailer_url, is_active)
VALUES ('The Matrix', 'The Matrix', 136, '1999-03-31', '1999-06-30', 'A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.', 'action', 'R', 'https://example.com/posters/matrix.jpg', 'https://youtube.com/matrix', true);
-- Sample 39: Romantic Drama
INSERT INTO movies (title, original_title, minute_duration, release_date, end_date, description, genre, rating, poster_url, trailer_url, is_active)
VALUES ('Eternal Sunshine of the Spotless Mind', 'Eternal Sunshine of the Spotless Mind', 108, '2004-03-19', '2004-06-19', 'When their relationship turns sour, a couple undergoes a medical procedure to have each other erased from their memories.', 'romance', 'R', 'https://example.com/posters/eternalsunshine.jpg', 'https://youtube.com/eternalsunshine', true);
-- Sample 40: Horror Thriller
INSERT INTO movies (title, original_title, minute_duration, release_date, end_date, description, genre, rating, poster_url, trailer_url, is_active)
VALUES ('Get Out', 'Get Out', 104, '2017-02-24', '2017-05-24', 'A young African-American visits his white girlfriend''s parents for the weekend, where his simmering uneasiness about their reception of him eventually reaches a boiling point.', 'thriller', 'R', 'https://example.com/posters/getout.jpg', 'https://youtube.com/getout', false);