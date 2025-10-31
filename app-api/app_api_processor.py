# a local shim to reuse processor functions; copy/paste processor contents or import from wheel
from ..app_api_processor_missing import processor  # fallback when packaging

# If you prefer, copy the functions needed here (normalize_event) to avoid import issues in Function runtime.
