import requests
import pandas as pd

# todo
# Change the set name in CAPS here
# Set names: "DOA%201st", "DOA%20Alter", "FTC", "ALC"
SET_NAME = "FTC"


def retrieve_all_cards(api_url):
    all_cards = []
    page = 1
    has_more = True

    while has_more:
        response = requests.get(api_url, params={'page': page})
        if response.status_code == 200:
            data = response.json()
            card_data = data.get('data', [])
            all_cards.extend(card_data)

            # Check if there are more pages
            has_more = data.get('has_more', False)
            page += 1
        else:
            print("Failed to retrieve data from API.")
            return None

    return all_cards


def retrieve_sorted_data(cards):
    # Sort card data by collector number
    sorted_cards = sorted(cards, key=lambda x: x.get('result_editions')[0].get('collector_number'))

    # Lookup table for rarity
    rarity_lookup = {
        1: 'C',
        2: 'U',
        3: 'R',
        4: 'SR',
        5: 'UR',
        6: 'PR',
        7: 'CSR',
        8: 'CUR'
    }

    # Extract data for each card
    sorted_data = []
    for card in sorted_cards:
        rarity_code = card.get('result_editions')[0].get('rarity')
        rarity = rarity_lookup.get(rarity_code, 'Unknown')
        collector_number = card.get('result_editions')[0].get('collector_number')
        name = card.get('name')
        total_thema = card.get('result_editions')[0].get('thema_foil')
        grace = card.get('result_editions')[0].get('thema_grace_foil')
        valor = card.get('result_editions')[0].get('thema_valor_foil')
        charm = card.get('result_editions')[0].get('thema_charm_foil')
        mystique = card.get('result_editions')[0].get('thema_mystique_foil')
        ferocity = card.get('result_editions')[0].get('thema_ferocity_foil')
        sorted_data.append({'Collector Number': collector_number, 'Rarity': rarity, 'Name': name,
                            'Total thema': total_thema, 'Grace': grace, 'Valor': valor, 'Charm': charm,
                            'Mystique': mystique, 'Ferocity': ferocity})

    return sorted_data


def save_to_excel(sorted_data, output_file):
    df = pd.DataFrame(sorted_data)
    df.to_excel(output_file, index=False)


# Set the API URL with the prefix
api_url = f"https://api.gatcg.com/cards/search?prefix={SET_NAME}"
output_file = f"{SET_NAME}_sorted_cards.xlsx"

all_cards = retrieve_all_cards(api_url)
if all_cards:
    sorted_data = retrieve_sorted_data(all_cards)
    save_to_excel(sorted_data, output_file)
    print(f"Data saved to {output_file}")
