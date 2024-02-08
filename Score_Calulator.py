import pandas as pd

def calculate_score(deck):
    """Calculates the score for a given deck, considering individual card points and combo bonuses."""
    score = {cat: 0 for cat in categories}
    for card_id in deck:
        for cat, value in card_scores[card_id].items():
            score[cat] += value
    for combo_id in deck:
        if set(combo_card_ids[combo_id]).issubset(deck):
            for cat, bonus in combo_bonuses[combo_id].items():
                score[cat] += bonus
    return score

def find_best_deck(remaining_cards, used_cards, deck, current_score, best_score, best_deck):
    """Recursively finds the best deck within the card limit, emphasizing the chosen category and fitting as many combos as possible."""
    if len(deck) == 50:
        new_score = calculate_score(deck)
        if new_score[chosen_category] > best_score[chosen_category]:
            best_score = new_score
            best_deck = deck.copy()
        return
    for i, card_id in enumerate(remaining_cards):
        if card_id not in used_cards:
            used_cards.append(card_id)
            deck.append(card_id)
            find_best_deck(remaining_cards[:i] + remaining_cards[i + 1:], used_cards.copy(), deck.copy(), current_score.copy(), best_score.copy(), best_deck.copy())
            used_cards.pop()
            deck.pop()

def clean_card_names(card_name):
    """Removes commas and extra spaces from the card name, preserving case."""
    return card_name.strip().replace(",", "")

def merge_card_lists(card_list1_path, card_list2_path, combo_sheet_path):
    """Merges card lists, handling duplicate and combo-related issues."""

    # Read Excel sheets
    card_list1_df = pd.read_excel(card_list1_path)
    card_list2_df = pd.read_excel(card_list2_path)
    combo_df = pd.read_excel(combo_sheet_path)

    # Create a common dictionary to store card information
    card_info = {}
    for index, row in pd.concat([card_list1_df, card_list2_df]).iterrows():
        card_name = clean_card_names(row["Card Name"])
        card_info[card_name] = {"card_id": row["Card ID"], "scores": row[3:].to_dict(), "category": row["Category"]}

    # Process comma-separated card names in combos
    combo_card_lists = []
    for _, row in combo_df.iterrows():
        combo_cards = [clean_card_names(card) for card in row["Cards"].split(";")]
        combo_card_lists.append(combo_cards)

    # Calculate combo bonuses for each card
    for combo_cards in combo_card_lists:
        for card_name in combo_cards:
            if card_name not in card_info:
                raise ValueError(f"Card '{card_name}' in a combo but not in card lists.")
            for category, bonus in combo_df[category].to_list()[combo_cards.index(card_name)].items():
                card_info[card_name]["scores"][category] += bonus

    # Create the merged DataFrame
    merged_df = pd.DataFrame.from_dict(card_info, orient="index", columns=["Card ID", "Category"] + list(categories))

    # Save the merged DataFrame to a new Excel file
    merged_df.to_excel("merged_card_list.xlsx", index=True)

if __name__ == "__main__":
    # Define sheets and categories
    card_sheet1 = "DOA%20Alter_sorted_cards.xlsx"
    card_sheet2 = "FTC_sorted_cards.xlsx"
    combo_sheet = "Set_Bonuses.xlsx"

    # Choose category for best deck calculation
    chosen_category = "Category1"  # Change this to your desired category

    # Read card data for both sheets
    card_data1 = pd.concat([card_sheet1, card_sheet2])
