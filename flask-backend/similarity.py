from resume_processor import process_resume
from paper_retrieval import get_research_papers
from sentence_transformers import SentenceTransformer, util

# Load Sentence-BERT model
embed_model = SentenceTransformer('all-MiniLM-L6-v2')

def compute_highest_similarity(extracted_data, papers):
    """Computes and returns the highest similarity score with the title and abstract."""
    skills = extracted_data.get('skills', [])
    projects = extracted_data.get('projects', [])

    # Combine extracted skills and projects into one string
    combined_text = " ".join(skills + projects)
    resume_embedding = embed_model.encode(combined_text, convert_to_tensor=True)

    highest_similarity = None
    highest_score = -1
    
    for paper in papers:
        title = paper.get('title', '')
        abstract = paper.get('abstract', '')
        paper_text = f"{title} {abstract}"
        
        # Compute similarity score
        paper_embedding = embed_model.encode(paper_text, convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(resume_embedding, paper_embedding).item()

        if similarity > highest_score:
            highest_score = similarity
            highest_similarity = (title, abstract, similarity)

    return highest_similarity

if __name__ == "__main__":
    # Process resume
    resume_file = input("Enter resume file path: ")
    extracted_data = process_resume(resume_file)

    # Get research papers
    author_name = input("Enter researcher's name: ")
    papers, _ = get_research_papers(author_name)


    if not papers:
        print("No papers found. Exiting...")
        exit()

    # Compute highest similarity
    highest_similarity = compute_highest_similarity(extracted_data, papers)

    if highest_similarity:
        title, abstract, score = highest_similarity
        print("\n💡 Highest Similarity Result:")
        print(f"Title: {title}")
        print(f"Abstract: {abstract}")
        print(f"Similarity Score: {score:.4f}")