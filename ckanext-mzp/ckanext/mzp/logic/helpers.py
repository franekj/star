import ckan.plugins.toolkit as tk

def get_package_source(package_id):
    return tk.get_action('package_source_list')({}, {"package_id": package_id})


def get_package_reference(package_id):
    return tk.get_action('package_reference_list')({}, {"package_id": package_id})