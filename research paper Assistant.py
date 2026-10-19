import os
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Reference:
    id: str
    authors: str
    title: str
    source: str
    year: int
    doi: Optional[str] = None

@dataclass
class Section:
    title: str
    content: str

class ResearchPaperAssistant:
    def __init__(self, paper_title: str, author_name: str):
        self.paper_title = paper_title
        self.author_name = author_name
        self.sections: List[Section] = []
        self.references: List[Reference] = []

    def add_section(self, title: str, content: str):
        """Adds a section (e.g., Abstract, Introduction) to the paper."""
        self.sections.append(Section(title=title, content=content))
        print(f"✅ Added Section: {title}")

    def add_reference(self, ref_id: str, authors: str, title: str, source: str, year: int, doi: str = None):
        """Adds a reference to the bibliography."""
        ref = Reference(ref_id, authors, title, source, year, doi)
        self.references.append(ref)
        print(f"✅ Added Reference: [{ref_id}] {title}")

    def format_apa_citation(self, ref: Reference) -> str:
        """Formats a reference in APA style."""
        citation = f"{ref.authors} ({ref.year}). {ref.title}. *{ref.source}*."
        if ref.doi:
            citation += f" https://doi.org/{ref.doi}"
        return citation

    def format_ieee_citation(self, ref: Reference, index: int) -> str:
        """Formats a reference in IEEE style."""
        citation = f"[{index}] {ref.authors}, \"{ref.title},\" {ref.source}, {ref.year}."
        if ref.doi:
            citation += f" doi: {ref.doi}."
        return citation

    def get_word_count(self) -> int:
        """Calculates the total word count of the paper's content."""
        total_words = 0
        for section in self.sections:
            total_words += len(section.content.split())
        return total_words

    def export_to_html(self, filename: str = "research_paper.html", citation_style: str = "APA"):
        """Generates a cleanly formatted HTML document of the research paper."""
        
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{self.paper_title}</title>
            <style>
                body {{ font-family: 'Times New Roman', Times, serif; line-height: 1.6; max-width: 800px; margin: 40px auto; padding: 20px; color: #333; }}
                h1 {{ text-align: center; margin-bottom: 5px; }}
                h2 {{ color: #2c3e50; border-bottom: 1px solid #ccc; padding-bottom: 5px; margin-top: 30px; }}
                .author {{ text-align: center; font-style: italic; margin-bottom: 30px; color: #555; }}
                .meta {{ text-align: right; font-size: 0.9em; color: #777; }}
                .content p {{ text-indent: 40px; text-align: justify; margin-bottom: 15px; }}
                .references li {{ margin-bottom: 10px; padding-left: 20px; text-indent: -20px; }} /* Hanging indent */
            </style>
        </head>
        <body>
            <div class="meta">Word Count: {self.get_word_count()}</div>
            <h1>{self.paper_title}</h1>
            <div class="author">By {self.author_name}</div>
        """

        # Add Sections
        for section in self.sections:
            html_content += f"<h2>{section.title}</h2>\n"
            html_content += "<div class=\"content\">\n"
            # Split by double newlines to create paragraphs
            paragraphs = section.content.split('\n\n')
            for p in paragraphs:
                if p.strip():
                    html_content += f"<p>{p.strip()}</p>\n"
            html_content += "</div>\n"

        # Add References
        if self.references:
            html_content += "<h2>References</h2>\n"
            if citation_style.upper() == "APA":
                html_content += "<ul class=\"references\" style=\"list-style-type: none; padding-left: 0;\">\n"
                # APA is usually sorted alphabetically by author
                sorted_refs = sorted(self.references, key=lambda x: x.authors)
                for ref in sorted_refs:
                    html_content += f"<li>{self.format_apa_citation(ref)}</li>\n"
                html_content += "</ul>\n"
            
            elif citation_style.upper() == "IEEE":
                html_content += "<ul class=\"references\" style=\"list-style-type: none; padding-left: 0;\">\n"
                for i, ref in enumerate(self.references, start=1):
                    html_content += f"<li>{self.format_ieee_citation(ref, i)}</li>\n"
                html_content += "</ul>\n"

        html_content += """
        </body>
        </html>
        """

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"\n📄 Success! Research paper exported to HTML: {os.path.abspath(filename)}")


# ==========================================
# Example Usage
# ==========================================
if __name__ == "__main__":
    # 1. Initialize the Assistant
    assistant = ResearchPaperAssistant(
        paper_title="The Impact of Artificial Intelligence on Automated Code Generation",
        author_name="Dr. Alan Turing Jr."
    )

    # 2. Add Content Sections
    assistant.add_section(
        title="Abstract",
        content="This paper explores the recent advancements in Large Language Models (LLMs) and their efficacy in automating software engineering tasks. We evaluate the generation of HTML, Python, and CSS across various domains, noting a significant decrease in boilerplate coding time."
    )

    assistant.add_section(
        title="1. Introduction",
        content="The advent of AI-assisted programming has shifted the paradigm of software development. Developers are increasingly relying on machine learning models to scaffold applications. \n\nHowever, ensuring the logical correctness of generated code remains a challenge. This study aims to quantify both the time saved and the error rates introduced by automated coding assistants."
    )

    assistant.add_section(
        title="2. Methodology",
        content="We conducted a controlled experiment with 50 software engineers. Group A used traditional IDEs, while Group B utilized an AI coding assistant. Both groups were tasked with building a responsive web application and a Python data-processing backend."
    )

    # 3. Add References
    assistant.add_reference(
        ref_id="vaswani2017",
        authors="Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., ... & Polosukhin, I.",
        title="Attention is all you need",
        source="Advances in neural information processing systems",
        year=2017
    )
    
    assistant.add_reference(
        ref_id="brown2020",
        authors="Brown, T., Mann, B., Ryder, N., Subbiah, M., Kaplan, J. D., Dhariwal, P., ... & Amodei, D.",
        title="Language models are few-shot learners",
        source="Advances in neural information processing systems",
        year=2020
    )

    # 4. Generate Output (Produces an actual HTML file you can open in your browser)
    assistant.export_to_html(filename="my_research_paper.html", citation_style="APA")