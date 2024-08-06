import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge
import logging
import random

DATA_MEMORY_SIZE = 1000 #must match with what is declared in data_memory.v
logging.basicConfig(level=logging.DEBUG, filename='../log/data_memory.log', force=True, filemode='w')

logging.info('Start: Data Memory Tests')

def initialize_memory(dut):
    memory_data_model = []
    for element in range(DATA_MEMORY_SIZE):
        data = random.getrandbits(32)
        memory_data_model.append(data)
        dut.data_memory_array[element].value = data
    
    logging.info(f'Memory data model has been generated')
    return memory_data_model

@cocotb.test()
async def reg_file_read_write(dut):
    logging.info('Test Scenario: Do read and write operations work')

    logging.info('Setting up clock')
    cocotb.start_soon(Clock(dut.clk, 1, units='ns').start())

    logging.info('Initializing memory data')
    memory_data_model = initialize_memory(dut)
    await RisingEdge(dut.clk)

    logging.info('Starting checks')

    for cnt in range(random.randint(10,20)):
        dut.enable.value = 1
        dut.read_write.value = random.randint(0,1)
        addr = random.randint(0,DATA_MEMORY_SIZE-1)
        dut.addr.value = addr
        data_write = random.getrandbits(32)
        dut.data_write.value = data_write
        await RisingEdge(dut.clk) #inputs get set
        original_data = dut.data_read.value
        await RisingEdge(dut.clk) #data_read gets set and data_memory gets updated

        logging.debug(cnt)

        if dut.enable.value and not dut.read_write.value:
            logging.debug(f'dut.data_read.value: {dut.data_read.value}')
            logging.debug(f'original_data: {original_data}')
            assert dut.data_read.value == original_data
        
        if dut.enable.value and dut.read_write.value:
            dut.read_write.value = 0
            await RisingEdge(dut.clk)
            logging.debug(f'dut.data_read.value: {dut.data_read.value}')
            logging.debug(f'data_write: {data_write}')
            assert dut.data_read.value == data_write

    logging.info('Test scenario complete')

logging.info('End: Data Memory Tests')