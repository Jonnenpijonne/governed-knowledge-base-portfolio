from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import validate  # noqa: E402


VALID = """---
type: policy
status: approved
date: 2026-09-13
classification: public-demo
owner_role: information-owner
description: Synthetic test document.
---
# Test
Only synthetic content.
"""


class ValidationTests(unittest.TestCase):
    def make_repo(self, content: str = VALID) -> Path:
        temp = TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        target = root / "docs" / "governance" / "test.md"
        target.parent.mkdir(parents=True)
        target.write_text(content, encoding="utf-8")
        return root

    def test_valid_document_passes(self):
        self.assertEqual(validate.validate(self.make_repo()), [])

    def test_missing_metadata_fails(self):
        root = self.make_repo(VALID.replace("owner_role: information-owner\n", ""))
        self.assertTrue(any("missing metadata field owner_role" in e for e in validate.validate(root)))

    def test_secret_pattern_fails(self):
        fake = "AKIA" + "A" * 16
        root = self.make_repo(VALID + fake)
        self.assertTrue(any("AWS access key" in e for e in validate.validate(root)))

    def test_email_fails(self):
        address = "person" + "@" + "example" + ".invalid"
        root = self.make_repo(VALID + address)
        self.assertTrue(any("email address" in e for e in validate.validate(root)))

    def test_internal_url_fails(self):
        url = "https://" + "portal" + ".internal/path"
        root = self.make_repo(VALID + url)
        self.assertTrue(any("private/internal URL" in e for e in validate.validate(root)))


if __name__ == "__main__":
    unittest.main()
