SPHINXBUILD  = sphinx-build
SOURCEDIR    = source
BUILDDIR     = build

.PHONY: help clean html apidoc github

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)"

clean:
	rm -rf "$(BUILDDIR)"

html:
	@$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)/html"

apidoc:
	sphinx-apidoc -f -M -o "$(SOURCEDIR)/api" ../pretty_loguru

github: clean html
	touch "$(BUILDDIR)/html/.nojekyll"

# 可選：支援所有 sphinx -M <target>
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)"
