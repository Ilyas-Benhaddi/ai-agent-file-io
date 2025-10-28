"""
ADK Agent Package
Exposes the file_io_agent for Google ADK
"""
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Import the agent module from root directory
import importlib.util
spec = importlib.util.spec_from_file_location("agent_module", os.path.join(project_root, "adk_agent.py"))
agent_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(agent_module)

# Re-export root_agent for ADK to discover
root_agent = agent_module.root_agent

__all__ = ['root_agent']
