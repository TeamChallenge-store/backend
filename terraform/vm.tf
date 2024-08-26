resource "google_compute_instance" "public_instance" {
  name         = "public-instance"
  machine_type = "e2-medium"

  boot_disk {
  initialize_params {
    image = "ubuntu-os-cloud/ubuntu-2004-lts" 
    size  = 30
  }
}

  network_interface {
    network = "default"
    access_config {}
  }

  tags = ["http-server", "https-server"]

  metadata = {
    ssh-keys = "${var.key_name}:${tls_private_key.rsa_4096.public_key_openssh}"
  }

  provisioner "local-exec" {
    command = "touch dynamic_inventory.ini"
  }

  provisioner "remote-exec" {
    inline = [
      "echo 'GCP instance is ready.'"
    ]

    connection {
      type        = "ssh"
      host        = google_compute_instance.public_instance.network_interface.0.access_config.0.nat_ip
      user        = "your_username"
      private_key = tls_private_key.rsa_4096.private_key_pem
    }
  }
  
}

data "template_file" "inventory" {
  template = <<-EOT
    [gcp_instances]
    ${google_compute_instance.public_instance.network_interface.0.access_config.0.nat_ip} ansible_user=ubuntu ansible_private_key_file=${path.module}/${var.key_name}
  EOT
}

resource "local_file" "dynamic_inventory" {
  depends_on = [google_compute_instance.public_instance]

  filename = "dynamic_inventory.ini"
  content  = data.template_file.inventory.rendered
}
