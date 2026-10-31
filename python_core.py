raw_products = [
    {"product_code": "P301", "name": "Laptop Dell XPS", "price": 25000000, "stock": 10, "status": "available"},
    {"product_code": " p101 ", "name": "Chuột Logitech", "price": 500000, "stock": 50, "status": "available"},
    {"product_code": "P202", "name": "Màn hình LG 27", "price": 6000000, "stock": 0, "status": "out_of_stock"},
    {"product_code": "P102", "name": "Bàn phím Cơ", "price": 1200000, "stock": 15, "status": "available"},
    {"product_code": "P302", "name": "Tai nghe Sony", "price": 3500000, "stock": 8, "status": "available"}
]

raw_orders = [
    {"order_code": "ORD001", "customer": "Nguyễn Văn A", "amount": 15000000, "status": "COMPLETED"},
    {"order_code": "ORD002", "customer": "Trần Thị B", "amount": 2500000, "status": "COMPLETED"},
    {"order_code": "ORD003", "customer": "Lê Văn C", "amount": 8000000, "status": "PENDING"},
    {"order_code": "ORD004", "customer": "Phạm Văn D", "amount": 45000000, "status": "COMPLETED"}
]

def clean_and_validate_products (raw_products):
    res = []
    for p in raw_products:
        code = p["product_code"].strip().upper()
        if len(code) == 4 and code.startswith("P") and code[1:].isdigit():
            res.append({**p, "product_code": code})
    return res

def binary_search_product(products, target_code):
    left, right = 0,len(products) - 1
    target = target_code.strip().upper()

    while left <= right:
        mid = (left + right) // 2
        cur = products[mid]["product_code"]
        if cur == target:
            return products[mid]
        if cur < target:
            left = mid + 1
        else:
            right = mid - 1
    return None

def sort_products_by_price_desc(products):
    if len(products) <= 1:
        return products
    mid = len(products) // 2
    left = sort_products_by_price_desc(products[:mid])
    right = sort_products_by_price_desc(products[mid:])

    res, i, j = [],0,0
    while i < len(left) and j < len(right):
        if left[i]["price"] >= right[j]["price"]:
            res.append(left[i])
            i += 1
        else:
            res.append(right[j])
            j += 1
    return res + left[i:] + right[j:]

def analyze_order_stats(orders):
    revenue = sum(
        o["ammount"] for o in orders if o.get("status") == "COMPLETED"
    )
    max_order = max(orders, key=lambda x: x["amount"]) if orders else None
    return {"total_revenue": revenue, "max_orders": max_order}