andebox
=======

Ansible Developer's (tool)Box, **andebox**, is a single script to assist Ansible developers
by encapsulating some boilerplate tasks. Right now the core feature is the ability to run
`ansible-test` on a collection dircetory without having to worry about your `COLLECTIONS_PATH`
environment variable nor having the _expected_ directory structure _above_ the collection 
directory.

It also allows some basic stats gathering from the `tests/sanity/ignore-X.Y.txt` files.

## Installation

Install it as usual:

    pip install andebox

### Dependencies

As of this version, the dependencies are `PyYAML` for reading `galaxy.yml`, and `ansible` itself for 
the drop-in `ansible-test` feature (see comments below).

## Usage

After installing the tool (ensuring it is reachable in from `PATH`), there are different actions available, as described below.

### Drop-in ansible-test

```
andebox test -h
usage: andebox test usage: andebox test [-h] [--keep] -- [ansible_test_params ...]

positional arguments:
  ansible_test_params

optional arguments:
  -h, --help            show this help message and exit
  --keep, -k            Keep temporary directory after execution
  --exclude-ignore, -ei
                        Matching lines in ignore files will be filtered out

Notice the use of '--' to delimit andebox's options from ansible-test's
```

Arranging the directories the way Ansible expects them to be is a boilerplate step, and not the way everyone likes to have their git repos.
No need to worry about that anymore.

    $ andebox test -- sanity --docker default -v --test validate-modules plugins/modules/system/xfconf.py

Producing an output similar to:

    namespace  = community
    collection = general
    top_dir    = /tmp/andebox.i2aeeqpm
    coll_dir   = /tmp/andebox.i2aeeqpm/ansible_collections/community/general
    
    Run command: docker images quay.io/ansible/default-test-container:2.7.0 --format '{{json .}}'
    Scanning collection root: /tmp/andebox.i2aeeqpm/ansible_collections
    Including collection: community.general (2565 files)
    [...]
    Running sanity test 'validate-modules' with Python 3.6
    Read 391 sanity test ignore line(s) for Ansible 2.10 from: tests/sanity/ignore-2.10.txt
    [...]
    Run command: /usr/bin/python3.6 /root/ansible/test/lib/ansible_test/_data/collection_detail.py /root/ansible_collections/commun ...
    Run command: /usr/bin/python3.6 /root/ansible/test/lib/ansible_test/_data/sanity/validate-modules/validate-modules --format jso ...
    [...]
    Run command: docker rm -f 7784964b35b32ae1a89e233a052045751d1fa6da73076eabfc40d0c5f4e72cb6

By default, `andebox` will discover the full name of the collection by parsing the `galaxy.yml` file usually found in the local directory.
If the file is not present or if it fails for any reason, the option `--collection` may be used to specify it, as in:

    andebox test --collection community.general -- sanity --docker default -v --test validate-modules plugins/modules/system/xfconf.py

Also notice that, as `andebox` uses whichever `ansible-test` is available in `PATH` for execution, the developer
freedom to use any version of `ansible` they see fit, and even allowing a more sophisticated setup (with `tox` for 
example) to test their code with multiple `ansible` versions.

### Stats on ignore files

```
andebox ignores -h
usage: andebox ignores [-h] [--ignore-file-spec {2.9,2.10,2.11,-}] [--depth DEPTH] [--file-filter FILE_FILTER] [--check-filter CHECK_FILTER] [--suppress-files] [--suppress-checks] [--head HEAD]

optional arguments:
  -h, --help            show this help message and exit
  --ignore-file-spec {2.9,2.10,2.11,-}, -ifs {2.9,2.10,2.11,-}
                        Use the ignore file matching this Ansible version. The special value '-' may be specified to read from stdin instead. If not specified, will use all available files
  --depth DEPTH, -d DEPTH
                        Path depth for grouping files
  --file-filter FILE_FILTER, -ff FILE_FILTER
                        Regexp matching file names to be included
  --check-filter CHECK_FILTER, -cf CHECK_FILTER
                        Regexp matching checks in ignore files to be included
  --suppress-files, -sf
                        Supress file names from the output, consolidating the results
  --suppress-checks, -sc
                        Suppress the checks from the output, consolidating the results
  --head HEAD, -H HEAD  Number of lines to display in the output: leading lines if positive, trailing lines if negative, all lines if zero.
```

Gathering stats from the ignore files can be quite annoying, especially if they are long.

    $ andebox ignores -v2.10 -d4 -i '.*:parameter-list-no-elements'

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

### Runtime config

```
andebox runtime -h
usage: andebox runtime [-h] [--plugin-type {connection,lookup,modules,doc_fragments,module_utils,callback,inventory}] [--regex] [--info-type INFO_TYPE] plugin_names [plugin_names ...]

positional arguments:
  plugin_names

optional arguments:
  -h, --help            show this help message and exit
  --plugin-type {connection,lookup,modules,doc_fragments,module_utils,callback,inventory}, -pt {connection,lookup,modules,doc_fragments,module_utils,callback,inventory}
                        Specify the plugin type to be searched
  --regex, --regexp, -r
                        Treat plugin names as regular expressions
  --info-type INFO_TYPE, -it INFO_TYPE
                        Restrict type of response elements. Must be in ('redirect', 'tombstone', 'deprecation'), may be shortened down to one letter.
```

Quickly peek what's in the `runtime.yml`:

```
$ andebox runtime scaleway_ip_facts
D modules scaleway_ip_facts: deprecation in 3.0.0 (current=2.4.0): Use community.general.scaleway_ip_info instead.
```

```
$ andebox runtime -r 'gc[pe]'
R lookup gcp_storage_file: redirected to community.google.gcp_storage_file
T modules gce: terminated in 2.0.0: Use google.cloud.gcp_compute_instance instead.
R modules gce_eip: redirected to community.google.gce_eip
R modules gce_img: redirected to community.google.gce_img
R modules gce_instance_template: redirected to community.google.gce_instance_template
R modules gce_labels: redirected to community.google.gce_labels
R modules gce_lb: redirected to community.google.gce_lb
R modules gce_mig: redirected to community.google.gce_mig
R modules gce_net: redirected to community.google.gce_net
R modules gce_pd: redirected to community.google.gce_pd
R modules gce_snapshot: redirected to community.google.gce_snapshot
R modules gce_tag: redirected to community.google.gce_tag
T modules gcp_backend_service: terminated in 2.0.0: Use google.cloud.gcp_compute_backend_service instead.
T modules gcp_forwarding_rule: terminated in 2.0.0: Use google.cloud.gcp_compute_forwarding_rule or google.cloud.gcp_compute_global_forwarding_rule instead.
T modules gcp_healthcheck: terminated in 2.0.0: Use google.cloud.gcp_compute_health_check, google.cloud.gcp_compute_http_health_check or google.cloud.gcp_compute_https_health_check instead.
T modules gcp_target_proxy: terminated in 2.0.0: Use google.cloud.gcp_compute_target_http_proxy instead.
T modules gcp_url_map: terminated in 2.0.0: Use google.cloud.gcp_compute_url_map instead.
R modules gcpubsub: redirected to community.google.gcpubsub
R modules gcpubsub_info: redirected to community.google.gcpubsub_info
R modules gcpubsub_facts: redirected to community.google.gcpubsub_info
R doc_fragments _gcp: redirected to community.google._gcp
R module_utils gce: redirected to community.google.gce
R module_utils gcp: redirected to community.google.gcp
```
where D=Deprecated, T=Tombstone, R=Redirect.
