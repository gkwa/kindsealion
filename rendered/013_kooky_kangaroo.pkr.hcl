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
 image        = "012_playful_platypus"
 output_image = "013_kooky_kangaroo"
 container_name = "kindsealion"
 reuse        = true
 skip_publish = false
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
    source      = "013_kooky_kangaroo-cloud-init.yml"
    destination = "/etc/cloud/cloud.cfg.d/custom-cloud-init.cfg"
  }
  provisioner "shell" {
    scripts = [
      "013_kooky_kangaroo.sh",
    ]
  }
}
