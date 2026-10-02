from langchain_kavel import KavelImageGenerator


def test_schema():
    tool = KavelImageGenerator()
    assert tool.name == "kavel_image_generator"
    assert set(tool.args) == {"prompt", "aspect_ratio", "image_url"}
