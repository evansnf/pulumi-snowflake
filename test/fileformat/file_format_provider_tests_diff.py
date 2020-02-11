import unittest
from unittest.mock import Mock

from pulumi_snowflake.fileformat import FileFormatProvider


class FileFormatProviderTests(unittest.TestCase):

    def test_when_type_and_database_are_unchanged_then_no_change(self):
        provider = FileFormatProvider(self.get_mock_provider(), Mock())
        result = provider.diff("test_file_format", {
            "type": "CSV",
            "database": "database_name"
        }, {
            "type": "CSV",
            "database": "database_name"
        })

        self.assertFalse(result.changes)
        self.assertSetEqual(set(result.replaces), set())

    def test_when_type_changed_then_needs_change(self):
        provider = FileFormatProvider(self.get_mock_provider(), Mock())
        result = provider.diff("test_file_format", {
            "type": "CSV",
            "database": "database_name"
        }, {
            "type": "JSON",
            "database": "database_name"
        })

        self.assertTrue(result.changes)
        self.assertSetEqual(set(result.replaces), {"type"})

    def test_when_database_changed_then_needs_change(self):
        provider = FileFormatProvider(self.get_mock_provider(), Mock())
        result = provider.diff("test_file_format", {
            "type": "CSV",
            "database": "database_name"
        }, {
            "type": "CSV",
            "database": "database_name_changed"
        })

        self.assertTrue(result.changes)
        self.assertSetEqual(set(result.replaces), {"database"})

    def test_when_name_changed_then_needs_change(self):
        provider = FileFormatProvider(self.get_mock_provider(), Mock())
        result = provider.diff("test_file_format", {
            "type": "CSV",
            "database": "database_name",
            "name": "name_old"
        }, {
            "type": "CSV",
            "database": "database_name",
            "name": "name_new"
        })

        self.assertTrue(result.changes)
        self.assertSetEqual(set(result.replaces), {"name"})

    def test_when_name_not_given_in_news_then_no_change(self):
        provider = FileFormatProvider(self.get_mock_provider(), Mock())
        result = provider.diff("test_file_format", {
            "type": "CSV",
            "database": "database_name",
            "name": "name_old"
        }, {
            "type": "CSV",
            "database": "database_name"
        })

        self.assertFalse(result.changes)
        self.assertSetEqual(set(result.replaces), set())

    def test_when_schema_changed_then_needs_change(self):
        provider = FileFormatProvider(self.get_mock_provider(), Mock())
        result = provider.diff("test_file_format", {
            "type": "CSV",
            "database": "database_name",
            "schema": "schema_old"
        }, {
            "type": "CSV",
            "database": "database_name",
            "schema": "schema_new"
        })

        self.assertTrue(result.changes)
        self.assertSetEqual(set(result.replaces), {"schema"})

    # HELPERS

    def get_mock_provider(self):
        mock_provider = Mock()
        mock_provider.database = None
        mock_provider.schema = None
        return mock_provider
