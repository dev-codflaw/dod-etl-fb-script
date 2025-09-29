# parser.py
import re
import json
import json_repair
from datetime import datetime, UTC
from parsel import Selector

from utils import c_replace, clean_url


def parse_profile(html_response: str, idd: str, input_url: str, html_file_path: str):
    """
    Parse Facebook profile/page HTML and extract structured info.
    Returns a dict ready to insert into MongoDB, or None if parsing fails.
    """

    tree = Selector(text=html_response)

    record = {
        "input_url": input_url,
        "time_stamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f"),
        "hash_id": idd,
        "pagesave": html_file_path,
        "fb_last_post_date": "",
        "fb_url": "",
        "fb_url_type": "",
        "fb_number_of_followers": "",
        "fb_company_name": "",
        "fb_company_intro": "",
        "fb_category": "",
        "fb_address": "",
        "fb_phone_number": "",
        "fb_email_address": "",
        "fb_website": "",
        "fb_website2": "",
        "fb_website3": "",
    }

    # Branch 1: profile_tile_section_type
    try:
        profile_data = tree.xpath('//script[@type="application/json"][contains(text(), "profile_tile_section_type")]/text()').get()
        if profile_data:
            profile_json = json.loads(profile_data)
            user_data = {}
            try:
                require_data = profile_json["require"][0][3][0]["__bbox"]["require"]
                for entry in require_data:
                    try:
                        data = entry[3][1]["__bbox"]["result"]["data"]
                        if "user" in data and "profile_tile_sections" in data["user"]:
                            user_data = data["user"]
                            break
                        elif "profile_tile_sections" in data:
                            user_data = data
                            break
                    except Exception:
                        continue
            except Exception:
                user_data = {}

            # category
            try:
                profile_category = [
                    item["node"]["timeline_context_item"]["renderer"]["context_item"]["title"]["text"]
                    for section in user_data.get("profile_tile_sections", {}).get("edges", [])
                    for view_node in section.get("node", {}).get("profile_tile_views", {}).get("nodes", [])
                    for item in
                    (view_node.get("view_style_renderer", {}) or {}).get("view", {}).get("profile_tile_items", {}).get("nodes", [])
                    if item.get("node", {}).get("timeline_context_item", {}).get("timeline_context_list_item_type") == "INTRO_CARD_INFLUENCER_CATEGORY"
                ]
            except:
                profile_category = []

            if profile_category:
                category = c_replace(profile_category[0])
                if category.lower().startswith("page ·"):
                    category = category[6:].strip()
                record["fb_category"] = category

            # address
            try:
                profile_address = [
                    item["node"]["timeline_context_item"]["renderer"]["context_item"]["title"]["text"]
                    for section in user_data.get("profile_tile_sections", {}).get("edges", [])
                    for view_node in section.get("node", {}).get("profile_tile_views", {}).get("nodes", [])
                    for item in
                    (view_node.get("view_style_renderer", {}) or {}).get("view", {}).get("profile_tile_items", {}).get("nodes", [])
                    if item.get("node", {}).get("timeline_context_item", {}).get("timeline_context_list_item_type") == "INTRO_CARD_ADDRESS"
                ]
            except:
                profile_address = []

            if profile_address:
                record["fb_address"] = c_replace(profile_address[0])

            # phone
            try:
                profile_contact = [
                    item["node"]["timeline_context_item"]["renderer"]["context_item"]["title"]["text"]
                    for section in user_data.get("profile_tile_sections", {}).get("edges", [])
                    for view_node in section.get("node", {}).get("profile_tile_views", {}).get("nodes", [])
                    for item in
                    (view_node.get("view_style_renderer", {}) or {}).get("view", {}).get("profile_tile_items", {}).get("nodes", [])
                    if item.get("node", {}).get("timeline_context_item", {}).get("timeline_context_list_item_type") == "INTRO_CARD_PROFILE_PHONE"
                ]
            except:
                profile_contact = []

            if profile_contact:
                record["fb_phone_number"] = profile_contact[0]

            # email
            try:
                mail_info = [
                    item["node"]["timeline_context_item"]["renderer"]["context_item"]["title"]["text"]
                    for section in user_data.get("profile_tile_sections", {}).get("edges", [])
                    for view_node in section.get("node", {}).get("profile_tile_views", {}).get("nodes", [])
                    for item in
                    (view_node.get("view_style_renderer", {}) or {}).get("view", {}).get("profile_tile_items", {}).get("nodes", [])
                    if item.get("node", {}).get("timeline_context_item", {}).get("timeline_context_list_item_type") == "INTRO_CARD_PROFILE_EMAIL"
                ]
            except:
                mail_info = []

            if mail_info:
                record["fb_email_address"] = mail_info[0]

            # websites
            try:
                website_info = [
                    item["node"]["timeline_context_item"]["renderer"]["context_item"]["title"]["text"]
                    for section in user_data.get("profile_tile_sections", {}).get("edges", [])
                    for view_node in section.get("node", {}).get("profile_tile_views", {}).get("nodes", [])
                    for item in
                    (view_node.get("view_style_renderer", {}) or {}).get("view", {}).get("profile_tile_items", {}).get("nodes", [])
                    if item.get("node", {}).get("timeline_context_item", {}).get("timeline_context_list_item_type") == "INTRO_CARD_WEBSITE"
                ]
            except:
                website_info = []

            if website_info:
                record["fb_website"] = clean_url(website_info[0] if len(website_info) > 0 else "")
                record["fb_website2"] = clean_url(website_info[1] if len(website_info) > 1 else "")
                record["fb_website3"] = clean_url(website_info[2] if len(website_info) > 2 else "")

    except Exception as e:
        print(f"⚠️ Error in profile_tile_section_type parsing: {e}")

    # Branch 2: full_address (pages)
    try:
        profile_data_2 = tree.xpath('//*[contains(text(),"full_address")]//text()').get()
        if profile_data_2:
            profile_json_2 = json.loads(profile_data_2)
            # Example: fetch address and category
            try:
                require_data = profile_json_2["require"][0][3][0]["__bbox"]["require"]
                for entry in require_data:
                    try:
                        data = entry[3][1]["__bbox"]["result"]["data"]
                        if "page" in data:
                            if "comet_page_cards" in data["page"]:
                                fields = data["page"]["comet_page_cards"][0]["page"]["page_about_fields"]
                                record["fb_address"] = c_replace(fields.get("address", {}).get("full_address", ""))
                                record["fb_category"] = c_replace(fields.get("page_categories", [{}])[0].get("text", ""))
                                record["fb_phone_number"] = fields.get("formatted_phone_number", "")
                                record["fb_website"] = clean_url(fields.get("website", ""))
                                record["fb_email_address"] = fields.get("email_address", "")
                    except:
                        continue
            except Exception as e:
                print(f"⚠️ Error in full_address parsing: {e}")
    except:
        pass

    # Branch 3: follower_count
    try:
        profile_data_3 = tree.xpath('//*[contains(text(),"follower_count")]//text()').get()
        if profile_data_3:
            profile_json_3 = json.loads(profile_data_3)
            try:
                require_data = profile_json_3["require"][0][3][0]["__bbox"]["require"]
                for entry in require_data:
                    try:
                        data = entry[3][1]["__bbox"]["result"]["data"]
                        if "page" in data:
                            page = data["page"]
                            record["fb_company_name"] = page.get("name", "")
                            record["fb_number_of_followers"] = page.get("follower_count", "")
                    except:
                        continue
            except Exception as e:
                print(f"⚠️ Error in follower_count parsing: {e}")
    except:
        pass

    return record
