import pygame
import time
import sys
import copy


test_field = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
        ]


def main(field):
    FPS = 60
    chose_flag = False
    pygame.init()
    sc = pygame.display.set_mode((450, 550))
    clock = pygame.time.Clock()
    # ---

    while True:
        render_field(sc, False)
        render_sudoku(field, sc)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    a = int(event.pos[0] / 50)
                    b = int(event.pos[1] / 50)
                    pygame.draw.rect(sc, (0, 130, 255), (a*50, b*50, 50, 50), 3)
                    chose_flag = [a, b]
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                field = solution(field, sc, False)
        clock.tick(FPS)


def render_field(sc, flag):
    pygame.draw.rect(sc, (0, 0, 0), (0, 0, 450, 550))
    x = 0
    y = 0
    while x < 450:
        while y < 450:
            pygame.draw.rect(sc, (255, 0, 0), (x, y, 50, 50), 3)
            y += 50
        x += 50
        y = 0
    pygame.draw.line(sc, (135, 135, 20), (150, 0), (150, 450), 6)
    pygame.draw.line(sc, (135, 135, 20), (300, 0), (300, 450), 6)
    pygame.draw.line(sc, (135, 135, 20), (0, 150), (450, 150), 6)
    pygame.draw.line(sc, (135, 135, 20), (0, 300), (450, 300), 6)
    if flag:
        pygame.draw.rect(sc, (133, 133, 133), (flag[1]*50, flag[0]*50, 50, 50), 6)


def render_sudoku(field, sc):
    f1 = pygame.font.Font(None, 36)
    x = 20
    y = 15
    for el in field:
        for i in el:
            if i:
                text = f1.render(str(i), 1, (55, 231, 77))
                sc.blit(text, (x, y))
            x += 50
        y += 50
        x = 20
    ticks = pygame.time.get_ticks()
    seconds = int(ticks / 1000 % 60)
    minutes = int(ticks / 60000 % 24)
    out = '{minutes:02d}:{seconds:02d}'.format(minutes=minutes, seconds=seconds)
    f1 = pygame.font.Font(None, 36)
    text = f1.render(out, 1, (125, 93, 244))
    sc.blit(text, (200, 500))
    pygame.display.update()


def solution(field, sc, flag):
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    render_field(sc, flag)
    render_sudoku(field, sc)
    time.sleep(0.2)
    if victory_check(field):
        return field
    empty_variant = [0 for i in range(1, len(field)+1)]
    for m in range(len(field)):
        for n in range(len(field[0])):
            variant = [i for i in range(1, len(field)+1)]
            if field[m][n] == 0:
                variant = row_variant(field[m], variant)
                variant = column_variant(field, n, variant)
                coub_n, coub_m = get_coub_coordinate(m, n)
                variant = cube_variant(field, coub_n, coub_m, variant)
                for el in variant:
                    if el != 0:
                        result = copy.deepcopy(field)
                        result[m][n] = el
                        flag = (m, n)
                        variant[el - 1] = 0
                        answer = solution(result, sc, flag)
                        if answer:
                            return answer
                if variant == empty_variant:
                    return False


def get_coub_coordinate(m, n):
    result = []
    first = [0, 1, 2]
    second = [3, 4, 5]
    third = [6, 7, 8]
    if m in first:
        result.append(first)
    elif m in second:
        result.append(second)
    elif m in third:
        result.append(third)
    if n in first:
        result.append(first)
    elif n in second:
        result.append(second)
    elif n in third:
        result.append(third)
    return result


def show_field(field):
    for i in field:
        print('')
        for j in i:
            print(j, end=' ')


def victory_check(field):
    victory = True
    for i in field:
        for j in i:
            if j == 0:
                victory = False
    if victory:
        return True
    return False


def row_variant(row, variant):
    for i in row:
        if i in variant and i != 0:
            variant[i-1] = 0
    return variant


def column_variant(field, n, variant):
    for j in range(len(field[n])):
        if field[j][n] in variant and field[j][n] != 0:
            variant[field[j][n] - 1] = 0
    return variant


def cube_variant(field, coub_n, coub_m, variant):
    for i in coub_n:
        for j in coub_m:
            if field[i][j] in variant and field[i][j] != 0:
                variant[field[i][j] - 1] = 0
    return variant


if __name__ == '__main__':
    main(test_field)
