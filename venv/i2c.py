import setup as s

# _____________________________#
# i2c BUS Logic
# ____________________________#
def read_i2c_byte(address):
    """
    Method to read byte from i2c-address
    :param address: i2c-address to read byte from
    :return: results stored on address
    """
    # Open i2c bus 1 and read one byte from address, offset 0
    b = s.BUS.read_byte(adress, 0)
    return b


def read_i2c_block(address, number):
    """
    Method to read block from i2c-address
    :param address: i2c-address to read block from
    :param number: number of parameters you want to read
    :return: block of numbers(int) bytes of adress, offset 0
    """
    # Read a block of number(int) bytes of address, offset 0
    # returning a list of number bytes
    block = s.BUS.read_i2c_block_data(address, 0, number)
    return block


def write_i2c_byte(address, data):
    """
    Method to write byte to i2c-adress
    :param address: i2c-address to write byte to
    :param data:  data you want to write
    :return: nothing
    """
    s.BUS.write_byte_data(address, 0, data)


def write_i2c_block(adress, offset, data):
    """
    Method to write block to i2c-adress
    :param adress: i2c-address to write block to
    :param offset: offset you want to consider
    :param data: data you want to wirte
    :return: nothing
    """
    s.BUS.write_i2c_block_data(adress, offset, data)