import psutil
import platform
import subprocess
import logging

def get_system_info():
    """Get basic system information"""
    try:
        info = {
            'cpu': platform.processor() or f"{psutil.cpu_count()} cores",
            'ram_total': f"{psutil.virtual_memory().total // (1024**3)}GB",
            'ram_available': f"{psutil.virtual_memory().available // (1024**3)}GB",
            'os': f"{platform.system()} {platform.release()}",
            'gpu': get_gpu_info()
        }
        return info
    except Exception as e:
        logging.error(f"Error getting system info: {e}")
        return {'error': str(e)}

def get_gpu_info():
    """Get GPU information including VRAM"""
    try:
        # Try nvidia-smi first
        result = subprocess.run(['nvidia-smi', '--query-gpu=name,memory.total', '--format=csv,noheader,nounits'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            gpus = []
            for line in lines:
                if line.strip():
                    name, vram = line.split(', ')
                    gpus.append(f"{name.strip()} ({vram.strip()}MB VRAM)")
            return ', '.join(gpus) if gpus else "NVIDIA GPU (VRAM unknown)"
    except:
        pass
    
    # Fallback: try wmic for basic GPU info
    try:
        result = subprocess.run(['wmic', 'path', 'win32_VideoController', 'get', 'name'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            lines = [line.strip() for line in result.stdout.split('\n') if line.strip() and 'Name' not in line]
            return lines[0] if lines else "GPU detected"
    except:
        pass
    
    return "No GPU info available"

def log_system_info():
    """Log system information at startup"""
    info = get_system_info()
    logging.info("=== SYSTEM INFORMATION ===")
    for key, value in info.items():
        logging.info(f"{key.upper()}: {value}")
    logging.info("========================")
    return info