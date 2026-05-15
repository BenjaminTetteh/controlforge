def add_section(
    sections: list,
    title: str,
    content: str
):

    sections.append(
        {
            "title": title,
            "content": content
        }
    )


def render_text_report(
    sections: list
):

    rendered = []

    for section in sections:

        rendered.append(
            f"{section['title']}\n"
            f"{'-' * len(section['title'])}\n\n"
            f"{section['content']}\n"
        )

    return "\n".join(rendered)