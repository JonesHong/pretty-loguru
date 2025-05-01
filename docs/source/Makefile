# 添加 apidoc 目標
apidoc:
	sphinx-apidoc -f -M -o "$(SOURCEDIR)/api" ../pretty_loguru

# 添加 github 目標 (用於 GitHub Pages)
github: clean html
	touch "$(BUILDDIR)/html/.nojekyll"