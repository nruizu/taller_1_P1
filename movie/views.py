from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie
import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64

# Create your views here.

def home(request):
    #return HttpResponse('<h1>Welcome to Home Page</h1>')
    #return render(request, 'home.html', {'name':'Nicolas Ruiz'})
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    
    return render(request, 'home.html', {'searchTerm':searchTerm, 'movies':movies})

def about(request):
    #return HttpResponse('<h1>Welcome to About Page</h1>')
    return render(request, 'about.html')

def statistics_view(request):
    matplotlib.use('Agg')
    years = Movie.objects.values_list('year', flat=True).distinct().order_by('year') #obtener todos los años de las peliculas
    movie_counts_by_year = {}
    for year in years:
        if year:
            movies_in_year = Movie.objects.filter(year=year)
        else:
            movies_in_year = Movie.objects.filter(year__isnull=True)
            year = 'None'
        count = movies_in_year.count()
        movie_counts_by_year[year] = count

    bar_width = 0.5
    bar_spacing = 0.5
    bar_positions = range(len(movie_counts_by_year))

    #crear la gráfica de barras
    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align='center')
    #personalizar la grafica
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)
    #ajustar el espaciado entre las barras
    plt.subplots_adjust(bottom=0.3)
    #guardar la grafica en un objeto BytesIO
    buffer_year = io.BytesIO()
    plt.savefig(buffer_year, format='png')
    buffer_year.seek(0)
    plt.close()

    #convertir la grafica base 64
    image_png = buffer_year.getvalue()
    buffer_year.close()
    graphic_year = base64.b64encode(image_png)
    graphic_year = graphic_year.decode('utf-8')


    genres = Movie.objects.values_list('genre', flat=True).distinct().order_by('genre') 
    movie_counts_by_genre = {}
    for genre in genres:
        if genre:
            movies_in_genre = Movie.objects.filter(genre=genre)
        else:
            movies_in_genre = Movie.objects.filter(genre__isnull=True)
            genre = 'None'
        count = movies_in_genre.count()
        movie_counts_by_genre[genre] = count

    bar_positions = range(len(movie_counts_by_genre))

    #crear la gráfica de barras
    plt.bar(bar_positions, movie_counts_by_genre.values(), width=bar_width, align='center')
    #personalizar la grafica
    plt.title('Movies per genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_genre.keys(), rotation=90)
    #ajustar el espaciado entre las barras
    plt.subplots_adjust(bottom=0.3)
    #guardar la grafica en un objeto BytesIO
    buffer_genre = io.BytesIO()
    plt.savefig(buffer_genre, format='png')
    buffer_genre.seek(0)
    plt.close()

    #convertir la grafica base 64
    image_png = buffer_genre.getvalue()
    buffer_genre.close()
    graphic_genre = base64.b64encode(image_png)
    graphic_genre = graphic_genre.decode('utf-8')


    #renderizar la plantilla statistics.html con la grafica
    return render(request, 'statistics.html', {'graphic_year':graphic_year, 'graphic_genre':graphic_genre})

def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email':email})