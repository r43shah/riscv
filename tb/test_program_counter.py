import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge
import logging
import random

logging.basicConfig(level=logging.DEBUG, filename='../log/program_counter.log', force=True, filemode='w')

logging.info('Start: Program Counter Tests')

@cocotb.test()
async def pc_read(dut):

    logging.info('Test Scenario: How does module behave when clock is on')

    logging.info('Setting up clock')
    cocotb.start_soon(Clock(dut.clk,1,units='ns').start())

    logging.info('Starting check')
    for cnt in range(random.randint(4,15)):
        dut.pc.value = cnt
        await RisingEdge(dut.clk)
        await RisingEdge(dut.clk)
        logging.debug(f'dut.pc.value: {str(dut.pc.value)}')
        logging.debug(f'dut.pc_out.value: {str(dut.pc_out.value)}')
        assert dut.pc_out.value == dut.pc.value + 4
    
    logging.info('Test scenario complete')

logging.info('End: Program Counter Tests')