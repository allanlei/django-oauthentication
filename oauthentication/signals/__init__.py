import django.dispatch

pizza_done = django.dispatch.Signal(providing_args=["toppings", "size"])
