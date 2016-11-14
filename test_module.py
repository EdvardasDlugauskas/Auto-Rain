import icon_get


def test_image_search():
    T = icon_get.get_image
    assert T("minecraft")
    assert T("Dota 2")
