from ckan.lib.navl.validators import not_empty

def package_sources_list_schema():
    schema = {
        'package_id': [not_empty, unicode]
    }
    return schema


def package_add_source_schema():
    schema = {
        'package_id': [not_empty, unicode],
        'source_link': [not_empty, unicode],
        'source_title': [not_empty, unicode],
    }
    return schema


def package_delete_source_schema():
    schema = {
        'source_id': [not_empty, unicode],
    }
    return schema
