
import os
import re
import sys


def parse_members_for_workspace(toml_path):
    with open(toml_path, mode='rb') as f:
        data = f.read()

    manifest = data.decode('utf8')

    regex = re.compile(r"^members\s*=\s*\[(.*?)\]", re.S | re.M)
    members_block = regex.findall(manifest)[0]

    out = []

    members = members_block.split('\n')
    regex2 = re.compile(r'\s*"(.*?)".*')
    for m in members:
        if (len(m.strip()) == 0) or re.match(r".*#\signore", m):
            continue
        out.append(regex2.findall(m)[0])

    return out


def parse_package_name(package_toml_path):
    with open(package_toml_path, mode='rb') as f:
        data = f.read()

    manifest = data.decode('utf8')

    regex = re.compile(r'^name\s*=\s*"(.*?)"', re.M)

    return regex.findall(manifest)[0]


if len(sys.argv) < 3:
    err = f"[usage] python3 {sys.argv[0]} cargo_toml_path workspace_path"
    raise ValueError(err)

toml_path = sys.argv[1]
workspace_path = sys.argv[2]

packages = []

members = parse_members_for_workspace(toml_path)
for m in members:
    pkg_toml_path = os.path.join(workspace_path, m, "Cargo.toml")
    pkg_name = parse_package_name(pkg_toml_path)

    packages.append(pkg_name)

print(";".join(packages), end="")