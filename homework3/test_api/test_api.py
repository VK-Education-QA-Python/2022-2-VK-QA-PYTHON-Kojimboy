import pytest

from base import ApiBase


class TestApiLogin(ApiBase):
    @pytest.fixture(scope='class', autouse=True)
    def setup(self, api_client):
        api_client.post_login()

    def test_api_login(self, api_client):
        assert api_client.session.get('https://target-sandbox.my.com/profile/contacts').url == \
               'https://target-sandbox.my.com/profile/contacts'


@pytest.mark.API
class TestCampaignApi(ApiBase):
    def test_campaign_creation_deletion(self, campaign):
        assert self.check_active_top_campaign_id(campaign.id) is True


@pytest.mark.API
class TestSegmentApi(ApiBase):
    # параметры передаются в segment и в source
    @pytest.mark.parametrize("object_type, url", [("remarketing_player", None), ])
    def test_segment_creation_deletion(self, segment):
        assert self.check_top_segment_id(segment.id) is True

    @pytest.mark.parametrize("object_type, url", [("remarketing_vk_group", "https://vk.com/vkedu"), ])
    def test_vk_ok_source_segment_creation_deletion(self, segment, source):
        assert self.check_source(source.vk_id) is True
        assert self.check_top_segment_id(segment.id) is True
