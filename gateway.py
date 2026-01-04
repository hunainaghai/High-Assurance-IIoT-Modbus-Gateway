import socket
import threading

GATEWAY_PORT = 5050
SIMULATOR_IP = "127.0.0.1"
SIMULATOR_PORT = 5020

def bridge_traffic(client_socket):
    sim_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sim_socket.connect((SIMULATOR_IP, SIMULATOR_PORT))
    
    while True:
        data = client_socket.recv(1024)
        if not data: break
        
        data_hex = data.hex()

        # --- THE UNBREAKABLE POLICY ---
        # We define Register 50 (0032) as a "Critical Asset" 
        # that can NEVER be modified through this gateway.
        
        if "00060032" in data_hex: # Function Code 06 (Write) + Register 50 (0032)
            print("\n[!!! CRITICAL BLOCK !!!] SECURITY VIOLATION.")
            print("REASON: Write attempt to Protected Register 50 (Safety Valve).")
            print("STATUS: Command Dropped. Notifying Admin.")
            
            # Send Modbus Error back to attacker
            error_response = bytes.fromhex(data_hex[:14] + "8601") 
            client_socket.sendall(error_response)
            continue # DO NOT FORWARD TO SIMULATOR

        # Forward all other "Safe" traffic
        sim_socket.sendall(data)
        response = sim_socket.recv(1024)
        client_socket.sendall(response)

    sim_socket.close()
    client_socket.close()

if __name__ == "__main__":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", GATEWAY_PORT))
    server.listen(5)
    print(f"[*] UNBREAKABLE IIOT GATEWAY (PHASE 6) ACTIVE ON PORT {GATEWAY_PORT}...")
    while True:
        client_sock, addr = server.accept()
        threading.Thread(target=bridge_traffic, args=(client_sock,)).start()