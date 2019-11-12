import random
import matplotlib.pyplot as plt

word_list = ['Jošt', 'Parnas', 'Letmo', 'mozzarella', 'niva', 'korbáčik', 'Maroko', 'Tokarczuková', 'střelka', 'placka',
             'nůžky', 'kletr', 'děj', 'nebo', 'orloj', 'Kryl', 'haluz', 'tečka', 'čárka', 'Braille',
             'buzola', 'zákys', 'semafor', 'čelovka', 'Kachna', 'Svíčky', 'Bedna', 'Sendvič', 'statek', 'eurofólie',
             'mřížka', 'kalendář', 'Ono', 'Okoř', 'mapa']


bingos = [None] * len(word_list)*3


def play():
    tickets = []
    with open('tickets') as f:
        for l in f.read().splitlines():
            tickets.append(l.split(','))

    pull_rec(word_list, tickets)


def pull_rec(words, tickets):
    round = 35 - len(words)
    current_words = words[:]
    if len(current_words) == 0:
        return
    word = current_words.pop(random.randint(0, len(current_words) - 1))

    for ticket in tickets:
        if ticket is None:
            continue
        for index, w in enumerate(ticket):
            if w == word:
                ticket[index] = 'X'

    for i, ticket in enumerate(tickets):
        if ticket is None:
            continue
        if validate_bingo(ticket):
            tickets[i] = None
            if bingos[round * 3] is None:
                bingos[round * 3] = 0
            bingos[round*3] += 1

    return pull_rec(current_words, tickets)


def validate_bingo(ticket):
    for i in range(0, 5):
        # test rows
        if all(x == 'X' for x in ticket[5*i:(5*i)+5]):
            return True
        # test cols
        if all(x == 'X' for x in ticket[i::5]):
            return True
    # test diagonals
    if all(x == 'X' for x in [ticket[0], ticket[6], ticket[12], ticket[18], ticket[24]]):
        return True
    if all(x == 'X' for x in [ticket[4], ticket[8], ticket[12], ticket[16], ticket[20]]):
        return True

    return False


limit = 1000
for i in range(0, limit):
    play()
    if i%10==0:
        print(f'Fnished simulation #{i}')


plt.xticks(range(0, len(word_list)*3)[0::3])
plt.yticks(range(0, 50))
plt.xlabel('Čas v minutách')
plt.ylabel('Týmy, které mají bingo')
plt.plot([x//limit if x is not None else None for x in bingos], 'go')

plt.show()
