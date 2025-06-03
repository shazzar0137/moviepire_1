from models import User, Movie, Review, Recommendation
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import click

engine = create_engine("sqlite:///movie_rcmdn.db", echo=True)
Session = sessionmaker(bind=engine)

def show_menu():
    while True:
        click.echo("\n🎬 MOVIE WATCHLIST & REVIEW MANAGER 🎬")
        click.echo("1. Add User")
        click.echo("2. Add Movie")
        click.echo("3. List Movies")
        click.echo("4. Mark Movie as Watched")
        click.echo("5. Write/Edit Review")
        click.echo("6. List Reviews")
        click.echo("7. Recommend Movie by Genre")
        click.echo("8. List Watched Movies")
        click.echo("9. List Users")
        click.echo("0. Exit")

        choice = click.prompt("\nEnter the number of your choice", type=int)

        if choice == 1:
            add_user()
        elif choice == 2:
            add_movie()
        elif choice == 3:
            list_movies()
        elif choice == 4:
            mark_watched()
        elif choice == 5:
            write_review()
        elif choice == 6:
            list_reviews()
        elif choice == 7:
            recommend_movie()
        elif choice == 8:
            list_movie_watched()
        elif choice == 9:
            list_users()
        elif choice == 0:
            click.echo("Goodbye! 🎬")
            break
        else:
            click.echo("Invalid choice. Please enter a number between 0-9.")


@click.group()
def cli():
    """CLI for the Movie Watchlist & Review Manager"""
    pass

@cli.command()
@click.option("--name", prompt="User name")
@click.option("--email", prompt="User email")
def add_user(name, email):
    session = Session()
    user = User(name=name, email=email)
    session.add(user)
    session.commit()
    click.echo(f"Added user: {user.name}")
    session.close()

@cli.command()
@click.option("--title", prompt="Movie title")
@click.option("--genre", prompt="Movie genre")
@click.option("--release_year", prompt="Movie release year", type=int)
@click.option("--watched", prompt="Movie watched", type=bool)
@click.option("--rating", prompt="Movie rating", type=float, default=None)
def add_movie(title, genre, release_year, watched, rating):
    session = Session()
    movie = Movie(title=title, genre=genre, release_year=release_year, watched=watched, rating=rating)
    session.add(movie)
    session.commit()
    click.echo(f"Added movie: {movie.title}")
    session.close()

@cli.command()
def list_movies():
    session = Session()
    movies = session.query(Movie).all()
    if not movies:
        click.echo("No movies found.")
    else:
        for movie in movies:
            click.echo(f"{movie.id}: {movie.title} - {movie.genre} ({movie.release_year})")
    session.close()

@cli.command()
def list_reviews():
    session = Session()
    reviews = session.query(Review).all()
    if not reviews:
        click.echo("No reviews found.")
    else:
        for review in reviews:
            click.echo(f"Review by User {review.user_id} for Movie {review.movie_id}: {review.review_text} (Rating: {review.rating})")
    session.close()

@cli.command()
@click.option("--title", prompt="Movie Title")
@click.option("--rating", type=float, default=None)
def mark_watched(title, rating):
    session = Session()
    movie = session.query(Movie).filter(Movie.title.ilike(title)).first()
    if not movie:
        click.echo(f"Movie '{title}' not found.")
    else:
        movie.watched = True
        if rating is not None:
            movie.rating = rating
        session.commit()
        click.echo(f"Marked '{movie.title}' as watched.{' Rating updated!' if rating else ''}")
    session.close()

@cli.command()
@click.option("--title", prompt="Movie Title")
@click.option("--text", prompt="Review Text")
@click.option("--rating", type=float, prompt="Rating (1-5)")
@click.option("--user_id", prompt="User ID", type=int)
def write_review(title, text, rating, user_id):
    session = Session()
    movie = session.query(Movie).filter(Movie.title.ilike(title)).first()
    if not movie:
        click.echo(f"Movie '{title}' not found.")
        session.close()
        return
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        click.echo(f"User ID {user_id} not found.")
        session.close()
        return
    review = session.query(Review).filter(Review.user_id == user_id, Review.movie_id == movie.id).first()
    if review:
        review.review_text = text
        review.rating = rating
        click.echo(f"Updated review for '{movie.title}'.")
    else:
        review = Review(user_id=user_id, movie_id=movie.id, rating=rating, review_text=text)
        session.add(review)
        click.echo(f"Added new review for '{movie.title}'.")
    session.commit()
    session.close()

@cli.command()
@click.option("--genre", prompt="Genre")
def recommend_movie(genre):
    session = Session()
    movies = session.query(Movie).filter(Movie.genre.ilike(genre), Movie.watched == False).all()
    if not movies:
        click.echo(f"No unwatched movies found in genre '{genre}'.")
    else:
        click.echo(f"Recommended movies in '{genre}':")
        for movie in movies:
            click.echo(f"- {movie.title} ({movie.release_year})")
    session.close()

@cli.command()
def list_movie_watched():
    session = Session()
    watched = session.query(Movie).filter(Movie.watched == True).all()
    if not watched:
        click.echo("No movies have been watched yet.")
    else:
        for movie in watched:
            click.echo(f"{movie.id}: {movie.title} - {movie.genre} ({movie.release_year})")
    session.close()

@cli.command()
def list_users():
    session = Session()
    users = session.query(User).all()
    if not users:
        click.echo("No users found.")
    else:
        for user in users:
            click.echo(f"ID: {user.id}, Name: {user.name}, Email: {user.email}")
    session.close()

@cli.command()
@click.argument("title")
def delete_movie(title):
    session = Session()
    movie = session.query(Movie).filter(Movie.title.ilike(title)).first()
    if not movie:
        click.echo(f"Movie '{title}' not found.")
    else:
        session.delete(movie)
        session.commit()
        click.echo(f"Deleted movie '{title}'.")
    session.close()

@cli.command()
@click.argument("user_id", type=int)
@click.argument("title")
def delete_review(user_id, title):
    session = Session()
    movie = session.query(Movie).filter(Movie.title.ilike(title)).first()
    if not movie:
        click.echo(f"Movie '{title}' not found.")
        session.close()
        return
    review = session.query(Review).filter(Review.user_id == user_id, Review.movie_id == movie.id).first()
    if not review:
        click.echo(f"No review found for '{title}' by user {user_id}.")
    else:
        session.delete(review)
        session.commit()
        click.echo(f"Deleted review for '{title}' by user {user_id}.")
    session.close()

if __name__ == "__main__":
    show_menu()