#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `planets` package."""

import pytest
import sys
from io import StringIO

from planets import cli


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/michaelaye/cookiecutter-pypackage-conda')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def capture_stdout(command, *args, **kwargs):
    """Capture stdout from a function call."""
    # Redirect stdout
    captured_output = StringIO()
    original_stdout = sys.stdout
    sys.stdout = captured_output

    # Call the command
    exit_code = command(*args, **kwargs)

    # Restore stdout
    sys.stdout = original_stdout

    return exit_code, captured_output.getvalue()


def test_command_line_interface():
    """Test the CLI."""
    # Save original sys.argv and mock it during testing
    original_argv = sys.argv
    sys.argv = ["planets"]  # Set to script name only for default test

    try:
        # Test default output
        exit_code, output = capture_stdout(cli.main)
        assert exit_code == 0
        assert "planets.cli.main" in output
        assert "Use --help to see available commands" in output

        # Test version flag
        exit_code, output = capture_stdout(cli.main, ["--version"])
        assert exit_code == 0
        assert "planets version" in output

        # Test list flag
        exit_code, output = capture_stdout(cli.main, ["--list"])
        assert exit_code == 0
        assert "Available bodies:" in output
        # Verify at least some known planets are in the output
        assert "Earth" in output
        assert "Mars" in output

        # Test body flag with a valid body
        exit_code, output = capture_stdout(cli.main, ["--body", "Earth"])
        assert exit_code == 0
        assert "Attributes for Earth" in output
        assert "name" in output

        # Test body flag with an invalid body
        exit_code, output = capture_stdout(cli.main, ["--body", "NonExistentPlanet"])
        assert exit_code == 1
        assert "Error: Body 'NonExistentPlanet' not found" in output

        # We can't easily test the help flag because argparse will call sys.exit()
        # Instead, we'll validate the parser has the expected arguments
        parser = cli.create_parser()
        actions = {action.dest: action for action in parser._actions}
        assert "help" in actions
        assert "version" in actions
        assert "list" in actions
        assert "body" in actions
    finally:
        # Restore original argv
        sys.argv = original_argv
