from django import template
import json

register = template.Library()

@register.filter
def get_product_data(product_data_json, product_id):
    product_data = json.loads(product_data_json)
    return product_data.get(str(product_id), {})