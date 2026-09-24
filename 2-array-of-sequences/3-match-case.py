
"""Small demo: match/case with sequence patterns (Python >= 3.10)"""

def handle_command(message):
    match message:
        case ['BEEPER', frequency, times]:      # exact length 3, first item fixed
            print(f"beep {times} times at {frequency}Hz")
        case ['NECK', angle]:                   # exact length 2
            print(f"rotate neck to {angle} degrees")
        case ['LED', ident, intensity]:
            print(f"set LED {ident} brightness to {intensity}")
        case _:                                 # wildcard = default
            print(f"unknown command: {message}")


def show_if_western(record):
    match record:
        case [name, _, (lat, lon)] if lon <= 0:  # nested unpack + guard
            print(f"{name}: lat={lat}, lon={lon}")


def describe(record):
    match record:
        case [str(name), *_, (float(lat), float(lon))]:  # type check + *_ skips middle items
            print(f"{name} -> ({lat}, {lon})")
        case _:
            print("no match")


if __name__ == "__main__":
    print("-- handle_command --")
    handle_command(['BEEPER', 440, 3])
    handle_command(['NECK', 90])
    handle_command(['LED', 1, 80])
    handle_command(['UNKNOWN', 1])

    print("\n-- show_if_western --")
    show_if_western(('Mexico City', 'MX', (19.43, -99.13)))
    show_if_western(('Tokyo', 'JP', (35.68, 139.69)))

    print("\n-- describe --")
    describe(['Shanghai', 'CN', (31.1, 121.3)])
    describe([123, 'x'])