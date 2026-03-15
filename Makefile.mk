# Makefile pour compiler tous les articles
SOURCES = $(wildcard articles/*/*.md)
TARGETS = $(SOURCES:.md=.pdf)

all: $(TARGETS)

articles/%.pdf: articles/%.md templates/tian-dao-article.tex
	cd $(dir $<) && pandoc $(notdir $<) \
		--template=../../templates/tian-dao-article.tex \
		--resource-path=".:../.." \
		-o $(notdir $@) \
		--pdf-engine=xelatex

clean:
	rm -f articles/*/*.pdf

.PHONY: all clean