
from bs4 import BeautifulSoup, NavigableString, Tag
import uuid
import re

def chunk_html(soup, max_chunk_size=1000):
    chunks = []
    
    # Define heading hierarchy
    heading_tags = ["h1", "h2", "h3", "h4", "h5", "h6"]
    
    # Get all headings with their hierarchy level
    headings = []
    for heading in soup.find_all(heading_tags):
        level = int(heading.name[1])  # h1 -> 1, h2 -> 2, etc.
        headings.append({
            "element": heading,
            "level": level,
            "text": heading.get_text(" ", strip=True)
        })
    
    # Process each heading with its complete content
    for i, heading_info in enumerate(headings):
        heading = heading_info["element"]
        current_level = heading_info["level"]
        
        # Find all content between this heading and the next heading of same or higher level
        content_elements = []
        
        # Get next heading at same or higher level
        next_heading_index = None
        for j in range(i + 1, len(headings)):
            if headings[j]["level"] <= current_level:
                next_heading_index = j
                break
        
        # Collect all elements between current and next heading
        current = heading.next_sibling
        end_element = headings[next_heading_index]["element"] if next_heading_index else None
        
        # Include sub-headings and their content
        sub_sections = []
        
        while current and current != end_element:
            if isinstance(current, Tag):
                if current.name in heading_tags:
                    # This is a sub-heading
                    sub_level = int(current.name[1])
                    if sub_level > current_level:
                        sub_sections.append({
                            "title": current.get_text(" ", strip=True),
                            "content": []
                        })
                elif current.name in ["p", "ul", "ol", "pre", "table", "blockquote"]:
                    # Regular content
                    if sub_sections:
                        # Add to the last sub-section
                        sub_sections[-1]["content"].append(current)
                    else:
                        content_elements.append(current)
            
            current = current.next_sibling
        
        # Format the complete chunk
        chunk_content = format_section_content(heading_info["text"], content_elements, sub_sections)
        
        # Only create chunk if there's meaningful content
        if chunk_content["content"].strip():
            # Check if we need to split due to size
            if len(chunk_content["content"].split()) > max_chunk_size:
                # Split large chunks while keeping sub-sections together
                split_chunks = chunk_content
                chunks.extend(split_chunks)
            else:
                chunks.append(chunk_content)
    
    # Handle any content before the first heading
    first_heading = headings[0]["element"] if headings else None
    if first_heading:
        intro_content = []
        current = soup.find()
        while current and current != first_heading:
            if isinstance(current, Tag) and current.name in ["p", "ul", "ol", "pre", "table", "blockquote"]:
                intro_content.append(current)
            current = current.next_sibling
        
        if intro_content:
            intro_chunk = {"title": "Introduction", "content": ""}
            for el in intro_content:
                intro_chunk["content"] += format_element_content(el) + "\n"
            if intro_chunk["content"].strip():
                chunks.insert(0, intro_chunk)
    
    return chunks

def format_section_content(main_title, content_elements, sub_sections):
    """Format a section with its main content and sub-sections"""
    chunk = {"title": main_title, "content": ""}
    
    # Add main content
    for el in content_elements:
        formatted = format_element_content(el)
        if formatted.strip():
            chunk["content"] += formatted + "\n\n"
    
    # Add sub-sections
    for sub in sub_sections:
        if sub["content"]:
            # Add sub-heading
            chunk["content"] += f"\n### {sub['title']}\n\n"
            
            # Add sub-section content
            for el in sub["content"]:
                formatted = format_element_content(el)
                if formatted.strip():
                    chunk["content"] += formatted + "\n\n"
    
    # Clean up formatting
    chunk["content"] = clean_content(chunk["content"])
    return chunk

def format_element_content(el):
    """Format element content based on its type"""
    if not el:
        return ""
    
    if el.name == "p":
        return el.get_text(" ", strip=True)
    
    elif el.name in ["ul", "ol"]:
        items = []
        for i, li in enumerate(el.find_all("li", recursive=False)):
            # Get direct text content
            text = ""
            for child in li.children:
                if isinstance(child, NavigableString):
                    text += str(child).strip()
                elif child.name not in ["ul", "ol"]:
                    text += child.get_text(" ", strip=True)
            
            if text:
                if el.name == "ul":
                    items.append(f"• {text}")
                else:
                    items.append(f"{i + 1}. {text}")
            
            # Handle nested lists
            for nested in li.find_all(["ul", "ol"], recursive=False):
                nested_content = format_element_content(nested)
                if nested_content:
                    # Indent nested items
                    indented = "\n".join("  " + line for line in nested_content.split("\n"))
                    items.append(indented)
        
        return "\n".join(items)
    
    elif el.name == "pre":
        code_text = el.get_text()
        return f"```\n{code_text}\n```"
    
    elif el.name == "code":
        return f"`{el.get_text()}`"
    
    elif el.name == "table":
        rows = []
        for tr in el.find_all("tr"):
            cells = [td.get_text(" ", strip=True) for td in tr.find_all(["td", "th"])]
            if cells:
                rows.append(" | ".join(cells))
        
        if rows:
            # Add header separator if first row appears to be headers
            if len(rows) > 1:
                rows.insert(1, " | ".join(["---"] * len(rows[0].split(" | "))))
        
        return "\n".join(rows)
    
    elif el.name == "blockquote":
        lines = el.get_text(" ", strip=True).split("\n")
        return "\n".join(f"> {line}" for line in lines if line.strip())
    
    else:
        return el.get_text(" ", strip=True)

def clean_content(content):
    """Clean up content formatting"""
    # Remove multiple consecutive newlines (keep max 2)
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    # Remove trailing whitespace from lines
    lines = [line.rstrip() for line in content.split('\n')]
    
    # Remove duplicate consecutive non-empty lines
    cleaned_lines = []
    prev_line = None
    
    for line in lines:
        if line != prev_line or not line:  # Allow empty lines
            cleaned_lines.append(line)
            if line:  # Only update prev_line for non-empty lines
                prev_line = line
    
    return '\n'.join(cleaned_lines).strip()

def transform_fetched_pages(fetched_pages):
    transformed_chunks = []
    
    for page in fetched_pages:
        soup = BeautifulSoup(page["body"]["storage"]["value"], "html.parser")
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        chunks = chunk_html(soup, max_chunk_size=1000)
        
        for i, chunk in enumerate(chunks):
            chunk_id = str(uuid.uuid4())
            
            # Format title with page context
            title = chunk['title'] or "Untitled Section"
            if page['title']:
                title = f"{title} ({page['title']})"
            
            transformed_chunks.append({
                "id": chunk_id,
                "title": title,
                "content": chunk["content"],
                "pageId": page["id"],
                "pageTitle": page["title"],
                "chunkIndex": i,
            })
    return transformed_chunks