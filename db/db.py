import psycopg
from psycopg import sql
from dotenv import load_dotenv
import os
import traceback


# Load environment variables from .env file
load_dotenv(os.path.join(os.getcwd(), ".env"))


# Database connection parameters
db_params = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
}

# sites
CS_VAPE = "CS_VAPE"
GETPOP = "GETPOP"
MY_VAPOR_STORE = "MY_VAPOR_STORE"
PERFECT_VAPE = "PERFECT_VAPE"
VAPE_DOT_COM = "VAPE.COM"
VAPE_SOURCING = "VAPE_SOURCING"
VAPE_WH = "VAPE_WH"
VAPING_DOT_COM = "VAPING.COM"
ELEMENT_VAPE = "ELEMENT_VAPE"
MIPOD = "MIPOD"



def product_exists(site_name, site_tag):
    try:
        connection = psycopg.connect(**db_params)
        cursor = connection.cursor()
        query = sql.SQL("""
            SELECT html
            FROM ecig_product
            WHERE site_name = %s AND site_tag = %s
        """)
        cursor.execute(query, (site_name, site_tag))
        val = cursor.fetchone() is not None
    except Exception as error:
        print(f"Error: {error}")
        traceback.print_exc()
        val = False
    finally:
        if cursor:
            cursor.close()
        if connection:  
            connection.close()
    return val


def map_product_data(site, data):
    try:

        connection = psycopg.connect(**db_params)
        cursor = connection.cursor()

        product_data = {}

        product_data = {
            'product_name': data.get('title', None),
            'site_name': site,
            'url': data.get('link', None),
            'site_category': data.get('site_category', None),
            'site_tag': data['tag'],
            'sku': None,
            'brand': data.get('brand', None),
            'html': data['html'],
            'plain_text': data.get('plain_text', None),
            'price': data.get('regular_price', None),
            'price_sale': data.get('sale_price', None),
            'flavor_text': data.get('flavor_text', None),
            'description': data.get('description', None),
            'package_contents': data.get('package_contents', None),
            'features': data.get('features', None),
            'ingredients': data.get('ingredients', None),
            'warnings': data.get('warnings', None),
            'eliquid_contents': data.get('eliquid_contents', None),
            'puffs': data.get('puffs', None),
            'coil': data.get('coil', None),
            'battery_text': data.get('battery', None),
            'power_level': data.get('power_level', None),
            'nicotine_level_text': data.get('nicotine_strength', None),
            'stock_status': data.get('stock_status', None),    
        }  
        # Insert into ecig_product and get the product_id
        product_id = insert_ecig_product(cursor, product_data)

        # Insert into other tables
        # insert_ecig_product_attributes(cursor, attributes_data)
        if len(data.get('reviews', [])) > 0:
            insert_reviews_to_postgres(data.get('reviews', []), product_id, cursor)

        if len(data.get('review_attributes', {}).keys()) > 0:
            insert_review_attributes_to_postgres(cursor, data.get('review_attributes', {}), product_id)
        if len(data.get('flavor_list', [])) > 0:
            for flavor in data.get('flavor_list', []):
                flavor_data = {
                    'product_id': product_id,
                    'flavor_name': flavor,
                    'flavor_description': None,
                    'flavor_category': None,
                    'iced_bool': None,
                    'cbd_bool': None,
                }
                insert_ecig_flavors(cursor, flavor_data)
        if len(data.get('nicotine_strengths', [])) > 0:
            for strength in data.get('nicotine_strengths', []):
                nicotine_level_data = {
                    'product_id': product_id,
                    'value': strength.get('value', None),
                    'unit': strength.get('unit', None),
                    'level': strength.get('level', None),
                }
                insert_ecig_nicotine_levels(cursor, nicotine_level_data)
        if len(data.get('images', [])) > 0:
            for image in data.get('images', []):
                image_data = {
                    'product_id': product_id,
                    'url': image.get('url', None),
                    'path': image.get('path', None),
                    'title': image.get('title', None),
                    'alt_text': image.get('alt', None),
                }
                insert_ecig_images(cursor, image_data)

        # Commit the transaction
        connection.commit()
        print("Data inserted successfully!")

    except Exception as error:
        print(f"map_product_data Error: {error}")
        traceback.print_exc()
        if connection:
            connection.rollback()
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def get_products(site_name):
    results = []
    try:
        connection = psycopg.connect(**db_params)
        cursor = connection.cursor()

        # The SQL query with a parameter placeholder for site_name
        query = """
        select ep.id as product_id, ep.html, ep.site_tag from ecig_product ep 
        where ep.site_name = %s
        order by 
            case when ep.site_category ilike %s
            then 1
            when ep.site_category ilike %s
            then 2
            else 3
            end, site_tag
        """

        # Execute the query with the site_name parameter
        cursor.execute(query, (site_name, '%disposable%', '%liquid%'))

        # Fetch all the results
        results = cursor.fetchall()
    except Exception as error:
        print(f"Error: {error}")
        traceback.print_exc()
        if connection:
            connection.rollback()
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    return results


def get_products_without_reviews(site_name):
    results = []
    try:
        connection = psycopg.connect(**db_params)
        cursor = connection.cursor()

        # The SQL query with a parameter placeholder for site_name
        query = """
        select er.id as review_id, ep.id as product_id, ep.html, ep.site_tag from ecig_product ep 
        left outer join ecig_reviews er 
        on ep.id = er.product_id
        where er.id is null
        and ep.site_name = %s
        order by 
            case when ep.site_category ilike %s
            then 1
            when ep.site_category ilike %s
            then 2
            else 3
            end,
            ep.id
        """

        # Execute the query with the site_name parameter
        cursor.execute(query, (site_name, '%disposable%', '%liquid%'))

        # Fetch all the results
        results = cursor.fetchall()


    except Exception as error:
        print(f"Error: {error}")
        traceback.print_exc()
        if connection:
            connection.rollback()
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    return results


def insert_review_attributes(review_attributes_dict, product_id):
    try:
        connection = psycopg.connect(**db_params)
        cursor = connection.cursor()
        insert_review_attributes_to_postgres(cursor, review_attributes_dict, product_id)

        # Commit the transaction
        connection.commit()
        print("Data inserted successfully!")

    except Exception as error:
        print(f"Error: {error}")
        traceback.print_exc()
        if connection:
            connection.rollback()
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def insert_review_attributes_to_postgres(cursor, review_attributes_dict, product_id):
    """
    Insert review attributes for a product into the ecig_review_attributes table.
    
    Args:
        cursor: PostgreSQL database cursor
        product_id: ID of the product the attributes belong to
        review_attributes_dict: Dictionary where keys are review_attribute_question and values are review_attribute_value
    
    Returns:
        List of IDs of the inserted records
    """
    inserted_ids = []
    
    for question, value in review_attributes_dict.items():
        query = """
        INSERT INTO public.ecig_review_attributes 
        (product_id, review_attribute_question, review_attribute_value) 
        VALUES (%s, %s, %s)
        ON CONFLICT (product_id, review_attribute_question) DO NOTHING
        RETURNING id;
        """
        
        # Execute the query with parameters
        cursor.execute(query, (product_id, question, value))
        
        # Get the ID of the inserted record
        inserted_row = cursor.fetchone()
        if inserted_row:        
            # If a record was inserted, get its ID
            inserted_id = inserted_row[0]
            inserted_ids.append(inserted_id)
    
    return inserted_ids


def insert_reviews(reviews, product_id): 
    try:
        connection = psycopg.connect(**db_params)
        cursor = connection.cursor()
        insert_reviews_to_postgres(reviews, product_id, cursor)

        # Commit the transaction
        connection.commit()
        print("Data inserted successfully!")

    except Exception as error:
        print(f"Error: {error}")
        traceback.print_exc()
        if connection:
            connection.rollback()
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def insert_reviews_to_postgres(reviews, product_id, cursor) -> None:
    """
    Insert reviews and their attributes into PostgreSQL database.
    
    Args:
        reviews: List of review dictionaries from the parser
        product_id: ID of the product these reviews belong to
        connection_params: Database connection parameters
    """
    skipped_count = 0
    for review in reviews:
        check_query = """
            SELECT id FROM public.ecig_reviews 
            WHERE product_id = %s 
            AND (author = %s)
            AND (review_date = %s)
            AND (review_text = %s)
            LIMIT 1;
            """

        # Insert review data
        insert_review_query = """
            INSERT INTO public.ecig_reviews
            (product_id, review_date, rating, author, verified, review_text, variant, sweet_level, iced_level)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (review_date, author, variant, rating) DO NOTHING
            RETURNING id;
            """
        
        # Convert review date string to date object if present
        review_date = review.get('date')
        author = review.get('author')
        content = review.get('review_text')
        sweet_level = review.get('sweet_level')
        iced_level = review.get('iced_level')
            
        cursor.execute(
            check_query, 
            (
                product_id,
                author,
                review_date,
                content
            )
        )
        
        existing_review = cursor.fetchone()
        
        if existing_review:
            # Review already exists, skip it
            print(f"Skipping duplicate review by {author}")
            skipped_count += 1
            continue
        

        cursor.execute(
            insert_review_query, 
            (
                product_id,
                review_date,
                review.get('rating'),
                author,
                review.get('verified_buyer', False),
                content,
                review.get('variant'),
                sweet_level,
                iced_level
            )
        )
        
        # Get the ID of the newly inserted review
        review_row = cursor.fetchone()
        if review_row:
            review_id = review_row[0]
        else:       
            # If no review was inserted, use a default value
            print(f"Review not inserted for {author}")  
            review_id = None
        
        # Insert review attributes if they exist
        if 'attributes' in review and review['attributes']:
            for attr_name, attr_value in review['attributes'].items():
                insert_attr_query = """
                INSERT INTO public.ecig_review_attributes
                (product_id, review_id, review_attribute_question, review_attribute_value)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (product_id, review_attribute_question) DO NOTHING;
                """
                
                # Convert attribute value to string if needed
                attr_value_str = str(attr_value) if attr_value is not None else None
                
                cursor.execute(
                    insert_attr_query,
                    (
                        product_id,
                        review_id,
                        attr_name,
                        attr_value_str
                    )
                )
        



def insert_ecig_product(cursor, product_data):
    query = sql.SQL("""
        INSERT INTO ecig_product (
            product_name, site_name, url, site_category, site_tag, sku,
            brand, html, plain_text, price, price_sale, flavor_text, description,
            package_contents, ingredients, warnings, 
            eliquid_contents, puffs, coil,  battery_text, power_level,
            nicotine_level_text, stock_status, features
        )
        VALUES (
            %(product_name)s, %(site_name)s, %(url)s, %(site_category)s, %(site_tag)s, %(sku)s,
            %(brand)s, %(html)s, %(plain_text)s, %(price)s, %(price_sale)s, %(flavor_text)s, %(description)s,
            %(package_contents)s, %(ingredients)s, %(warnings)s, 
            %(eliquid_contents)s, %(puffs)s, %(coil)s,  %(battery_text)s, %(power_level)s,
            %(nicotine_level_text)s, %(stock_status)s, %(features)s
        )
        RETURNING id;
    """)
    cursor.execute(query, product_data)
    return cursor.fetchone()[0]


def insert_ecig_product_attributes(cursor, attributes_data):
    query = sql.SQL("""
        INSERT INTO ecig_product_attributes (
            product_id, total_ounces_per_ml, product_category, screen_bool, disposable_bool,
            rechargeable_bool, battery_bool, usb_bool, adjustable_bool,
            tfn_bool, nic_free_bool
        )
        VALUES (
            %(product_id)s, %(total_ounces_per_ml)s, %(product_category)s, %(screen_bool)s, %(disposable_bool)s,
            %(rechargeable_bool)s, %(battery_bool)s, %(usb_bool)s, %(adjustable_bool)s,
            %(tfn_bool)s, %(nic_free_bool)s
        );
    """)
    cursor.execute(query, attributes_data)


def insert_ecig_flavors(cursor, flavors_data):
    query = sql.SQL("""
        INSERT INTO ecig_flavors (
            product_id, flavor_name, flavor_description, flavor_category, iced_bool, cbd_bool
        )
        VALUES (
            %(product_id)s, %(flavor_name)s, %(flavor_description)s, %(flavor_category)s, %(iced_bool)s, %(cbd_bool)s
        );
    """)
    cursor.execute(query, flavors_data)


def insert_ecig_nicotine_levels(cursor, nicotine_levels_data):
    query = sql.SQL("""
        INSERT INTO ecig_nicotine_levels (
            product_id, value, unit, level
        )
        VALUES (
            %(product_id)s, %(value)s, %(unit)s, %(level)s
        );
    """)
    cursor.execute(query, nicotine_levels_data)


def insert_ecig_images(cursor, images_data):
    query = sql.SQL("""
        INSERT INTO ecig_images (
            product_id, url, path, title, alt_text
        )
        VALUES (
            %(product_id)s, %(url)s, %(path)s, %(title)s, %(alt_text)s
        );
    """)
    cursor.execute(query, images_data)
