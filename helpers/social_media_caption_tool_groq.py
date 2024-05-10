import os
from groq import Groq
from newspaper import Article
import time


class SocialMediaCaptionToolGroq:
    def __init__(self, links, target_audience="general"):
        self.links = links
        self.client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        self.target_audience = target_audience

    def scrape_article(self, url):
        try:
            article = Article(url)
            article.download()
            article.parse()
            return article.text
        except Exception as e:
            print(f"Error scraping article at {url}: {e}")
            return None

    def generate_summary(self, article_text):
        try:
            response = self.client.chat.completions.create(
                model=os.getenv('GROQ_MODEL_NAME'),
                temperature=0,
                max_tokens=1024,
                messages=[
                    {"role": "system", "content": "You are a sophisticated summarizing assistant with a sharp eye for detail and a knack for distilling complex information into its essence."},
                    {"role": "user",
                        "content": f"Please extract and provide a concise summary of the key points from the following article:\n\n {article_text}"},
                ],
                top_p=1,
                stream=False,
                stop=None,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating summary: {e}")
            return None

    def generate_social_media_captions(self, summary, url, selected_platforms, include_url):
        if summary is None:
            return {}
        try:
            captions = {}  # Initialize an empty dictionary for captions

            # Define prompts for each social media platform, tailored as per your previous setup
            prompts = {
                'Instagram': f"Write an Instagram caption that captures the essence of this summary, specifically crafted for {self.target_audience}. ALWAYS insert double spaces between sentences for easier reading. Include 3 relevant hashtags. Ensure it's engaging and fits the Instagram style:\n\n{summary}" + (f"\n\nInclude this link: {url}" if include_url else ""),
                'Facebook Group': f"Write a Facebook Group post caption that resonates with {self.target_audience}, derived from this summary. ALWAYS insert double spaces between sentences for easier reading. Include 3 relevant hashtags. Make it conversational and community-focused:\n\n{summary}" + (f"\n\nInclude this link: {url}" if include_url else ""),
                'Facebook Page': f"Write a Facebook Page post caption from this summary, tailored for {self.target_audience}. ALWAYS insert double spaces between sentences for easier reading. Include 3 relevant hashtags. Aim for a tone that's informative yet approachable:\n\n{summary}" + (f"\n\nInclude this link: {url}" if include_url else ""),
                'LinkedIn Page': f"Write a LinkedIn Page post caption from this summary, targeting {self.target_audience}. ALWAYS insert double spaces between sentences for easier reading. Include 3 relevant hashtags. Focus on a professional but engaging tone:\n\n{summary}" + (f"\n\nInclude this link: {url}" if include_url else ""),
                'LinkedIn Company Page': f"Write a LinkedIn Company Page post caption that appeals to {self.target_audience}, based on this summary. ALWAYS insert double spaces between sentences for easier reading. Include 3 relevant hashtags. Emphasize professionalism and brand values:\n\n{summary}" + (f"\n\nInclude this link: {url}" if include_url else ""),
                'YouTube Community Page': f"Write a YouTube Community post caption with this summary, aimed at engaging {self.target_audience}. ALWAYS insert double spaces between sentences for easier reading. Include 3 relevant hashtags. Make it lively and community-engaging:\n\n{summary}" + (f"\n\nInclude this link: {url}" if include_url else ""),
                'Twitter': f"Write a Twitter post caption using this summary, intended for {self.target_audience}. ALWAYS insert double spaces between sentences for easier reading. Include 3 relevant hashtags and ensure it's concise and impactful:\n\n{summary}" + (f"\n\nInclude this link: {url}" if include_url else ""),
                'Pinterest': f"Write a Pinterest post caption using this summary, intended for {self.target_audience}. ALWAYS insert double spaces between sentences for easier reading. Include 3 relevant hashtags and ensure it's concise and impactful:\n\n{summary}" + (f"\n\nInclude this link: {url}" if include_url else ""),
                'TikTok': f"Write a TikTok post caption using this summary, intended for {self.target_audience}. ALWAYS insert double spaces between sentences for easier reading. Include 3 relevant hashtags and ensure it's concise and impactful:\n\n{summary}" + (f"\n\nInclude this link: {url}" if include_url else ""),
                'YouTube Shorts': f"Write a YouTube Shorts post caption using this summary, intended for {self.target_audience}. ALWAYS insert double spaces between sentences for easier reading. Include 3 relevant hashtags and ensure it's concise and impactful:\n\n{summary}" + (f"\n\nInclude this link: {url}" if include_url else ""),
                'Email Copy': f"Write an email copy using this summary, intended for {self.target_audience}.\n\n{summary}\n\nInclude this link in a call to action button: {url}",
                'YouTube Video Script': f"Write a YouTube video script using this summary, intended for {self.target_audience}. Ensure it's engaging and fits the YouTube style and include a click bait video title:\n\n{summary}",
            }

            for platform in selected_platforms:
                if platform in prompts:  # Check if the platform was selected and has a defined prompt
                    prompt = prompts[platform]
                    response = self.client.chat.completions.create(
                        model="mixtral-8x7b-32768",
                        temperature=0.7,
                        max_tokens=1024,
                        messages=[
                            {"role": "system", "content": f"You are a social media management assistant providing creative and engaging captions for a blogger's social media posts. Ensure that each caption effectively highlights the essence of the blog post and is tailored to resonate with {self.target_audience} audience. Avoid adding extraneous characters before or after each caption. Alwaus insert double spaces between sentences for easier reading."},
                            {"role": "user", "content": prompt},
                        ],
                        top_p=1,
                        stream=False,
                        stop=None,
                    )
                    captions[platform] = response.choices[0].message.content.strip().strip(
                        '"').strip("'")
                    time.sleep(1)  # Wait for 1 second
                else:
                    # Ensure every selected platform has a key in the dictionary, even if empty
                    captions[platform] = ""

            return captions
        except Exception as e:
            print(f"Error generating captions: {e}")
            # Return the captions dictionary with whatever content has been generated so far
            return captions