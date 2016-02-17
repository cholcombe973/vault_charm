backend "consul" {
  path = "vault"
}

listener "tcp" {
  address = "{{private_address}}:8200"
  tls_disable = 1
}

listener "tcp" {
  tls_disable = 1
}