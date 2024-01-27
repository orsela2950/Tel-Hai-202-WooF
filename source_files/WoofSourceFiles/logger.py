import os
import time
from Security.SecurityEvent import SecurityEvent
import uuid


# uuid.uuid4().hex # 32 bit uuidfor logging

class Logger:
    """
    This class serves as a centralized logger for your application, providing functions to write log messages
    to different files ("main", "security", and "debug") with timestamps.

    Attributes:
        log_dir: The directory where all log files are stored.

    Methods:
        __init__(): Initializes the logger by creating the required directory and file handles.
        log_main(request_method, client_host, port, url, target_url): Logs a message to the "main.log" file,
            containing specific information about incoming requests.
        log_security(client_ip, request_host, security_breaks): Logs a message to the "security.log" file,
            highlighting detected security vulnerabilities.
        log_debug(message): Logs a message to the "debug.log" file for general debugging purposes.
        close_debug_log(): Closes the "debug.log" file at the end of the program.
    """

    def __init__(self, debugging: bool):
        """Initializes the Logger object by creating the necessary directory and file handles."""
        # Set the debugging field
        self._debugging = debugging

        current_dir = os.path.dirname(os.path.realpath(__file__))
        self.log_dir = os.path.join(current_dir, "logs")

        # Ensure the logs directory exists
        os.makedirs(self.log_dir, exist_ok=True)

        # Create file handles for main and security logs (closed after each use)
        self.main_log_file = os.path.join(self.log_dir, "main.log")
        self.security_log_file = os.path.join(self.log_dir, "security.log")

        # Keep debug log file open for continuous logging
        self.debug_log_file = open(os.path.join(self.log_dir, "debug.log"), "a")

    def log_main(self, request_method: str, client_host: str, port: int, url: str, target_url: str):
        """
        Logs a message to the "main.log" file, recording information about incoming requests.
        Args:
            request_method: The HTTP request method used (e.g., GET, POST).
            client_host: The IP address of the client making the request.
            port: The port number used for the request.
            url: The requested URL.
            target_url: The targeted URL (domain+path).
        """
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(self.main_log_file, "a") as f:
            f.write(f"{timestamp} - {request_method} - {client_host}:{port} - {url} - {target_url}\n")

    # def log_security(self, client_ip: str, request_host: str, security_breaks: list):
    def log_security(self, event: SecurityEvent):
        """
        Logs a message to the "security.log" file, highlighting detected security vulnerabilities.

        Args:
            client_ip: The IP address of the client potentially causing security concern.
            request_host: The requested hostname involved in the potential security issue.
            security_breaks: A list of identified security vulnerabilities (e.g., XSS, SQL injection).
        """
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        risks = [str(risk.getName()) for risk in event.SecurityRisks]
        host = str(event.request.headers.get("host"))

        # Write to file
        with open(self.security_log_file, "a") as f:
            f.write(f"{timestamp} - {event.ip} - {host} - {', '.join(risks)}\n")

    def log_debug(self, message: str):
        """
        Logs a message to the "debug.log" file for general debugging purposes.

        Args:
            message: The debug message to be logged.
        """
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        self.debug_log_file.write(f"{timestamp} - {message}\n")

    def close_debug_log(self):
        """Closes the "debug.log" file to ensure proper resource management."""
        self.debug_log_file.close()
