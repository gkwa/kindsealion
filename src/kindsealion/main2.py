import dataclasses
import logging
import pathlib
import typing
import urllib.error
import urllib.parse
import urllib.request

import jinja2
import networkx
import ruamel.yaml

from .parse_args import parse_args

ringgem_tpl = pathlib.Path("ringgem.sh.j2")


def get_template(template_name):
    TEMPLATES_PATH = pathlib.Path(__file__).resolve().parent / "templates"
    loader = jinja2.FileSystemLoader(searchpath=TEMPLATES_PATH)
    env = jinja2.Environment(loader=loader, keep_trailing_newline=True)
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
    G = networkx.DiGraph()
    for i, manifest in enumerate(manifests):
        G.add_node(manifest.name)
        if i > 0:
            G.add_edge(manifests[i - 1].name, manifest.name)
    return G


def load_manifest_data(
    manifest_path: typing.Union[str, pathlib.Path],
) -> typing.Dict[typing.Any, typing.Any]:
    if not manifest_path:
        raise ValueError("Manifest path cannot be empty")

    yaml_parser = ruamel.yaml.YAML(typ="safe")

    parsed_url = urllib.parse.urlparse(str(manifest_path))
    is_url = parsed_url.scheme in ("http", "https")

    try:
        if is_url:
            with urllib.request.urlopen(manifest_path) as response:
                return yaml_parser.load(response)
        else:
            path = pathlib.Path(manifest_path)
            with path.open("r", encoding="utf-8") as file:
                return yaml_parser.load(file)

    except FileNotFoundError:
        raise FileNotFoundError(f"Manifest file not found: {manifest_path}")
    except urllib.error.URLError as e:
        raise urllib.error.URLError(f"Failed to fetch manifest from URL: {e}")
    except ruamel.yaml.YAMLError as e:
        raise ruamel.yaml.YAMLError(f"Failed to parse YAML content: {e}")


def create_manifests(data, starting_image):
    all_manifests = []
    for i, item in enumerate(data["manifests"]):
        script_content = item.get("script_content", "")
        if script_content:
            script_content = ruamel.yaml.scalarstring.PreservedScalarString(
                script_content
            )
        manifest = Builder(
            name=item["name"],
            script_content=script_content,
            cloud_init=item.get("cloud_init", ""),
        )
        prefix = f"{i:03d}_{manifest.name}"
        manifest.script = f"{prefix}.sh"
        manifest.output_image = prefix
        manifest.task = prefix
        manifest.packer_file = f"{prefix}.pkr.hcl"
        manifest.cloud_init_file = f"{prefix}-cloud-init.yml"
        if i == 0:
            manifest.image = starting_image
        else:
            manifest.image = all_manifests[-1].output_image
        all_manifests.append(manifest)
    return all_manifests


def filter_manifests(all_manifests):
    return [m for m in all_manifests if m.script_content or m.cloud_init]


def update_manifest_dependencies(manifests, dependency_tree):
    manifests_by_name = {m.name: m for m in manifests}
    for manifest in manifests:
        parent = list(dependency_tree.predecessors(manifest.name))
        if parent:
            manifest.deps.append(manifests_by_name[parent[0]].task)


def process_manifest(manifest, outdir, skip_publish, data):
    logging.info(
        f"Processing manifest: {manifest.name}\n"
        f"Script: {manifest.script}\n"
        f"Image: {manifest.image}\n"
        f"Output Image: {manifest.output_image}\n\n"
    )
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
            ringgem=ringgem_tpl.with_suffix("").name,
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


def write_taskfile(outdir, manifests, dependency_tree, manifests_by_name):
    taskfile_path = outdir / "Taskfile.yml"
    with taskfile_path.open("w") as taskfile:
        rendered_taskfile = render_template(
            "Taskfile.yml.j2",
            manifests=manifests,
            dependency_tree=dependency_tree,
            manifests_by_name=manifests_by_name,
        )
        rendered_taskfile = rendered_taskfile.strip()
        taskfile.write(rendered_taskfile + "\n")


def write_ringgem_update(outdir):
    bash = ringgem_tpl.with_suffix("")
    name = str(ringgem_tpl)
    out = outdir / bash
    with out.open("w") as f:
        u = render_template(name, ringgem=bash)
        f.write(u)


def write_dns(outdir):
    dns_path = outdir / "dns.sh"
    with dns_path.open("w") as ringgem:
        r = render_template(
            "dns.sh.j2",
        )
        ringgem.write(r)


def configure_logging(verbose):
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=log_level, format="%(levelname)s: %(message)s")


def main():
    args = parse_args()
    outdir = args.outdir
    starting_image = args.starting_image
    skip_publish = args.skip_publish
    manifest_url = args.manifest_url
    verbose = args.verbose

    configure_logging(verbose)

    data = load_manifest_data(manifest_url)
    all_manifests = create_manifests(data, starting_image)
    manifests = filter_manifests(all_manifests)
    dependency_tree = build_dependency_tree(manifests)
    update_manifest_dependencies(manifests, dependency_tree)

    outdir.mkdir(parents=True, exist_ok=True)
    for manifest_name in networkx.topological_sort(dependency_tree):
        manifest = next(m for m in manifests if m.name == manifest_name)
        process_manifest(manifest, outdir, skip_publish, data)

    manifests_by_name = {m.name: m for m in manifests}
    write_taskfile(outdir, manifests, dependency_tree, manifests_by_name)
    write_ringgem_update(outdir)
    write_dns(outdir)


if __name__ == "__main__":
    main()
