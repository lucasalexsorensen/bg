use std::fs;

use anyhow::Result;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RawCard {
    pub id: u32,
    pub collectible: u32,
    pub slug: String,
    #[serde(rename = "classId")]
    pub class_id: Option<u32>,
    #[serde(rename = "multiClassIds")]
    pub multi_class_ids: Vec<u32>,
    #[serde(rename = "minionTypeId")]
    pub minion_type_id: Option<u32>,
    #[serde(rename = "multiTypeIds")]
    pub multi_type_ids: Option<Vec<u32>>,
    #[serde(rename = "cardTypeId")]
    pub card_type_id: u32,
    #[serde(rename = "cardSetId")]
    pub card_set_id: u32,
    #[serde(rename = "rarityId")]
    pub rarity_id: Option<u32>,
    #[serde(rename = "artistName")]
    pub artist_name: Option<String>,
    pub health: Option<u32>,
    pub attack: Option<u32>,
    #[serde(rename = "manaCost")]
    pub mana_cost: u32,
    pub armor: Option<u32>,
    pub name: String,
    pub text: String,
    pub image: String,
    #[serde(rename = "imageGold")]
    pub image_gold: String,
    #[serde(rename = "flavorText")]
    pub flavor_text: String,
    #[serde(rename = "cropImage")]
    pub crop_image: String,
    #[serde(rename = "childIds")]
    pub child_ids: Option<Vec<u32>>,
    #[serde(rename = "keywordIds")]
    pub keyword_ids: Option<Vec<u32>>,
    #[serde(rename = "isZilliaxFunctionalModule")]
    pub is_zilliax_functional_module: bool,
    #[serde(rename = "isZilliaxCosmeticModule")]
    pub is_zilliax_cosmetic_module: bool,
    pub battlegrounds: BattlegroundsMetadata,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BattlegroundsMetadata {
    pub tier: Option<u32>,
    pub hero: bool,
    pub quest: bool,
    pub reward: bool,
    #[serde(rename = "duosOnly")]
    pub duos_only: bool,
    #[serde(rename = "solosOnly")]
    pub solos_only: bool,
    #[serde(rename = "companionId")]
    pub companion_id: Option<u32>,
    #[serde(rename = "upgradeId")]
    pub upgrade_id: Option<u32>,
    pub image: String,
    #[serde(rename = "imageGold")]
    pub image_gold: String,
}

pub struct RawCardDataset {
    pub heroes: Vec<RawCard>,
    pub minions: Vec<RawCard>,
    pub quests: Vec<RawCard>,
    pub quest_rewards: Vec<RawCard>,
    pub tavern_spells: Vec<RawCard>,
    pub anomalies: Vec<RawCard>,
    pub trinkets: Vec<RawCard>,
}

pub fn load_dataset() -> Result<RawCardDataset> {
    let json_content = fs::read_to_string("data/cards.json")?;
    let cards: Vec<RawCard> = serde_json::from_str(&json_content)?;

    let heroes = cards
        .iter()
        .filter(|card| card.card_type_id == 3)
        .cloned()
        .collect();
    let minions = cards
        .iter()
        .filter(|card| card.card_type_id == 4)
        .cloned()
        .collect();
    let quests = cards
        .iter()
        .filter(|card| card.card_type_id == 5)
        .cloned()
        .collect();
    let quest_rewards = cards
        .iter()
        .filter(|card| card.card_type_id == 40)
        .cloned()
        .collect();
    let tavern_spells = cards
        .iter()
        .filter(|card| card.card_type_id == 42)
        .cloned()
        .collect();
    let anomalies = cards
        .iter()
        .filter(|card| card.card_type_id == 43)
        .cloned()
        .collect();
    let trinkets = cards
        .iter()
        .filter(|card| card.card_type_id == 44)
        .cloned()
        .collect();

    Ok(RawCardDataset {
        heroes,
        minions,
        quests,
        quest_rewards,
        tavern_spells,
        anomalies,
        trinkets,
    })
}
