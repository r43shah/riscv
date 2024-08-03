import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge
import random
import logging

INSTRUCTION_MEMORY_SIZE = 16 #must match with what is declared in instruction_memory.v
logging.basicConfig(level=logging.DEBUG, filename='../log/instruction_memory.log', force=True, filemode='w')

logging.info('Start: Instruction Memory Tests')

def initialize_memory(dut):

    instructions=[] #instructions will be used to compare to dut output
    for element in range(INSTRUCTION_MEMORY_SIZE):
        instruction_byte = random.randint(0, 255) #generate random byte
        instructions.append(bin(instruction_byte)[2:].zfill(8)) #initialize local model
        dut.inst_array[element].value = instruction_byte #initialize dut's intruction memory
    
    logging.info('Printing instruction model')
    logging.info(instructions)
    return instructions
        
@cocotb.test()
async def inst_when_read_enable(dut):

    logging.info('Test Scenario: How does module behave when read is always enabled')
    
    logging.info('Setting up clock')
    cocotb.start_soon(Clock(dut.clk, 1, units = 'ns').start()) #start clock

    instructions = initialize_memory(dut) #initialize memory
    dut.read_enable.value = 1 #enabling read operation

    await RisingEdge(dut.clk) #let the variables get set

    logging.info(f'read_enable is set HIGH: {str(dut.read_enable.value)}')
    instruction_int_list = [str(b) for b in dut.inst_array.value]
    logging.info(f'dut.inst_array: {str(instruction_int_list)}')

    logging.info(f'Starting comparison')
    for cnt in range(int(INSTRUCTION_MEMORY_SIZE/4)):
        logging.debug(f'{cnt}')
        inst_cnt = cnt*4 #to accommodate for byte addressable inst_array
        dut.read_address.value = inst_cnt
        instruction_model = instructions[inst_cnt+3]+instructions[inst_cnt+2]+instructions[inst_cnt+1]+instructions[inst_cnt] #instructions is a list of string
        await RisingEdge(dut.clk)
        logging.debug(f'read_address: {dut.read_address.value}')
        logging.debug(f'dut.instruction.value: {dut.instruction.value}')
        logging.debug(f'instruction_model: {instruction_model}')
        await RisingEdge(dut.clk) #need this to let dut.instruction get assigned the value
        assert dut.instruction.value == instruction_model
    
    dut.read_enable.value = 0
    await RisingEdge(dut.clk)

    logging.info('Completed test scenario')

@cocotb.test()
async def inst_when_read_disable(dut):
    logging.info('Test Scenario: How does module behave when read is disabled')
    
    cocotb.start_soon(Clock(dut.clk, 1, units='ns').start()) #start clock
    
    #initialize instruction memory
    instructions = initialize_memory(dut)

    #set read_enable to LOW
    dut.read_enable.value = 0
    await RisingEdge(dut.clk) #let the read enable get set LOW

    #instruction should always be x
    logging.info('Starting comparison')
    for cnt in range(INSTRUCTION_MEMORY_SIZE//4):
        inst_cnt = cnt*4
        dut.read_address.value = inst_cnt
        await RisingEdge(dut.clk)
        assert dut.instruction.value == 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' or dut.instruction.value == 'zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz'
    
    dut.read_enable.value = 0
    await RisingEdge(dut.clk)
    
    logging.info('Completed test scenario')

@cocotb.test()
async def inst_when_read_enable_toggles(dut):
    logging.info('Test Scenario: How does module behave when we toggle read_enable')

    logging.info('Setting up clock')
    cocotb.start_soon(Clock(dut.clk, 1, units='ns').start()) #start clock

    instructions = initialize_memory(dut) #initialize memory

    dut.read_enable.value = 1
    await RisingEdge(dut.clk)

    dut.read_enable.value = 0 #disabling read operation
    await RisingEdge(dut.clk) #let read enable get disabled
    logging.info(f'dut.read_enable.value: {str(dut.read_enable.value)}')

    for cnt in range((INSTRUCTION_MEMORY_SIZE//4)//2):
        inst_cnt = cnt*4
        dut.read_address.value = inst_cnt
        await RisingEdge(dut.clk) #for setting read_addres
        await RisingEdge(dut.clk) #for setting dut.instruction
        logging.debug(f'dut.instruction_value: {str(dut.instruction.value)}')
        assert dut.instruction.value == 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' or dut.instruction.value == 'zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz'
    
    dut.read_enable.value = 1 #enabling read operation
    await RisingEdge(dut.clk)
    logging.info(f'dut.read_enable.value: {str(dut.read_enable.value)}')

    for cnt in range((INSTRUCTION_MEMORY_SIZE//4)//2):
        inst_cnt = cnt*4 + INSTRUCTION_MEMORY_SIZE//2
        dut.read_address.value = inst_cnt
        await RisingEdge(dut.clk)
        await RisingEdge(dut.clk)
        instruction_model = instructions[inst_cnt+3]+instructions[inst_cnt+2]+instructions[inst_cnt+1]+instructions[inst_cnt]
        assert dut.instruction.value == instruction_model
    
    dut.read_enable.value = 0
    await RisingEdge(dut.clk)

    logging.info('Completed test scenario')