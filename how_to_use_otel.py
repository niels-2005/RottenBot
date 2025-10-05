from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
import time

# OTLP gRPC
exporter = OTLPSpanExporter(endpoint="http://localhost:4317", insecure=True)

provider = TracerProvider()
provider.add_span_processor(BatchSpanProcessor(exporter))
trace.set_tracer_provider(provider)

tracer = trace.get_tracer(__name__)

# Beispiel 1: Nested Spans (Parent-Child Hierarchie)
with tracer.start_as_current_span("parent-operation") as parent_span:
    # Parent Span Code
    parent_span.set_attribute("user_id", "123")
    parent_span.add_event("Parent operation started")
    
    time.sleep(0.1)
    
    # Child Span 1
    with tracer.start_as_current_span("child-operation-1") as child1:
        child1.set_attribute("step", "1")
        time.sleep(0.05)
        # Dein Code hier
    
    # Child Span 2
    with tracer.start_as_current_span("child-operation-2") as child2:
        child2.set_attribute("step", "2")
        time.sleep(0.05)
        
        # Nested Child (Enkelkind)
        with tracer.start_as_current_span("nested-operation"):
            time.sleep(0.02)
    
    parent_span.add_event("Parent operation completed")




# ----------------------------------------------------------------------------




# Beispiel 2: Sequentielle Spans auf gleicher Ebene
with tracer.start_as_current_span("main-workflow") as main:
    main.set_attribute("workflow_id", "workflow-123")
    
    with tracer.start_as_current_span("step-1-fetch-data"):
        # Daten holen
        time.sleep(0.1)
    
    with tracer.start_as_current_span("step-2-process-data"):
        # Verarbeiten
        time.sleep(0.2)
    
    with tracer.start_as_current_span("step-3-save-data"):
        # Speichern
        time.sleep(0.1)





# ----------------------------------------------------------------------------





# Beispiel 3: Mit Funktionen
def fetch_user(user_id: str):
    with tracer.start_as_current_span("fetch_user") as span:
        span.set_attribute("user_id", user_id)
        time.sleep(0.05)
        return {"id": user_id, "name": "Test User"}

def process_user(user_data: dict):
    with tracer.start_as_current_span("process_user") as span:
        span.set_attribute("user_name", user_data["name"])
        time.sleep(0.1)
        return user_data

def save_user(user_data: dict):
    with tracer.start_as_current_span("save_user") as span:
        span.set_attribute("db", "postgres")
        time.sleep(0.08)

# Hauptworkflow mit mehreren Funktionen
with tracer.start_as_current_span("user-registration-flow"):
    user = fetch_user("user-456")
    processed = process_user(user)
    save_user(processed)





# ----------------------------------------------------------------------------





# Beispiel 4: Mit Error Handling
with tracer.start_as_current_span("operation-with-error-handling") as span:
    try:
        with tracer.start_as_current_span("risky-operation"):
            # Simuliere einen Fehler
            raise ValueError("Something went wrong")
    except ValueError as e:
        span.set_attribute("error", True)
        span.set_attribute("error.message", str(e))
        span.add_event("Error occurred", {"error.type": type(e).__name__})
        # Error wird im Trace sichtbar sein





# ----------------------------------------------------------------------------





# Beispiel 5: Manuelle Span-Erstellung (ohne Context Manager)
span = tracer.start_span("manual-span")
span.set_attribute("manual", True)
try:
    time.sleep(0.05)
finally:
    span.end()