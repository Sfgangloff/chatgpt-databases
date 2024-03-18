import yaml
from jinja2 import Template

# Step 1: Read YAML file
with open('data/molecular_biology/with_text.yaml', 'r') as file:
    yaml_content = yaml.safe_load(file)

# Step 2: Parse YAML
sections = yaml_content["sections"]

# Step 3: Generate HTML using a template
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Your YAML to HTML Page</title>
</head>
<body>
    {% for section in sections %}
        <h1 style="text-align:center">{{section["number"]}}- {{ section["title"] }}</h1>

        {% for subsection in section["subsections"] %}
            <h2>{{section["number"]}}.{{subsection["number"]}}- {{ subsection["title"] }}</h2>
                <p>{{ subsection["content"]["content"] }}</p>
        {% endfor %}
    {% endfor %}
</body>
</html>
"""

template = Template(html_template)

# Step 4: Write to HTML file
with open('output.html', 'w') as html_file:
    html_file.write(template.render(sections=sections))