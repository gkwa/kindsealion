import argparse
import dataclasses
import pathlib

import jinja2
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


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--outdir",
        type=pathlib.Path,
        help="Output directory",
        default="kindsealion",
    )
    return parser.parse_args()


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
            )
        )

    outdir.mkdir(parents=True, exist_ok=True)
    for manifest in manifests:
        script_path = outdir / f"{manifest.name}.sh"
        with script_path.open("w") as script_file:
            script_file.write(manifest.script)


if __name__ == "__main__":
    main()
