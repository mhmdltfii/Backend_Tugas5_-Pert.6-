categories = [
    {"id": 1, "name": "Makanan"},
    {"id": 2, "name": "Minuman"},
    {"id": 3, "name": "Kerajinan"}
]


def get_all():
    return categories


def get_by_id(category_id):
    for category in categories:
        if category["id"] == category_id:
            return category
    return None


def create(name):
    new_id = max(
        [category["id"] for category in categories],
        default=0
    ) + 1

    new_category = {
        "id": new_id,
        "name": name
    }

    categories.append(new_category)
    return new_category


def update(category_id, name):
    category = get_by_id(category_id)

    if category:
        category["name"] = name

    return category


def delete(category_id):
    category = get_by_id(category_id)

    if category:
        categories.remove(category)
        return True

    return False