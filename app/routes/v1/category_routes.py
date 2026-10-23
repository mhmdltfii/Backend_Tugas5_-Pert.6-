from flask import Blueprint, request
from app.services import category_service as service
from app.utils.response_helper import success_response, fail_response

# URL prefix menggunakan bentuk tunggal: /api/v1/category
categories_bp_v1 = Blueprint('categories_v1', __name__, url_prefix='/api/v1/category')


@categories_bp_v1.route('', methods=['GET'])
def get_categories():
    categories = service.get_all()
    return success_response(
        data={"categories": categories, "total": len(categories)},
        message="Berhasil mengambil data kategori",
        code=200
    )


@categories_bp_v1.route('/<int:category_id>', methods=['GET'])
def get_category(category_id):
    category = service.get_by_id(category_id)

    if category is None:
        return fail_response(
            errors={"category_id": "Kategori tidak ditemukan"},
            code=404
        )

    return success_response(
        data=category,
        message="Berhasil mengambil detail kategori",
        code=200
    )


@categories_bp_v1.route('', methods=['POST'])
def create_category():
    if not request.is_json:
        return fail_response(errors={"content_type": "Harus application/json"}, code=400)

    body = request.get_json(silent=True)
    if not isinstance(body, dict):
        return fail_response(errors={"body": "Harus berupa objek JSON yang valid"}, code=400)

    category, error = service.create(body)

    if error:
        return fail_response(errors={"name": error}, code=400)

    return success_response(
        data=category,
        message="Kategori berhasil ditambahkan",
        code=201
    )


@categories_bp_v1.route('/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    if not request.is_json:
        return fail_response(errors={"content_type": "Harus application/json"}, code=400)

    body = request.get_json(silent=True)
    if not isinstance(body, dict):
        return fail_response(errors={"body": "Harus berupa objek JSON yang valid"}, code=400)

    category, error = service.update(category_id, body)

    if error:
        code = 404 if error == "Kategori tidak ditemukan" else 400
        return fail_response(errors={"category": error}, code=code)

    return success_response(
        data=category,
        message="Kategori berhasil diperbarui",
        code=200
    )


@categories_bp_v1.route('/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    success, error = service.delete(category_id)

    if not success:
        code = 404 if error == "Kategori tidak ditemukan" else 409
        return fail_response(errors={"category": error}, code=code)

    return success_response(
        data={},
        message="Kategori berhasil dihapus",
        code=200
    )