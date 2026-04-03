# from libs import Attributer, ProgressBar, Player, PlayerLoadDTO
from libs.graphics.polygons import Recalc
from libs.math import Vector2, Size2

if __name__ == "__main__":
    print(....__class__())
    # attr = Attributer()
    # print(attr)
    # print(dict(attr))

    # attr2 = Attributer()
    # attr2.load_from_str('<Attributer_{"basic":[1,0,0,0,0,0,0,0],"elevated":[2,0,0,0,0,0,0,0],"artefacts":[0,0,0,0,0,0,0,0],"effects":[0,0,0,0,0,0,0,0],"ratio":[3,0,0,0,0,0,0,0]}>')
    # attr2.update()
    # print(attr2)
    # print(attr2.constitution)
    # bar = ProgressBar()
    # print(bar)

    # player = Player()
    # player.name = "1234"
    # player.race = "test"
    # print(player, player.race)
    # player2 = Player.__copy__(player)
    # print(player2, player2.race)
    # player3 = Player.load_from_config(PlayerLoadDTO(
    #     race="human",
    #     attributes={
    #       "basic": [10, 10, 10, 10, 10, 10, 10, 10],
    #       "ratio": [1, 1, 1, 1, 1, 1, 1, 1]
    #     },
    #     to_first_lvlup=100,
    #     raising_xp=1.05,
    #     xp_boost=1.0
    # ))
    # print(player3, player3.race)

    # recalc = Recalc(Vector2(2, 3), Vector2(4, 5))
    #
    # print(recalc)
    #
    # recalc2 = Recalc.load_from_str("<Recalc:<Vector2:2,3>/<Vector2:4,5>>")
    # print(recalc2.value(Size2(1, 1)))

    def f(m):
        m2 = [0] * 8
        if type(m[0]) == float:
            m2[0] = m[0]
        else:
            m2[2] = m[0]
        if type(m[1]) == float:
            m2[1] = m[1]
        else:
            m2[3] = m[1]
        if type(m[2]) == float:
            m2[4] = m[2]
        else:
            m2[6] = m[2]
        if type(m[3]) == float:
            m2[5] = m[3]
        else:
            m2[7] = m[3]
        return '["<Recalc:<Vector2:{},{}>/<Vector2:{},{}>>", "<Recalc:<Vector2:{},{}>/<Vector2:{},{}>>"]'.format(
            *m2
        )

    # print(
    #     '["<Recalc:<Vector2:{},{}>/<Vector2:{},{}>>", "<Recalc:<Vector2:{},{}>/<Vector2:{},{}>>"]'.format(
    #         *f([200, 330, 400, 75])
    #     )
    # )
    print(f([200, 330, 400, 75]))