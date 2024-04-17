import argparse
import dataclasses
import pathlib

import jinja2
import networkx as nx
import ruamel.yaml


def get_template(template_name):
    TEMPLATES_PATH = pathlib.Path(__file__).resolve().parent / "templates"
    loader = jinja2.FileSystemLoader(searchpath=TEMPLATES_PATH)
    env = jinja2.Environment(loader=loader)
    return env.get_template(template_name)


def render_template(template_name, data=None):
    template = get_template(template_name)
    return template.render(data=data)


@dataclasses.dataclass
class Builder:
    name: str
    script: ruamel.yaml.scalarstring.PreservedScalarString
    parent: str = None


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--outdir",
        type=pathlib.Path,
        help="Output directory",
        default="kindsealion",
    )
    return parser.parse_args()


def build_dependency_tree(manifests):
    G = nx.DiGraph()
    for manifest in manifests:
        G.add_node(manifest.name)
        if manifest.parent:
            G.add_edge(manifest.parent, manifest.name)
    return G


def main():
    args = parse_args()
    outdir = args.outdir
    yaml_parser = ruamel.yaml.YAML()

    with open("manifest.yml", "r") as file:
        data = yaml_parser.load(file)

    manifests = []
    for item in data:
        manifests.append(
            Builder(
                name=item["name"],
                script=ruamel.yaml.scalarstring.PreservedScalarString(item["script"]),
                parent=item.get("parent"),
            )
        )

    dependency_tree = build_dependency_tree(manifests)

    outdir.mkdir(parents=True, exist_ok=True)
    for manifest_name in nx.topological_sort(dependency_tree):
        manifest = next(m for m in manifests if m.name == manifest_name)
        parent = manifest.parent if manifest.parent else "None"
        print(f"Processing manifest: {manifest_name}, Parent: {parent}")
        script_path = outdir / f"{manifest.name}.sh"
        with script_path.open("w") as script_file:
            rendered_script = render_template(
                "script.sh.j2", data={"script": manifest.script}
            )
            script_file.write(rendered_script)
