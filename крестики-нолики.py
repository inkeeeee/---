field = [['@', 1, 2, 3], [1, '-', '-', '-'], [2, '-', '-', '-'], [3, '-', '-', '-']]


def check_win(field):
    for i in range(1, 4):
        if field[i][1] == field[i][2] == field[i][3] and field[i][1] != '-':  # проверка побед по горизонтали
            return True

        if field[1][i] == field[2][i] == field[3][i] and field[1][i] != '-':  # проверка побед по вертикали
            return True

    if field[1][3] == field[2][2] == field[3][1] and field[2][2] != '-':  # проверка побед по диагонали
        return True

    elif field[3][1] == field[2][2] == field[1][3] and field[2][2] != '-':
        return True

    return False


print(
    'Это игра "крестики-нолики". Для того, чтобы походить в определённую ячейку, введите через пробел сначала номер её строки, а затем номер столбца. Например:\n4 3\nСначала ходят крестики.Приятной игры!!!')
player = 'X'  # переменная, содержащая информацию о том, кто делает ход
for el in field:  # выводим поле на экран
    print(*el)
flag = False
counter_steps = 0  # счётчик ходов
while True:
    print('-------------')
    print(player, 'сделайте ход')
    while True:
        try:  # проверяем корректность данных
            row, column = map(int, input().split())
            if row in [1, 2, 3] and column in [1, 2, 3]:  # проверяем корректность данных
                if field[row][column] == '-':  # проверяем, свободна ли эта ячейка
                    field[row][column] = player
                    counter_steps += 1
                    for el in field:  # выводим поле на экран
                        print(*el)
                    if check_win(field):
                        print(player, 'победили!!!')
                        flag = True
                        break
                    else:
                        if counter_steps == 9:
                            print('ничья!!!')
                            flag = True
                        if player == 'X':
                            player = '0'
                        else:
                            player = 'X'

                        break
                else:
                    print('Эта ячейка занята, давайте ещё раз')
            else:
                print('Вы ввели что-то не то, давайте ещё раз')

        except:
            print('Вы ввели что-то не то, давайте ещё раз')
    if flag:
        exit(0)
