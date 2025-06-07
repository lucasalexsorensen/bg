pub mod cards;

use anyhow::Result;
use cards::raw::load_dataset;
use std::fs;

fn main() -> Result<()> {
    let dataset = load_dataset()?;

    // print the name of all tavern spells
    for card in dataset.tavern_spells {
        println!("{}", card.name);
    }

    Ok(())
}
