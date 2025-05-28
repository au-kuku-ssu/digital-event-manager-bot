provider "libvirt" {
	uri = "qemu+ssh://${var.ssh_string}/system"
}
