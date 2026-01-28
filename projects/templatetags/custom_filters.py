from django import template
register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Get item from dictionary by key"""
    return dictionary.get(key, 0)

@register.filter
def format_category(category):
    """Map category names to their proper display format"""
    # Since the categories are now stored with their full names,
    # we can just return them as is, or apply any specific formatting if needed
    return category 