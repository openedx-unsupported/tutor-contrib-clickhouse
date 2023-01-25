from glob import glob
import os
import pkg_resources

from tutor import hooks

from .__about__ import __version__


########################################
# CONFIGURATION
########################################

hooks.Filters.CONFIG_DEFAULTS.add_items(
    [
        # Add your new settings that have default values here.
        # Each new setting is a pair: (setting_name, default_value).
        # Prefix your setting names with 'CLICKHOUSE_'.
        ("CLICKHOUSE_VERSION", __version__),
        ("CLICKHOUSE_HOST", "clickhouse_service"),
        ("CLICKHOUSE_PORT", "9000"),
        ("CLICKHOUSE_HTTP_PORT", "8123"),
        ("CLICKHOUSE_XAPI_DATABASE", "xapi"),

        # This can be used to override some configuration values in
        # via "docker_config.xml" file, which will be read from a
        # mount on /etc/clickhouse-server/config.d/ on startup.
        # See https://clickhouse.com/docs/en/operations/configuration-files
        #
        # This default allows connecting to Clickhouse when run as a
        # standalone docker container, instead of through docker-compose.
        ("CLICKHOUSE_EXTRA_XML_CONFIG", """
    <listen_host>::</listen_host>
    <listen_host>0.0.0.0</listen_host>
    <listen_try>1</listen_try>
        """),
    ]
)

hooks.Filters.CONFIG_UNIQUE.add_items(
    [
        # Add settings that don't have a reasonable default for all users here.
        # For instance: passwords, secret keys, etc.
        # Each new setting is a pair: (setting_name, unique_generated_value).
        # Prefix your setting names with 'CLICKHOUSE_'.
        # For example:
        # ("CLICKHOUSE_SECRET_KEY", "{{ 24|random_string }}"),
        ("CLICKHOUSE_ADMIN_USER", "ch_admin"),
        ("CLICKHOUSE_ADMIN_PASSWORD", "{{ 24|random_string }}"),
        ("CLICKHOUSE_LRS_USER", "ch_lrs"),
        ("CLICKHOUSE_LRS_PASSWORD", "{{ 24|random_string }}"),
        ("CLICKHOUSE_REPORT_USER", "ch_report"),
        ("CLICKHOUSE_REPORT_PASSWORD", "{{ 24|random_string }}"),
    ]
)

hooks.Filters.CONFIG_OVERRIDES.add_items(
    [
        # Danger zone!
        # Add values to override settings from Tutor core or other plugins here.
        # Each override is a pair: (setting_name, new_value). For example:
        # ("PLATFORM_NAME", "My platform"),
    ]
)


########################################
# INITIALIZATION TASKS
########################################

# To run the script from templates/clickhouse/tasks/myservice/init.sh, add:
hooks.Filters.COMMANDS_INIT.add_item((
    "clickhouse_service",
    ("clickhouse", "tasks", "init.sh"),
))


########################################
# DOCKER IMAGE MANAGEMENT
########################################

# hooks.Filters.IMAGES_BUILD.add_item((
#     "clickhouse_service",
#     ("plugins", "clickhouse", "build", "clickhouse_service"),
#     "tutor_clickhouse:{{ CLICKHOUSE_VERSION }}",
#     (),
# ))

# To pull/push an image with `tutor images pull myimage` and `tutor images push myimage`, write:
# hooks.Filters.IMAGES_PULL.add_item((
#     "myimage",
#     "docker.io/myimage:{{ CLICKHOUSE_VERSION }}",
# )
# hooks.Filters.IMAGES_PUSH.add_item((
#     "myimage",
#     "docker.io/myimage:{{ CLICKHOUSE_VERSION }}",
# )


########################################
# TEMPLATE RENDERING
# (It is safe & recommended to leave
#  this section as-is :)
########################################

hooks.Filters.ENV_TEMPLATE_ROOTS.add_items(
    # Root paths for template files, relative to the project root.
    [
        pkg_resources.resource_filename("tutorclickhouse", "templates"),
    ]
)

hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
    # For each pair (source_path, destination_path):
    # templates at ``source_path`` (relative to your ENV_TEMPLATE_ROOTS) will be
    # rendered to ``source_path/destination_path`` (relative to your Tutor environment).
    # For example, ``tutorclickhouse/templates/clickhouse/build``
    # will be rendered to ``$(tutor config printroot)/env/plugins/clickhouse/build``.
    [
        ("clickhouse/build", "plugins"),
        ("clickhouse/apps", "plugins"),
    ],
)

hooks.Filters.ENV_PATCHES.add_item(
    (
        "local-docker-compose-services",
        """
clickhouse_service:
    image: clickhouse/clickhouse-server:latest
    environment:
        CLICKHOUSE_DB: xapi
        CLICKHOUSE_USER: "{{ CLICKHOUSE_ADMIN_USER }}"
        CLICKHOUSE_PASSWORD: "{{ CLICKHOUSE_ADMIN_PASSWORD }}"
        CLICKHOUSE_DEFAULT_ACCESS_MANAGEMENT: 1
    ports:
        - 18123:{{ CLICKHOUSE_HTTP_PORT }}
        - 19000:{{ CLICKHOUSE_PORT }}
    ulimits:
        nofile:
            soft: 262144
            hard: 262144
    volumes:
        - ../../data/clickhouse:/var/lib/clickhouse/
        - ../../env/plugins/clickhouse/apps/config:/etc/clickhouse-server/config.d/
        """
    )
)

hooks.Filters.ENV_PATCHES.add_item(
    (
        "local-docker-compose-jobs-services",
        """
clickhouse_service-job:
    image: clickhouse/clickhouse-server:latest
    depends_on: 
        - clickhouse_service
        """,
    )
)


########################################
# PATCH LOADING
# (It is safe & recommended to leave
#  this section as-is :)
########################################

# For each file in tutorclickhouse/patches,
# apply a patch based on the file's name and contents.
for path in glob(
    os.path.join(
        pkg_resources.resource_filename("tutorclickhouse", "patches"),
        "*",
    )
):
    with open(path, encoding="utf-8") as patch_file:
        hooks.Filters.ENV_PATCHES.add_item((os.path.basename(path), patch_file.read()))
