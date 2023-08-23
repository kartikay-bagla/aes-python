import json
from bs4 import BeautifulSoup, Tag


def generate_mapping(soup: BeautifulSoup) -> dict[int, int]:
    """Given a soup with table tag, return the mapping."""
    all_rows = soup.find_all("tr")

    top_row: list[Tag] = [i.text.strip() for i in all_rows[0].find_all("th")]
    first_col: list[Tag] = [
        i.find("th").text.strip() for i in all_rows if i.find("th") is not None
    ]

    output_dict = {}
    for col_selector in range(1, len(top_row)):
        least_significant_nibble = top_row[col_selector][1]
        for row_selector in range(1, len(first_col)):
            most_significant_nibble = first_col[row_selector][0]
            nibble = int(f"{most_significant_nibble}{least_significant_nibble}", 16)
            mapped_to = (
                all_rows[row_selector].find_all("td")[col_selector - 1].text.strip()
            )  # because row is like th, td, td, ...
            output_dict[nibble] = int(mapped_to, 16)
    return output_dict


with open("generate_s_box/s_box_table.html") as f:
    soup = BeautifulSoup(f, "html.parser")

output_dict = generate_mapping(soup)

with open("generate_s_box/inverse_s_box_table.html") as f:
    inv_soup = BeautifulSoup(f, "html.parser")

inv_output_dict = generate_mapping(inv_soup)

with open("output.py", "w") as f:
    f.writelines([
        "S_BOX_MAPPING = {\n",
        *[f"    {k}: {v},\n" for k, v in output_dict.items()],
        "}\n",
        "\n",
        "INV_S_BOX_MAPPING = {\n",
        *[f"    {k}: {v},\n" for k, v in inv_output_dict.items()],
        "}\n",
    ])
