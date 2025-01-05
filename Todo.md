# Rules
1. An alias must always be more specific than a general.
2. An alias should contain it's alternate spellings and language: this is because we want fast easy access to a default for reverting to default.
3. The Regex for an alternate spelling may and often will catch the primary spelling used in the translations (for default). For this reason, you should *always* check against translations, then aliases, then alternate spellings. Otherwise you may end up in such a situations that the wrong localisation is used and the "ignore default localisation" option is ignored...
4. Only capture for ignored spaces if you can be absolutely sure that no conflict between tags shall arise (See superpower vs super power for examples on how capturing this greedily can cause issues and change a tag's meaning if incorrectly detected as an alternate spelling with a regex.)
5. Alternate spellings will point to their alias before pointing to a default location. Always. This is to account for errors where an alternate spelling can skip a true alias. (EG: "Japanese Mafia" -> (skips) Yakuza -> Gangs).

# Changes to Make
(Yakuza, Mafia) -> Gang [As True Alias]
(Real Robot) -> Cyborg [??]
(Urban/Contemporary Fantasy) -> Fantasy [As True Alias]
(Dark Slapstick Crude Gag Comedy) -> Comedy [As True Alias]
(Succubus Incubus) -> Demons [As True Alias]

Add all alternate spellings for disability tag. Mark Blind, Paralysed, Deaf, and Amputee as true alias

# To Do
1. Split aliases into true alias and alternate spelling.
2. All sports tags should be listed under "Sports" tag.
3. Alternate spellings should be { spelling: alias || default }
4. Convert from storing explicit values to storing Regexs... (For alt spellings.)
5. Aliases should be a map of alias -> override. Where if override flag is set, alias will always be used instead of default regardless of if "use default" is checked.

# Questions
1. How do we handle conflicts in synonyms?? EG: Superpower and Super Power


test string vs regex comparison