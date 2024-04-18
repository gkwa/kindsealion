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
      "{{ script }}",
    ]
  }
}
