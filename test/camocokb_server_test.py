# -*- coding: utf-8 -*-
import os
import time
import unittest
from configparser import ConfigParser
from pprint import pprint as pp

from camocokb.camocokbImpl import camocokb
from camocokb.camocokbServer import MethodContext
from camocokb.authclient import KBaseAuth as _KBaseAuth

from installed_clients.WorkspaceClient import Workspace


class camocokbTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = os.environ.get('KB_AUTH_TOKEN', None)
        config_file = os.environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('camocokb'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'camocokb',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = Workspace(cls.wsURL)
        cls.serviceImpl = camocokb(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']
        suffix = int(time.time() * 1000)
        cls.wsName = "test_ContigFilter_" + str(suffix)
        ret = cls.wsClient.create_workspace({'workspace': cls.wsName})  # noqa

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    def getContext(self):
        return self.__class__.ctx

    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    def test_ref_data(self):
        # Prepare test objects in workspace if needed using
        # self.getWsClient().save_objects({'workspace': self.getWsName(),
        #                                  'objects': []})
        #
        # Run your method by
        # ret = self.getImpl().your_method(self.getContext(), parameters...)
        #
        # Check returned data with
        # self.assertEqual(ret[...], ...) or other unittest methods

        # This test will build all the camoco objects using impl functions and data provided from the reference data
        # mount. This data is provided by camoco, and roughly follows there tutorial process, and can be accessed here:
        # https://camoco.readthedocs.io/en/latest/tutorial.html . Check out scripts/entrypoint.sh to see how reference
        # data is downloaded and processed

        # Refgen data
        if os.path.exists('/data/ZmB73_5b_FGS.gff'):
            self.refgen_file = '/data/ZmB73_5b_FGS.gff'
        else:
            raise FileNotFoundError('RefGen reference data does not exist at: /data/ZmB73_5b_FGS.gff')

        # Expression data
        if os.path.exists('/data/Hirsch2014_PANGenomeFPKM.txt'):
            self.expr_file = '/data/Hirsch2014_PANGenomeFPKM.txt'
        else:
            raise FileNotFoundError('Expression reference data does not exist at: /data/Hirsch2014_PANGenomeFPKM.txt')

        # Ontology base data
        if os.path.exists('/data/go.obo'):
            self.base_ontology_file = '/data/go.obo'
        else:
            raise FileNotFoundError('Base ontology reference data does not exist at: /data/go.obo')

        # Maize ontology data
        if os.path.exists('/data/zm_go.tsv'):
            self.maize_ontology_file = '/data/zm_go.tsv'
        else:
            raise FileNotFoundError('Maize ontology reference data does not exist at: /data/zm_go.tsv')

        if os.path.exists('/data/ZmIonome.allLocs.csv'):
            self.maize_gwas_file = '/data/ZmIonome.allLocs.csv'
        else:
            raise FileNotFoundError('Maize GWAS reference data does not exist at: /data/ZmIonome.allLocs.csv')

    def mk_refgen(self):
        self.test_ref_data()

        self.refgen_name = 'Zm5bFGS'

        refgen_params = {
            'filename': self.refgen_file,
            'refgen_name': self.refgen_name,
            'description': 'GFF Genome file from KBase',
            'build': 5.0,
            'organism': 'Zea Mays'
        }

        self.serviceImpl.buildrefgen(self.getContext(), refgen_params)

    def mk_cob(self):
        self.mk_refgen()

        cob_params = {
            'filename': self.expr_file,
            'cob_name': 'ZmRoot',
            'description': 'Maize Root Network',
            'refgen_name': self.refgen_name
        }

        self.serviceImpl.buildcob(self.getContext(), cob_params)

    def test_mk_ontology(self):
        self.mk_cob()

        ontology_params = {
            'filename': self.maize_ontology_file,
            'base_onotology_path': self.base_ontology_file,
            'ontology_name': "ZmGO",
            'description': "Maize GO",
            'refgen_name': self.refgen_name
        }

        self.serviceImpl.buildcob(self.getContext(), cob_params)

