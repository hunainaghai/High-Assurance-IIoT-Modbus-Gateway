from pymodbus.client.sync import ModbusTcpClient
import time

def run_auditor():
    # CONNECT TO GATEWAY (5050)
    client = ModbusTcpClient('127.0.0.1', port=5050)
    client.connect()

    print("--- PHASE 1: TESTING THROUGH GATEWAY ---")
    
    # Try to write to Reg 50 while locked
    print("\n[Step 1] Attempting write to Reg 50 (Locked State)...")
    client.write_register(50, 99)
    res1 = client.read_holding_registers(50, 1)
    print(f"Result (Should be 0): {res1.registers[0]}")

    # Unlock via Reg 20 (Semantic Gap)
    print("\n[Step 2] Sending Unlock command to Reg 20...")
    client.write_register(20, 1)
    time.sleep(1)

    # Try to write again
    print("\n[Step 3] Attempting write to Reg 50 (Unlocked State)...")
    client.write_register(50, 99)
    res2 = client.read_holding_registers(50, 1)
    print(f"Result (Should be 99): {res2.registers[0]}")

    client.close()

if __name__ == "__main__":
    run_auditor()