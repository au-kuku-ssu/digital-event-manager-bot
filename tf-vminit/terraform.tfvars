prefix = "studyvms-"

ssh_string = "user@vm-host"

pool_path = "/opt/kvms/pools/"

image = {
  name = "debian-bookworm-generic.qcow2"
  url  = "https://cloud.debian.org/images/cloud/bookworm/20250428-2096/debian-12-generic-amd64-20250428-2096.qcow2"
}

vm = {
  bridge = "virbr0"
  cpu    = 2
  disk   = 10 * 1024 * 1024 * 1024
  ram    = 1024
}
