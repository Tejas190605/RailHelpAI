"""
RailHelpAI Design Tokens & Theme Specification.
Centralized visual tokens for railway operations UI.
"""

# Color Palette Tokens
PRIMARY = "#C8102E"       # Signal Red
CHARCOAL = "#1E242B"      # Dark Slate Header / Primary Text
SLATE_MUTED = "#5A6672"   # Muted Subtext
BG_LIGHT = "#F8F9FA"      # Background Neutral
SURFACE_LIGHT = "#FFFFFF" # Container Surface
BORDER_LIGHT = "#E1E4E8"  # Subtle Container Borders

# Priority Semantic Colors
PRIORITY_COLORS = {
    "P1": {"bg": "#FEE2E2", "text": "#991B1B", "border": "#FCA5A5", "label": "P1 · CRITICAL"},
    "P2": {"bg": "#FFEDD5", "text": "#C2410C", "border": "#FDBA74", "label": "P2 · HIGH"},
    "P3": {"bg": "#FEF3C7", "text": "#B45309", "border": "#FDE68A", "label": "P3 · MEDIUM"},
    "P4": {"bg": "#E0E7FF", "text": "#3730A3", "border": "#A5B4FC", "label": "P4 · LOW"}
}

# Status Semantic Colors
STATUS_COLORS = {
    "NEW": {"bg": "#F3F4F6", "text": "#374151", "border": "#D1D5DB"},
    "AI_ANALYZED": {"bg": "#E0F2FE", "text": "#0369A1", "border": "#BAE6FD"},
    "PENDING_REVIEW": {"bg": "#FEF3C7", "text": "#B45309", "border": "#FDE68A"},
    "ASSIGNED": {"bg": "#E0E7FF", "text": "#4338CA", "border": "#C7D2FE"},
    "IN_PROGRESS": {"bg": "#DBEAFE", "text": "#1E40AF", "border": "#93C5FD"},
    "WAITING_FOR_INFORMATION": {"bg": "#FCE7F3", "text": "#9D174D", "border": "#FBCFE8"},
    "RESOLVED": {"bg": "#DCFCE7", "text": "#15803D", "border": "#86EFAC"},
    "CLOSED": {"bg": "#F3F4F6", "text": "#4B5563", "border": "#E5E7EB"}
}

# SLA Status Semantic Colors
SLA_COLORS = {
    "WITHIN_SLA": {"bg": "#DCFCE7", "text": "#15803D", "border": "#86EFAC", "label": "WITHIN SLA"},
    "APPROACHING_SLA": {"bg": "#FEF3C7", "text": "#B45309", "border": "#FDE68A", "label": "APPROACHING (50%)"},
    "ESCALATION_WARNING": {"bg": "#FFEDD5", "text": "#C2410C", "border": "#FDBA74", "label": "ESCALATION (90%)"},
    "BREACHED": {"bg": "#FEE2E2", "text": "#991B1B", "border": "#FCA5A5", "label": "BREACHED"}
}
