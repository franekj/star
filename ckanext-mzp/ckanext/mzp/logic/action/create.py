import ckan.plugins.toolkit as toolkit
from ckan.lib.navl.dictization_functions import validate
from ckanext.mzp.logic.schema import package_add_source_schema
from ckanext.mzp.model import DatasetSourceModel


def package_add_source(context, data_dict):
    '''List sources associated with a package.

     :param package_id: id or name of the package
     :type package_id: string

     :rtype: list of dictionaries
     '''

    toolkit.check_access('package_update', context, data_dict)

    # validate the incoming data_dict
    validated_data_dict, errors = validate(data_dict,
                                           package_add_source_schema(),
                                           context)

    if errors:
        raise toolkit.ValidationError(errors)


    package_id, source_link, source_title = toolkit.get_or_bust(validated_data_dict, ['package_id', 'source_link', 'source_title'])
    if not source_link.startswith('http'):
        source_dict = toolkit.get_action('package_show')(context, {'name_or_id': source_link})
        return DatasetSourceModel.create(package_id=package_id, source_link=source_dict['id'], source_title=source_dict['title'])

    return DatasetSourceModel.create(package_id=package_id, source_link=source_link, source_title=source_title)
