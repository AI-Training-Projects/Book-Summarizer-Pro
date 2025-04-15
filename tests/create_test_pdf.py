from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.units import inch

def create_test_pdf():
    doc = SimpleDocTemplate(
        "tests/sample_ai_article.pdf",
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )

    # Wikipedia content about AI
    content = """Artificial Intelligence

Artificial intelligence (AI) is intelligence demonstrated by computers, as opposed to human or animal intelligence. The field of AI research defines itself as the study of "intelligent agents": any system that perceives its environment and takes actions that maximize its chance of achieving its goals.

The term "artificial intelligence" had its origins in the 1950s, when early computer scientists began exploring how machines could solve problems by mimicking human biological neural networks. The field has since expanded dramatically, encompassing various approaches such as expert systems, machine learning, and deep learning.

Key Applications:
1. Machine Learning: Systems that can learn from data without being explicitly programmed
2. Natural Language Processing: Enabling computers to understand and generate human language
3. Computer Vision: Systems that can interpret and analyze visual information from the world
4. Robotics: Machines that can interact with and manipulate the physical world
5. Expert Systems: Programs designed to emulate decision-making of human experts

Modern AI has become an essential part of the technology industry, contributing to solutions in healthcare, finance, transportation, and many other fields. Despite its achievements, AI still faces challenges in areas such as common-sense reasoning, generalization, and ethical decision-making.

The development of AI raises important questions about its impact on society, including job displacement, privacy concerns, and the need for responsible development practices. As AI continues to advance, these considerations become increasingly important for researchers, developers, and society at large."""

    styles = getSampleStyleSheet()
    story = []

    # Create custom style for paragraphs
    custom_style = ParagraphStyle(
        'CustomStyle',
        fontSize=12,
        leading=14,
        spaceAfter=10,
        parent=styles['Normal']
    )

    # Split content into paragraphs and add to story
    paragraphs = content.split('\n\n')
    for p in paragraphs:
        if p.strip():
            story.append(Paragraph(p, custom_style))

    doc.build(story)

if __name__ == "__main__":
    create_test_pdf()
