import MMO

if __name__ == "__main__":
    game = MMO.App()
    game.user_data = MMO.ConnectClientDTO(
        version=MMO.CORE.version,
        name="test_client",
        password="123"
    )
    game.run()
