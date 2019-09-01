
MAIN = eag

all:
	pdflatex $(MAIN) 
	bibtex $(MAIN) 
	pdflatex $(MAIN) 
	pdflatex $(MAIN) 

	open $(MAIN).pdf

clean:
	rm -rf *.aux *.log *.bbl *.blg *.dvi *.pdf *.toc

