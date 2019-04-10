import ckan.plugins.toolkit as toolkit
from ckan.lib.navl.dictization_functions import validate
from ckanext.mzp.logic.schema import package_delete_source_schema
from ckanext.mzp.model import DatasetSourceModel


def package_source_delete(context, data_dict):
    '''List sources associated with a package.

     :param package_id: id or name of the package
     :type package_id: string

     :rtype: list of dictionaries
     '''

    toolkit.check_access('package_update', context, data_dict)

    # validate the incoming data_dict
    validated_data_dict, errors = validate(data_dict,
                                           package_delete_source_schema(),
                                           context)

    if errors:
        raise toolkit.ValidationError(errors)


    source_id = toolkit.get_or_bust(validated_data_dict, ['source_id'])
    DatasetSourceModel.delete_package_source(source_id)
    return True

