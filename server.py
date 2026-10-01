from fastmcp import FastMCP
import socket
import json

mcp = FastMCP("Blender")

BLENDER_HOST = "127.0.0.1"
BLENDER_PORT = 9876

def send_to_blender(payload, timeout=10):
    """Envía comandos a Blender a través de un socket TCP con timeout ampliado."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((BLENDER_HOST, BLENDER_PORT))
            s.sendall(json.dumps(payload).encode('utf-8'))
            
            chunks = []
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                chunks.append(chunk)
            
            data = b"".join(chunks)
            return json.loads(data.decode('utf-8'))
    except Exception as e:
        return {"status": "error", "message": f"Error de conexión con Blender: {str(e)}"}

@mcp.tool()
def ejecutar_script_blender(python_code: str) -> str:
    """Ejecuta código Python en Blender de forma segura en el hilo principal."""
    res = send_to_blender({"action": "execute", "code": python_code})
    return json.dumps(res, indent=2, ensure_ascii=False)

@mcp.tool()
def obtener_info_escena() -> str:
    """Obtiene información básica de la escena actual de Blender."""
    res = send_to_blender({"action": "get_info"})
    return json.dumps(res, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    mcp.run()