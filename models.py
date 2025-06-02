from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(), nullable=False)
    email = Column(String(), nullable=False, unique=True)

    reviews = relationship("Review", back_populates="user")
    recommendations = relationship("Recommendation", back_populates="user")

    def __repr__(self):
        return f"<User(name={self.name}, email={self.email})>"


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    release_year = Column(Integer)
    watched = Column(Boolean, default=False)
    rating = Column(Float, nullable=True)  # Optional rating

    reviews = relationship("Review", back_populates="movie")
    recommendations = relationship("Recommendation", back_populates="movie")

    def __repr__(self):
        return f"<Movie(title={self.title}, genre={self.genre}, release_year={self.release_year})>"


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    rating = Column(Float, nullable=False)
    review_text = Column(Text)
    date_reviewed = Column(String)  # Store date as string or use DateTime

    user = relationship("User", back_populates="reviews")
    movie = relationship("Movie", back_populates="reviews")

    def __repr__(self):
        return f"<Review(user_id={self.user_id}, movie_id={self.movie_id}, rating={self.rating})>"


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    reason = Column(Text)

    user = relationship("User", back_populates="recommendations")
    movie = relationship("Movie", back_populates="recommendations")

    def __repr__(self):
        return f"<Recommendation(user_id={self.user_id}, movie_id={self.movie_id}, reason={self.reason})>"
