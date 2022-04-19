import logging

from rdflib.namespace import Namespace, RDF, SKOS
from rdflib import URIRef, BNode, Literal

import ckan.logic as logic

from ckanext.dcat.profiles import RDFProfile, DCAT, LOCN, VCARD, DCT, FOAF, ADMS, OWL, SCHEMA, TIME

DCATAPIT = Namespace('http://dati.gov.it/onto/dcatapit#')

log = logging.getLogger(__name__)


class UmbriaDCATAPProfile(RDFProfile):
    """
    Customization of DCATAP-IT for Regione Umbria
    """

    def parse_dataset(self, dataset_dict, dataset_ref):
        return dataset_dict

    def graph_from_dataset(self, dataset_dict, dataset_ref):
        self._replace_poc_with_publisher(dataset_dict, dataset_ref)
        self._augment_publisher_info(dataset_dict, dataset_ref)

    def _replace_poc_with_publisher(self, dataset_dict, dataset_ref):
        g = self.g
        org_dict = _get_org(dataset_dict.get('owner_org'))

        # Remove previous poc
        # for s, p, o in g.triples((dataset_ref, DCAT.contactPoint, None)):
        #     log.info(f"UmbriaProfile: Removing contactPoint {o}")
        #     g.remove((s, p, o))

        # Add new poc
        pub_name = dataset_dict.get('publisher_name')
        pub_mail = dataset_dict.get('publisher_email')
        pub_url = dataset_dict.get('publisher_url')

        poc = BNode()
        g.add((dataset_ref, DCAT.contactPoint, poc))
        g.add((poc, RDF.type, DCATAPIT.Organization))
        g.add((poc, RDF.type, VCARD.Kind))
        g.add((poc, RDF.type, VCARD.Organization))

        g.add((poc, VCARD.fn, Literal(pub_name if pub_name else org_dict.get('name'))))

        if pub_mail:
            g.add((poc, VCARD.hasEmail, Literal(pub_mail)))
        elif 'email' in org_dict.keys():
            # this element is mandatory for dcatapit, but it may not have been filled for imported datasets
            g.add((poc, VCARD.hasEmail, URIRef(org_dict.get('email'))))

        if 'telephone' in org_dict.keys():
            g.add((poc, VCARD.hasTelephone, Literal(org_dict.get('telephone'))))

        if pub_url:
            g.add((poc, VCARD.hasURL, Literal(pub_url)))
        elif 'site' in org_dict.keys():
            g.add((poc, VCARD.hasURL, Literal(org_dict.get('site'))))

    def _augment_publisher_info(self, dataset_dict, dataset_ref):
        publisher = self.g.value(subject=dataset_ref, predicate=DCT.publisher, object=None, any=False)

        if publisher:
            for key, predicate in (
                    ('publisher_email', FOAF.mbox),
                    ('publisher_url', FOAF.homepage),
            ):
                self.g.add((publisher, predicate, Literal(self._get_dict_value(dataset_dict, key, 'N/A'))))


def _get_org(org_id):
    org_dict = {}
    if org_id:
        try:
            org_dict = logic.get_action('organization_show')(
                {'ignore_auth': True},
                {'id': org_id,
                 'include_datasets': False,
                 'include_tags': False,
                 'include_users': False,
                 'include_groups': False,
                 'include_extras': True,
                 'include_followers': False}
                )
        except Exception as err:
            log.warning("Cannot get org for %s: %s", org_id, err, exc_info=err)

    return org_dict
