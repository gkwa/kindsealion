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
 image        = "009_perky_porcupine"
 output_image = "010_merry_manatee"
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
    source      = "010_merry_manatee-cloud-init.yml"
    destination = "/etc/cloud/cloud.cfg.d/custom-cloud-init.cfg"
  }
  provisioner "shell" {
    scripts = [
      "010_merry_manatee.sh",
    ]
  }
}
