import os
import random
from PIL import Image
from unidecode import unidecode
import PyPDF2
from datetime import datetime

word_list = ['Jošt', 'Parnas', 'Letmo', 'mozzarella', 'niva', 'korbáčik', 'Maroko', 'Tokarczuková', 'střelka', 'placka',
             'nůžky', 'kletr', 'děj', 'nebo', 'orloj', 'Kryl', 'haluz', 'tečka', 'čárka', 'Braille',
             'buzola', 'zákys', 'semafor', 'čelovka', 'Kachna', 'Svíčky', 'Bedna', 'Sendvič', 'statek', 'eurofólie',
             'mřížka', 'kalendář', 'Ono', 'Okoř', 'mapa']

print('words length: ', len(word_list))

tickets = []

limit = 270
ticketLen = 25


def build_ticket_rec(ticket, words):
    current_words = words[:]
    if len(ticket) == ticketLen:
        return ticket
    ticket.append(current_words.pop(random.randint(0, len(current_words) - 1)))

    return build_ticket_rec(ticket, current_words)


def build_tex(words, filename):
    output = '''
\\documentclass[11pt]{article}
\\pagenumbering{gobble}
\\usepackage{graphicx}
\\usepackage{geometry}
\\geometry{
 a5paper,
 left=4mm,
 top=30mm,
 }
\\usepackage{fontspec}
\\defaultfontfeatures{Mapping=tex-text,Scale=MatchLowercase}
\\setmainfont{Calibri}

\\begin{document}
  \\textit{V tomto hracím plánu pro hru BINGO nehledejte šifru.}
  \\vspace{\\baselineskip}
  \\vspace{\\baselineskip}
  
  \\begin{tabular}{ | c | c | c | c | c | }
    \\hline
        '''

    for i, word in enumerate(words):
        img_path = f'./img/scaled/{unidecode(word).lower()}.png'
        width, height = Image.open(img_path).size
        dimension = 'width' if width > height else 'height'
        if i % 5 == 4:
            output += f'\\includegraphics[{dimension}=22.1mm]{{{img_path}}} \\\\\n\\hline\n'
        else:
            output += f'\\includegraphics[{dimension}=22.1mm]{{{img_path}}} &\n'

    output += '''
    \\hline
  \\end{tabular}
\\end{document}
    '''

    with open(f'tmp/{filename}.tex', 'w') as f:
        f.write(output)


# merge pdf via some random python library
def merge_src_header(sourcePath, pdfHeaderPath, outputPath):
    srcfile = open(sourcePath, "rb")
    hdrfile = open(pdfHeaderPath, "rb")
    outfile = open(outputPath, "wb")
    srcpage = PyPDF2.PdfFileReader(srcfile).getPage(0)
    hdrpage = PyPDF2.PdfFileReader(hdrfile).getPage(0)
    srcpage.mergePage(hdrpage)
    writer = PyPDF2.PdfFileWriter()
    writer.addPage(srcpage)  # now with header
    writer.write(outfile)
    srcfile.close()
    hdrfile.close()
    outfile.close()


while len(tickets) < limit:
    tickets.append(build_ticket_rec([], word_list))

w = ''
for ticket in tickets:
    w += ','.join(ticket)
    w += '\n'

with open('tickets', 'w') as f:
    f.write(w)

version = datetime.now().strftime('%m-%d_%H-%M')

for i, ticket in enumerate(tickets):
    name = f'bingo_tiket_{i:03}_v{version}'
    build_tex(tickets[i], 'tiket')
    os.system(f'lualatex --output-dir=./tmp tmp/tiket.tex')
    merge_src_header(f'tmp/tiket.pdf', 'header.pdf', f'out/{name}.pdf')

