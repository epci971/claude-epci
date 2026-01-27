#!/usr/bin/env python3
"""Tests for deploy.py - EPCI deployment script."""

import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch


class TestDeployScript(unittest.TestCase):
    """Test suite for deploy.py functions."""

    def setUp(self):
        """Create temporary directories for testing."""
        self.temp_dir = tempfile.mkdtemp()
        self.src_dir = Path(self.temp_dir) / "src"
        self.build_dir = Path(self.temp_dir) / "build" / "epci"

        # Create mock source structure
        self.src_dir.mkdir(parents=True)
        (self.src_dir / ".claude-plugin").mkdir()
        (self.src_dir / ".claude-plugin" / "plugin.json").write_text(
            '{"name": "test", "version": "1.0.0", "description": "test", "skills": []}'
        )
        (self.src_dir / "skills").mkdir()
        (self.src_dir / "agents").mkdir()

        # Create __pycache__ that should be excluded
        pycache_dir = self.src_dir / "__pycache__"
        pycache_dir.mkdir()
        (pycache_dir / "test.pyc").write_text("cache")

    def tearDown(self):
        """Clean up temporary directories."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_copy_tree_safe_creates_destination(self):
        """Test that copy_tree_safe creates the destination directory."""
        from deploy import copy_tree_safe

        copy_tree_safe(self.src_dir, self.build_dir, force=True)

        self.assertTrue(self.build_dir.exists())
        self.assertTrue((self.build_dir / ".claude-plugin" / "plugin.json").exists())

    def test_copy_tree_safe_excludes_pycache(self):
        """Test that __pycache__ directories are excluded from copy."""
        from deploy import copy_tree_safe

        copy_tree_safe(self.src_dir, self.build_dir, force=True)

        self.assertFalse((self.build_dir / "__pycache__").exists())

    def test_copy_tree_safe_excludes_pyc_files(self):
        """Test that .pyc files are excluded from copy."""
        from deploy import copy_tree_safe

        # Create a .pyc file in skills
        (self.src_dir / "skills" / "test.pyc").write_text("compiled")

        copy_tree_safe(self.src_dir, self.build_dir, force=True)

        self.assertFalse((self.build_dir / "skills" / "test.pyc").exists())

    def test_copy_tree_safe_excludes_tests_directory(self):
        """Test that tests/ directories are excluded from copy."""
        from deploy import copy_tree_safe

        # Create tests directory
        tests_dir = self.src_dir / "tests"
        tests_dir.mkdir()
        (tests_dir / "test_something.py").write_text("test code")

        copy_tree_safe(self.src_dir, self.build_dir, force=True)

        self.assertFalse((self.build_dir / "tests").exists())

    def test_copy_tree_safe_fails_if_dest_exists_without_force(self):
        """Test that copy fails if destination exists and force=False."""
        from deploy import copy_tree_safe

        self.build_dir.mkdir(parents=True)

        with self.assertRaises(FileExistsError):
            copy_tree_safe(self.src_dir, self.build_dir, force=False)

    def test_dry_run_does_not_modify_filesystem(self):
        """Test that --dry-run does not create any files."""
        from deploy import deploy

        result = deploy(
            src=self.src_dir,
            dest=self.build_dir,
            dry_run=True,
            force=True,
            verbose=False,
        )

        self.assertFalse(self.build_dir.exists())
        self.assertEqual(result, 0)  # Success exit code

    def test_rollback_on_validation_failure(self):
        """Test that build directory is removed if validation fails."""
        from deploy import deploy

        # Create invalid plugin.json that will fail validation
        (self.src_dir / ".claude-plugin" / "plugin.json").write_text(
            '{"invalid": "json without required fields"}'
        )

        result = deploy(
            src=self.src_dir,
            dest=self.build_dir,
            dry_run=False,
            force=True,
            verbose=False,
        )

        # Build dir should be removed after failed validation
        self.assertFalse(self.build_dir.exists())
        self.assertNotEqual(result, 0)  # Non-zero exit code


if __name__ == "__main__":
    unittest.main()
