import pytest
from sdks.generator.sdk_generator import sdk_generator, MultiLanguageSDKGenerator

def test_developer_sdk_generator_all_languages():
    for lang in ["python", "typescript", "swift", "kotlin", "rust"]:
        sdk_res = sdk_generator.generate_sdk_source(lang)

        assert sdk_res["target_language"] == lang
        assert sdk_res["sdk_version"] == "V11.0"
        assert len(sdk_res["source_code"]) > 20
        assert sdk_res["zero_dependencies"] is True

def test_developer_sdk_generator_invalid_language():
    with pytest.raises(ValueError) as exc:
        sdk_generator.generate_sdk_source("golang")
    assert "UNSUPPORTED_SDK_LANGUAGE" in str(exc.value)
