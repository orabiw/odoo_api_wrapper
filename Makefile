.PHONY: generate-docs clean test
.SILENT: generate-docs clean test

clean:
	rm -fr docs

generate-docs: clean
	pdoc3 --html --output-dir=docs odoo_api_wrapper

test:
	tox -c odoo_api_wrapper
