import requests
from bs4 import BeautifulSoup
from functools import lru_cache


@lru_cache
def fetch_top_players_page(page_number):
    # URL template for paginated results
    url = f"https://www.transfermarkt.com/marktwerte/wertvollstespieler/marktwertetop?page={page_number}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    # Fetch the page content
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(
            f"Failed to retrieve page {page_number}. HTTP Status code: {response.status_code}"
        )
        return [], None

    # Parse the page content
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all player rows in the table
    table_rows = soup.select(
        "table.items tbody tr"
    )  # This is an example, you may need to adjust the selector

    player_data = []

    # Extract player info from each row
    for row in table_rows:
        # If this row contains a player name (not an empty row)
        name_column = row.select_one("td.hauptlink a")

        if name_column:
            player_name = name_column.text.strip()  # Player name
            # The rank is determined by the first column
            rank_column = row.select_one("td:nth-of-type(1)")
            rank = (
                rank_column.text.strip() if rank_column else "Unknown"
            )

            # Ensure we don't add the empty duplicate row
            if player_name and rank != "":
                player_data.append(
                    {"rank": rank, "player_name": player_name}
                )

    return (
        player_data,
        page_number + 1,
    )
    # Return current page's data and next page number


# Function to fetch top 100 players by iterating through pages
def fetch_top_100_players(verbose=True):
    """
    verbose provides logging on screen on the individual steps
    """
    all_players = []
    page_number = 1

    while True:
        if verbose:
            print(f"Fetching page {page_number}...")
        player_data, next_page = fetch_top_players_page(page_number)

        if not player_data:
            break

        all_players.extend(player_data)

        if int(player_data[-1]["rank"]) >= 100:
            break

        page_number = next_page

    return all_players


if __name__ == "__main__":
    # Fetch top 100 players and print the result
    top_100_players = fetch_top_100_players()
    for player in top_100_players:
        print(
            f"Rank: {player['rank']}, Player: {player['player_name']}"
        )
