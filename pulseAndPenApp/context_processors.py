def active_tab_processor(request):
    return {'active': request.resolver_match.url_name}
