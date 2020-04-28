import json
import requests


def main():
    item_names = get_item_names()
    while True:
        my_search = input("Enter item name (or exit to close): \n")
        #my_search = my_search.lower()
        if my_search == "exit":
            exit()
        found_item = search_the_dict(item_names, my_search)
        if found_item == False:
            pass
        else:
            for item in found_item:
                found_item_name = item
                found_item_code = found_item[item]
            item_rarity = choose_rarity()
            print(f"\nDisplaying results for {found_item_name}: \n")
            get_market_data(found_item_code, item_rarity)


def search_the_dict(names_dict, search):
    found_items = {}
    search = search.replace("'", "")
    # Iterate through whole dictionary
    if search[0] == '"' and search[-1] == '"':
        search = search.replace('"','')
        for x in names_dict:
            if search == x:
                found_items[x] = names_dict[x]
                return found_items
            elif search.lower() == x.lower():
                found_items[x] = names_dict[x]
                return found_items
        print(f"\nNothing found: {search}\n")
        return False
    search = search.lower()
    for x in names_dict:
        # Checks if searched item full name equals to any entry in the items data, returns item if true
        if search.lower() == x.lower():
            found_items[x] = names_dict[x]
            return found_items
        # Checks if full searched name is partial match of an items data entry item, adds it to found items if true, but it does not stop searching for other partial matches 
        elif search.lower() in x.lower():
            found_items[x] = names_dict[x]
        found_word = search_by_word(search.lower(), x.lower())
        if found_word != False:
            found_items[x] = names_dict[x]
    # If no items are found, prints the string below
    if len(found_items) == 0:
        print(f"\nNothing found: {search}\n")
        return False
    elif len(found_items) > 1:
        return choose_item(found_items)
    else:
        return found_items


def search_by_word(search, data_item):
    word_list = search.split(" ")
    found_items = []
    for word in word_list:
        if word in data_item:
            found_items.append(data_item)
    if len(found_items) != 0 and len(found_items) == len(word_list):
        return found_items[0]
    else:
        return False


def choose_item(found_items):
    found_items_list = []
    my_item = {}
    for item in found_items:
        found_items_list.append(item)
    i = 0
    for item in found_items_list:
        print(f"{i}: {item}")
        i += 1
    while True:
        chosen_item = input("Choose your item, by selecting the corresponding number: ")
        try:
            chosen_item = int(chosen_item)
            if chosen_item >= 0 and chosen_item < len(found_items_list):
                break
            else:
                print("Choose a number on the list.")
        except:
            print("You need to enter a number.")
    print(found_items_list[chosen_item])
    my_item[found_items_list[chosen_item]] = found_items[found_items_list[chosen_item]]
    return my_item


def get_item_names():
    item_names = {}
    response = requests.get("https://raw.githubusercontent.com/broderickhyman/ao-bin-dumps/master/formatted/items.json")
    content = response.json()
    for item in content:
        if "LocalizedNames" in item and item["LocalizedNames"] != None:
            name = item["LocalizedNames"]["EN-US"]
            name = name.replace("'", "")
            code = item["UniqueName"]
            if name not in item_names.keys():
                item_names[name] = code
    return item_names


def get_item_names2():
    item_names = {}
    with open("./items.json", encoding="utf8") as json_file:
        content = json.load(json_file)
        for item in content:
            if "LocalizedNames" in item and item["LocalizedNames"] != None:
                name = item["LocalizedNames"]["EN-US"]
                name = name.replace("'", "")
                code = item["UniqueName"]
                if name not in item_names.keys():
                    item_names[name] = code
        return item_names


def choose_rarity():
    rarities = [0, 1, 2, 3]
    while True:
        item_rarity = input("\nSelect item rarity (Number between 0 and 3): \n")
        try:
            item_rarity = int(item_rarity)
            if item_rarity in rarities:
                return item_rarity+1
            else:
                print("Number is not between 0 and 3!")
        except:
            print("You need to enter a number!")


def get_market_data(item, rarity):
    response = requests.get(f"https://www.albion-online-data.com/api/v2/stats/prices/{item}?qualities={rarity}")
    content = response.json()
    cities = ["Bridgewatch", "Martlock", "Lymhurst", "Fort Sterling", "Thetford"]
    prices = 0
    num_of_cities = 0
    for item in content:
        if item["city"] in cities:
            item_price = item["sell_price_min"]
            city = item["city"]
            print(f"{city}: {item_price}")
            if item_price != 0:
                num_of_cities += 1
                prices += item_price
        else:
            item_price = item["sell_price_min"]
            city = item["city"]
            print(f"{city}: {item_price}")
    if prices != 0:
        average = prices/num_of_cities
        print(f"\nAverage price in royal cities: {average}")
    print("\n")


if __name__ == "__main__":
    main()