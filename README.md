### 🎬 Moviepire
A command-line app to manage a movie watchlist, track watched movies, write reviews, and get recommendations. Built with Python, SQLAlchemy, SQLite, and Click.

##  Features
-Add and list users
-Add, list, and update movies
-Mark movies as watched with ratings
-Write/edit reviews
-Recommend movies by genre

##  Tools
-Python 3
-SQLAlchemy
-SQLite
-Click
-Alembic

## Setup
# Clone the repo:
bash
git clone git@github.com:shazzar0137/moviepire_1.git

# Create and activate a virtual environment:
bash
python -m venv env
source env/bin/activate

# Install dependencies:
bash
pip install -r requirements.txt

# Run migrations:
bash
alembic upgrade head

# Start the interactive menu:
bash
python cli.py

## CLI Commands

# Add a user
python cli.py add-user

# Add a movie
python cli.py add-movie

# List all movies
python cli.py list-movies

# Mark a movie as watched
python cli.py mark-watched --title "The Acountant"

# Write or update a review
python cli.py write-review --title "Final Destination" --text "Solid film" --rating 4.5 --user_id 1

# Get genre-based recommendation
python cli.py recommend-movie --genre "Sci-Fi"

## DB Schema
-User: id, name, email
-Movie: id, title, genre, release_year, watched, rating
-Review: id, user_id, movie_id, review_text, rating
-Recommendation: id, movie_id, genre

## Future Additions
-Add basic authentication
-Improve recommendation logic
-Web frontend 


### License
MIT License.