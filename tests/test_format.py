# stdlib
import os

# 3rd party
import black
from parameterized import parameterized  # type: ignore

# this package
from formate_black import black_hook
from tests.util import DEFAULT_MODE, THIS_DIR, BlackBaseTestCase, read_data

SIMPLE_CASES = [
		"beginning_backslash",
		"bracketmatch",
		"class_blank_parentheses",
		"class_methods_new_line",
		"collections",
		"comments",
		"comments2",
		"comments3",
		"comments4",
		"comments5",
		"comments6",
		"comments_non_breaking_space",
		"comment_after_escaped_newline",
		"composition",
		"composition_no_trailing_comma",
		"docstring",
		"empty_lines",
		"expression",
		"fmtonoff",
		"fmtonoff2",
		"fmtonoff3",
		"fmtonoff4",
		"fmtskip",
		"fmtskip2",
		"fmtskip3",
		"fmtskip4",
		"fmtskip5",
		"fstring",
		"function",
		"function2",
		"function_trailing_comma",
		"import_spacing",
		"remove_parens",
		"slices",
		"string_prefixes",
		"tricky_unicode_symbols",
		"tupleassign",
		]

SIMPLE_CASES_PY2 = [
		"numeric_literals_py2",
		"python2",
		"python2_unicode_literals",
		]

EXPERIMENTAL_STRING_PROCESSING_CASES = [
		"cantfit",
		"comments7",
		"long_strings",
		"long_strings__edge_case",
		"long_strings__regression",
		"percent_precedence",
		]

BLACK_BASE_DIR = os.path.abspath(os.path.join(black.__file__, ".."))

BLACK_SOURCES = [
		"__init__.py",
		"__main__.py",
		"brackets.py",
		"cache.py",
		"comments.py",
		"concurrency.py",
		"const.py",
		"debug.py",
		"files.py",
		"linegen.py",
		"lines.py",
		"mode.py",
		"nodes.py",
		"numerics.py",
		"output.py",
		"parsing.py",
		"report.py",
		"rusty.py",
		"strings.py",
		"trans.py",
		]

SOURCES = [os.path.join(BLACK_BASE_DIR, path) for path in BLACK_SOURCES]


class TestSimpleFormat(BlackBaseTestCase):

	@parameterized.expand(SIMPLE_CASES)
	def test_simple_format(self, filename: str) -> None:
		self.check_file(filename, DEFAULT_MODE, kwargs={})

	@parameterized.expand(EXPERIMENTAL_STRING_PROCESSING_CASES)
	def test_experimental_format(self, filename: str) -> None:
		self.check_file(
				filename,
				black.Mode(experimental_string_processing=True),  # type: ignore[call-arg]
				kwargs=dict(experimental_string_processing=True)
				)

	@parameterized.expand(SOURCES)
	def test_source_is_formatted(self, filename: str) -> None:
		path = THIS_DIR.parent / filename
		self.check_file(str(path), DEFAULT_MODE, data=False, kwargs={})

	def check_file(self, filename: str, mode: black.Mode, kwargs: dict, *, data: bool = True) -> None:
		source, expected = read_data(filename, data=data)
		actual = black_hook(source, filename, **kwargs)
		self.assertFormatEqual(expected, actual)
		if source != actual:
			black.assert_equivalent(source, actual)
			black.assert_stable(source, actual, mode)
