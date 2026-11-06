from app.repositories.product_repository import (
    search_products,
    get_product_details,
    get_products_by_category,
    get_product_categories,
)


def search(query, limit=10):
    return search_products(query, limit=limit)


def details(product_id):
    return get_product_details(product_id)


def by_category(category, limit=10):
    return get_products_by_category(category, limit=limit)


def categories():
    return get_product_categories()