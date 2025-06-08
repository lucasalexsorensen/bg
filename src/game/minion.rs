use rand::{Rng, rng};

#[derive(Debug, Clone, Copy, Default)]
pub struct Minion {
    pub uuid: u32,
    pub id: u32,
    pub attack: i32,
    pub health: i32,
    pub taunt: bool,
    pub divine_shield: bool,
    pub has_attacked: bool,
}

impl Minion {
    pub fn from_id(id: u32) -> Self {
        let uuid = rng().random_range(0..=u32::MAX);
        match id {
            116734 => Self {
                uuid,
                id,
                attack: 3,
                health: 2,
                ..Default::default()
            },
            119994 => Self {
                uuid,
                id,
                attack: 1,
                health: 3,
                ..Default::default()
            },
            98582 => Self {
                uuid,
                id,
                attack: 2,
                health: 2,
                ..Default::default()
            },
            _ => panic!("Unknown minion id: {}", id),
        }
    }
}
