def generate_mappings_doc(title, mappings, column_one_header="Note/CC"):
    # print(mappings)
    output = ""
    output += "# %s\n" % title
    output += "\n| %s | Mode | Action (default) | Action (with FN) | \n" % column_one_header
    output += ("| --- " * 4) + " |\n"
    for message, maps in sorted(mappings.items()):
        # output += "| %s | " % message
        for mode, actions in sorted(maps.items()):
            output += "| "
            output += "%s\t| " % message
            output += "%s\t| " % mode
            output += "%s | " % actions[0]
            if len(actions) > 1:
                output += "%s | " % actions[1]
            output += "|\n"

    output += "\n----\n"

    print(output)
