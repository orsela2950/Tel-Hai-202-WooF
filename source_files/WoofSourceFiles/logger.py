from os.path import join, abspath, dirname
from os import makedirs
import time
from Security.SecurityEvent import SecurityEvent
import toml


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

        self.log_dir = join(abspath(dirname(__file__)), '..', 'logs')

        # Ensure the logs directory exists
        makedirs(self.log_dir, exist_ok=True)

        # Create file handles for main and security logs (closed after each use)
        self.main_log_file = join(self.log_dir, "main.toml")
        self.security_log_file = join(self.log_dir, "security.toml")

        # Keep debug log file open for continuous logging
        self.debug_log_file = open(join(self.log_dir, "debug.toml"), "a")

    def log_main_toml(self, request_method: str, client_host: str, port: int, url: str, target_url: str):
        """
        Logs a message to the "main.log" file in TOML format, recording information about incoming requests.

        Args:
            request_method: The HTTP request method used (e.g., GET, POST).
            client_host: The IP address of the client making the request.
            port: The port number used for the request.
            url: The requested URL.
            target_url: The targeted URL (domain+path).
        """
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            "timestamp": timestamp,
            "request_method": request_method,
            "client_host": f"{client_host}:{port}",
            "url": url,
            "target_url": target_url
        }

        # Append the log entry within the [[logs]] section
        with open(self.main_log_file, "a") as f:
            f.write(toml.dumps({"logs": [log_entry]}) + '\n')

    def log_security_toml(self, event: SecurityEvent):
        """
        Logs a message to the "security.log" file in TOML format, highlighting detected security vulnerabilities.

        Args:
            event: An instance of SecurityEvent containing security-related information.
        """
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        risks = [str(risk.get_name()) for risk in event.SecurityRisks]
        host = str(event.request.headers.get("host"))
        log_entry = {
            "timestamp": timestamp,
            "client_ip": event.ip,
            "host": host,
            "risks": risks
        }

        # Append the log entry within the [[logs]] section
        with open(self.security_log_file, "a") as f:
            f.write(toml.dumps({"logs": [log_entry]}) + '\n')

    def log_debug_toml(self, message: str):
        """
        Logs a message to the "debug.log" file in TOML format for general debugging purposes.

        Args:
            message: The debug message to be logged.
        """
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            "timestamp": timestamp,
            "message": message
        }

        with open(self.debug_log_file.name, "a") as f:
            f.write(toml.dumps({"logs": [log_entry]}) + '\n')

    def close_debug_log(self):
        """Closes the "debug.log" file to ensure proper resource management."""
        self.debug_log_file.close()
