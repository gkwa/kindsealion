packer {
 required_plugins {
   incus = {
     version = ">= 1.0.0"
     source  = "github.com/bketelsen/incus"
   }
   ansible = {
     version = "~> 1"
     source = "github.com/hashicorp/ansible"
   }
 }
}

source "incus" "jammy" {
 image        = "{{ image }}"
 output_image = "{{ output_image }}"
 container_name = "kindsealion"
 reuse        = true
 skip_publish = {{ skip_publish }}
}

build {
  sources = ["incus.jammy"]

  provisioner "shell" {
    scripts = [
      "dns.sh",
    ]
  }
  provisioner "file" {
    source      = "ringgem_update.sh"
    destination = "/var/lib/cloud/scripts/per-boot/ringgem_update.sh"
  }
  provisioner "shell" {
    inline = [
      "chmod +x /var/lib/cloud/scripts/per-boot/ringgem_update.sh",
    ]
  }
  provisioner "file" {
    source      = "{{ cloud_init }}"
    destination = "/etc/cloud/cloud.cfg.d/custom-cloud-init.cfg"
  }
  provisioner "shell" {
    inline = [
      "cloud-init status --wait",
    ]
  }
  provisioner "shell" {
    scripts = [
      "{{ script }}",
    ]
  }
}
