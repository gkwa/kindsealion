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
 image        = "images:ubuntu/20.04/cloud"
 output_image = "000_wacky_pickle"
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
    source      = "000_wacky_pickle-cloud-init.yml"
    destination = "/etc/cloud/cloud.cfg.d/custom-cloud-init.cfg"
  }
  provisioner "shell" {
    scripts = [
      "000_wacky_pickle.sh",
    ]
  }
}
