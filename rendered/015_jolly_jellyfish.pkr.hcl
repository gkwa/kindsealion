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
 image        = "014_kooky_kangaroo"
 output_image = "015_jolly_jellyfish"
 container_name = "kindsealion"
 reuse        = true
 skip_publish = false
}

build {
  sources = ["incus.jammy"]

  provisioner "file" {
    source      = "ringgem.sh"
    destination = "/var/lib/cloud/scripts/per-boot/ringgem.sh"
  }
  provisioner "shell" {
    inline = [
      "chmod +x /var/lib/cloud/scripts/per-boot/ringgem.sh",
    ]
  }

  provisioner "file" {
    source      = "015_jolly_jellyfish-cloud-init.yml"
    destination = "/etc/cloud/cloud.cfg.d/custom-cloud-init.cfg"
  }

  provisioner "shell" {
    inline = [
      "cloud-init status --wait",
    ]
  }

  provisioner "shell" {
    scripts = [
      "015_jolly_jellyfish.sh",
    ]
  }
}
