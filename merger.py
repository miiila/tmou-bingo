import PyPDF2
import os

for dirName, subdirList, fileList in os.walk('./out/karty'):
    target = open('bingo_karty.pdf', "wb")
    target_pdf = PyPDF2.PdfFileWriter()
    for f in fileList:
        if 'bingo' not in f and 'pdf' in f:
            srcfile = open(f'out/karty/{f}', "rb")
            srcpage = PyPDF2.PdfFileReader(srcfile).getPage(0)
            target_pdf.addPage(srcpage)
            target_pdf.write(target)

            srcfile.close()

