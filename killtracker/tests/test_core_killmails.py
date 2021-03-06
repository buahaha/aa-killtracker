from datetime import timedelta
import unittest
from unittest.mock import patch

import requests_mock

from django.utils.dateparse import parse_datetime
from django.utils.timezone import now

from . import CacheStub, BravadoOperationStub
from ..core.killmails import Killmail, EntityCount, ZKB_REDISQ_URL, ZKB_API_URL
from .testdata.helpers import killmails_data, load_killmail
from ..utils import NoSocketsTestCase


MODULE_PATH = "killtracker.core.killmails"
unittest.util._MAX_LENGTH = 1000


@requests_mock.Mocker()
class TestCreateFromZkbRedisq(NoSocketsTestCase):
    def test_normal(self, requests_mocker):
        requests_mocker.register_uri(
            "GET",
            ZKB_REDISQ_URL,
            status_code=200,
            json={"package": killmails_data()[10000001]},
        )

        killmail = Killmail.create_from_zkb_redisq()

        self.assertIsNotNone(killmail)
        self.assertEqual(killmail.id, 10000001)
        self.assertEqual(killmail.solar_system_id, 30004984)
        self.assertAlmostEqual(killmail.time, now(), delta=timedelta(seconds=120))

        self.assertEqual(killmail.victim.alliance_id, 3011)
        self.assertEqual(killmail.victim.character_id, 1011)
        self.assertEqual(killmail.victim.corporation_id, 2011)
        self.assertEqual(killmail.victim.damage_taken, 434)
        self.assertEqual(killmail.victim.ship_type_id, 603)

        self.assertEqual(len(killmail.attackers), 3)

        attacker_1 = killmail.attackers[0]
        self.assertEqual(attacker_1.alliance_id, 3001)
        self.assertEqual(attacker_1.character_id, 1001)
        self.assertEqual(attacker_1.corporation_id, 2001)
        self.assertEqual(attacker_1.damage_done, 434)
        self.assertEqual(attacker_1.security_status, -10)
        self.assertEqual(attacker_1.ship_type_id, 34562)
        self.assertEqual(attacker_1.weapon_type_id, 2977)

        self.assertEqual(killmail.zkb.location_id, 50012306)
        self.assertEqual(killmail.zkb.fitted_value, 10000)
        self.assertEqual(killmail.zkb.total_value, 10000)
        self.assertEqual(killmail.zkb.points, 1)
        self.assertFalse(killmail.zkb.is_npc)
        self.assertFalse(killmail.zkb.is_solo)
        self.assertFalse(killmail.zkb.is_awox)

    def test_zkb_returns_empty_package(self, requests_mocker):
        requests_mocker.register_uri(
            "GET",
            ZKB_REDISQ_URL,
            status_code=200,
            json={"package": None},
        )

        killmail = Killmail.create_from_zkb_redisq()
        self.assertIsNone(killmail)

    def test_zkb_can_handle_no_solar_system(self, requests_mocker):
        requests_mocker.register_uri(
            "GET",
            ZKB_REDISQ_URL,
            status_code=200,
            json={"package": killmails_data()[10000402]},
        )

        killmail = Killmail.create_from_zkb_redisq()
        self.assertIsNotNone(killmail)


class TestKillmailSerialization(NoSocketsTestCase):
    def test_dict_serialization(self):
        killmail = load_killmail(10000001)
        dct_1 = killmail.asdict()
        killmail_2 = Killmail.from_dict(dct_1)
        self.maxDiff = None
        self.assertEqual(killmail, killmail_2)

    def test_json_serialization(self):
        killmail = load_killmail(10000001)
        json_1 = killmail.asjson()
        killmail_2 = Killmail.from_json(json_1)
        self.maxDiff = None
        self.assertEqual(killmail, killmail_2)


class TestKillmailBasics(NoSocketsTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.killmail = load_killmail(10000001)

    def test_str(self):
        self.assertEqual(str(self.killmail), "Killmail(id=10000001)")

    def test_repr(self):
        self.assertEqual(repr(self.killmail), "Killmail(id=10000001)")

    def test_entity_ids(self):
        result = self.killmail.entity_ids()
        expected = {
            1011,
            2011,
            3011,
            603,
            30004984,
            1001,
            1002,
            1003,
            2001,
            3001,
            34562,
            2977,
            3756,
            2488,
            500001,
            500004,
        }
        self.assertSetEqual(result, expected)

    def test_attackers_ships_types(self):
        self.assertListEqual(
            self.killmail.attackers_ship_type_ids(), [34562, 3756, 3756]
        )

    def test_ships_types(self):
        self.assertSetEqual(
            set(self.killmail.ship_type_ids()), {603, 34562, 3756, 3756}
        )


class TestEntityCount(NoSocketsTestCase):
    def test_is_alliance(self):
        alliance = EntityCount(1, EntityCount.CATEGORY_ALLIANCE)
        corporation = EntityCount(2, EntityCount.CATEGORY_CORPORATION)

        self.assertTrue(alliance.is_alliance)
        self.assertFalse(corporation.is_alliance)

    def test_is_corporation(self):
        alliance = EntityCount(1, EntityCount.CATEGORY_ALLIANCE)
        corporation = EntityCount(2, EntityCount.CATEGORY_CORPORATION)

        self.assertFalse(alliance.is_corporation)
        self.assertTrue(corporation.is_corporation)


@patch(MODULE_PATH + ".cache", CacheStub())
@patch(MODULE_PATH + ".esi")
@requests_mock.Mocker()
class TestCreateFromZkbApi(NoSocketsTestCase):
    def test_normal(self, mock_esi, requests_mocker):
        killmail_id = 10000001
        killmail_data = killmails_data()[killmail_id]
        zkb_api_data = [
            {"killmail_id": killmail_data["killID"], "zkb": killmail_data["zkb"]}
        ]
        requests_mocker.register_uri(
            "GET",
            f"{ZKB_API_URL}killID/{killmail_id}/",
            status_code=200,
            json=zkb_api_data,
        )
        killmail_data["killmail"]["killmail_time"] = parse_datetime(
            killmail_data["killmail"]["killmail_time"]
        )
        mock_esi.client.Killmails.get_killmails_killmail_id_killmail_hash.return_value = BravadoOperationStub(
            killmail_data["killmail"]
        )

        killmail = Killmail.create_from_zkb_api(killmail_id)
        self.assertIsNotNone(killmail)
        self.assertEqual(killmail.id, killmail_id)
        self.assertAlmostEqual(killmail.time, now(), delta=timedelta(seconds=120))

        self.assertEqual(killmail.victim.alliance_id, 3011)
        self.assertEqual(killmail.victim.character_id, 1011)
        self.assertEqual(killmail.victim.corporation_id, 2011)
        self.assertEqual(killmail.victim.damage_taken, 434)
        self.assertEqual(killmail.victim.ship_type_id, 603)

        self.assertEqual(len(killmail.attackers), 3)

        attacker_1 = killmail.attackers[0]
        self.assertEqual(attacker_1.alliance_id, 3001)
        self.assertEqual(attacker_1.character_id, 1001)
        self.assertEqual(attacker_1.corporation_id, 2001)
        self.assertEqual(attacker_1.damage_done, 434)
        self.assertEqual(attacker_1.security_status, -10)
        self.assertEqual(attacker_1.ship_type_id, 34562)
        self.assertEqual(attacker_1.weapon_type_id, 2977)

        self.assertEqual(killmail.zkb.location_id, 50012306)
        self.assertEqual(killmail.zkb.fitted_value, 10000)
        self.assertEqual(killmail.zkb.total_value, 10000)
        self.assertEqual(killmail.zkb.points, 1)
        self.assertFalse(killmail.zkb.is_npc)
        self.assertFalse(killmail.zkb.is_solo)
        self.assertFalse(killmail.zkb.is_awox)
