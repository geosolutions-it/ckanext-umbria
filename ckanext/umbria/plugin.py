import logging

from ckan.lib.plugins import DefaultTranslation
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.common import _

from ckanext.dcatapit.helpers import get_dcatapit_package_schema
from ckanext.dcatapit.interfaces import ICustomSchema, ICustomOrganizationSchema
from ckanext.dcatapit.schema import FIELD_THEMES_AGGREGATE

log = logging.getLogger(__name__)


class UmbriaPlugin(plugins.SingletonPlugin, DefaultTranslation):

    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.ITranslation)

    plugins.implements(ICustomSchema)
    plugins.implements(ICustomOrganizationSchema)

    # IConfigurer
    # ------------------------------------------------------------
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('public', 'umbria')  # path, webasset name

    # ITemplateHelpers
    # ------------------------------------------------------------
    def get_helpers(self):
        return {
            'umbria_get_groups': umbria_get_groups,
            'get_dcatapit_package_schema': UmbriaPlugin.get_umbria_cached_package_schema,
        }

    CACHED_PACKAGE_SCHEMA = None

    @classmethod
    def get_umbria_cached_package_schema(cls):
        if cls.CACHED_PACKAGE_SCHEMA is None:
            cls.CACHED_PACKAGE_SCHEMA = get_umbria_package_schema()
        return cls.CACHED_PACKAGE_SCHEMA

    # ICustomSchema
    # ------------------------------------------------------------
    def get_custom_schema(self):
        return [
            {
                'name': 'publisher_email',
                'validator': ['ignore_missing'],
                'element': 'input',
                'type': 'text',
                'label': _('Editor email label'),
                'placeholder': _('Editor email help'),
                'is_required': False,
                'help': _('Editor email info'),
                'in_tab': True,
            },
            {
                'name': 'publisher_url',
                'validator': ['ignore_missing'],
                'element': 'input',
                'type': 'text',
                'label': _('Editor site label'),
                'placeholder': _('Editor site help'),
                'is_required': False,
                'help': _('Editor site info'),
                'in_tab': True,
            },
            {
                'name': 'geographical_si_ref',
                'validator': ['ignore_missing'],
                'element': 'input',
                'type': 'text',
                'label': _('SI REF label'),
                'placeholder_url': _('Enter SI REF'),
                'placeholder_name': 'e.g. EPSG:4326',
                'help': _('SI REF help'),
                'in_tab': True,
            },

        ]

    def get_schema_updates(self):
        return {
            'identifier': {
                'ignore': True,
                'ignore_from_edit': True,
                'read_only': True,
                'validator': ['ignore_missing'],
            },
            'language': {
                'ignore': True,
                'ignore_from_edit': True,
                'default': 'ITA',
            },
            'is_version_of': {
                'ignore': True,
                'ignore_from_edit': True,
            },
            'geographical_name': {
                'element': 'input',
                'type': 'text',
                'placeholder': _('Organizational Unit Responsible Competence Area'),
                'vocabulary_name': None,
                'data_module_source': None,
            },
            'geographical_geonames_url': {
                'label': _('GeoNames COVERAGE'),
            },
            'publisher': {
                'label': _('Editor label'),
            },
        }

    def get_custom_org_schema(self):
        return [
            {
                'name': 'geographical_geonames_url',
                'validator': ['ignore_missing'],
                'element': 'geonames',
                'type': 'geonames',
                'label': _('GeoNames URL'),
                'placeholder_url': _('Enter geonames URL'),
                'placeholder_name': _('Enter name of place'),
                'help': _('package_geographical_geonames_url_help')
             },
        ]


def umbria_get_groups(limit=10):
    return toolkit.get_action('group_list')\
        (
            data_dict={
                'sort': 'package_count desc',
                'all_fields': True,
                'limit': limit
            }
        )


def get_umbria_package_schema():
    dcatapit_schema = get_dcatapit_package_schema()

    def get_schema_field(name):
        for field in dcatapit_schema:
            if field['name'] == name:
                return field

        raise ValueError(f'Field not found {name}')

    return [get_schema_field(name) for name in [
        # 'identifier',
        FIELD_THEMES_AGGREGATE,
        'publisher',
        'publisher_email',
        'publisher_url',
        'issued',
        'modified',
        'frequency',
        'geographical_name',
        'geographical_geonames_url',
        'geographical_si_ref',
        'temporal_coverage',
        #'language',
        'rights_holder',
        #'is_version_of',
        #'conforms_to',
        'alternate_identifier',
        'creator',
    ]]
