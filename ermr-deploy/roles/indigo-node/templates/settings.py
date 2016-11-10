KEYSPACE = 'indigo'
LOG_LEVEL = 'INFO'
{% if cassandra_interface is defined %}
CASSANDRA_HOSTS = ("{{ hostvars[inventory_hostname]['ansible_' ~ cassandra_interface]['ipv4']['address'] }}", )
{% else %}
CASSANDRA_HOSTS = ("127.0.0.1", )
{% endif %}
REPLICATION_FACTOR = {{ cassandra_replication_factor }}
