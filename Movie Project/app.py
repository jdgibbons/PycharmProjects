import datetime
import database

menu = """Please select one of the following options:
1) Add new movie.
2) View upcoming movies.
3) View all movies
4) Watch a movie
5) View watched movies.
6) Exit.

Your selection: """
welcome = "Welcome to the watchlist app!"

print(welcome)
database.create_tables()


def prompt_add_movie():
    title = input("Movie title: ")
    release_date = input("Release data (mm-dd-YYYY): ")
    parsed_date = datetime.datetime.strptime(release_date, '%m-%d-%Y').replace(tzinfo=datetime.timezone.utc)
    timestamp = parsed_date.timestamp()

    database.add_movie(title, timestamp)


def print_movie_list(heading, films):
    print(f"-- {heading} Movies --")
    for movie in films:
        movie_date = datetime.datetime.fromtimestamp(movie[1])
        human_date = movie_date.strftime('%B %d %Y')
        print(f"{movie[0]} (on {human_date})")
    print('---  \n')


def print_watched_movie_list(username, movies):
    print(f"-- {username}'s watched movies --")
    for movie in movies:
        print(f"{movie[1]}")
    print("=== \n")


def prompt_watch_movie():
    viewer = input("Enter viewer's name: ")
    movie_title = input("Enter the title of the movie you've watched: ")
    database.watch_movie(viewer, movie_title)


while (user_input := input(menu)) != "6":
    if user_input == "1":
        prompt_add_movie()
    elif user_input == "2":
        movies = database.get_movies(True)
        print_movie_list('Upcoming', movies)
    elif user_input == "3":
        movies = database.get_movies(False)
        print_movie_list('All', movies)
    elif user_input == "4":
        prompt_watch_movie()
    elif user_input == "5":
        viewer = input("Enter viewer's name: ")
        movies = database.get_watched_movies(viewer)
        print_watched_movie_list('Watched', movies)
    else:
        print("Invalid input, please try again!")
