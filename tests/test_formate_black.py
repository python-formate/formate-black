# stdlib
import re
import sys

# 3rd party
import black
import pytest
from black import InvalidInput
from coincidence import AdvancedFileRegressionFixture

# this package
from formate_black import black_hook
from tests.util import DEFAULT_MODE, THIS_DIR, read_data


def test_async_as_identifier() -> None:
	source_path = (THIS_DIR / "data" / "async_as_identifier.py").resolve()
	source, expected = read_data("async_as_identifier")
	actual = black_hook(source, formate_filename=source_path)
	assert expected == actual

	major, minor = sys.version_info[:2]
	if major < 3 or (major <= 3 and minor < 7):
		black.assert_equivalent(source, actual)

	black.assert_stable(source, actual, DEFAULT_MODE)

	# ensure black can parse this when the target is 3.6
	black_hook(source, formate_filename=source_path, target_version="py36")

	# but not on 3.7, because async/await is no longer an identifier
	with pytest.raises(InvalidInput, match="Cannot parse: 1:4: def async()"):
		black_hook(source, formate_filename=source_path, target_version="py37")


def test_python37() -> None:
	source_path = (THIS_DIR / "data" / "python37.py").resolve()
	source, expected = read_data("python37")
	actual = black_hook(source, formate_filename=source_path)
	assert expected == actual

	major, minor = sys.version_info[:2]
	if major < 3 or (major <= 3 and minor < 7):
		black.assert_equivalent(source, actual)

	black.assert_stable(source, actual, DEFAULT_MODE)

	# ensure black can parse this when the target is 3.7
	black_hook(source, formate_filename=source_path, target_version="py37")

	# but not on 3.6, because we use async as a reserved keyword
	with pytest.raises(
			InvalidInput,
			match=re.escape("Cannot parse: 26:18:     return (await awaitable for awaitable in awaitable_list)"),
			):
		black_hook(source, formate_filename=source_path, target_version="py36")


def test_python38() -> None:
	source_path = (THIS_DIR / "data" / "python38.py").resolve()
	source, expected = read_data("python38")
	actual = black_hook(source, formate_filename=source_path)
	assert expected == actual

	major, minor = sys.version_info[:2]
	if major > 3 or (major == 3 and minor >= 8):
		black.assert_equivalent(source, actual)

	black.assert_stable(source, actual, DEFAULT_MODE)


@pytest.mark.parametrize("length", [80, 115, 300])
def test_line_length(advanced_file_regression: AdvancedFileRegressionFixture, length: int) -> None:
	source_path = (THIS_DIR / "data" / "long_strings.py").resolve()
	source, expected = read_data("long_strings")

	actual = black_hook(source, formate_filename=source_path, line_length=length)
	advanced_file_regression.check(actual)

	# TODO:
	# black.assert_stable(source, actual, DEFAULT_MODE)


@pytest.mark.parametrize("length", [80, 115, 300])
def test_line_length_global(advanced_file_regression: AdvancedFileRegressionFixture, length: int) -> None:
	source_path = (THIS_DIR / "data" / "long_strings.py").resolve()
	source, expected = read_data("long_strings")

	actual = black_hook(source, formate_filename=source_path, formate_global_config={"line_length": length})
	advanced_file_regression.check(actual)

	# TODO:
	# black.assert_stable(source, actual, DEFAULT_MODE)


def test_python39() -> None:
	source_path = (THIS_DIR / "data" / "python39.py").resolve()
	source, expected = read_data("python39")
	actual = black_hook(source, formate_filename=source_path)
	assert expected == actual

	major, minor = sys.version_info[:2]
	if major > 3 or (major == 3 and minor >= 9):
		black.assert_equivalent(source, actual)

	black.assert_stable(source, actual, DEFAULT_MODE)


def test_tab_comment_indentation() -> None:
	contents_tab = "if 1:\n\tif 2:\n\t\tpass\n\t# comment\n\tpass\n"
	contents_spc = "if 1:\n    if 2:\n        pass\n    # comment\n    pass\n"
	assert contents_spc == black_hook(contents_spc, formate_filename="code.py")
	assert contents_spc == black_hook(contents_tab, formate_filename="code.py")
	assert contents_spc == black_hook(contents_spc, formate_filename="code.py", use_tabs=False)
	assert contents_spc == black_hook(contents_tab, formate_filename="code.py", use_tabs=False)

	contents_tab = "if 1:\n\tif 2:\n\t\tpass\n\t\t# comment\n\tpass\n"
	contents_spc = "if 1:\n    if 2:\n        pass\n        # comment\n    pass\n"
	assert contents_spc == black_hook(contents_spc, formate_filename="code.py")
	assert contents_spc == black_hook(contents_tab, formate_filename="code.py")
	assert contents_spc == black_hook(contents_spc, formate_filename="code.py", use_tabs=False)
	assert contents_spc == black_hook(contents_tab, formate_filename="code.py", use_tabs=False)

	# mixed tabs and spaces (valid Python 2 code)
	contents_tab = "if 1:\n        if 2:\n\t\tpass\n\t# comment\n        pass\n"
	contents_spc = "if 1:\n    if 2:\n        pass\n    # comment\n    pass\n"
	assert contents_spc == black_hook(contents_spc, formate_filename="code.py")
	assert contents_spc == black_hook(contents_tab, formate_filename="code.py")
	assert contents_spc == black_hook(contents_spc, formate_filename="code.py", use_tabs=False)
	assert contents_spc == black_hook(contents_tab, formate_filename="code.py", use_tabs=False)

	contents_tab = "if 1:\n        if 2:\n\t\tpass\n\t\t# comment\n        pass\n"
	contents_spc = "if 1:\n    if 2:\n        pass\n        # comment\n    pass\n"
	assert contents_spc == black_hook(contents_spc, formate_filename="code.py")
	assert contents_spc == black_hook(contents_tab, formate_filename="code.py")
	assert contents_spc == black_hook(contents_spc, formate_filename="code.py", use_tabs=False)
	assert contents_spc == black_hook(contents_tab, formate_filename="code.py", use_tabs=False)


def test_tab_comment_indentation_use_tabs() -> None:
	contents_tab = "if 1:\n\tif 2:\n\t\tpass\n\t# comment\n\tpass\n"
	contents_spc = "if 1:\n    if 2:\n        pass\n    # comment\n    pass\n"
	assert contents_tab == black_hook(contents_spc, formate_filename="code.py", use_tabs=True)
	assert contents_tab == black_hook(contents_tab, formate_filename="code.py", use_tabs=True)

	contents_tab = "if 1:\n\tif 2:\n\t\tpass\n\t\t# comment\n\tpass\n"
	contents_spc = "if 1:\n    if 2:\n        pass\n        # comment\n    pass\n"
	assert contents_tab == black_hook(contents_spc, formate_filename="code.py", use_tabs=True)
	assert contents_tab == black_hook(contents_tab, formate_filename="code.py", use_tabs=True)


def test_tab_comment_indentation_use_tabs_global() -> None:
	contents_tab = "if 1:\n\tif 2:\n\t\tpass\n\t# comment\n\tpass\n"
	contents_spc = "if 1:\n    if 2:\n        pass\n    # comment\n    pass\n"
	assert contents_tab == black_hook(
			contents_spc,
			formate_filename="code.py",
			formate_global_config={"indent": '\t'},
			)
	assert contents_tab == black_hook(
			contents_tab,
			formate_filename="code.py",
			formate_global_config={"indent": '\t'},
			)

	contents_tab = "if 1:\n\tif 2:\n\t\tpass\n\t\t# comment\n\tpass\n"
	contents_spc = "if 1:\n    if 2:\n        pass\n        # comment\n    pass\n"
	assert contents_tab == black_hook(
			contents_spc,
			formate_filename="code.py",
			formate_global_config={"indent": '\t'},
			)
	assert contents_tab == black_hook(
			contents_tab,
			formate_filename="code.py",
			formate_global_config={"indent": '\t'},
			)
