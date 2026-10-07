import pytest
from src.crawler import BECEMockCrawler
from src.download_pipeline import DownloadPipeline
from src.sitemap_harvester import SitemapHarvester


def test_crawler_allowed_domains():
    crawler = BECEMockCrawler()
    # Allowed domains
    assert crawler._is_allowed_domain("https://ghanaeducation.org/bece-mock") is True
    assert crawler._is_allowed_domain("https://passco.com.gh/math-past-questions") is True
    assert crawler._is_allowed_domain("https://ug.edu.gh/exams") is True
    assert crawler._is_allowed_domain("https://drive.google.com/file/d/123/view") is True

    # Blocked domains
    assert crawler._is_allowed_domain("https://random-commercial-site.com/stuff") is False
    assert crawler._is_allowed_domain("https://shopping.co.uk/promo") is False


def test_resolve_external_storage_url():
    # Google Drive view link -> direct uc download
    gdrive_view = "https://drive.google.com/file/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/view"
    resolved_gdrive = SitemapHarvester.resolve_external_storage_url(gdrive_view)
    assert "export=download" in resolved_gdrive
    assert "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms" in resolved_gdrive

    # Google Docs link -> export pdf
    gdoc_url = "https://docs.google.com/document/d/1xyz789_abc/edit"
    resolved_gdoc = SitemapHarvester.resolve_external_storage_url(gdoc_url)
    assert "format=pdf" in resolved_gdoc
    assert "1xyz789_abc" in resolved_gdoc


@pytest.mark.asyncio
async def test_download_pipeline_inflight_deduplication(tmp_path):
    pipeline = DownloadPipeline()
    url = "https://example.com/test_paper.pdf"

    # Simulate URL being currently downloaded (in flight)
    pipeline.in_flight_urls.add(url)
    result = await pipeline.download_file(url)
    assert result is None  # Must skip concurrently active URL
