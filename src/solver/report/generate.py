# Basic Jinja2 template rendering

from pathlib import Path
import jinja2


def build_report():
    template_dir = Path(__file__).parent / "templates"
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(template_dir),
        autoescape=jinja2.select_autoescape(["html", "xml"]),
    )
    template = env.get_template("report.html")
    print(template.render())


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    main()
