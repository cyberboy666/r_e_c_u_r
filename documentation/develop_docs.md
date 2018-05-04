# how to develop r_e_c_u_r

i have tried to write this application so it can easily be read and modified for different use cases. i recommend forking the repo to experiment with the codebase. open a pull request into origin <your_branch> if you want to contribute your changes back into the project.

this [diagram] might help understand the design : 

![design_overview][design_overview]

here are some examples of changes you might want to make:

## rearranging the _keypad_ controls

to simplify the key-mapping process, i have pre-mapped the numpad keys to the _labels_ `a` to `s` like this:

![premapped_keys][premapped_keys]

(see [dotfiles] for description of this process)

for each _label_ the application will read the [keypad_action_mapping.json] file and map it to an [action]. the format also allows unique actions per _control_mode_ and per the `FUNCTION` toggle :

```
...
"x": {
	"NAV_BROWSER": ["trigger_this_action_in_browser_mode"],
	"DEFAULT": ["trigger_this_action_in_any_other_mode_with_FN_off","trigger_this_action_in_any_other_mode_with_FN_on"],
}
```
## creating a new action

## beyond

i hope the foundations iv provided encourage you to make larger changes for more ambitious features. if so you could try getting in touch (langolierz@gmail.com) first and maybe i could help align your approach with the rest of the project

[diagram]: https://docs.google.com/drawings/d/1ltWCv82rKVzOiFe6GaDDPlneG2oki0yRujArPU5V2ss/edit?usp=sharing
[design_overview]: design_overview.jpg
[premapped_keys]: vectorfront_blank_keys.png
[dotfiles]: ../dotfiles
[keypad_action_mapping.json]: ../data_centre/json_objects/keypad_action_mapping.json
[action]: ../actions.py 

