"""Server for movie ratings app."""

# from flask import Flask
from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined


app = Flask(__name__)

app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

# Replace this with routes and view functions!

@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')

@app.route("/movies")
def all_movies():
    """View all movies."""

    movies = crud.get_movies()

    return render_template("all_movies.html", movies=movies)

@app.route("/movies/<movie_id>")
def show_movie(movie_id):
    """Show details on a particular movie."""
    
    movie = crud.get_movie_by_id(movie_id)

    return render_template("movie_details.html", movie=movie)

@app.route("/users")
def all_users():
    
    users=crud.get_users()
    
    return render_template("all_users.html", users=users)

@app.route("/users", methods=["POST"])
def register_user():
    """Create a new user."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if user:
        flash("Cannot create an account with that email. Try again.")
    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")

    return redirect("/")

@app.route("/users/<user_id>")
def show_profile(user_id):
    
    user = crud.get_user_by_id(user_id)
    
    return render_template("user_details.html", user = user)

@app.route("/login", methods = ["POST"])
def user_login_page():
    password = request.form.get("password")
    email = request.form.get("email")
    user_password = crud.check_user_by_password(password, email)

    if user_password:
        flash("Logged in!")
        session["email"] = email
        return redirect("/")
    else:
        flash("Incorrect password or email")
        return redirect("/")

@app.route("/rating")
def rate_movies():
    movies = crud.get_movies()
    ratings = range(1, 6)
    
    return render_template("rating.html", movies=movies, ratings=ratings)

@app.route("/rating", methods=["POST"])
def add_rating(movie_id):
    logged_in_email = session.get("email")

    rating = request.form.get('ratings')
    movie_id =request.form.get(movie)

    if logged_in_email is None:
        flash("You must log in to rate a movie.")
    elif not rating:
        flash("Error: you didn't select a score for your rating.")
    else:
        user = crud.get_user_by_email(logged_in_email)
        movie = crud.get_movie_by_id(movie_id)

        rating = crud.create_rating(user, movie, int(rating))
        db.session.add(rating)
        db.session.commit()

        flash(f"You rated this movie {rating} out of 5.")

    return redirect("/")

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
