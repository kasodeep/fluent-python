"""
Define a family of algorithms, encapsulate each one, and make them interchangeable.
Strategy lets the algorithm vary independently from clients that use it.

Context:
Provides a service by delegating some computation to interchangeable components
that implement alternative algorithms. In the ecommerce example,
the context is an Order, which is configured to apply a promotional discount
according to one of several algorithms.

Strategy:
The interface common to the components that implement the different algorithms. 
In our example, this role is played by an abstract class called Promotion.

Concrete strategy:
One of the concrete subclasses of Strategy. FidelityPromo, BulkPromo, and
LargeOrderPromo are the three concrete strategies implemented.
"""

from collections.abc import sequence
from dataclasses import dataclass
from decimal import Decimal
from typing import Callable, Optional, NamedTuple

class Customer(NamedTuple):
    name: str
    fidelity: int

class LineItem(NamedTuple):
    product: str
    quantity: int
    price: Decimal

    def total(self) -> Decimal:
        return self.price * self.quantity

@dataclass(frozen=True)
class Order:
    customer: Customer
    cart: sequence[LineItem]
    promotion: Optional[Callable[['Order'], Decimal]] = None # takes an order argument or returns None.

    def total(self) -> Decimal:
        if not hasattr(self, '__total'):
            self.__total = sum(item.total() for item in self.cart)
        return self.__total

    def due(self) -> Decimal:
        if self.promotion is None:
            discount = Decimal('0')
        else:
            discount = self.promotion(self)
        return self.total() - discount

    def __repr__(self) -> str:
        fmt = '<Order total: {:.2f} due: {:.2f}>'
        return fmt.format(self.total(), self.due())

def fidelity_promo(order: Order) -> Decimal:
    """5% discount for customers with 1000 or more fidelity points"""
    return order.total() * Decimal('0.05') if order.customer.fidelity >= 1000 else Decimal('0')

def bulk_item_promo(order: Order) -> Decimal:
    """10% discount for each LineItem with 20 or more units"""
    discount = Decimal('0')
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * Decimal('0.1')
    return discount

def large_order_promo(order: Order) -> Decimal:
    """7% discount for orders with 10 or more distinct items"""
    distinct_items = {item.product for item in order.cart}
    if len(distinct_items) >= 10:
        return order.total() * Decimal('0.07')
    return Decimal('0')

joe = Customer('John Doe', 0)
ann = Customer('Ann Smith', 1100)

cart = [
    LineItem('banana', 4, Decimal('0.5')),
    LineItem('apple', 10, Decimal('1.5')),
    LineItem('watermelon', 5, Decimal('5.0')),
]
print(Order(joe, cart, fidelity_promo))

long_order_cart = [LineItem(str(item_code), 1, Decimal('1.0')) for item_code in range(10)]
print(Order(ann, long_order_cart, large_order_promo))
