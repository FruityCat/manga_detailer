import unittest
from tagging.tag_tools import TagTools


class TestTagTools(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        TagTools.reload()

    def test_find_translations(self):
        query = "1-panel"
        expected_id = "GHthFcCppABKx-okOMBFM"
        expected_parent = "GHthFcCppABKx-okOMBFM"

        result = TagTools.find(query)
        fail_msg = f"Query '{query}' expected '{expected_parent}:{expected_id}', found '{result.parent_id}:{result.id}'"
        self.assertEqual(
            result.id,
            expected_id,
            fail_msg
        )
        self.assertEqual(
            result.parent_id,
            expected_parent,
            fail_msg
        )
        print(f"{query} |\n Expected: {expected_parent}:{expected_id} - Found: {result.parent_id}:{result.id}")

    def test_find_translations_1(self):
        query = "yandere"
        expected_id = "Aqfs4DtaDQFei0vx9d9yl"
        expected_parent = "Aqfs4DtaDQFei0vx9d9yl"

        result = TagTools.find(query)
        fail_msg = f"Query '{query}' expected '{expected_parent}:{expected_id}', found '{result.parent_id}:{result.id}'"
        self.assertEqual(
            result.id,
            expected_id,
            fail_msg
        )
        self.assertEqual(
            result.parent_id,
            expected_parent,
            fail_msg
        )
        print(f"{query} |\n Expected: {expected_parent}:{expected_id} - Found: {result.parent_id}:{result.id}")

    def test_find_translations_2(self):
        query = "ThisIsNotARealTag"
        expected_id = None
        expected_parent = None

        result = TagTools.find(query)
        fail_msg = ""
        if result:
            fail_msg = f"Query '{query}' expected '{expected_parent}:{expected_id}', found '{result.parent_id}:{result.id}'"
        self.assertEqual(
            result,
            expected_id,
            fail_msg
        )
        self.assertEqual(
            result,
            expected_parent,
            fail_msg
        )
        print(f"{query} |\n Expected: {None}:{None} - Found: {result}:{result}")

    def test_find_aliases(self):
        query = "yakuza"
        expected_id = "8qW02GELImGk9MKez0Ry2"
        expected_parent = "X0S2qdOkxLC6NLACXUfcX"

        result = TagTools.find(query)
        fail_msg = f"Query '{query}' expected '{expected_parent}:{expected_id}', found '{result.parent_id}:{result.id}'"
        self.assertEqual(
            result.id,
            expected_id,
            fail_msg
        )
        self.assertEqual(
            result.parent_id,
            expected_parent,
            fail_msg
        )
        print(f"{query} |\n Expected: {expected_parent}:{expected_id} - Found: {result.parent_id}:{result.id}")

    def test_find_aliases_1(self):
        query = "school band"
        expected_id = "s_1S5lxsbr4KIHXn7Pkhr"
        expected_parent = "s_1S5lxsbr4KIHXn7Pkhr"

        result = TagTools.find(query)
        fail_msg = f"Query '{query}' expected '{expected_parent}:{expected_id}', found '{result.parent_id}:{result.id}'"
        self.assertEqual(
            result.id,
            expected_id,
            fail_msg
        )
        self.assertEqual(
            result.parent_id,
            expected_parent,
            fail_msg
        )
        print(f"{query} |\n Expected: {expected_parent}:{expected_id} - Found: {result.parent_id}:{result.id}")

    def test_find_alternate_spellings(self):
        query = "basket-ball"
        expected_id = "Z0RmnbuHQJHb3YXADgIJ4"
        expected_parent = "KMrJRGscw5qLwlcDIzI8U"

        result = TagTools.find(query)
        fail_msg = f"Query '{query}' expected '{expected_parent}:{expected_id}', found '{result.parent_id}:{result.id}'"
        self.assertEqual(
            result.id,
            expected_id,
            fail_msg
        )
        self.assertEqual(
            result.parent_id,
            expected_parent,
            fail_msg
        )
        print(f"{query} |\n Expected: {expected_parent}:{expected_id} - Found: {result.parent_id}:{result.id}")

    def test_find_alternate_spellings_1(self):
        query = "school-band"
        expected_id = "s_1S5lxsbr4KIHXn7Pkhr"
        expected_parent = "s_1S5lxsbr4KIHXn7Pkhr"

        result = TagTools.find(query)
        fail_msg = f"Query '{query}' expected '{expected_parent}:{expected_id}', found '{result.parent_id}:{result.id}'"
        self.assertEqual(
            result.id,
            expected_id,
            fail_msg
        )
        self.assertEqual(
            result.parent_id,
            expected_parent,
            fail_msg
        )
        print(f"{query} |\n Expected: {expected_parent}:{expected_id} - Found: {result.parent_id}:{result.id}")

    def test_find_alternate_spellings_2(self):
        query = "schools"
        expected_id = "HEoNGy9TTQSZZoWqDsMcd"
        expected_parent = "HEoNGy9TTQSZZoWqDsMcd"

        result = TagTools.find(query)
        fail_msg = f"Query '{query}' expected '{expected_parent}:{expected_id}', found '{result.parent_id}:{result.id}'"
        self.assertEqual(
            result.id,
            expected_id,
            fail_msg
        )
        self.assertEqual(
            result.parent_id,
            expected_parent,
            fail_msg
        )
        print(f"{query} |\n Expected: {expected_parent}:{expected_id} - Found: {result.parent_id}:{result.id}")


if __name__ == "__main__":
    unittest.main()
