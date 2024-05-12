from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse
from technews.models import NewsPost
#from urllib.parse import urljoin

# Add the necessary imports for scraping and 
import requests
from bs4 import BeautifulSoup

#Pagination
from django.core.paginator import Paginator

# Create your views here.

def x(request):
    try:
        # Get the most recent post
        recent_post = NewsPost.objects.latest('date_added')
        # Get all posts except the most recent one
        other_posts = NewsPost.objects.exclude(pk=recent_post.pk)[:15]
    except NewsPost.DoesNotExist:
        raise Http404("BlogPost does not exist")


    context = {
        'recent_post': recent_post,
        'other_posts': other_posts,
    }

    return render(request, 'technews/index.html', context)

def home(request):
    all_posts = NewsPost.objects.all()
    paginator = Paginator(all_posts, 10)  # Change 10 to the number of items per page you want
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'technews/index.html', {'page_obj': page_obj})

def news(request, slug):
    try:
        post = NewsPost.objects.get(slug=slug)
    except NewsPost.DoesNotExist:
        raise Http404("BlogPost does not exist")

    post = NewsPost.objects.get(slug=slug)
    context={'post':post}
    return render(request, 'technews/newscontent.html', context)



def scrape():
    scraped_dict={}
    url = "https://www.techcrunch.com"
    res = requests.get(url)

    soup=BeautifulSoup(res.content, "html.parser")

    latest=soup.find(class_='wp-block-tc23-post-picker-group rapid-read-enabled rapid-read-date')

    #number of articles
    no_of_articles=0
    articles=latest.find_all('div',class_='wp-block-tc23-post-picker')
    for article in articles:
        no_of_articles+=1

    #article title
    article_title=latest.find_all('h2', class_='wp-block-post-title')

    #article authors
    article_authors=latest.find_all('div', class_="wp-block-tc23-author-card-name")

    #article Description
    article_desc=latest.find_all('p', class_='wp-block-post-excerpt__excerpt')

    #article small image url
    article_image_url_small=latest.find_all('figure',class_="wp-block-post-featured-image")

    #======================================================================================


    for article in range(no_of_articles):
        #list of content for each article
        each_article=[]

        #=======================
        #inserting article title
        each_article.append(article_title[article].find('a').get_text().strip())
        scraped_dict[article]=each_article

        #=========================
        #inserting article authors
        authors_list=[]
        if article < len(article_authors):
            for author in article_authors[article].find_all('a'):
                authors_list.append(author.get_text().strip())
            scraped_dict[article].append(", ".join(authors_list))
        else:
            # Handle the case where there are no authors listed for the article
            scraped_dict[article].append("No author listed")

        #=============================
        #inserting article description
        each_article.append(article_desc[article].get_text().strip())
        scraped_dict[article]=each_article

        #=================================
        #inserting article small image url
        if article < len(article_image_url_small):
            image_url = article_image_url_small[article].find('img')['src']
            each_article.append(image_url)
        else:
            # Handle the case where there is no small image URL for the article
            each_article.append("No image available")
        #scraped_dict[article].append(article_image_url_small[article].findChildren('img')[0]['src'])


        #================== ++ FULL CONTENT OF ARTICLE URL
        #=================== ++
        #article url content
        url_link= article_title[article].find('a')['href']
        scraped_dict[article].append(url_link)


        res_content = requests.get(url_link)
        soup_cont = BeautifulSoup(res_content.content, "html.parser")
        #lar_image = soup_cont.find(class_='wp-block-group single-post__content has-global-padding is-layout-constrained wp-block-group-is-layout-constrained')
        lat_cont = soup_cont.find('div', class_='wp-block-post-content') #-->All the Article content
        #cont = lat_cont.find_all('p')
        

        #insert the article full content
        all_text = lat_cont.prettify()
        scraped_dict[article].append(all_text)

    # After scraping, check for duplicates before saving

    for article in scraped_dict.values():
        title = article[0]
        # Check if an article with this title already exists
        if not NewsPost.objects.filter(title=title).exists():
            desc = article[2]
            url = article[4]
            author = article[1]
            body = article[5]
            image1 = article[3]
            #image2 = article[5]
            ''''
            base_url = 'https://www.techcrunch.com/'  # Replace with your base URL
            image1 = urljoin(base_url, article[1])
            image2 = urljoin(base_url, article[5])
            '''
            # Create and save the Post object
            post = NewsPost(title=title, desc=desc, url=url, author=author, body=body, image1=image1)
            post.save()
