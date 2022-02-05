#!/usr/bin/env python3
#
#  __init__.py
"""
Use black with formate.
"""
#
#  Copyright © 2021 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
import itertools
from collections.abc import Mapping
from typing import Optional

# 3rd party
import black
from black import TargetVersion
from black.lines import Line
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.typing import PathLike
from domdf_python_tools.words import TAB
from formate.config import wants_filename, wants_global_config

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2021 Dominic Davis-Foster"
__license__: str = "MIT License"
__version__: str = "0.2.0"
__email__: str = "dominic@davis-foster.co.uk"

__all__ = ["black_hook"]


@wants_filename
@wants_global_config
def black_hook(
		source: str,
		formate_filename: PathLike,
		formate_global_config: Optional[Mapping] = None,
		**kwargs,
		) -> str:
	r"""
	Call `black <https://pypi.org/project/black/>`_, using the given keyword arguments as its configuration.

	:param source: The source to reformat.
	:param formate_global_config: The global configuration dictionary. Optional.
	:param \*\*kwargs:

	:returns: The reformatted source.
	"""

	black_mode_cls = black.Mode

	if "use_tabs" in kwargs:
		if kwargs.pop("use_tabs"):
			black_mode_cls = TabsMode
	elif formate_global_config:
		if formate_global_config.get("indent") == TAB:
			black_mode_cls = TabsMode

	if "line_length" not in kwargs and formate_global_config:
		if "line_length" in (formate_global_config or {}):
			kwargs["line_length"] = formate_global_config["line_length"]

	kwargs["is_pyi"] = PathPlus(formate_filename).suffix == ".pyi"

	if "target_versions" in kwargs:
		kwargs["target_versions"] = {TargetVersion[val.upper()] for val in kwargs["target_versions"]}
	else:
		kwargs["target_versions"] = set()

	if "target_version" in kwargs:
		kwargs["target_versions"].add(TargetVersion[kwargs.pop("target_version").upper()])

	return black.format_str(source, mode=black_mode_cls(**kwargs))


# The following adapted from black itself
# https://github.com/psf/black
# MIT Licensed
# Copyright (c) 2018 Łukasz Langa


def line_str(self: Line) -> str:
	"""
	Render the line.
	"""

	if not self:
		return '\n'

	if getattr(self.mode, "use_tabs", False):
		indent = '\t' * self.depth
	else:
		indent = "    " * self.depth

	leaves = iter(self.leaves)
	first = next(leaves)
	res = f"{first.prefix}{indent}{first.value}"

	for leaf in leaves:
		res += str(leaf)

	for comment in itertools.chain.from_iterable(self.comments.values()):
		res += str(comment)

	return res + '\n'


Line.__str__ = line_str  # type: ignore


class TabsMode(black.Mode):
	use_tabs = True
