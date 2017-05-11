""" Database seed module """
from dao import insert_category, get_all_categories
from database_setup import Category

CATEGORY_1 = Category(category_name="Antiques", category_description="Antiques")
insert_category(CATEGORY_1)
CATEGORY_2 = Category(category_name="Appliances", category_description="Appliances")
insert_category(CATEGORY_2)
CATEGORY_3 = Category(category_name="Furniture", category_description="Furniture")
insert_category(CATEGORY_3)
CATEGORY_4 = Category(category_name="Jewelry", category_description="Jewelry")
insert_category(CATEGORY_4)
CATEGORY_5 = Category(category_name="Computers", category_description="Computers")
insert_category(CATEGORY_5)
CATEGORY_6 = Category(category_name="Cell Phones", category_description="Cell Phones")
insert_category(CATEGORY_6)
CATEGORY_7 = Category(category_name="Video Gaming", category_description="Video Gaming")
insert_category(CATEGORY_7)
CATEGORY_8 = Category(category_name="Electronics", category_description="Electronics")
insert_category(CATEGORY_8)
CATEGORY_9 = Category(category_name="Cars", category_description="Cars")
insert_category(CATEGORY_9)
CATEGORY_10 = Category(category_name="Collectibles", category_description="Collectibles")
insert_category(CATEGORY_10)

CATEGORIES = get_all_categories()
for item in CATEGORIES:
    print("Name: %s, Id: %s, Desc: %s") %(item.category_name,\
                                          item.category_id, item.category_description)

