andebox
=======

Ansible Developer's (tool)Box, **andebox**, is a single script to assist Ansible developers
by encapsulating some boilerplate tasks. Right now the core feature is the ability to run
`ansible-test` on a collection dircetory without having to worry about your `COLLECTIONS_PATH`
environment variable nor having the _expected_ directory structure _above_ the collection 
directory.

It also allows some basic stats gathering from the `tests/sanity/ignore-X.Y.txt` files.

## Installation

For the time being, install directly from the git URL:

    pip install git+https://github.com/russoz/andebox

We should soon enough put it into PyPI for a more regular procedure.

### Dependencies

As of this version, the dependencies are `PyYAML` for reading `galaxy.yml`, and `ansible` itself for 
the drop-in `ansible-test` feature (see comments below).

## Featured actions

### Drop-in ansible-test

After installing the tool, ensuring it is in your `PATH` or use the absolute path for it, simply run:

    cd git/community.general   # example, it should work on any collection
    andebox test -- sanity --docker default -v --test validate-modules plugins/modules/system/xfconf.py

Producing an output similar to:

    namespace  = community
    collection = general
    top_dir    = /tmp/andebox.i2aeeqpm
    coll_dir   = /tmp/andebox.i2aeeqpm/ansible_collections/community/general
    
    Run command: docker images quay.io/ansible/default-test-container:2.7.0 --format '{{json .}}'
    Scanning collection root: /tmp/andebox.i2aeeqpm/ansible_collections
    Including collection: community.general (2565 files)
    Creating a payload archive containing 3284 files...
    Created a 4284192 byte payload archive containing 3284 files in 0 seconds.
    Assuming Docker is available on localhost.
    Run command: docker run --detach --volume /sys/fs/cgroup:/sys/fs/cgroup:ro --privileged=false --security-opt seccomp=unconfined ...
    Run command: docker exec -i 7784964b35b32ae1a89e233a052045751d1fa6da73076eabfc40d0c5f4e72cb6 dd of=/root/docker.sh bs=65536
    Run command: docker exec 7784964b35b32ae1a89e233a052045751d1fa6da73076eabfc40d0c5f4e72cb6 /bin/bash /root/docker.sh
    Run command: docker exec -i 7784964b35b32ae1a89e233a052045751d1fa6da73076eabfc40d0c5f4e72cb6 dd of=/root/test.tgz bs=65536
    Run command: docker exec 7784964b35b32ae1a89e233a052045751d1fa6da73076eabfc40d0c5f4e72cb6 tar oxzf /root/test.tgz -C /root
    Run command: docker exec 7784964b35b32ae1a89e233a052045751d1fa6da73076eabfc40d0c5f4e72cb6 /usr/bin/env ANSIBLE_TEST_CONTENT_ROO ...
    Running sanity test 'validate-modules' with Python 3.6
    Read 391 sanity test ignore line(s) for Ansible 2.10 from: tests/sanity/ignore-2.10.txt
    Run command: /usr/bin/python3.6 /root/ansible/test/lib/ansible_test/_data/quiet_pip.py install --disable-pip-version-check -r / ...
    Run command: /usr/bin/python3.6 /root/ansible/test/lib/ansible_test/_data/quiet_pip.py install --disable-pip-version-check -r / ...
    Run command: /usr/bin/python3.6 /root/ansible/test/lib/ansible_test/_data/quiet_pip.py check --disable-pip-version-check
    Run command: /usr/bin/python3.6 /root/ansible/test/lib/ansible_test/_data/yamlcheck.py
    Run command: /usr/bin/python3.6 /root/ansible/test/lib/ansible_test/_data/collection_detail.py /root/ansible_collections/commun ...
    Run command: /usr/bin/python3.6 /root/ansible/test/lib/ansible_test/_data/sanity/validate-modules/validate-modules --format jso ...
    Run command: docker exec 7784964b35b32ae1a89e233a052045751d1fa6da73076eabfc40d0c5f4e72cb6 tar czf /root/output.tgz --exclude .t ...
    Run command: docker exec -i 7784964b35b32ae1a89e233a052045751d1fa6da73076eabfc40d0c5f4e72cb6 dd if=/root/output.tgz bs=65536
    Run command: tar oxzf /tmp/ansible-result-_s6h3314.tgz -C /tmp/andebox.i2aeeqpm/ansible_collections/community/general/tests
    Run command: docker rm -f 7784964b35b32ae1a89e233a052045751d1fa6da73076eabfc40d0c5f4e72cb6

By default, `andebox` will search for a `galaxy.yml` file in the local directory and it will read the collections's
namespace and name from there. If the file is not present or if it fails for any reason, the option `--collection` may
be used to specify it, as in:

    andebox test --collection community.general -- sanity --docker default -v --test validate-modules plugins/modules/system/xfconf.py

Also notice that `andebox` rely on `ansible-test` being available in `PATH` for execution. This gives the developer 
freedom to use any version of `ansible` they see fit, and even allowing a more sophisticated setup (with `tox` for 
example) to test their code with multiple `ansible` versions.

### Stats on ignore files

After installing the tool, ensuring it is in your `PATH` or use the absolute path for it, simply run:

    cd git/community.general   # example, it should work on any collection
    andebox ignores -v2.10 -d4 -i '.*:parameter-list-no-elements' | head

Producing an output similar to:

    24  plugins/modules/cloud/ovirt validate-modules:parameter-list-no-elements
     8  plugins/modules/cloud/centurylink validate-modules:parameter-list-no-elements
     6  plugins/modules/remote_management/redfish validate-modules:parameter-list-no-elements
     5  plugins/modules/cloud/oneandone validate-modules:parameter-list-no-elements
     4  plugins/modules/cloud/rackspace validate-modules:parameter-list-no-elements
     4  plugins/modules/remote_management/oneview validate-modules:parameter-list-no-elements
     3  plugins/modules/cloud/opennebula validate-modules:parameter-list-no-elements
     3  plugins/modules/cloud/univention validate-modules:parameter-list-no-elements
     3  plugins/modules/clustering/consul validate-modules:parameter-list-no-elements
     3  plugins/modules/monitoring/sensu validate-modules:parameter-list-no-elements

## CLI Help

### Basic usage
```
# andebox -h
usage: andebox [-h] [--collection COLLECTION] {test,ignores} ...

Ansible Collection Developer's Box

positional arguments:
  {test,ignores}
    test                Runs ansible-test in a temporary environment
    ignores             Gathers stats on ignore*.txt file(s)

optional arguments:
  -h, --help            show this help message and exit
  --collection COLLECTION, -c COLLECTION
                        Ansible name for the collection, in the form namespace.name
```

### Ansible Test usage
```
# andebox test -h
usage: andebox test usage: andebox test [-h] [--keep] -- ansible_test_params [ansible_test_params ...]

positional arguments:
  ansible_test_params

optional arguments:
  -h, --help           show this help message and exit
  --keep, -k           Keep temporary directory after execution

Notice the use of '--' to delimit andebox's options from ansible-test's
```

### Gathers stats on ignore files
```
# andebox ignores -h
usage: andebox ignores [-h] [--version {2.9,2.10,2.11,-}] [--depth DEPTH] [--filter FILTER] [--igfilter IGFILTER] [--sort-ignores]
                       [--count-ignores]

optional arguments:
  -h, --help            show this help message and exit
  --version {2.9,2.10,2.11,-}, -v {2.9,2.10,2.11,-}
                        Use the ignore file matching this Ansible version. The special value '-' may be specified to read from
                        stdin instead. If not specified, will use all available files
  --depth DEPTH, -d DEPTH
                        Path depth for grouping files
  --filter FILTER, -f FILTER
                        Regexp to filter out file names
  --igfilter IGFILTER, -i IGFILTER
                        Regexp to filter out ignored checks
  --sort-ignores, -s    Sort the ignored checks only
  --count-ignores, -c   Count the ignored checks per file only
```
