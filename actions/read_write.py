from xarm.wrapper import XArmAPI

class read_write_control():

    def __init__(self, arm:XArmAPI):
        self.arm = arm

    def read_coil_bits(self, addr, quantity):
        """
        ([Standard Modbus TCP](../UF_ModbusTCP_Manual.md)) Read Coils (0x01)

        Args:
            addr: the starting address of the register to be read

            quantity: number of registers
        
        Returns:
            out: tuple((code, bits)) returned result is only corrent when code is 0.
            
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.

                Note: code 129~144 means modbus tcp exception, the actual modbus tcp exception code is (code-0x80), refer to [Standard Modbus TCP](../UF_ModbusTCP_Manual.md)
        """
        return self.arm.read_coil_bits(addr, quantity)

    def read_input_bits(self, addr, quantity):
        """
        ([Standard Modbus TCP](../UF_ModbusTCP_Manual.md)) Read Discrete Inputs (0x02)

        Args:
            addr: the starting address of the register to be read

            quantity: number of registers

        Returns:
            out: tuple((code, bits)) returned result is only corrent when code is 0.

            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.

                Note: code 129~144 means modbus tcp exception, the actual modbus tcp exception code is (code-0x80), refer to [Standard Modbus TCP](../UF_ModbusTCP_Manual.md)
        """
        return self.arm.read_input_bits(addr, quantity)
    
    def read_holding_registers(self, addr, quantity, is_signed=False):
        """
        ([Standard Modbus TCP](../UF_ModbusTCP_Manual.md)) Read Holding Registers (0x03)

        Args:
            addr: the starting address of the register to be read

            quantity: number of registers
        
            is_signed: whether to convert the read register value into a signed form

        Returns:
            out: tuple((code, bits)) returned result is only corrent when code is 0.

            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.

                Note: code 129~144 means modbus tcp exception, the actual modbus tcp exception code is (code-0x80), refer to [Standard Modbus TCP](../UF_ModbusTCP_Manual.md)
        """
        return self.arm.read_holding_registers(addr, quantity, is_signed)
    
    def read_input_registers(self, addr, quantity, is_signed=False):
        """
        ([Standard Modbus TCP](../UF_ModbusTCP_Manual.md)) Read Input Registers (0x04)

        Args:
            addr: the starting address of the register to be read
        
            quantity: number of registers
        
            is_signed: whether to convert the read register value into a signed form

        Returns:
            out: tuple((code, bits)) returned result is only corrent when code is 0.

            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.

                Note: code 129~144 means modbus tcp exception, the actual modbus tcp exception code is (code-0x80), refer to [Standard Modbus TCP](../UF_ModbusTCP_Manual.md)
        """
        return self.arm.read_input_registers(addr, quantity, is_signed)
    
    def write_single_coil_bit(self, addr, bit_val):
        """
        ([Standard Modbus TCP](../UF_ModbusTCP_Manual.md)) Write Single Coil (0x05)

        Args:
            addr: register address
        
            bit_val: the value to write (0/1)

        Returns:
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.

                Note: code 129~144 means modbus tcp exception, the actual modbus tcp exception code is (code-0x80), refer to [Standard Modbus TCP](../UF_ModbusTCP_Manual.md)
        """
        return self.arm.write_single_coil_bit(addr, bit_val)
    
    def write_single_holding_register(self, addr, reg_val):
        """
        ([Standard Modbus TCP](../UF_ModbusTCP_Manual.md)) Write Single Holding Register (0x06)

        Args:
            addr: register address
        
            bit_val: the value to write

        Returns:
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.

                Note: code 129~144 means modbus tcp exception, the actual modbus tcp exception code is (code-0x80), refer to [Standard Modbus TCP](../UF_ModbusTCP_Manual.md)
        """
        return self.arm.write_single_holding_register(addr, reg_val)

    def write_multiple_coil_bits(self, addr, bits):
        """
        ([Standard Modbus TCP](../UF_ModbusTCP_Manual.md)) Write Multiple Coils (0x0F)

        Args:
            addr: the starting address of the register to be written
        
            bits: array of values to write

        Returns:
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.

                Note: code 129~144 means modbus tcp exception, the actual modbus tcp exception code is (code-0x80), refer to [Standard Modbus TCP](../UF_ModbusTCP_Manual.md)
        """
        return self.arm.write_multiple_coil_bits(addr, bits)

    def write_multiple_holding_registers(self, addr, regs):
        """
        ([Standard Modbus TCP](../UF_ModbusTCP_Manual.md)) Write Multiple Holding Registers (0x10)

        Args:
            addr: the starting address of the register to be written
        
            regs: array of values to write

        Returns:
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.

                Note: code 129~144 means modbus tcp exception, the actual modbus tcp exception code is (code-0x80), refer to [Standard Modbus TCP](../UF_ModbusTCP_Manual.md)
        """
        return self.arm.write_multiple_holding_registers(addr, regs)
    
    def mask_write_holding_register(self, addr, and_mask, or_mask):
        """
        ([Standard Modbus TCP](../UF_ModbusTCP_Manual.md)) Mask Write Holding Register (0x16)

        Args:
            addr: register address
        
            and_mask: mask to be AND with
        
            or_mask: mask to be OR with

        Returns:
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.

                Note: code 129~144 means modbus tcp exception, the actual modbus tcp exception code is (code-0x80), refer to [Standard Modbus TCP](../UF_ModbusTCP_Manual.md)
        """
        return self.arm.mask_write_holding_register(addr, and_mask, or_mask)

    def write_and_read_holding_registers(self, r_addr, r_quantity, w_addr, w_regs, is_signed=False):
        """
        ([Standard Modbus TCP](../UF_ModbusTCP_Manual.md)) Write and Read Holding Registers (0x17)

        Args:
            r_addr: the starting address of the register to be read
        
            r_quantity: number of registers to read
        
            w_addr: the starting address of the register to be written
        
            w_regs: array of values to write
        
            is_signed: whether to convert the read register value into a signed form

        Returns:
            out: tuple((code, regs)) returned result is only corrent when code is 0.
            
            code: See the [API Code Documentation](./xarm_api_code.md#api-code) for details.

                Note: code 129~144 means modbus tcp exception, the actual modbus tcp exception code is (code-0x80), refer to [Standard Modbus TCP](../UF_ModbusTCP_Manual.md)
        """
        return self.arm.write_and_read_holding_registers(r_addr, r_quantity, w_addr, w_regs, is_signed)