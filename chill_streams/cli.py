from .app import vlc_main


def main():
    try:
        return vlc_main()
    except KeyboardInterrupt:
        print("Keyboard interrupt. Quitting.")
        exit(0)


if __name__ == "__main__":
    exit(main())
