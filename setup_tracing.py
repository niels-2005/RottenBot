from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource

# Nur EINMAL initialisieren!
def setup_tracing(service_name: str = "my-app"):
    resource = Resource.create({"service.name": service_name})
    
    provider = TracerProvider(resource=resource)
    exporter = OTLPSpanExporter(endpoint="http://localhost:4317", insecure=True)
    provider.add_span_processor(BatchSpanProcessor(exporter))
    
    trace.set_tracer_provider(provider)
    
    return trace.get_tracer(__name__)

# Helper-Funktion für andere Module
def get_tracer(module_name: str):
    return trace.get_tracer(module_name) 


# Hauptprogramm
# Initialisiere Tracing EINMAL am Start
# setup_tracing(service_name="main-app")
# tracer = get_tracer(__name__)

# def main():
#     with tracer.start_as_current_span("main-workflow") as span:
#         span.set_attribute("workflow_id", "123")
#         span.add_event("Workflow started")
        
#         # Ruft Funktion in app_2.py auf
#         # Der Context wird AUTOMATISCH weitergegeben!
#         data = process_data(user_id="user-456")
        
#         # Ruft Funktion in app_3.py auf
#         # Auch hier wird der Context weitergegeben
#         save_to_database(data)
        
#         span.add_event("Workflow completed")

# if __name__ == "__main__":
#     main()


# ANDERE MODULE 
# from otel_setup import get_tracer
# import time

# tracer = get_tracer(__name__)

# def process_data(user_id: str):
#     # Dieser Span wird AUTOMATISCH ein Child des Spans aus app.py!
#     with tracer.start_as_current_span("process_data") as span:
#         span.set_attribute("user_id", user_id)
#         span.add_event("Processing started")
        
#         # Sub-Operation
#         result = fetch_user(user_id)
        
#         time.sleep(0.1)
#         span.add_event("Processing completed")
#         return result
