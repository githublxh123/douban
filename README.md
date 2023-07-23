# Douban project

## python版本

- `python`: 3.11

##  启动

### 1.建库

建一个库名叫 douban

### 2.建表

sql="""
CREATE TABLE IF NOT EXISTS books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255),
    image_url TEXT,
    publisher VARCHAR(255),
    publication_date VARCHAR(20),
    price varchar(20),
    rating NUMERIC(3, 1),
    rating_count varchar(20),
    quotes TEXT
    );
    
CREATE UNIQUE INDEX uni_title_author ON books (title,author);

"""

### 3. 创建虚拟环境

setings  -->  项目  --->python解释器  ---> 添加本地解释器  ---> 新建环境

### 4. 导入环境

pip install -r requirements.txt

### 5. 数据迁移 

python manage.py migrate

### 6.运行命令启动

python manage.py runserver   

### 7.访问 http://127.0.0.1:8000/book/book_list/

点击按钮时(等待1～2s)，程序自动抓取豆瓣读书TOP250的数据，进行数据清洗并提取关键信息，将信息保存到数据库中，并以列表的形式展示。

### 8.创建admin的账号用户

python manage.py createsuperuser

示例：
Username (leave blank to use 'your_default_username'): admin
Email address: 
Password: admin
Password (again): admin
Superuser created successfully.

### 9.访问 http://127.0.0.1:8000/admin/book/book/

展示爬取的数据，并可以进行CRUD

