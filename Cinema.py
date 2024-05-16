import threading


class Cinema:
    def __init__(self):
        self.movies = {}
        self.lock = threading.Lock()

    def add_movie(self, movie_name, show_times, seats):
        with self.lock:
            self.movies[movie_name] = {'show_times': show_times, 'seats': seats}

    def book_seat(self, movie_name, show_time, seat):
        thread_name = threading.current_thread().name
        with self.lock:
            movie = self.movies.get(movie_name)
            if movie and show_time in movie['show_times'] and seat in movie['seats']:
                if movie['seats'][seat]:
                    movie['seats'][seat] = False
                    print(f"Seat {seat} for {movie_name} at {show_time} is booked by thread: {thread_name}")
                else:
                    print(f"Seat {seat} for {movie_name} at {show_time} is already booked.")
            else:
                print(f"Invalid movie, showtime, or seat.")


cinema = Cinema()
cinema.add_movie("Movie 1", ["10:00"], {1: True, 2: True, 3: False})
cinema.add_movie("Movie 2", ["12:00"], {1: True, 2: True, 3: True})


def book_seat(movie_name, showtime, seat):
    cinema.book_seat(movie_name, showtime, seat)


threads = []
for movie_name in cinema.movies:
    movie = cinema.movies[movie_name]
    show_times = movie['show_times']
    seats = list(movie['seats'].keys())

    for show_time in show_times:
        for seat in seats:
            thread = threading.Thread(target=cinema.book_seat, args=(movie_name, show_time, seat))
            threads.append(thread)
            thread.start()

for thread in threads:
    thread.join()

