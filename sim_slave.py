from pymodbus.server.sync import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext

class StatefulDataBlock(ModbusSequentialDataBlock):
    def setValues(self, address, values):
        # We target Register 51 in code to represent "Register 50" (due to +1 offset)
        if address == 51:
            # Check if Register 21 is UNLOCKED (Value 1)
            is_unlocked = self.getValues(21, 1)[0] == 1
            if not is_unlocked:
                print("!!! SUCCESSFUL BLOCK: Write rejected. Register 21 is 0 (Locked) !!!")
                return 
            print("!!! SUCCESSFUL ALLOW: Write accepted. Register 21 is 1 (Unlocked) !!!")
        
        super().setValues(address, values)

def run_stateful_server():
    # Initialize registers 0-100 with zeros
    block = StatefulDataBlock(0, [0]*100)
    store = ModbusSlaveContext(hr=block, ir=block, co=block, di=block)
    context = ModbusServerContext(slaves=store, single=True)
    
    print("--- STATEFUL SIMULATOR STARTING ON PORT 5020 ---")
    StartTcpServer(context=context, address=("127.0.0.1", 5020))

if __name__ == "__main__":
    run_stateful_server()