import html
def escape_html(text: str | None) -> str:
    return "" if text is None else html.escape(text, quote=True).replace("'", "&#39;")

def transform_fetched_pages(fetched_pages):
    transformed_chunks = []
    for page in fetched_pages:
        if len(escape_html(page["body"]["storage"]["value"])) < 500:
            transformed_chunks.append({
                "title": page["title"],
                "id": page["id"],
                "content": escape_html(page["body"]["storage"]["value"])
            })
        else:
            start = 0 
            end = 500
            while start < len(page["body"]["storage"]["value"]):
                transformed_chunks.append({
                    "title": page["title"],
                    "id": page["id"],
                    "content": escape_html(page["body"]["storage"]["value"][start:end])
                })
                start += 500
                end += 500

    print(transformed_chunks)
    return transformed_chunks