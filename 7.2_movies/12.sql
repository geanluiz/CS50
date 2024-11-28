SELECT title FROM movies
JOIN stars ON movies.id = stars.movie_id
JOIN people ON stars.person_id = people.id
WHERE people.name = 'Bradley Cooper' OR people.name = 'Jennifer Lawrence'
GROUP BY title HAVING COUNT(DISTINCT people.name) = 2;
