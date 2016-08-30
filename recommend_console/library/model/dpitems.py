from scrapy.item import Item, Field

class UserItem(Item):
    name = Field()
    user_url = Field()

class RestaurantItem(Item):
    name = Field()
    type = Field()
    scores = Field()
    score_times = Field()
    location = Field()
    address = Field()
    telephone = Field()
    price = Field()
    level = Field()
    shop_url = Field()
    image_url = Field()
    comment = Field()
    
class FoodItem(Item):
    name = Field()
    price = Field()
    recommend_times = Field()
    food_url = Field()
    image_url = Field()
    restaurant_id = Field()
    
class UserRestaurantItem(Item):
    user_id = Field()
    restaurant_id = Field()
    score = Field()
    comment = Field()