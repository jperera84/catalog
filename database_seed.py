""" Database seed module """
from dao import insert_category, get_all_categories, update_category,\
                insert_item, insert_user, insert_favourite, get_all_users, get_user_by_email,\
                get_user_by_email_provider, insert_item, get_lates_items, get_items_by_category,\
                update_item
from database_setup import Category, User, Item, Favourite

#CATEGORY_1 = Category(category_name="Antiques", category_description="Antiques")
#insert_category(CATEGORY_1)
#CATEGORY_2 = Category(category_name="Appliances", category_description="Appliances")
#insert_category(CATEGORY_2)
#CATEGORY_3 = Category(category_name="Furniture", category_description="Furniture")
#insert_category(CATEGORY_3)
#CATEGORY_4 = Category(category_name="Jewelry", category_description="Jewelry")
#insert_category(CATEGORY_4)
#CATEGORY_5 = Category(category_name="Computers", category_description="Computers")
#insert_category(CATEGORY_5)
#CATEGORY_6 = Category(category_name="Cell Phones", category_description="Cell Phones")
#insert_category(CATEGORY_6)
#CATEGORY_7 = Category(category_name="Video Gaming", category_description="Video Gaming")
#insert_category(CATEGORY_7)
#CATEGORY_8 = Category(category_name="Electronics", category_description="Electronics")
#insert_category(CATEGORY_8)
#CATEGORY_9 = Category(category_name="Cars", category_description="Cars")
#insert_category(CATEGORY_9)
#CATEGORY_10 = Category(category_name="Collectibles", category_description="Collectibles")
#insert_category(CATEGORY_10)

#CATEGORY_11 = Category(category_name="Collectibles", category_description="Collectibles")
#update_category(10, CATEGORY_11)

#CATEGORIES = get_all_categories()
#for item in CATEGORIES:
#    print("Name: %s, Id: %s, Desc: %s") %(item.category_name,\
#                                          item.category_id, item.category_description)

#USER = User(user_name="Jose R. Perera", user_email="jpereramor@gmail.com",\
#            user_picture=None, user_provider="Google")
#insert_user(USER)

#USERS = get_all_users()

#for us in USERS:
    #print("Name: %s, Id: %s, Provider: %s Email: %s, Picture: %s") %(us.user_name, us.user_id, us.user_provider, us.user_email, us.user_picture)

#USERS = get_user_by_email("jpereramor@gmail.com")
#for us in USERS:
#    print("Name: %s, Id: %s") %(us.user_name, us.user_id)

#USER = get_user_by_email_provider("jpereramor@gmail.com", "Google")
#print("Name: %s, Id: %s") %(USER.user_name, USER.user_id)

#ITEM1 = Item(item_name="Keyboard",\
#             item_description="I have a really clean Cherry MX Mechanical keyboard with Brown switches",\
#             item_picture="https://en.wikipedia.org/wiki/Computer_keyboard#/media/File:QWERTY_keyboard.jpg",\
#             item_price=30.0, category_id=5, user_id=1)

#insert_item(ITEM1)

ITEMS = get_lates_items()

for Item in ITEMS:
    it = Item
    it.item_picture = "imgComp.jpg"
    update_item(Item.item_id, it)
