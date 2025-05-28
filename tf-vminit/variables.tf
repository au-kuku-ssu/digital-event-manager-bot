# Префикс для создаваемых объектов
variable "prefix" {
  type    = string
}

variable "ssh_string" {
  type = string
}

# Путь, где будет хранится пул проекта
variable "pool_path" {
  type    = string
}

# Параметры облачного образа
variable "image" {
  type = object({
    name = string
    url  = string
  })
}

# Параметры виртуальной машины
variable "vm" {
  type = object({
    cpu    = number
    ram    = number
    disk   = number
    bridge = string
  })
}
