# bg

Hearthstone battlegrounds simulator project


## Architecture
* Minions
  * Keep track of the minions on the board.

* Board
  * Keeps track of the player's minions and enemy minions.
  * Also tracks board metadata (like blood gems stats and beetle sizes).

* Events
  * Events are triggered by things like
  * Here are all the current events (and an example minion which reacts to the given event):
    * `CombatStarted` (e.g. Hawkstriker Herald)
    * `MinionSummoned` (e.g. Deflect-o-Bot)
    * `MinionDied` (e.g. Hungry Snapjaw)
    * `MinionBuffed` (e.g. Whelp Smuggler)
    * `PreAttack` (e.g. Dozy Whelp)
    * `PostAttack` (e.g. Cave Hydra, i.e. cleave)
    * `DeathrattleTriggered` (e.g. Manasaber, Unholy Sanctum)
    * `BattlecryTriggered` (e.g. Blazing Skyfin)
    * `SpaceAvailable` (e.g. Sharptooth Snapper)
    * `DivineShieldLost` (e.g. Grease Bot)

* Effects
  * Effects are invoked as consequence of events, and effects can even trigger new consequent events.
  * Effects can (and typically do) modify the Board
  * Examples:
    * `BuffMinion`
    * `SummonBeetle`
    * The list goes on...
