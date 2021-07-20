from .app import vlc_main
from .station_list import station_list_main


def main():
    try:
        return vlc_main()
    except KeyboardInterrupt:
        print("Keyboard interrupt. Quitting.")
        exit(0)


def sl_main():
    try:
        return station_list_main()
    except KeyboardInterrupt:
        exit(0)


if __name__ == "__main__":
    exit(main())
