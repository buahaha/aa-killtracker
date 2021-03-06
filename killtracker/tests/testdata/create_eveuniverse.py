from django.test import TestCase

from eveuniverse.tools.testdata import create_testdata, ModelSpec

from . import test_data_filename


class CreateEveUniverseTestData(TestCase):
    def test_create_testdata(self):
        testdata_spec = [
            ModelSpec("EveFaction", ids=[500001]),
            ModelSpec(
                "EveType",
                ids=[603, 621, 638, 2488, 2977, 3756, 11379, 16238, 34562, 37483],
            ),
            ModelSpec(
                "EveSolarSystem", ids=[30001161, 30004976, 30004984, 30045349, 31000005]
            ),
            ModelSpec("EveRegion", ids=[10000038], include_children=True),
        ]
        create_testdata(testdata_spec, test_data_filename())
