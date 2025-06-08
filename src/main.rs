pub mod cards;
pub mod game;

use anyhow::Result;
use cards::raw::load_dataset;

fn main() -> Result<()> {
    let dataset = load_dataset()?;

    for card in dataset.tavern_spells {
        println!("{}", card.name);
    }

    Ok(())
}
