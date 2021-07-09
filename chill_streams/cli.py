from .app import station_selection


def main():
    try:
        return station_selection()
    except KeyboardInterrupt:
        print("Keyboard interrupt. Quitting.")
        exit(0)


if __name__ == "__main__":
    exit(main())
