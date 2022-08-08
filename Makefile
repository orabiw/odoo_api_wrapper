.PHONY: generate-docs clean
.SILENT: generate-docs clean

clean:
	rm -fr docs

generate-docs: clean
	pdoc3 --html --output-dir=docs odoo_api_wrapper
