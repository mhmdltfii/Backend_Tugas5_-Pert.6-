from app.repositories import category_repository
from app.repositories import item_repository as repo


def get_all():
    return repo.get_all()


def get_by_id(item_id):
    return repo.get_by_id(item_id)


def validate(data, partial=False):
    if not isinstance(data, dict):
        return None, "Data JSON wajib berupa objek"

    if not partial:
        # Pengecekan field wajib yang fleksibel untuk category / category_id
        if "name" not in data or "price" not in data:
            return None, "Field name dan price wajib diisi"
        if "category_id" not in data and "category" not in data:
            return None, "Field category atau category_id wajib diisi"

    result = {}

    if "name" in data:
        name = data["name"]
        if not isinstance(name, str) or not name.strip():
            return None, "Nama barang wajib diisi"
        result["name"] = name.strip()

    if "price" in data:
        price = data["price"]
        if type(price) not in [int, float] or price < 0:
            return None, "Harga harus berupa angka nonnegatif"
        result["price"] = int(price)

    if "stock" in data:
        stock = data["stock"]
        if type(stock) is not int or stock < 0:
            return None, "Stok harus berupa bilangan bulat nonnegatif"
        result["stock"] = stock

    if "active" in data:
        result["active"] = bool(data["active"])

    # Penanganan category_id maupun category nama string
    if "category_id" in data:
        category_id = data["category_id"]
        if type(category_id) is not int or category_id <= 0:
            return None, "category_id harus berupa bilangan bulat positif"

        category = category_repository.get_by_id(category_id)
        if category is None:
            return None, "Kategori tidak ditemukan"

        result["category_id"] = category_id
        result["category"] = category["name"]

    elif "category" in data:
        cat_name = str(data["category"]).strip()
        if not cat_name:
            return None, "Kategori tidak boleh kosong"
        
        # Cari category_id berdasarkan nama jika ada
        all_cats = category_repository.get_all()
        found_cat = next((c for c in all_cats if c["name"].lower() == cat_name.lower()), None)
        
        result["category"] = cat_name
        if found_cat:
            result["category_id"] = found_cat["id"]

    return result, None


def create(data):
    values, error = validate(data)

    if error:
        return None, error

    item = repo.create(
        values["name"],
        values.get("category", "Umum"),
        values["price"],
        values.get("stock", 0),
        values.get("active", True)
    )

    return item, None


def update(item_id, data):
    if repo.get_by_id(item_id) is None:
        return None, "Barang tidak ditemukan"

    values, error = validate(data, partial=True)

    if error:
        return None, error

    if not values:
        return None, "Minimal satu field harus diperbarui"

    return repo.update(item_id, values), None


def delete(item_id):
    if repo.get_by_id(item_id) is None:
        return False

    return repo.delete(item_id)