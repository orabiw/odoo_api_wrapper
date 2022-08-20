.PHONY: generate-docs clean test build
.SILENT: generate-docs clean test build

clean:
	rm -fr docs

generate-docs: clean
	pdoc3 --html --output-dir=docs odoo_api_wrapper
	mv docs/odoo_api_wrapper/* docs/
	rmdir docs/odoo_api_wrapper

test:
	tox --develop

build:
	tox --notest
