import scrapy

class RigzoneSpider(scrapy.Spider):
    name = 'rigzone_spider'
    allowed_domains = ['www.rigzone.com']
    start_urls = [
        # 'https://www.rigzone.com/news/jadestone_doubles_stake_in_western_australia_oil_fields-15-feb-2024-175754-article/',
        # 'https://www.rigzone.com/news/latam_explorer_discovers_chile_gas_field-05-feb-2020-160990-article/',
        # 'https://www.rigzone.com/news/aramco_starts_gas_production_in_south_ghawar-20-nov-2023-174761-article/',
        # 'https://www.rigzone.com/news/oil_gas/a/147755/startup_of_malikai_oil_field_to_boost_malaysias_kimanis_exports/',
        # 'https://www.rigzone.com/news/oil_gas/a/132000/ipr_make_offshore_egypt_find/',
        # 'https://www.rigzone.com/news/wire/exxonmobil_unit_shuts_oil_sands_mine_after_pipeline_spill-02-sep-2020-163189-article/',
        # 'https://www.rigzone.com/news/oil_gas/a/144564/suncor_shuts_oil_sands_mine_again_as_alberta_fires_spread/',
        # 'https://www.rigzone.com/news/oil_gas/a/144370/syncrude_says_alberta_oil_sands_mine_shut_down_because_of_wildfire/',
        # 'https://www.rigzone.com/news/oil_gas/a/133327/total_suspends_work_on_alberta_joslyn_oil_sands_mine_cites_cost/',
        # 'https://www.rigzone.com/news/oil_gas/a/25268/ameccolt_jv_wins_athabasca_oil_sands_mine_expansion_phase_3_contract/',
        # 'https://www.rigzone.com/news/oil_gas/a/94454/gas_discovered_at_snadd_north_prospect/',
        # 'https://www.rigzone.com/news/oil_gas/a/71038/statoilhydro_to_drill_production_wells_on_gjoa/',
        # 'https://www.rigzone.com/news/oil_gas/a/51753/gawler_reports_production_increases_on_high_island_in_gom/',
        # 'https://www.rigzone.com/news/hnra_confirms_boost_in_untapped_oil_in_permian_basin_asset-15-mar-2024-176093-article/',
        'https://www.rigzone.com/news/oil_gas/a/44604/roxar_to_supply_wet_gas_meters_for_statoil/',
        'https://www.rigzone.com/news/oil_gas/a/74724/tnkbp_to_invest_1b_by_2012_for_samotlor_field_development/',
        'https://www.rigzone.com/news/oil_gas/a/53207/elixir_provides_production_update_on_gulf_of_mexico_fields/',
        # 'https://www.rigzone.com/news/oil_gas/a/137472/norways_offshore_knarr_field_to_deliver_gas_to_britain/',
        # 'https://www.rigzone.com/news/oil_gas/a/142609/petrobras_halts_oil_natgas_platform_output_for_second_time_in_8_days/',
        # 'https://www.rigzone.com/news/kosmos_boosts_profit_set_to_take_over_bp_operatorship_of_senegal_field-08-nov-2023-174626-article/',
        # 'https://www.rigzone.com/news/cnooc_starts_production_at_several_oil_gas_projects-17-nov-2023-174737-article/',
        ]

    def parse(self, response):
        # Extracting the title
        title = response.css('h1.articleTitle::text').get().strip()

        # Extracting the author
        author = response.css('div.articleAuthor a::text').get()

        # Extracting the publication date
        try:
            publication_date = response.css('div.articleDate::text').get().strip()
        except AttributeError:
            publication_date = ''

        # Extracting the article text
        paragraphs = response.css('div.divArticleText p::text').getall()
        article_text = '\n'.join(paragraphs)

        yield {
            'url': response.url,
            'title': title,
            'author': author,
            'publication_date': publication_date,
            'article_text': article_text
        }
