resource "google_container_cluster" "slon-cluster" {
  name     = "my-gke-cluster"
  location = "us-central1"
  remove_default_node_pool = true
  initial_node_count       = 1
}

resource "google_container_node_pool" "slon-pool" {
  name       = "my-node-pool"
  location   = "us-central1"
  cluster    = google_container_cluster.slon-cluster.name
  node_count = 1  

  node_config {
    preemptible  = true
    machine_type = "e2-medium"  
  }
}
