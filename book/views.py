import psycopg2
from django.shortcuts import render, get_object_or_404, redirect
from .models import Book
from django.http import JsonResponse
import requests
import re
from lxml import etree


def book_list(request):
    return render(request, 'book/book_list.html')


def book_spider(request):
    base_url = 'https://book.douban.com/top250'  # https://book.douban.com/top250?start=25   https://book.douban.com/top250?start=50

    all_book_list = []
    # 爬取top250数据信息
    for page in range(10):
        url = base_url + '?start={}'.format(page * 25)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        }
        response = requests.get(url=url, headers=headers)

        etree_html = etree.HTML(response.text)
        tr_item = etree_html.xpath('.//div[@class="indent"]//tr')

        for li in tr_item:
            # 书名
            title = li.xpath('.//div[@class="pl2"]/a//text()')
            book_title = ''.join([x.strip() for x in title])

            # 图片
            book_image = li.xpath('.//a[@class="nbg"]/img/@src')[0]

            # 作者/出版社/出版时间/定价
            cbs_pub = li.xpath('.//p[@class="pl"]/text()')[0].strip()
            cbs_pub = cbs_pub.split('/')
            # 作者
            author = ''.join(cbs_pub[:-3])
            # 出版社
            press = cbs_pub[-3]
            # 出版时间
            publication_time = cbs_pub[-2]
            # 定价
            book_price = cbs_pub[-1]

            # 评分
            star = li.xpath('.//div[@class="star clearfix"]/span[@class="rating_nums"]/text()')
            rating_nums = ''.join([x.strip() for x in star])

            # 评分的人数
            pl = li.xpath('.//div[@class="star clearfix"]/span[@class="pl"]/text()')
            rate_pl = re.findall(r'\d+', pl[0])[0] + '人评价'

            # 经典语录
            quote = li.xpath('.//p[@class="quote"]/span/text()')
            if quote:
                quotions = quote[0]
            else:
                quotions = ''

            book_item = {'book_title': book_title,
                         'author': author,
                         'book_image': book_image,
                         'publisher': press,
                         'publication_date': publication_time,
                         'price': book_price,
                         'rating': rating_nums,
                         'rating_count': rate_pl,
                         'quotes': quotions}
            all_book_list.append(book_item)
            # print(book_item)
    # print(all_book_list)

    connection = psycopg2.connect(
        host="localhost",
        database="douban",
        user="postgres",
        password="123456"
    )
    cursor = connection.cursor()

    for data in all_book_list:
        insert_query = """
            INSERT INTO books (title, author, image_url, publisher, publication_date, price, rating, rating_count, quotes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (title, author) DO NOTHING;
            """

        data_tuple = tuple(data.values())
        cursor.execute(insert_query, data_tuple)
        connection.commit()

    return JsonResponse(all_book_list, safe=False)
