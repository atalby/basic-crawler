from crawler.utils import should_skip_url

def test_should_skip_url():
    assert should_skip_url("https://example.com/image.png")
    assert should_skip_url("https://example.com/video.mp4")
    assert not should_skip_url("https://example.com/page")
    assert not should_skip_url("https://example.com/index.html")

