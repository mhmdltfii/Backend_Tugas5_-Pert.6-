from flask import request
from app.routes import categories_bp
from app.services import category_service as service
from app.utils.response_helper import success_response, fail_response


@categories_bp.route("", methods=["GET"])
def get_categories():
    return success_response(
        data=service.get_all(),
        message="Berhasil mengambil daftar kategori",
        code=200
    )


@categories_bp.route("/<int:category_id>", methods=["GET"])
def get_category(category_id):
    category = service.get_by_id(category_id)

    if category is None:
        return fail_response(
            errors={"category_id": "Kategori tidak ditemukan"},
            message="Kategori tidak ditemukan",
            code=404
        )

    return success_response(
        data=category,
        message="Berhasil mengambil detail kategori",
        code=200
    )


@categories_bp.route("", methods=["POST"])
def create_category():
    category, error = service.create(request.get_json(silent=True))

    if error:
        return fail_response(
            errors={"name": error},
            message=error,
            code=400
        )

    return success_response(
        data=category,
        message="Kategori berhasil ditambahkan",
        code=201
    )


@categories_bp.route("/<int:category_id>", methods=["PUT"])
def update_category(category_id):
    category, error = service.update(
        category_id, request.get_json(silent=True)
    )

    if error:
        status_code = 404 if error == "Kategori tidak ditemukan" else 400
        return fail_response(
            errors={"category": error},
            message=error,
            code=status_code
        )

    return success_response(
        data=category,
        message="Kategori berhasil diperbarui",
        code=200
    )


@categories_bp.route("/<int:category_id>", methods=["DELETE"])
def delete_category(category_id):
    success, error = service.delete(category_id)

    if not success:
        status_code = 404 if error == "Kategori tidak ditemukan" else 409
        return fail_response(
            errors={"category": error},
            message=error,
            code=status_code
        )

    return success_response(
        data={},
        message="Kategori berhasil dihapus",
        code=200
    )