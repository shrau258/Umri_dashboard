from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Solar SCADA Dashboard"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    # Database
    DATABASE_URL: str = "mssql+pyodbc://sa:YourPassword@localhost:1433/SolarSCADA?driver=ODBC+Driver+17+for+SQL+Server"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Modbus TCP
    MODBUS_HOST: str = "192.168.1.100"
    MODBUS_PORT: int = 502
    MODBUS_UNIT_ID: int = 1
    MODBUS_TIMEOUT: int = 5
    MODBUS_RETRY_COUNT: int = 3
    MODBUS_RETRY_DELAY: int = 2

    # Weather Stations
    WMS1_HOST: str = "192.168.1.101"
    WMS1_PORT: int = 502
    WMS2_HOST: str = "192.168.1.102"
    WMS2_PORT: int = 502

    # Inverter
    INVERTER_COUNT: int = 10
    INVERTER_BASE_ADDRESS: int = 1

    # Data Acquisition
    DATA_ACQUISITION_INTERVAL: int = 5
    WEATHER_ACQUISITION_INTERVAL: int = 30

    # Alarm
    ALARM_CHECK_INTERVAL: int = 10
    ALARM_RETENTION_DAYS: int = 365

    # Report
    REPORT_GENERATION_TIME: str = "00:00"
    REPORT_RETENTION_DAYS: int = 3650

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:3000", "http://127.0.0.1:5173"]

    # WebSocket
    WS_HEARTBEAT_INTERVAL: int = 30
    WS_MAX_CONNECTIONS: int = 1000

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()