from collections import Counter
from app.firestore_service import get_places
places_result = list()
result_list = list()
places_from_db = get_places()
def sort_places(answer):
    for place in places_from_db:
    #MONEY
        if place.to_dict().get("money") == answer.get("money"):
            places_result.append(place)
    #AGE
        if place.to_dict().get("age") == answer.get("money"):
            places_result.append(place)
    #MOOD
        if place.to_dict().get("mood") == answer.get("mood"):
            places_result.append(place)
    #MUSIC
        if place.to_dict().get("music") == answer.get("music"):
            places_result.append(place)
    #DRINK
        if place.to_dict().get("drink") == answer.get("drink"):
            places_result.append(place)
    #FOOD
        if place.to_dict().get("food") == answer.get("food"):
            places_result.append(place)
    #DRESS
        if place.to_dict().get("dress") == answer.get("dress"):
            places_result.append(place)

    c = Counter(places_result)
    first_three = c.most_common(3)
    for item in first_three:
        result_list.append(item[0]) #the first item of the tuple ([place], counter)

    return result_list