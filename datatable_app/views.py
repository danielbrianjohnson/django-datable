from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models import Q
from django.apps import apps  
import json
from .models import Product, Order  # Import your models
from decimal import Decimal

def index(request):
    return render(request, 'datatable_app/index.html')

@csrf_exempt  # Remove in production
def dynamic_data(request):
    draw = int(request.GET.get('draw', 1))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))

    # 🔹 Get the model dynamically
    model_name = request.GET.get('model', 'Product')
    try:
        ModelClass = apps.get_model('datatable_app', model_name)
    except LookupError:
        return JsonResponse({"error": f"Model '{model_name}' not found"}, status=400)

    # 🔹 Extract filters dynamically
    filters = {}
    search_value = request.GET.get('searchValue', '').strip().lower()
    search_fields = request.GET.getlist("searchFields")

    # 🔹 Get valid fields from the model
    valid_fields = {field.attname for field in ModelClass._meta.fields}

    # 🔹 Validate and Clean Filters
    for key, value in request.GET.items():
        if key in valid_fields:
            selected_values = request.GET.get(key, "").split(",")  # ✅ Correctly extract multi-select values
            if selected_values and selected_values != [""]:
                filters[key + "__in"] = selected_values  # ✅ Apply multiple filters dynamically


    # 🔹 Apply search dynamically across specified fields
    filter_query = Q()
    if search_value:
        search_query = Q()
        for field in ModelClass._meta.get_fields():
            if hasattr(field, "attname") and (not search_fields or field.attname in search_fields):
                search_query |= Q(**{f"{field.attname}__icontains": search_value})
        filter_query &= search_query

    # 🔹 Apply filters & retrieve queryset
    if filter_query:
        queryset = ModelClass.objects.filter(filter_query, **filters)
    else:
        queryset = ModelClass.objects.filter(**filters)

    # 🔹 Apply sorting dynamically
    order_column_index = int(request.GET.get("orderColumn", 0))
    order_direction = request.GET.get("orderDir", "asc")

    fields = [field.attname for field in ModelClass._meta.fields]
    sort_field = fields[order_column_index] if 0 <= order_column_index < len(fields) else "id"

    queryset = queryset.order_by(f"-{sort_field}" if order_direction == "desc" else sort_field)

    # 🔹 Apply pagination
    paginator = Paginator(queryset, length)
    page = (start // length) + 1
    page_data = paginator.get_page(page)

    # 🔹 Convert Decimal Fields to JSON-Safe Format
    def serialize(obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return obj

    # 🔹 Build JSON response
    data = [
        {field.attname: serialize(getattr(obj, field.attname)) for field in ModelClass._meta.fields}
        for obj in page_data
    ]

    return JsonResponse({
        "draw": draw,
        "recordsTotal": ModelClass.objects.count(),
        "recordsFiltered": paginator.count,
        "data": data,
        "selectedFilters": {key: list(value) for key, value in filters.items()},  # ✅ Convert to list
    })




def get_model_fields(request):
    """ Fetches column names dynamically from a model and extracts unique values for filters. """
    model_name = request.GET.get('model', 'Product')

    try:
        ModelClass = apps.get_model('datatable_app', model_name)
    except LookupError:
        return JsonResponse({"error": f"Model '{model_name}' not found"}, status=400)

    fields = [
        {"key": field.attname, "title": field.verbose_name.replace("_", " ").title()}
        for field in ModelClass._meta.fields if hasattr(field, "attname")
    ]

    # Extract unique filter values for each field
    filters = {}
    for field in ModelClass._meta.fields:
        if hasattr(field, "attname"):
            unique_values = ModelClass.objects.values_list(field.attname, flat=True).distinct()
            filters[field.attname] = list(unique_values)

    return JsonResponse({"columns": fields, "filters": filters})
