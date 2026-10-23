from flask import request
from app.routes import items_bp
from app.services import item_service as service
from app.utils.response_helper import success_response, fail_response


@items_bp.route("", methods=["GET"])
def get_items():
    result = service.get_all()

    min_price = request.args.get("min_price")
    category = request.args.get("category")

    if min_price is not None:
        try:
            min_price = int(min_price)
            if min_price < 0:
                raise ValueError
        except ValueError:
            return fail_response(
                errors={"min_price": "min_price harus berupa bilangan bulat nonnegatif"},
                message="min_price harus berupa bilangan bulat nonnegatif",
                code=400
            )

        result = [
            item for item in result
            if item["price"] >= min_price
        ]

    if category is not None:
        result = [
            item for item in result
            if str(item.get("category", "")).lower() == str(category).lower()
        ]

    return success_response(
        data={"total": len(result), "items": result},
        message="Berhasil mengambil data barang",
        code=200
    )


@items_bp.route("/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = service.get_by_id(item_id)

    if item is None:
        return fail_response(
            errors={"item_id": "Barang tidak ditemukan"},
            message="Barang tidak ditemukan",
            code=404
        )

    return success_response(
        data=item,
        message="Berhasil mengambil detail barang",
        code=200
    )


@items_bp.route("", methods=["POST"])
def create_item():
    item, error = service.create(request.get_json(silent=True))

    if error:
        status_code = 404 if error == "Kategori tidak ditemukan" else 400
        return fail_response(
            errors={"item": error},
            message=error,
            code=status_code
        )

    return success_response(
        data=item,
        message="Barang berhasil ditambahkan",
        code=201
    )


@items_bp.route("/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    item, error = service.update(
        item_id, request.get_json(silent=True)
    )

    if error:
        if error in ["Barang tidak ditemukan", "Kategori tidak ditemukan"]:
            status_code = 404
        else:
            status_code = 400

        return fail_response(
            errors={"item": error},
            message=error,
            code=status_code
        )

    return success_response(
        data=item,
        message="Barang berhasil diperbarui",
        code=200
    )


@items_bp.route("/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    if not service.delete(item_id):
        return fail_response(
            errors={"item_id": "Barang tidak ditemukan"},
            message="Barang tidak ditemukan",
            code=404
        )

    return success_response(
        data={},
        message="Barang berhasil dihapus",
        code=200
    )