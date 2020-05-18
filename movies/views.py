from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Movie
import redis

# Create your views here.

def connect():
    my_host_name = 'testpravredis.redis.cache.windows.net'
    my_password = 'Nfr7QWkbOM0U3ied7IXzQTxOYy60oTsTI9ZmcmHIcjk='
    r = redis.StrictRedis(host = my_host_name,
                          port = 6380,
                          password = my_password,
                          ssl = True)
    return r

def get_object_from_db(movie_id):
    
    db_object = get_object_or_404(Movie, pk=movie_id)
    return db_object

def index(request):
    
    movies = Movie.objects.all()
    return render(request, 'movies/index.html', {'movies':movies})

def detail(request, movie_id):
    redis_conn = connect()
    movie = redis_conn.get('movie'+str(movie_id))
    if  movie is None:
        redis_conn.set('movie'+ str(movie_id),str(get_object_from_db(movie_id)))
        movie = get_object_from_db(movie_id)
        return render(request, 'movies/details.html', {'movie':movie})
    else:
        movie = redis_conn.get('movie'+str(movie_id))
        movie = movie.decode('utf-8')
        return render(request, 'movies/details.html', {'movie': movie})