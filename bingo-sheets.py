import random
from typing import Tuple
from pathlib import Path

import drawsvg as d

PAPER_W = 210
PAPER_H = 297
SHEET_W = 88
SHEET_H = 132
NUMBER_FONT_FAMILY = "Arial Rounded MT Bold"


def get_numbers(low_high: Tuple[int, int]) -> list[int]:
    low, high = low_high
    return random.sample([i for i in range(low, high + 1)], 25)


def make_paper() -> d.Drawing:
    paper = d.Drawing(
        width=PAPER_W,
        height=PAPER_H,
        origin="center",
    )

    paper.set_pixel_scale(4)

    paper.append(
        d.Rectangle(
            x=-(PAPER_W / 2),
            y=-(PAPER_H / 2),
            width=PAPER_W,
            height=PAPER_H,
            fill="#ffffff",
        )
    )

    return paper


def make_bingo_sheet(low_high: Tuple[int, int] = None) -> d.Group:
    sheet = d.Group()
    xy = [(sx, sy) for sx in range(4, 69, 16) for sy in range(48, 113, 16)]
    numbers = get_numbers(low_high) if low_high else []

    outer_border = d.Rectangle(
        x=0,
        y=0,
        width=SHEET_W,
        height=SHEET_H,
        fill="#eeeeee",
    )
    sheet.append(outer_border)

    title = d.Text(
        text="Bingo!",
        font_size=24,
        center=True,
        x=SHEET_W / 2,
        y=xy[0][1] / 2 + 6,
        font_family=NUMBER_FONT_FAMILY,
        fill="#000000",
    )
    sheet.append(title)

    for i, (x, y) in enumerate(xy):
        space = d.Rectangle(
            x=x,
            y=y,
            width=16,
            height=16,
            stroke_width=1,
            stroke="black",
            fill="white",
        )
        sheet.append(space)
        if numbers:
            number = d.Text(
                text=f"{numbers[i]}",
                font_size=10,
                x=x + 8,
                y=y + 12,
                center=True,
                font_family=NUMBER_FONT_FAMILY,
                fill="#555555",
            )
            sheet.append(number)
            label = d.Text(
                text=f"For the numbers {low_high[0]} to {low_high[1]}.",
                font_size=4,
                x=xy[0][0],
                y=xy[0][1] - 4,
                font_family=NUMBER_FONT_FAMILY,
                word_spacing=8,
                letter_spacing=10,
                fill="#aaaaaa",
            )
            sheet.append(label)

    return sheet


def put_sheets_on_paper(low_high: Tuple[int, int] = None) -> d.Drawing:
    paper = make_paper()

    sheet_1 = make_bingo_sheet(low_high)
    sheet_2 = make_bingo_sheet(low_high)
    sheet_3 = make_bingo_sheet(low_high)
    sheet_4 = make_bingo_sheet(low_high)

    paper.append(d.Use(sheet_1, -(PAPER_W / 2 + SHEET_W), -(PAPER_H / 2 + SHEET_H)))
    paper.append(d.Use(sheet_2, -(PAPER_W / 2), -(PAPER_H / 2 + SHEET_H)))
    paper.append(d.Use(sheet_3, -(PAPER_W / 2 + SHEET_W), -(PAPER_H / 2)))
    paper.append(d.Use(sheet_4, -(PAPER_W / 2), -(PAPER_H / 2)))

    # Cut marks.
    vertical_cut_mark = d.Group()
    vertical_cut_mark.append(d.Line(0, 0, 0, 2, stroke="#000000", stroke_width=0.25))

    vertical_cut_mark_positions = [
        (-(PAPER_W / 2 + SHEET_W) + 1, -(PAPER_H / 2 + SHEET_H) - 1),  # top left
        (-(PAPER_W / 2), -(PAPER_H / 2 + SHEET_H) - 1),  # top middle
        (-(PAPER_W / 2) + SHEET_W - 1, -(PAPER_H / 2 + SHEET_H) - 1),  # top right
        (-(PAPER_W / 2 + SHEET_W) + 1, -(PAPER_H / 2) + SHEET_H - 1),  # bottom left
        (-(PAPER_W / 2), -(PAPER_H / 2) + SHEET_H - 1),  # bottom middle
        (-(PAPER_W / 2) + SHEET_W - 1, -(PAPER_H / 2) + SHEET_H - 1),  # bottom right
    ]

    for x, y in vertical_cut_mark_positions:
        paper.append(d.Use(vertical_cut_mark, x, y))

    horizontal_cut_mark = d.Group()
    horizontal_cut_mark.append(d.Line(0, 0, 2, 0, stroke="#000000", stroke_width=0.25))

    horizontal_cut_mark_positions = [
        (-(PAPER_W / 2 + SHEET_W) - 1, -(PAPER_H / 2 + SHEET_H) + 1),  # top left
        (-(PAPER_W / 2) + SHEET_W - 1, -(PAPER_H / 2 + SHEET_H) + 1),  # top right
        (-(PAPER_W / 2 + SHEET_W) - 1, -(PAPER_H / 2)),  # middle left
        (-(PAPER_W / 2) + SHEET_W - 1, -(PAPER_H / 2)),  # middle right
        (-(PAPER_W / 2 + SHEET_W) - 1, -(PAPER_H / 2) + SHEET_H - 1),  # bottom left
        (-(PAPER_W / 2) + SHEET_W - 1, -(PAPER_H / 2) + SHEET_H - 1),  # bottom right
    ]

    for x, y in horizontal_cut_mark_positions:
        paper.append(d.Use(horizontal_cut_mark, x, y))

    return paper


def make_paper_list(
    count: int = 1, low_high: Tuple[int, int] = None
) -> list[d.Drawing]:
    return [put_sheets_on_paper(low_high) for i in range(count)]


def make_filename(sheet_number: int = None, low_high: Tuple[int, int] = None) -> str:
    if low_high:
        low, high = low_high
        return f"{sheet_number:02}_bingo_sheets_A4_{low}_{high}.svg"
    else:
        return "bingo_sheets_A4_blank.svg"


def make_subdirectory_name(low_high: Tuple[int, int] = None) -> str:
    if low_high:
        low, high = low_high
        return f"bingo_sheets_A4_{low}_{high}_svg"
    else:
        return "bingo_sheets_A4_blank_svg"


def output_papers(count: int = 1, low_high: Tuple[int, int] = None):
    script_dir = Path(__file__).parent
    subdir_name = make_subdirectory_name(low_high)
    subdir_path = script_dir / subdir_name
    subdir_path.mkdir(parents=True, exist_ok=True)

    for f in range(1, count + 1):
        file_name = make_filename(f, low_high)
        file_path = subdir_path / file_name
        bingo_sheet = put_sheets_on_paper(low_high)
        bingo_sheet.save_svg(file_path)


if __name__ == "__main__":
    output_papers()

    # for n in [25, 28, 32, 36, 40, 42, 45, 48, 50]:
    #     output_papers(count=25, low_high=(1, n))
