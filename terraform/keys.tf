resource "google_compute_ssh_key" "ssh_key" {
  project     = "your-google-cloud-project"
  public_key  = "${var.key_name}:${tls_private_key.rsa_4096.public_key_openssh}"
}

resource "local_file" "private_key" {
  content  = tls_private_key.rsa_4096.private_key_pem
  filename = var.key_name

  provisioner "local-exec" {
    command = "chmod 400 ${var.key_name}"
  }
}

resource "tls_private_key" "rsa_4096" {
  algorithm = "RSA"
  rsa_bits  = 4096
}