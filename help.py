def display(summary, *args):
    args = list(args)
    usage = ""
    example = ""
    details = ""
    delimiter = "="

    try:
        usage = args.pop(0)
        example = args.pop(0)
        details = args.pop(0)
    except IndexError:
        # End of arg list
        pass

    for x in range(1, len(summary)):
        delimiter = delimiter + "="

    print("")
    print(summary)
    print(delimiter)
    if usage:
        print("Usage: " + usage)
    if example:
        print("Example: " + example)
    if details:
        print("")
        print(details)
    print("")
