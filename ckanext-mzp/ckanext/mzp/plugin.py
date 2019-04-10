import os
import sys
import logging

import ckan.plugins as plugins
import ckan.lib.plugins as lib_plugins
import ckan.lib.helpers as h
from ckan.plugins import toolkit as tk
from ckan.common import OrderedDict
from ckan import model as ckan_model
from routes.mapper import SubMapper

from ckanext.mzp.model import setup as model_setup
from ckanext.mzp.logic.action.get import package_source_list, package_reference_list
from ckanext.mzp.logic.action.create import package_add_source
from ckanext.mzp.logic.action.delete import package_source_delete
from ckanext.mzp.logic.helpers import get_package_source, get_package_reference


c = tk.c
_ = tk._

log = logging.getLogger(__name__)

DATASET_TYPE_NAME = 'showcase'


class MzpPlugin(plugins.SingletonPlugin, lib_plugins.DefaultDatasetForm):
    plugins.implements(plugins.IConfigurable)
    plugins.implements(plugins.IConfigurer)
    # plugins.implements(plugins.IDatasetForm)
    # plugins.implements(plugins.IFacets, inherit=True)
    plugins.implements(plugins.IRoutes, inherit=True)
    # plugins.implements(plugins.IAuthFunctions)
    plugins.implements(plugins.IActions)
    # plugins.implements(plugins.IPackageController, inherit=True)
    plugins.implements(plugins.ITemplateHelpers)

    # ITranslation only available in 2.5+
    # try:
    #     plugins.implements(plugins.ITranslation)
    # except AttributeError:
    #     pass

    # IConfigurer

    def update_config(self, config):
        tk.add_template_directory(config, 'templates')
        # tk.add_public_directory(config, 'public')
        # if tk.check_ckan_version(min_version='2.4'):
        #     tk.add_ckan_admin_tab(config, 'ckanext_showcase_admins',
        #                           'Showcase Config')

    # IConfigurable

    def configure(self, config):
        model_setup()

    # IDatasetForm
    #
    # def package_types(self):
    #     return [DATASET_TYPE_NAME]
    #
    # def is_fallback(self):
    #     return False
    #
    # def search_template(self):
    #     return 'showcase/search.html'
    #
    # def new_template(self):
    #     return 'showcase/new.html'
    #
    # def read_template(self):
    #     return 'showcase/read.html'
    #
    # def edit_template(self):
    #     return 'showcase/edit.html'
    #
    # def package_form(self):
    #     return 'showcase/new_package_form.html'
    #
    # def create_package_schema(self):
    #     return showcase_schema.showcase_create_schema()
    #
    # def update_package_schema(self):
    #     return showcase_schema.showcase_update_schema()
    #
    # def show_package_schema(self):
    #     return showcase_schema.showcase_show_schema()
    #
    # # ITemplateHelpers
    #
    def get_helpers(self):
        return {
            'get_package_sources': get_package_source,
            'get_package_reference': get_package_reference,
        }
    #
    # # IFacets
    #
    # def dataset_facets(self, facets_dict, package_type):
    #     '''Only show tags for Showcase search list.'''
    #     if package_type != DATASET_TYPE_NAME:
    #         return facets_dict
    #     return OrderedDict({'tags': _('Tags')})

    # IRoutes
    def before_map(self, map):
        # These named routes are used for custom dataset forms which will use
        # the names below based on the dataset.type ('dataset' is the default
        # type)
        with SubMapper(map, controller='ckanext.mzp.controller:SourceController') as m:
            # m.connect('ckanext_showcase_index', '/showcase', action='search',
            #           highlight_actions='index search')
            # m.connect('ckanext_showcase_new', '/showcase/new', action='new')
            # m.connect('ckanext_showcase_delete', '/showcase/delete/{id}',
            #           action='delete')
            # m.connect('ckanext_showcase_read', '/showcase/{id}', action='read',
            #           ckan_icon='picture')
            # m.connect('ckanext_showcase_edit', '/showcase/edit/{id}',
            #           action='edit', ckan_icon='edit')
            # m.connect('ckanext_showcase_manage_datasets',
            #           '/showcase/manage_datasets/{id}',
            #           action="manage_datasets", ckan_icon="sitemap")
            m.connect('dataset_source_list', '/dataset/sources/{id}',
                      action='dataset_source_list', ckan_icon='picture')
            # m.connect('ckanext_showcase_admins', '/ckan-admin/showcase_admins',
            #           action='manage_showcase_admins', ckan_icon='picture'),
            # m.connect('ckanext_showcase_admin_remove',
            #           '/ckan-admin/showcase_admin_remove',
            #           action='remove_showcase_admin')
        # map.redirect('/showcases', '/showcase')
        # map.redirect('/showcases/{url:.*}', '/showcase/{url}')
        return map

    # IActions

    def get_actions(self):
        action_functions = {
            'package_source_list': package_source_list,
            'package_add_source': package_add_source,
            'package_delete_source': package_source_delete,
            'package_reference_list': package_reference_list,
        }
        return action_functions

    # IPackageController

    # def _add_to_pkg_dict(self, context, pkg_dict):
    #     '''
    #     Add key/values to pkg_dict and return it.
    #     '''
    #
    #     if pkg_dict['type'] != 'showcase':
    #         return pkg_dict
    #
    #     # Add a display url for the Showcase image to the pkg dict so template
    #     # has access to it.
    #     image_url = pkg_dict.get('image_url')
    #     pkg_dict[u'image_display_url'] = image_url
    #     if image_url and not image_url.startswith('http'):
    #         pkg_dict[u'image_url'] = image_url
    #         pkg_dict[u'image_display_url'] = \
    #             h.url_for_static('uploads/{0}/{1}'
    #                              .format(DATASET_TYPE_NAME,
    #                                      pkg_dict.get('image_url')),
    #                              qualified=True)
    #
    #     # Add dataset count
    #     pkg_dict[u'num_datasets'] = len(
    #         tk.get_action('ckanext_showcase_package_list')(
    #             context, {'showcase_id': pkg_dict['id']}))
    #
    #     # Rendered notes
    #     pkg_dict[u'showcase_notes_formatted'] = \
    #         h.render_markdown(pkg_dict['notes'])
    #     return pkg_dict
    #
    # def after_show(self, context, pkg_dict):
    #     '''
    #     Modify package_show pkg_dict.
    #     '''
    #     pkg_dict = self._add_to_pkg_dict(context, pkg_dict)
    #
    # def before_view(self, pkg_dict):
    #     '''
    #     Modify pkg_dict that is sent to templates.
    #     '''
    #
    #     context = {'model': ckan_model, 'session': ckan_model.Session,
    #                'user': c.user or c.author}
    #
    #     return self._add_to_pkg_dict(context, pkg_dict)
    #
    # def before_search(self, search_params):
    #     '''
    #     Unless the query is already being filtered by this dataset_type
    #     (either positively, or negatively), exclude datasets of type
    #     `showcase`.
    #     '''
    #     fq = search_params.get('fq', '')
    #     filter = 'dataset_type:{0}'.format(DATASET_TYPE_NAME)
    #     if filter not in fq:
    #         search_params.update({'fq': fq + " -" + filter})
    #     return search_params
    #
    # # ITranslation
    #
    # # The following methods copied from ckan.lib.plugins.DefaultTranslation so
    # # we don't have to mix it into the class. This means we can use Showcase
    # # even if ITranslation isn't available (less than 2.5).
    #
    # def i18n_directory(self):
    #     '''Change the directory of the *.mo translation files
    #
    #     The default implementation assumes the plugin is
    #     ckanext/myplugin/plugin.py and the translations are stored in
    #     i18n/
    #     '''
    #     # assume plugin is called ckanext.<myplugin>.<...>.PluginClass
    #     extension_module_name = '.'.join(self.__module__.split('.')[0:2])
    #     module = sys.modules[extension_module_name]
    #     return os.path.join(os.path.dirname(module.__file__), 'i18n')
    #
    # def i18n_locales(self):
    #     '''Change the list of locales that this plugin handles
    #
    #     By default the will assume any directory in subdirectory in the
    #     directory defined by self.directory() is a locale handled by this
    #     plugin
    #     '''
    #     directory = self.i18n_directory()
    #     return [d for
    #             d in os.listdir(directory)
    #             if os.path.isdir(os.path.join(directory, d))]
    #
    # def i18n_domain(self):
    #     '''Change the gettext domain handled by this plugin
    #
    #     This implementation assumes the gettext domain is
    #     ckanext-{extension name}, hence your pot, po and mo files should be
    #     named ckanext-{extension name}.mo'''
    #     return 'ckanext-{name}'.format(name=self.name)
