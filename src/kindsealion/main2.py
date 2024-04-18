import dataclasses
import pathlib
import urllib.request

import jinja2
import networkx as nx
import ruamel.yaml

from .parse_args import parse_args


def get_template(template_name):
    TEMPLATES_PATH = pathlib.Path(__file__).resolve().parent / "templates"
    loader = jinja2.FileSystemLoader(searchpath=TEMPLATES_PATH)
    env = jinja2.Environment(loader=loader)
    return env.get_template(template_name)


def render_template(template_name, **kwargs):
    template = get_template(template_name)
    return template.render(**kwargs)


@dataclasses.dataclass
class Builder:
    name: str
    script_content: ruamel.yaml.scalarstring.PreservedScalarString
    script: str = ""
    image: str = ""
    output_image: str = ""
    task: str = ""
    packer_file: str = ""
    deps: list = dataclasses.field(default_factory=list)
    cloud_init_file: str = ""
    cloud_init: str = ""


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
    starting_image = args.starting_image
    skip_publish = args.skip_publish
    manifest_url = args.manifest_url
    yaml_parser = ruamel.yaml.YAML()

    try:
        with open("manifest.yml", "r") as file:
            data = yaml_parser.load(file)
    except FileNotFoundError:
        if manifest_url.startswith("http"):
            with urllib.request.urlopen(manifest_url) as response:
                data = yaml_parser.load(response)
        else:
            with open(manifest_url, "r") as file:
                data = yaml_parser.load(file)

    manifests = []
    for i, item in enumerate(data["manifests"]):
        script_content = item.get("script_content", "")
        if script_content:
            script_content = ruamel.yaml.scalarstring.PreservedScalarString(
                script_content
            )
        manifests.append(
            Builder(
                name=item["name"],
                script_content=script_content,
            )
        )
        manifests[-1].script = f"{i:03d}_{manifests[-1].name}.sh"
        manifests[-1].output_image = f"{i:03d}_{manifests[-1].name}"
        manifests[-1].task = f"{i:03d}_{manifests[-1].name}"
        manifests[-1].packer_file = f"{i:03d}_{manifests[-1].name}.pkr.hcl"
        manifests[-1].cloud_init_file = f"{i:03d}_{manifests[-1].name}-cloud-init.yml"
        manifests[-1].cloud_init = item.get("cloud_init", "")
        if i == 0:
            manifests[-1].image = starting_image
        else:
            manifests[-1].image = manifests[-2].output_image

    dependency_tree = build_dependency_tree(manifests)
    manifests_by_name = {m.name: m for m in manifests}

    for manifest in manifests:
        parent = list(dependency_tree.predecessors(manifest.name))
        if parent:
            manifest.deps.append(manifests_by_name[parent[0]].task)

    outdir.mkdir(parents=True, exist_ok=True)
    for i, manifest_name in enumerate(nx.topological_sort(dependency_tree)):
        manifest = next(m for m in manifests if m.name == manifest_name)
        print(
            f"Processing manifest: {manifest_name}\n"
            f"Script: {manifest.script}\n"
            f"Image: {manifest.image}\n"
            f"Output Image: {manifest.output_image}\n\n"
        )
        if manifest.script_content:
            script_path = outdir / f"{manifest.script}"
            with script_path.open("w") as script_file:
                rendered_script = render_template(
                    "script.sh.j2", script_content=manifest.script_content
                )
                script_file.write(rendered_script)
            packer_path = outdir / manifest.packer_file
            with packer_path.open("w") as packer_file:
                rendered_packer = render_template(
                    "ubuntu.pkr.hcl",
                    image=manifest.image,
                    output_image=manifest.output_image,
                    script=manifest.script,
                    skip_publish="true" if skip_publish else "false",
                    cloud_init=manifest.cloud_init_file,
                )
                packer_file.write(rendered_packer)

            cloud_init_content = data.get("cloud_init", "")
            if manifest.cloud_init:
                cloud_init_content = manifest.cloud_init

            if cloud_init_content:
                cloud_init_path = outdir / manifest.cloud_init_file
                with cloud_init_path.open("w") as cloud_init_file:
                    cloud_init_file.write(cloud_init_content)

    taskfile_path = outdir / "Taskfile.yml"
    with taskfile_path.open("w") as taskfile:
        rendered_taskfile = render_template(
            "Taskfile.yml.j2",
            manifests=manifests,
            dependency_tree=dependency_tree,
            manifests_by_name=manifests_by_name,
        )
        taskfile.write(rendered_taskfile)


if __name__ == "__main__":
    main()
