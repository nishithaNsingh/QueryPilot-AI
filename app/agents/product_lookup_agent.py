from app.services import product_service


def handle_product_lookup(entities):
    pid = (entities or {}).get("product_id")
    category = (entities or {}).get("category")
    query = (entities or {}).get("product_name")

    if pid:
        product = product_service.details(pid)
        if not product:
            return {"success": False, "response": f"Product {pid} not found."}
        return {"success": True, "response": "Product found.", "products": [product]}

    if category:
        products = product_service.by_category(category)
        if not products:
            return {"success": False, "response": f"No products found in category '{category}'."}
        return {
            "success": True,
            "response": f"Found {len(products)} products in category '{category}'.",
            "products": products,
        }

    if query:
        products = product_service.search(query)
        if not products:
            return {"success": False, "response": f"No products match '{query}'."}
        return {
            "success": True,
            "response": f"Found {len(products)} products matching '{query}'.",
            "products": products,
        }

    cats = product_service.categories()[:20]
    return {
        "success": False,
        "response": "Specify a category, product ID, or keyword to search products.",
        "categories": cats,
    }