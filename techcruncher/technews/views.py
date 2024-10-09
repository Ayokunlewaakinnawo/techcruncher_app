from turtle import title
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
    full_url = request.build_absolute_uri()

    #print(full_url)
    try:
        post = NewsPost.objects.get(slug=slug)
        post_title = post.title 

    except NewsPost.DoesNotExist:
        raise Http404("BlogPost does not exist")

    post = NewsPost.objects.get(slug=slug)
    context={'post':post,
             'full_url':full_url,
             'post_title':post_title
             }
    return render(request, 'technews/newscontent.html', context)



def scrape():
    scraped_dict={}
    url = "https://www.techcrunch.com"
    res = requests.get(url)

    soup=BeautifulSoup(res.content, "html.parser")

    latest=soup.find(class_='wp-block-post-template is-layout-flow wp-block-post-template-is-layout-flow')

    #number of articles

    no_of_articles=0
    articles=latest.find_all('li',class_='wp-block-post')
    for article in articles:
        no_of_articles+=1


    #article title
    article_title=latest.find_all('h3', class_='loop-card__title')


    #article authors
    article_authors=latest.find_all('div', class_="loop-card__meta")

    #article Description
    #article_desc=latest.find_all('p', class_='wp-block-post-excerpt__excerpt')


    #article small image url
    article_image_url_small=latest.find_all('figure',class_="loop-card__figure")

    #print(article_image_url_small)
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
        #Getting the url for each article to get first paragraph article description
        url_link= article_title[article].find('a')['href']
        res_content = requests.get(url_link)
        soup_cont = BeautifulSoup(res_content.content, "html.parser")
        lat_cont = soup_cont.find('div', class_='entry-content wp-block-post-content is-layout-constrained wp-block-post-content-is-layout-constrained') #-->All the Article content

        if lat_cont:
            # Find all paragraphs within the article content
            art_desc = lat_cont.find_all('p', id='speakable-summary')
            
            # Initialize an empty string to store the article description
            article_text = ""
            
            # Concatenate the text from each paragraph
            for paragraph in art_desc:
                article_text += paragraph.get_text().strip() + " "
            
            # Append the article description to each_article
            each_article.append(article_text.strip())
            
            # Add the data to the scraped dictionary
            scraped_dict[article] = each_article
        #=============================
        #inserting article description
        #each_article.append(article_desc[article].get_text().strip())
        #scraped_dict[article]=each_article
        


        #=================================
        #inserting article small image url
        scraped_dict[article].append(article_image_url_small[article].findChildren('img')[0]['src'])




        #================== ++ FULL CONTENT OF ARTICLE URL
        #=================== ++
        #article url content
        url_link= article_title[article].find('a')['href']
        scraped_dict[article].append(url_link)


        res_content = requests.get(url_link)
        soup_cont = BeautifulSoup(res_content.content, "html.parser")
        #lar_image = soup_cont.find(class_='wp-block-group single-post__content has-global-padding is-layout-constrained wp-block-group-is-layout-constrained')
        lat_cont = soup_cont.find('div', class_='entry-content wp-block-post-content is-layout-constrained wp-block-post-content-is-layout-constrained') #-->first para the Article content

        #scraped_dict[article].append(art_desc.get_text().strip())


        #article large image url
        #article_image_url=lar_image.find_all('figure', class_="wp-block-post-featured-image")

        #inserting article Large Image
        #im_url=""
        #for img_element in article_image_url:
            #im_url = img_element.find('img')['src']
        #scraped_dict[article].append(im_url)


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
