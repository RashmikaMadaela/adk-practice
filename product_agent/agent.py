from __future__ import annotations

from typing import Literal

import dotenv
from google.adk.agents import Agent

dotenv.load_dotenv()


PRODUCTS = [
    {
        "product_id": "LAPTOP-PRO-14",
        "name": "Laptop Pro 14",
        "category": "laptop",
        "price_lkr": 425000,
        "stock": 8,
        "description": "14-inch laptop for engineering and design teams.",
    },
    {
        "product_id": "MONITOR-27-4K",
        "name": "27-inch 4K Monitor",
        "category": "monitor",
        "price_lkr": 145000,
        "stock": 15,
        "description": "High-resolution monitor for productivity workstations.",
    },
    {
        "product_id": "HEADSET-USB-C",
        "name": "USB-C Headset",
        "category": "accessory",
        "price_lkr": 18500,
        "stock": 32,
        "description": "Noise-cancelling headset for calls and meetings.",
    },
]


def list_products(
    category: Literal["laptop", "monitor", "accessory"] | None = None,
) -> dict:
    """List products, optionally filtered by category.

    Args:
        category: Optional product category to filter by.

    Returns:
        Matching products and a count.
    """
    matches = []
    for product in PRODUCTS:
        if category and product["category"] != category:
            continue
        matches.append(product.copy())

    return {"status": "success", "count": len(matches), "products": matches}


def get_product_details(product_id: str) -> dict:
    """Get details for one product.

    Args:
        product_id: Product identifier, for example LAPTOP-PRO-14.

    Returns:
        Product details if found.
    """
    for product in PRODUCTS:
        if product["product_id"] == product_id:
            return {"status": "success", "product": product.copy()}

    return {"status": "error", "message": f"Unknown product_id: {product_id}"}


def check_stock(product_id: str, quantity: int = 1) -> dict:
    """Check whether the requested product quantity is available.

    Args:
        product_id: Product identifier.
        quantity: Requested quantity.

    Returns:
        Availability result.
    """
    for product in PRODUCTS:
        if product["product_id"] == product_id:
            available = product["stock"] >= quantity
            return {
                "status": "success",
                "product_id": product_id,
                "requested_quantity": quantity,
                "available_stock": product["stock"],
                "is_available": available,
            }

    return {"status": "error", "message": f"Unknown product_id: {product_id}"}


root_agent = Agent(
    name="product_agent",
    model="gemini-2.5-flash",
    description="Product catalogue assistant with simple function tools.",
    instruction="""
You are a product catalogue assistant.

Use the provided tools as the source of truth for product names, prices, stock, and descriptions.
Do not invent product details.
When users ask what is available, list products with product id, name, price, and stock.
When users ask about availability, call the stock tool before answering.
""",
    tools=[
        list_products,
        get_product_details,
        check_stock,
    ],
)