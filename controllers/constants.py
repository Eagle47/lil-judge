ROLES = {
    'user': 1 << 0,
    'judge': 1 << 1,
    'master': 1 << 2
}

ROLES_INVERTED = dict(
    map(
        lambda t: (t[1], t[0]),
        ROLES.items()
    )
)
