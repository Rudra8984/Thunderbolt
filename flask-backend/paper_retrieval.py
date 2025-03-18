import requests

def get_research_papers(author_name):
    """Fetch research papers using Semantic Scholar API."""
    
    # Step 1: Get author ID by name
    url = f"https://api.semanticscholar.org/graph/v1/author/search?query={author_name}&fields=authorId,name,affiliations"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to fetch author ID: {response.status_code}")
        return None, None
    
    author_data = response.json()
    if not author_data.get('data'):
        print(f"No author found with name '{author_name}'.")
        return None, None
    
    # Get the first matching author
    author = author_data['data'][0]
    author_id = author['authorId']
    researcher_name = author.get('name', 'Unknown')

    # Handle missing affiliations
    affiliations = author.get('affiliations', [])
    institution = affiliations[0].get('name', 'Unknown Institution') if affiliations else 'Unknown Institution'
    
    # Step 2: Get papers using author ID (including paperId for the link)
    url = f"https://api.semanticscholar.org/graph/v1/author/{author_id}/papers?fields=title,abstract,paperId"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to fetch papers: {response.status_code}")
        return None, None
    
    papers = response.json().get('data', [])
    
    # Step 3: Format the output
    details = {
        "researcher": researcher_name,
        "papers": []
    }
    
    results = []
    
    for paper in papers:
        title = paper.get('title', 'No Title')
        abstract = paper.get('abstract', 'No Abstract')
        paper_id = paper.get('paperId', '')
        link = f"https://www.semanticscholar.org/paper/{paper_id}" if paper_id else 'No Link'
        
        # Append to results (title, abstract, link)
        results.append({"title": title, "abstract": abstract, "link": link})
        
        # Append to details (title, abstract, link)
        details["papers"].append({"title": title, "abstract": abstract, "link": link})
    
    return results, details

if __name__ == "__main__":
    author_name = input("Enter researcher's name: ")
    results, details = get_research_papers(author_name)
    print(results)
    print()
    print(details)