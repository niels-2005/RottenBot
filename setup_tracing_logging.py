from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
import logging

def setup_tracing_and_logging(service_name: str = "my-app"):
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
    
    return trace.get_tracer(__name__)


# Helper-Funktion für andere Module
def get_tracer(module_name: str):
    return trace.get_tracer(module_name) 


from otel_setup import setup_tracing_and_logging, get_tracer
import logging
# Initialisiere EINMAL am Start
# setup_tracing_and_logging(service_name="main-app")
# tracer = get_tracer(__name__)
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