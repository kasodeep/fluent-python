from collections.abc import Callable
from decimal import Decimal

Promotion = Callable[[Order], Decimal]  # type alias for a promotion function that takes an Order and returns a Decimal

promos = list[Promotion] = []

def promotion(promo_func: Promotion) -> Promotion:
    promos.append(promo_func)
    return promo_func

def best_promo(order: Order) -> Decimal:
    """Select best discount available"""
    return max(promo(order) for promo in promos)

@promotion
def fidelity_promo(order: Order) -> Decimal:
    """5% discount for customers with 1000 or more fidelity points"""
    return order.total() * Decimal('0.05') if order.customer.fidelity >= 1000 else Decimal('0')

@promotion
def bulk_item_promo(order: Order) -> Decimal:
    """10% discount for each LineItem with 20 or more units"""
    discount = Decimal('0')
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * Decimal('0.1')
    return discount

@promotion
def large_order_promo(order: Order) -> Decimal:
    """7% discount for orders with 10 or more distinct items"""
    distinct_items = {item.product for item in order.cart}
    if len(distinct_items) >= 10:
        return order.total() * Decimal('0.07')
    return Decimal('0')