from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger,  Paginator
from .choices import price_choices, bedroom_choices, state_choices
from .models import Listing, Comment
from django.contrib import messages



def index(request):
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)
    
    """отвечает цифра за количество показанных объектов на страничке"""
    paginator = Paginator(listings, 6)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    context = {
        'listings': paged_listings
    }

    return render(request, 'listings/listings.html', context)

def ascending(request):
    listings = Listing.objects.order_by('price').filter(is_published=True)
    
    """отвечает цифра за количество показанных объектов на страничке"""
    paginator = Paginator(listings, 6)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    context = {
        'listings': listings
    }

    return render(request, 'listings/listings.html', context)

def descending(request):
    listings = Listing.objects.order_by('-price').filter(is_published=True)
    
    """отвечает цифра за количество показанных объектов на страничке"""
    paginator = Paginator(listings, 6)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    context = {
        'listings': listings
    }

    return render(request, 'listings/listings.html', context)


def listing(request, listing_id ):
    listing = get_object_or_404(Listing, pk=listing_id)
    comments = Comment.objects.order_by('-id').filter(listing_id=listing_id)

    paginator = Paginator(comments, 6)
    page = request.GET.get('page')
    paged_comments = paginator.get_page(page)


    context = {
        'listing': listing,
        'comments': comments
    }

    return render(request, 'listings/listing.html', context)
               

#ПОИСК
def search(request):
    queryset_list = Listing.objects.order_by('-list_date')

    # Keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(description__icontains=keywords)

    # City
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_list = queryset_list.filter(city__iexact=city)

    # State
    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            queryset_list = queryset_list.filter(state__iexact=state)

    # Bedrooms
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)

    # Price
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            queryset_list = queryset_list.filter(price__lte=price)


    context = {
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'listings': queryset_list,
        'values': request.GET,
    }

    return render(request, 'listings/search.html', context)

def comment(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        body = request.POST['body']
        user_id = request.POST['user_id']

        comment = Comment(listing=listing, listing_id=listing_id, name=name, email=email, body=body, user_id=user_id)

        comment.save()

        comments = Comment.objects.order_by('-id').filter(listing_id=listing_id)

        messages.success(request, 'Your review has been added')

        return redirect('/listings/'+listing_id, {'comments':comments})
