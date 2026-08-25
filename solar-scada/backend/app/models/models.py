from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100))
    role = Column(String(20), default="operator")  # admin, engineer, operator, viewer
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    alarms_acknowledged = relationship("Alarm", back_populates="acknowledged_by_user")


class Plant(Base):
    __tablename__ = "plants"

    id = Column(Integer, primary_key=True, index=True)
    plant_code = Column(String(20), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    capacity_mw = Column(Float, nullable=False)
    location = Column(String(200))
    latitude = Column(Float)
    longitude = Column(Float)
    commissioning_date = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    inverters = relationship("Inverter", back_populates="plant")
    weather_stations = relationship("WeatherStation", back_populates="plant")
    energy_meters = relationship("EnergyMeter", back_populates="plant")
    transformers = relationship("Transformer", back_populates="plant")
    alarms = relationship("Alarm", back_populates="plant")
    generation_data = relationship("GenerationData", back_populates="plant")
    weather_data = relationship("WeatherData", back_populates="plant")


class Inverter(Base):
    __tablename__ = "inverters"

    id = Column(Integer, primary_key=True, index=True)
    plant_id = Column(Integer, ForeignKey("plants.id"), nullable=False)
    inverter_code = Column(String(20), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    manufacturer = Column(String(50))
    model = Column(String(50))
    rated_power_kw = Column(Float)
    modbus_address = Column(Integer, unique=True, nullable=False)
    connection_type = Column(String(20), default="modbus_tcp")  # modbus_tcp, modbus_rtu
    ip_address = Column(String(45))
    port = Column(Integer, default=502)
    unit_id = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    plant = relationship("Plant", back_populates="inverters")
    inverter_data = relationship("InverterData", back_populates="inverter")
    alarms = relationship("Alarm", back_populates="inverter")


class WeatherStation(Base):
    __tablename__ = "weather_stations"

    id = Column(Integer, primary_key=True, index=True)
    plant_id = Column(Integer, ForeignKey("plants.id"), nullable=False)
    station_code = Column(String(20), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    station_type = Column(String(20), default="WMS")  # WMS-1, WMS-2
    manufacturer = Column(String(50))
    model = Column(String(50))
    modbus_address = Column(Integer, unique=True, nullable=False)
    ip_address = Column(String(45))
    port = Column(Integer, default=502)
    unit_id = Column(Integer, default=1)
    latitude = Column(Float)
    longitude = Column(Float)
    elevation = Column(Float)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    plant = relationship("Plant", back_populates="weather_stations")
    weather_data = relationship("WeatherData", back_populates="weather_station")


class EnergyMeter(Base):
    __tablename__ = "energy_meters"

    id = Column(Integer, primary_key=True, index=True)
    plant_id = Column(Integer, ForeignKey("plants.id"), nullable=False)
    meter_code = Column(String(20), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    meter_type = Column(String(20), default="export")  # export, import, station_use
    manufacturer = Column(String(50))
    model = Column(String(50))
    modbus_address = Column(Integer, unique=True, nullable=False)
    ip_address = Column(String(45))
    port = Column(Integer, default=502)
    unit_id = Column(Integer, default=1)
    ct_ratio = Column(Float, default=1.0)
    pt_ratio = Column(Float, default=1.0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    plant = relationship("Plant", back_populates="energy_meters")
    meter_data = relationship("EnergyMeterData", back_populates="energy_meter")


class Transformer(Base):
    __tablename__ = "transformers"

    id = Column(Integer, primary_key=True, index=True)
    plant_id = Column(Integer, ForeignKey("plants.id"), nullable=False)
    transformer_code = Column(String(20), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    manufacturer = Column(String(50))
    model = Column(String(50))
    rated_power_kva = Column(Float)
    primary_voltage = Column(Float)
    secondary_voltage = Column(Float)
    modbus_address = Column(Integer, unique=True, nullable=False)
    ip_address = Column(String(45))
    port = Column(Integer, default=502)
    unit_id = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    plant = relationship("Plant", back_populates="transformers")
    transformer_data = relationship("TransformerData", back_populates="transformer")


class InverterData(Base):
    __tablename__ = "inverter_data"

    id = Column(Integer, primary_key=True, index=True)
    inverter_id = Column(Integer, ForeignKey("inverters.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # AC Side
    active_power_kw = Column(Float, default=0)
    reactive_power_kvar = Column(Float, default=0)
    apparent_power_kva = Column(Float, default=0)
    power_factor = Column(Float, default=1.0)
    frequency_hz = Column(Float, default=50.0)

    # Phase Voltages (R, Y, B)
    voltage_r_v = Column(Float, default=0)
    voltage_y_v = Column(Float, default=0)
    voltage_b_v = Column(Float, default=0)

    # Phase Currents (R, Y, B)
    current_r_a = Column(Float, default=0)
    current_y_a = Column(Float, default=0)
    current_b_a = Column(Float, default=0)

    # DC Side
    dc_power_kw = Column(Float, default=0)
    dc_voltage_v = Column(Float, default=0)
    dc_current_a = Column(Float, default=0)

    # Energy
    today_generation_kwh = Column(Float, default=0)
    total_generation_kwh = Column(Float, default=0)

    # Efficiency & Temperature
    efficiency_pct = Column(Float, default=0)
    temperature_c = Column(Float, default=0)

    # Status
    running_status = Column(String(20), default="stopped")  # running, stopped, fault, standby
    fault_code = Column(String(50), nullable=True)
    communication_status = Column(String(20), default="offline")  # online, offline, timeout

    # Calculated
    co2_saved_kg = Column(Float, default=0)

    # Relationships
    inverter = relationship("Inverter", back_populates="inverter_data")

    __table_args__ = (
        Index('ix_inverter_data_inverter_timestamp', 'inverter_id', 'timestamp'),
    )


class WeatherData(Base):
    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True, index=True)
    plant_id = Column(Integer, ForeignKey("plants.id"), nullable=False)
    weather_station_id = Column(Integer, ForeignKey("weather_stations.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Irradiance
    ghi_wm2 = Column(Float, default=0)  # Global Horizontal Irradiance
    gti_wm2 = Column(Float, default=0)  # Global Tilted Irradiance
    poa_wm2 = Column(Float, default=0)  # Plane of Array Irradiance

    # Temperature
    ambient_temp_c = Column(Float, default=0)
    module_temp_c = Column(Float, default=0)

    # Wind
    wind_speed_ms = Column(Float, default=0)
    wind_direction_deg = Column(Float, default=0)

    # Other
    humidity_pct = Column(Float, default=0)
    rain_status = Column(Boolean, default=False)
    pressure_hpa = Column(Float, default=1013.25)
    uv_index = Column(Float, default=0)
    solar_elevation_deg = Column(Float, default=0)

    # Status
    communication_status = Column(String(20), default="offline")

    # Relationships
    plant = relationship("Plant", back_populates="weather_data")
    weather_station = relationship("WeatherStation", back_populates="weather_data")

    __table_args__ = (
        Index('ix_weather_data_plant_timestamp', 'plant_id', 'timestamp'),
        Index('ix_weather_data_station_timestamp', 'weather_station_id', 'timestamp'),
    )


class EnergyMeterData(Base):
    __tablename__ = "energy_meter_data"

    id = Column(Integer, primary_key=True, index=True)
    energy_meter_id = Column(Integer, ForeignKey("energy_meters.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Energy
    active_energy_kwh = Column(Float, default=0)
    reactive_energy_kvarh = Column(Float, default=0)
    apparent_energy_kvah = Column(Float, default=0)

    # Power
    active_power_kw = Column(Float, default=0)
    reactive_power_kvar = Column(Float, default=0)
    apparent_power_kva = Column(Float, default=0)

    # Voltage & Current
    voltage_r_v = Column(Float, default=0)
    voltage_y_v = Column(Float, default=0)
    voltage_b_v = Column(Float, default=0)
    current_r_a = Column(Float, default=0)
    current_y_a = Column(Float, default=0)
    current_b_a = Column(Float, default=0)

    # Power Factor & Frequency
    power_factor = Column(Float, default=1.0)
    frequency_hz = Column(Float, default=50.0)

    # Status
    communication_status = Column(String(20), default="offline")

    # Relationships
    energy_meter = relationship("EnergyMeter", back_populates="meter_data")

    __table_args__ = (
        Index('ix_meter_data_meter_timestamp', 'energy_meter_id', 'timestamp'),
    )


class TransformerData(Base):
    __tablename__ = "transformer_data"

    id = Column(Integer, primary_key=True, index=True)
    transformer_id = Column(Integer, ForeignKey("transformers.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Primary Side
    primary_voltage_r_v = Column(Float, default=0)
    primary_voltage_y_v = Column(Float, default=0)
    primary_voltage_b_v = Column(Float, default=0)
    primary_current_r_a = Column(Float, default=0)
    primary_current_y_a = Column(Float, default=0)
    primary_current_b_a = Column(Float, default=0)

    # Secondary Side
    secondary_voltage_r_v = Column(Float, default=0)
    secondary_voltage_y_v = Column(Float, default=0)
    secondary_voltage_b_v = Column(Float, default=0)
    secondary_current_r_a = Column(Float, default=0)
    secondary_current_y_a = Column(Float, default=0)
    secondary_current_b_a = Column(Float, default=0)

    # Power
    active_power_kw = Column(Float, default=0)
    reactive_power_kvar = Column(Float, default=0)
    apparent_power_kva = Column(Float, default=0)

    # Temperature
    winding_temp_c = Column(Float, default=0)
    oil_temp_c = Column(Float, default=0)

    # Status
    tap_position = Column(Integer, default=0)
    communication_status = Column(String(20), default="offline")

    # Relationships
    transformer = relationship("Transformer", back_populates="transformer_data")

    __table_args__ = (
        Index('ix_transformer_data_transformer_timestamp', 'transformer_id', 'timestamp'),
    )


class GenerationData(Base):
    __tablename__ = "generation_data"

    id = Column(Integer, primary_key=True, index=True)
    plant_id = Column(Integer, ForeignKey("plants.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Generation
    current_generation_mw = Column(Float, default=0)
    today_generation_mwh = Column(Float, default=0)
    monthly_generation_mwh = Column(Float, default=0)
    total_generation_mwh = Column(Float, default=0)

    # Performance
    pr_pct = Column(Float, default=0)  # Performance Ratio
    cuf_pct = Column(Float, default=0)  # Capacity Utilization Factor
    plant_availability_pct = Column(Float, default=0)
    grid_availability_pct = Column(Float, default=0)

    # Revenue & Environment
    revenue_usd = Column(Float, default=0)
    co2_saved_tonnes = Column(Float, default=0)

    # Relationships
    plant = relationship("Plant", back_populates="generation_data")

    __table_args__ = (
        Index('ix_generation_data_plant_timestamp', 'plant_id', 'timestamp'),
    )


class Alarm(Base):
    __tablename__ = "alarms"

    id = Column(Integer, primary_key=True, index=True)
    plant_id = Column(Integer, ForeignKey("plants.id"), nullable=True)
    inverter_id = Column(Integer, ForeignKey("inverters.id"), nullable=True)
    alarm_code = Column(String(50), index=True, nullable=False)
    alarm_name = Column(String(200), nullable=False)
    alarm_type = Column(String(20), default="fault")  # fault, warning, info
    severity = Column(String(20), default="medium")  # critical, high, medium, low
    message = Column(Text, nullable=True)
    source = Column(String(50), nullable=True)  # inverter, weather_station, meter, transformer, grid
    value = Column(Float, nullable=True)
    threshold = Column(Float, nullable=True)
    unit = Column(String(20), nullable=True)

    # Status
    is_active = Column(Boolean, default=True)
    is_acknowledged = Column(Boolean, default=False)
    acknowledged_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    acknowledged_at = Column(DateTime, nullable=True)

    # Timestamps
    occurred_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    cleared_at = Column(DateTime, nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    plant = relationship("Plant", back_populates="alarms")
    inverter = relationship("Inverter", back_populates="alarms")
    acknowledged_by_user = relationship("User", back_populates="alarms_acknowledged")

    __table_args__ = (
        Index('ix_alarm_plant_occurred', 'plant_id', 'occurred_at'),
        Index('ix_alarm_inverter_occurred', 'inverter_id', 'occurred_at'),
        Index('ix_alarm_active', 'is_active'),
    )


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    plant_id = Column(Integer, ForeignKey("plants.id"), nullable=True)
    report_type = Column(String(20), nullable=False)  # daily, monthly, yearly, custom
    report_name = Column(String(200), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_format = Column(String(10), nullable=False)  # pdf, excel
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    generated_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    file_size_bytes = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    plant = relationship("Plant")