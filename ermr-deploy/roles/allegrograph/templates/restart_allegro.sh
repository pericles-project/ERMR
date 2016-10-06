#/bin/sh

{{ install_dir }}/ag5.1/bin/agraph-control  --config {{ install_dir }}/ag5.1/lib/agraph.cfg stop
{{ install_dir }}/ag5.1/bin/agraph-control  --config {{ install_dir }}/ag5.1/lib/agraph.cfg start
