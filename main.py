project = input(
    """
    What would you like to run?
    1 - Ball Simulation
    2 - Dangled Rope Simulation
    3 - Rope Bridge Simulation
    4 - Save loader
    5 - Save Editor

    """
    )

match project:
    case "1":
        import balls
    case "2":
        import rope_dangled
    case "3":
        import rope
    case "4":
        import loader
    case "5":
        import editor