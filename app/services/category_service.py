from app.repositories import category_repository as repo
from app.repositories import item_repository


def get_all():
    return repo.get_all()


def get_by_id(category_id):
    return repo.get_by_id(category_id)


def create(data):
    if not isinstance(data, dict):
        return None, "Data JSON wajib berupa objek"

    name = data.get("name")

    if not isinstance(name, str) or not name.strip():
        return None, "Nama kategori wajib diisi"

    name = name.strip()

    if any(
        c["name"].lower() == name.lower()
        for c in repo.get_all()
    ):
        return None, "Nama kategori sudah digunakan"

    return repo.create(name), None


def update(category_id, data):
    category = repo.get_by_id(category_id)

    if category is None:
        return None, "Kategori tidak ditemukan"

    if not isinstance(data, dict):
        return None, "Data JSON wajib berupa objek"

    name = data.get("name")

    if not isinstance(name, str) or not name.strip():
        return None, "Nama kategori wajib diisi"

    name = name.strip()

    if any(
        c["id"] != category_id
        and c["name"].lower() == name.lower()
        for c in repo.get_all()
    ):
        return None, "Nama kategori sudah digunakan"

    return repo.update(category_id, name), None


def delete(category_id):
    category = repo.get_by_id(category_id)

    if category is None:
        return False, "Kategori tidak ditemukan"

    # Pengecekan aman untuk relasi category_id atau category nama string
    cat_name = category["name"].lower()
    if any(
        item.get("category_id") == category_id or str(item.get("category", "")).lower() == cat_name
        for item in item_repository.get_all()
    ):
        return False, "Kategori masih digunakan oleh barang"

    repo.delete(category_id)
    return True, None