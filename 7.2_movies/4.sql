SELECT COUNT(*) FROM movies WHERE ID IN
(
    SELECT movie_id FROM ratings WHERE rating = 10.0
);
