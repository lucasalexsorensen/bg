use anyhow::Result;
use rand::{Rng, rng, seq::IteratorRandom};

use crate::game::minion::Minion;

/// The result of a board evaluation.
/// Positive => player deals damage to opponent
/// Negative => opponent deals damage to player
/// Zero => tie
pub type CombatResult = isize;

pub fn simulate_combat(player: Vec<Minion>, opponent: Vec<Minion>) -> Result<CombatResult> {
    let mut board = Board::from_minions(player, opponent);
    board.evaluate()
}

#[derive(Clone, Copy)]
enum Player {
    Me,
    Opponent,
}

impl std::ops::Not for Player {
    type Output = Player;

    fn not(self) -> Self::Output {
        match self {
            Player::Me => Player::Opponent,
            Player::Opponent => Player::Me,
        }
    }
}

pub struct Board {
    pub player: Vec<Minion>,
    pub opponent: Vec<Minion>,
    last_turn: Option<Player>,
}

impl Board {
    pub fn from_minions(player: Vec<Minion>, opponent: Vec<Minion>) -> Self {
        Self {
            player,
            opponent,
            last_turn: None,
        }
    }

    /// Evaluate the board and return the combat result.
    ///
    /// The evaluation works by looping until the board is in a terminal state
    /// Terminal meaning: one of the players has run out of viable minions
    /// The loop proceeds by:
    /// 1. Determining whose turn it is to attack
    /// 2. Determining which minion should perform the attack
    /// 3. Determining which minion should be the target
    /// 4. Performing the attack
    /// 5. Processing the result of the attack
    pub fn evaluate(&mut self) -> Result<CombatResult> {
        loop {
            // 1. Determine whose turn it is to attack
            let turn = self.determine_turn();

            let (own_minions, enemy_minions) = match turn {
                Player::Me => (&mut self.player, &mut self.opponent),
                Player::Opponent => (&mut self.opponent, &mut self.player),
            };

            // 2. Determine which minion should perform the attack
            let attacker = Self::determine_attacker(own_minions);
            if attacker.is_none() {
                break;
            }
            let (attacker_idx, _) = attacker.unwrap();
            let attacker = &mut own_minions[attacker_idx];

            // 3. Determine which minion should be the target
            let target = Self::determine_target(enemy_minions);
            if target.is_none() {
                break;
            }
            let (target_idx, _) = target.unwrap();
            let target = &mut enemy_minions[target_idx];

            // TODO: 4. Perform the attack
            attacker.health -= target.attack;
            target.health -= attacker.attack;
            attacker.has_attacked = true;
            target.has_attacked = true;

            if attacker.health <= 0 {
                own_minions.remove(attacker_idx);
            }
            if target.health <= 0 {
                enemy_minions.remove(target_idx);
            }
        }

        Ok(0)
    }

    fn determine_turn(&self) -> Player {
        match self.last_turn {
            Some(p) => !p,
            None => {
                let player_count = self.player.len();
                let opponent_count = self.opponent.len();

                if player_count > opponent_count {
                    Player::Me
                } else if player_count < opponent_count {
                    Player::Opponent
                } else {
                    let mut thread_rng = rng();
                    if thread_rng.random_bool(0.5) {
                        Player::Me
                    } else {
                        Player::Opponent
                    }
                }
            }
        }
    }

    fn determine_attacker(minions: &[Minion]) -> Option<(usize, &Minion)> {
        minions
            .iter()
            .enumerate()
            .find(|(_, minion)| !minion.has_attacked)
    }

    fn determine_target(minions: &[Minion]) -> Option<(usize, &Minion)> {
        if minions.is_empty() {
            return None;
        }

        let mut rng = rng();
        let taunt_minion = minions
            .iter()
            .enumerate()
            .filter(|(_, minion)| minion.taunt)
            .choose(&mut rng);

        if let Some(taunt_minion) = taunt_minion {
            Some(taunt_minion)
        } else {
            Some(minions.iter().enumerate().choose(&mut rng).unwrap())
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_next_minion_to_attack() {
        let my_minions = vec![Minion::from_id(116734)];
        let enemy_minions = vec![Minion::from_id(119994), Minion::from_id(98582)];

        let result = simulate_combat(my_minions, enemy_minions).unwrap();
        assert_eq!(result, 0);
    }
}
