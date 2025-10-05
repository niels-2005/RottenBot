from opentelemetry import trace, metrics
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
import logging

def setup_observability(service_name: str = "my-app"):
    resource = Resource.create({"service.name": service_name})
    
    # Tracing Setup
    trace_provider = TracerProvider(resource=resource)
    trace_exporter = OTLPSpanExporter(endpoint="http://localhost:4317", insecure=True)
    trace_provider.add_span_processor(BatchSpanProcessor(trace_exporter))
    trace.set_tracer_provider(trace_provider)
    
    # Logging Setup
    logger_provider = LoggerProvider(resource=resource)
    log_exporter = OTLPLogExporter(endpoint="http://localhost:4317", insecure=True)
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))
    set_logger_provider(logger_provider)
    
    # Python logging Handler
    handler = LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(logging.INFO)
    
    # Metrics Setup
    metric_exporter = OTLPMetricExporter(endpoint="http://localhost:4317", insecure=True)
    metric_reader = PeriodicExportingMetricReader(metric_exporter, export_interval_millis=15000)
    meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
    metrics.set_meter_provider(meter_provider)
    
    return trace.get_tracer(__name__), metrics.get_meter(__name__)


def get_tracer(module_name: str):
    return trace.get_tracer(module_name)


def get_meter(module_name: str):
    return metrics.get_meter(module_name)


from otel_setup import setup_tracing_and_logging, get_tracer
import logging
# Initialisiere EINMAL am Start
# # Initialisiere EINMAL am Start
# tracer, meter = setup_observability(service_name="main-app")
# logger = logging.getLogger(__name__)

# def main():
#     with tracer.start_as_current_span("main-workflow") as span:
#         logger.info("Workflow started", extra={
#             "workflow_id": "123",
#             "user_id": "user-456"
#         })
        
#         span.set_attribute("workflow_id", "123")
        
#         try:
#             # Dein Code
#             logger.debug("Processing data...")
#             result = process_data()
#             logger.info("Data processed successfully", extra={"result_count": len(result)})
            
#         except Exception as e:
#             logger.error("Error occurred", exc_info=True, extra={
#                 "error_type": type(e).__name__
#             })
#             span.set_attribute("error", True)
#             raise
        
#         logger.info("Workflow completed") 


# ANDERE MODULE 
# from otel_setup import get_tracer
# tracer = get_tracer(__name__) 
# logger = logging.getLogger(__name__) 


# ----------------------------------------------

# METRICS 

# COUNTER - Zählt Ereignisse (monoton steigend)
# request_counter = meter.create_counter(
#     name="http_requests_total",
#     description="Total number of HTTP requests",
#     unit="1"
# )

# # HISTOGRAM - Misst Verteilungen (z.B. Latenz, Größen)
# request_duration = meter.create_histogram(
#     name="http_request_duration_seconds",
#     description="HTTP request duration in seconds",
#     unit="s"
# )

# # UP/DOWN COUNTER - Kann steigen und fallen (z.B. aktive Connections)
# active_requests = meter.create_up_down_counter(
#     name="http_active_requests",
#     description="Number of active HTTP requests",
#     unit="1"
# )