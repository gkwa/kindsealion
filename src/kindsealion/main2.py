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
    script_content: ruamel.yaml.scalarstring.PreservedScalarString
    script: str = ""
    image: str = ""
    output_image: str = ""


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
    for i, manifest in enumerate(manifests):
        G.add_node(manifest.name)
        if i > 0:
            G.add_edge(manifests[i - 1].name, manifest.name)
    return G


def main():
    args = parse_args()
    outdir = args.outdir
    yaml_parser = ruamel.yaml.YAML()

    with open("manifest.yml", "r") as file:
        data = yaml_parser.load(file)

    manifests = []
    for i, item in enumerate(data):
        manifests.append(
            Builder(
                name=item["name"],
                script_content=ruamel.yaml.scalarstring.PreservedScalarString(
                    item["script_content"]
                ),
            )
        )
        manifests[-1].script = f"{i:03d}_{manifests[-1].name}.sh"
        manifests[-1].output_image = f"{i:03d}_{manifests[-1].name}"
        if i == 0:
            manifests[-1].image = "ubuntu/20.04/cloud"
        else:
            manifests[-1].image = manifests[-2].output_image

    dependency_tree = build_dependency_tree(manifests)

    outdir.mkdir(parents=True, exist_ok=True)
    for manifest_name in nx.topological_sort(dependency_tree):
        manifest = next(m for m in manifests if m.name == manifest_name)
        parent = next(
            (
                m.name
                for m in manifests
                if manifest_name in dependency_tree.successors(m.name)
            ),
            None,
        )
        print(
            f"Processing manifest: {manifest_name}, Parent: {parent}, Script: {manifest.script}, Image: {manifest.image}, Output Image: {manifest.output_image}"
        )
        script_path = outdir / f"{manifest.script}"
        with script_path.open("w") as script_file:
            rendered_script = render_template(
                "script.sh.j2", data={"script_content": manifest.script_content}
            )
            script_file.write(rendered_script)


if __name__ == "__main__":
    main()
