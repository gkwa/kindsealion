packer {
   required_plugins {
       incus = {
           version = ">= 1.0.0"
           source = "github.com/bketelsen/incus"
       }
       ansible = {
           version = "~> 1"
           source = "github.com/hashicorp/ansible"
       }
   }
}

source "incus" "jammy" {
   image = "{{ data.image }}"
   output_image = "{{ data.output_image }}"
   container_name = "mythai"
   reuse = true
   skip_publish = {{ data.skip_publish }}
}

build {
   sources = ["incus.jammy"]
   provisioner "shell" {
       scripts = [
           "{{ data.script }}",
       ]
   }
}
