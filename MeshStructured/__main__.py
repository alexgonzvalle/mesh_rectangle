import logging

from MeshStructured import MeshStructured

logging.basicConfig(level=logging.INFO)


def main():
    logging.info(MeshStructured)


if __name__ == '__main__':
    logging.debug('>>> Estamos comenzando la ejecución del paquete.')

    main()

    logging.debug('>>> Estamos finalizando la ejecución del paquete.')