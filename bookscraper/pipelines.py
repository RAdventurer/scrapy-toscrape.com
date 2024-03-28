# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != 'description':
                value = adapter.get(field_name)

                adapter[field_name] = value[0].strip()

                
                
                
        lowercase_keys = ['category', 'product_type']
        for lowery in lowercase_keys:
            value = adapter.get(lowery)
            adapter[lowery] = value.lower()
            
            
            
        price_keys = ['price', 'price_excl_tax', 'price_incl_tax', 'tax']
        for price in price_keys:
            value = adapter.get(price)
            value = value.replace('£','')           
            adapter[price] = float(value)
            
            
            
            
            
        availab_str = adapter.get('availability')
        split_str =availab_str.split('(')
        if len (split_str) < 2: 
            adapter['availability'] = 0
        else:
            availab_array = split_str[1].split(' ')
            adapter['availability'] = int(availab_array[0])         
        
        
        
        
        
        nbr_reviews = adapter.get('num_reviews')
        adapter['num_reviews'] = int (nbr_reviews)
        
   #  'stars': 'star-rating Three'  
        stars_mapping = {
            'Zero':0,
            'One': 1,
            'Two': 2,
            'Three': 3,
            'Four': 4,
            'Five': 5
        }

        # Extract the star rating from the item
        star_text = adapter.get('stars')  # Assuming 'stars' is the key for the star rating
        words = star_text.split()
    # Search for words representing star ratings in the text
        for word in words:
            if word in stars_mapping:
                
                numeric_star = stars_mapping[word]
        adapter['stars'] = int(numeric_star)
            
            
    
        return item

import mysql.connector

class Savetmysqlpip:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='rootr',
            database='books'
        )
        self.cur = self.conn.cursor()

        # Create the table if it doesn't exist
        self.create_table()

    def create_table(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INT AUTO_INCREMENT PRIMARY KEY,
                url VARCHAR(255),
                title VARCHAR(255),
                upc VARCHAR(255),
                product_type VARCHAR(255),
                price_excl_tax DECIMAL(10, 2),
                price_incl_tax DECIMAL(10, 2),
                tax DECIMAL(10, 2),
                price DECIMAL(10, 2),
                availability INT,
                num_reviews INT,
                stars INT,
                category VARCHAR(255),
                description TEXT
            )
        """)
        self.conn.commit()

    def process_item(self, item, spider):
        self.cur.execute("""
            INSERT INTO books (
                url, title, upc, product_type, price_excl_tax,
                price_incl_tax, tax, price, availability, num_reviews,
                stars, category, description
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            item['url'],
            item['title'],
            item['upc'],
            item['product_type'],
            item['price_excl_tax'],
            item['price_incl_tax'],
            item['tax'],
            item['price'],
            item['availability'],
            item['num_reviews'],
            item['stars'],
            item['category'],
            item['description'][0] if item['description'] else None
        ))
        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

