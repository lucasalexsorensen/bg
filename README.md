# bg

Hearthstone battlegrounds simulator project

## Tasks
- [ ] Build a very primitive simulator (maybe vibe code a lot of it)
- [ ] Build a tool to record data from my own games
- [ ] Collect a dataset of matchups and their outcomes
- [ ] Build a validation tool using this dataset
- [ ] Iterate on the simulator until it's pretty good


## Architecture
* Minion
  * Tracks the minion's stats and effects
  * Each minion is assigned a unique ID upon creation

* Board
  * Tracks two sets of minions (one for each player)
  * Also tracks board metadata (like blood gems stats and beetle sizes)

* Events
  * Events are triggered throughout the combat
  * Events can be listened to by either the board (via trinkets, hero powers, etc.) or by minions
  * Here are all the current events:
    * `CombatStarted` (e.g. Hawkstriker Herald)
    * `MinionSummoned` (e.g. Deflect-o-Bot)
    * `MinionDied` (e.g. Hungry Snapjaw)
    * `MinionBuffed` (e.g. Whelp Smuggler)
    * `PreAttack` (e.g. Dozy Whelp)
    * `PostAttack` (e.g. Cave Hydra and other cleave minions)
    * `DeathrattleTriggered` (e.g. Unholy Sanctum)
    * `BattlecryTriggered` (e.g. Blazing Skyfin)
    * `SpaceAvailable` (e.g. Sharptooth Snapper)
    * `DivineShieldLost` (e.g. Grease Bot)

* Effects
  * Effects are invoked as consequence of events
  * Effects can even trigger new consequent events
  * Effects can (and typically do) modify the board
  * Examples: deathrattle effects, battlecry effects, etc.
