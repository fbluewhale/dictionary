from cli import actions_cli, create_dictionary_cli


def main():
    dictionary = create_dictionary_cli()
    if dictionary is None:
        return
    actions_cli(dictionary)


if __name__ == "__main__":
    main()
