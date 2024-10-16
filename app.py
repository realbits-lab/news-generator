from hackernews import scrape_hacker_news

if __name__ == "__main__":
    entries = scrape_hacker_news()

    # Sort entries by points (descending order)
    entries_by_points = sorted(entries, key=lambda x: x["points"], reverse=True)
    for entry in entries_by_points[:5]:  # Display top 5 entries
        print(f"{entry['title']} - {entry['points']} points")

    import requests
    from bs4 import BeautifulSoup
    from openai import OpenAI
    import os
    from dotenv import load_dotenv

    load_dotenv()

    client = OpenAI()
    client.api_key = os.getenv("OPENAI_API_KEY")

    def summarize_text(text):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes text.",
                },
                {
                    "role": "user",
                    "content": f"Summarize the following text in 3 itemized sentences in Korean. Use numbering for items.:\n\n{text}",
                },
            ],
            max_tokens=4096,
            n=1,
            temperature=0.5,
        )
        # print(f"response: {response}")
        return response.choices[0].message.content.strip()

    def generate_excerpt(summaries):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that generates an excerpt from a list of summaries.",
                },
                {
                    "role": "user",
                    "content": f"Generate excerpt from a list of summaries in Korean within 100 characters.\n\n{summaries}",
                },
            ],
            max_tokens=4096,
            n=1,
            temperature=0.5,
        )
        # print(f"response: {response}")
        return response.choices[0].message.content.strip()

    def crawl_and_summarize(url):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            text = soup.get_text()
            return summarize_text(text[:4000])  # Limit text to 4000 characters
        except Exception as e:
            return f"Error crawling {url}: {str(e)}"

    print("\nTop 5 entries with summaries:")
    summaries = []
    for entry in entries_by_points[:5]:
        title = entry["title"]
        url = entry["url"]
        summary = crawl_and_summarize(url)
        summaries.append(summary)

        print(f"<a href='{url}'>{title}</a>")
        print(summary)
        print()

    excerpt = generate_excerpt(summaries)
    print(f"\nExcerpt: {excerpt}")
