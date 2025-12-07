import pytest
from fastapi import FastAPI
from unittest.mock import AsyncMock
from arcreactor.core.managers.plugin_manager import PluginManager
from arcreactor.core.interfaces.plugin import PluginTiming


@pytest.mark.asyncio
async def test_router_plugins_load():
    # Setup App Context
    app = FastAPI()
    app.state.subprocess_launcher = AsyncMock()
    app.state.subprocess_launcher.run.return_value = (0, "On branch main", "")
    
    # Initialize PluginManager
    plugin_manager = PluginManager(plugin_dir="src/arcreactor/plugins", config_path="test-config.toml", context=app)
    app.state.plugin_manager = plugin_manager
    
    # Load Default Plugins (GitControl is default)
    await plugin_manager.load_plugins(PluginTiming.DEFAULT)
    
    # Verify GitControl loaded
    plugin = plugin_manager.get_plugin("router-git")
    assert plugin is not None
    assert type(plugin).__name__ == "GitControlPlugin"
    
    # Verify Router
    router = plugin.get_router()
    assert router is not None
    
    # Verify Routes
    routes = [r.path for r in router.routes]
    assert "/git/status" in routes
