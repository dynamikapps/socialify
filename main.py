import datetime
import pandas as pd
from dotenv import load_dotenv
import streamlit as st
from helpers.blog_url_finder import BlogUrlFinder
from helpers.social_media_caption_tool_claude import SocialMediaCaptionToolClaude as SocialMediaCaptionTool
# from helpers.social_media_caption_tool_groq import SocialMediaCaptionToolGroq as SocialMediaCaptionTool
# from helpers.social_media_caption_tool_openai import SocialMediaCaptionToolOpenAI as SocialMediaCaptionTool


load_dotenv()


def get_blog_links(url):
    finder = BlogUrlFinder(url)
    # Use the BlogUrlFinder to get blog URLs
    blog_post_urls = finder.fetch_blog_urls()
    return blog_post_urls


def generate_captions(selected_links, selected_platforms, target_audience, include_url, include_summary, separate_files):
    smct = SocialMediaCaptionTool(selected_links, target_audience)
    data = []
    for link in selected_links:
        print(f"Processing: {link}")
        article_text = smct.scrape_article(link)
        summary = smct.generate_summary(
            article_text) if article_text else "Summary generation failed"
        captions = smct.generate_social_media_captions(
            summary, link, selected_platforms, include_url)

        # Ensure the row includes all selected platforms, even if some captions are empty
        row = {'blog_post_url': link}
        if include_summary:
            row['blog_post_summary'] = summary
        row.update(captions)  # Merge the captions into the row dictionary
        data.append(row)

    # Create DataFrame
    dataframe = pd.DataFrame(data)

    # Output to CSV
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    if separate_files:
        output_csv_paths = []
        for platform in selected_platforms:
            platform_df = dataframe[[
                'blog_post_url'] + (['blog_post_summary'] if include_summary else []) + [platform]].copy()
            platform_df.dropna(how='any', inplace=True)
            # Replace spaces with underscores and convert to lowercase
            platform_name = platform.replace(" ", "_").lower()
            output_csv_path = f"output_{platform_name}_{timestamp}.csv"
            platform_df.to_csv(output_csv_path, index=False)
            output_csv_paths.append(output_csv_path)
        print(f"Output written to: {', '.join(output_csv_paths)}")
        return output_csv_paths  # Optionally return the paths of the generated CSV files
    else:
        # Ensure DataFrame includes all selected platforms as columns
        for platform in selected_platforms:
            if platform not in dataframe.columns:
                dataframe[platform] = ""
        output_csv_path = f"output_{timestamp}.csv"
        dataframe.to_csv(output_csv_path, index=False)
        print(f"Output written to {output_csv_path}")
        return output_csv_path  # Optionally return the path of the generated CSV file


def main():
    st.title("🚀 Socialify")
    st.subheader(
        "Generate social content for multiple platforms from your blog in one click.")

    if 'website_url' not in st.session_state:
        st.session_state.website_url = ''
    if 'target_audience' not in st.session_state:
        st.session_state.target_audience = 'general'
    if 'selected_links' not in st.session_state:
        st.session_state.selected_links = []
    if 'selected_platforms' not in st.session_state:
        st.session_state.selected_platforms = []
    if 'include_url' not in st.session_state:
        st.session_state.include_url = True
    if 'separate_files' not in st.session_state:
        st.session_state.separate_files = False

    with st.form(key='my_form'):
        st.session_state.website_url = st.text_input(
            "Enter your website URL", st.session_state.website_url)
        st.session_state.target_audience = st.text_input(
            "Enter your target audience (optional)", st.session_state.target_audience)
        blog_links = get_blog_links(
            st.session_state.website_url) if st.session_state.website_url else []
        st.session_state.selected_links = st.multiselect(
            "Select the URLs you want to generate content for", blog_links, st.session_state.selected_links)
        platforms = ['Instagram', 'Facebook Group', 'Facebook Page', 'LinkedIn Page', 'LinkedIn Company Page',
                     'YouTube Community Page', 'Twitter', 'Pinterest', 'TikTok', 'Email Copy', 'YouTube Shorts', 'YouTube Video Script']
        st.session_state.selected_platforms = st.multiselect(
            "Select the social media platforms", platforms, st.session_state.selected_platforms)
        st.session_state.include_url = st.checkbox(
            "Include blog post URL in content", value=True)
        st.session_state.include_summary = st.checkbox(
            "Include blog post summary in file", value=True)
        st.session_state.separate_files = st.checkbox(
            "Generate separate file for each social media platform", value=False)
        submit_button = st.form_submit_button(label='Generate Content')

    if submit_button:
        if st.session_state.website_url and st.session_state.selected_links and st.session_state.selected_platforms:
            output_csv_paths = generate_captions(
                st.session_state.selected_links, st.session_state.selected_platforms, st.session_state.target_audience, st.session_state.include_url, st.session_state.include_summary, st.session_state.separate_files)
            if isinstance(output_csv_paths, list):
                st.write(f"Output written to: {', '.join(output_csv_paths)}")
            else:
                st.write(f"Output written to: {output_csv_paths}")
        else:
            st.write("Please fill in all the fields.")


if __name__ == "__main__":
    main()
