from __future__ import annotations

import unittest

from build_site import add_related_articles


class RelatedArticlesTests(unittest.TestCase):
    def test_related_articles_prefer_shared_specific_tags(self) -> None:
        articles = [
            {
                "id": "retrieval-one",
                "title": "Building Retrieval Systems",
                "date": "2026-07-16",
                "tags": ["ai", "retrieval", "knowledge-management"],
            },
            {
                "id": "retrieval-two",
                "title": "Practical Knowledge Retrieval",
                "date": "2026-07-15",
                "tags": ["retrieval", "knowledge-management"],
            },
            {
                "id": "unrelated",
                "title": "Power Apps Date Controls",
                "date": "2026-07-14",
                "tags": ["power-apps", "forms"],
            },
        ]
        add_related_articles(articles)
        self.assertEqual(articles[0]["related"][0]["id"], "retrieval-two")
        self.assertNotIn("unrelated", [item["id"] for item in articles[0]["related"]])


if __name__ == "__main__":
    unittest.main()

