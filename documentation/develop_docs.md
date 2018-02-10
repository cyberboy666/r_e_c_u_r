# how to develop r_e_c_u_r

i have tried to write this application so it can easily be read and modified for different use cases. i recomend forking the repo to experiment with the codebase. open a pull request into origin <your_branch> if you want to contribe your changes back into the project.

this [diagram] might help understand the design : 

![diagram_pic][diagram_pic]

here are some examples of changes you might want to make:

## rearranging the _keypad_ controls

to simpify the key-mapping process, i have premapped the numpad keys to the _labels_ `a` to `s` like this:

![premapped_keys][premapped_keys]

(see [dotfiles] for description of this process)

for each _label_ the application will read the `[keypad_action_mapping.json]` file and map it to an `[action]`. currently the format also allows unique actions per _display_mode_ and per the `2ND FUNC` toggle :

```
...
	"x": {
		"BROWSER": ["trigger_this_action_in_display_mode"],
		"DEFAULT": ["trigger_this_action_in_any_other_mode_with_FN_off","trigger_this_action_in_any_other_mode_with_FN_on"],
	}
```

## adding a new screen resolution option to the _settings_ menu

## creating a new action

## adding a new `user input` device

## beyond

i hope the foundations iv provided encourage you to make larger changes for more ambitious features. if so you could try getting [in touch] first and maybe i could help align your approach with the rest of the project

[diagram]: https://docs.google.com/drawings/d/1ltWCv82rKVzOiFe6GaDDPlneG2oki0yRujArPU5V2ss/edit?usp=sharing
[diagram_pic]:
[premapped_keys]:
[dotfiles]: ../dotfiles
[keypad_action_mapping.json]: ../data_centre/json_objects/keypad_action_mapping.json
[action]: ../actions.py 
[in touch]: langolierz@gmail.com
