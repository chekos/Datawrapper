serve:
	@rm -rf docs/_build
	@rm -rf docs/_build_html
	@cd docs && uv run make livehtml
