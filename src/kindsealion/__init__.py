import dataclasses

import ruamel.yaml

from . import main2

__project_name__ = "kindsealion"


@dataclasses.dataclass
class Builder:
    name: str
    script: str


def main() -> int:
    args = main2.parse_args()
    outdir = args.outdir

    yaml_parser = ruamel.yaml.YAML()
    with open("manifest.yml", "r") as file:
        data = yaml_parser.load(file)

    manifests = []
    for item in data:
        manifests.append(
            Builder(
                name=item["name"],
                script=item["script"],
            )
        )

    template = main2.get_template("script.sh.j2")

    outdir.mkdir(parents=True, exist_ok=True)
    for manifest in manifests:
        script_path = outdir / f"{manifest.name}.sh"
        rendered_script = template.render(script=manifest.script)
        with script_path.open("w") as script_file:
            script_file.write(rendered_script)


if __name__ == "__main__":
    main()
