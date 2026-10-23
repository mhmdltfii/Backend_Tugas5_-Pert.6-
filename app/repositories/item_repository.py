items = [
    {"id": 1, "name": "Keripik Pisang", "category": "Makanan", "price": 15000, "stock": 20, "active": True},
    {"id": 2, "name": "Kopi Banyuwangi", "category": "Minuman", "price": 25000, "stock": 15, "active": True},
    {"id": 3, "name": "Batik Banyuwangi", "category": "Kerajinan", "price": 85000, "stock": 10, "active": True},
    {"id": 4, "name": "Kue Bagiak", "category": "Makanan", "price": 20000, "stock": 18, "active": True},
    {"id": 5, "name": "Teh Herbal", "category": "Minuman", "price": 18000, "stock": 12, "active": True},
    {"id": 6, "name": "Tas Anyaman", "category": "Kerajinan", "price": 50000, "stock": 8, "active": True},
    {"id": 7, "name": "Sambal Pecel", "category": "Makanan", "price": 12000, "stock": 25, "active": True},
    {"id": 8, "name": "Madu Asli", "category": "Minuman", "price": 45000, "stock": 10, "active": True}
]


def get_all():
    return items


def get_by_id(item_id):
    for item in items:
        if item["id"] == item_id:
            return item
    return None


def create(name, category, price, stock, active=True):
    new_id = max([i["id"] for i in items], default=0) + 1

    item = {
        "id": new_id,
        "name": name,
        "category": category,
        "price": price,
        "stock": stock,
        "active": active
    }

    items.append(item)
    return item


def update(item_id, data):
    item = get_by_id(item_id)

    if item:
        item.update(data)

    return item


def delete(item_id):
    item = get_by_id(item_id)

    if item:
        items.remove(item)
        return True

    return False

