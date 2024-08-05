import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge
import logging
import random

logging.basicConfig(level=logging.DEBUG, filename='../log/register_file.log', force=True, filemode='w')

logging.info('Start: Register File Tests')

def initialize_reg_file(dut):

    reg_file_model = [] #this will be the model to compare real values against
    for cnt in range(32): #reg_file is 32 registers long
        data = random.getrandbits(32)
        reg_file_model.append(data)
        dut.reg_file[cnt].value = data
    
    logging.info(f'register_file_model: {reg_file_model}')
    return reg_file_model

@cocotb.test()
async def reg_file_read(dut):
    logging.info('Test Scenario: Does read operation work?')

    logging.info('Setting up clock')
    cocotb.start_soon(Clock(dut.clk, 1, units='ns').start())

    reg_file_model = initialize_reg_file(dut) #initialize register file
    await RisingEdge(dut.clk)

    logging.info('Starting checks')
    for cnt in range(32//2): #we can read two registers at the same time
        model_data1 = reg_file_model[cnt] #get POR value
        model_data2 = reg_file_model[cnt+16]
        dut.read_reg1.value = cnt
        dut.read_reg2.value = cnt+16
        dut.read_write.value = random.randint(0,1) #this signal should not affect read operations
        await RisingEdge(dut.clk) #let values set
        assert dut.read_data1 == model_data1
        assert dut.read_data2 == model_data2
    
    logging.info('Completed test scenario')

@cocotb.test()
async def reg_file_write(dut):
    logging.info('Test Scenario: Do write operations work?')

    logging.info('Setting up clock')
    cocotb.start_soon(Clock(dut.clk, 1, units='ns').start())

    logging.info('Starting checks')
    for cnt in range(32): #we will test writing 32 times
        dut.read_write.value = random.randint(0,1) #randomly set write_enable
        write_reg = random.randint(0,31) #get a random register to write to
        dut.write_reg.value = write_reg
        dut.read_reg1.value = write_reg #we want to read after write to verify success
        write_data = random.getrandbits(32)
        dut.write_data.value = write_data
        await RisingEdge(dut.clk) #set the signals
        original_data = dut.read_data1.value
        await RisingEdge(dut.clk) #write operation occurs here (I think)
        if dut.read_write.value == 1:
            assert dut.read_data1.value == write_data
        else:
            assert dut.read_data1.value == original_data
        

    logging.info('Test scenario complete')

logging.info('End: Register File Tests')
