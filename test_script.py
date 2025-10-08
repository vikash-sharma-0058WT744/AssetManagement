#!/usr/bin/env python3
"""
Test script for webMethods.io Integration Asset Puller
"""

import json
import os
import sys

# Import the script as a module
sys.path.append('.')
import webmethods_asset_puller

def test_with_mock_data():
    """
    Test the script functions with mock data
    """
    print("Testing with mock data...")
    
    # Create mock assets data
    mock_assets = {
        "workflows": [
            "fl9ab13f7e0aabe9bc714b5b",
            "fl6fd2d8f7d9630a78d80d8a"
        ],
        "flows": [
            "StellantisSubscriber",
            "flow_2",
            "OrchestrationFlow"
        ],
        "listener": [
            {
                "providerName": "WmSAP",
                "adapterID": "com.wm.adapter.sap.SAPAdapter",
                "listenerListData": [
                    {
                        "listenerData": {
                            "listenerName": "routingListener",
                            "listenerTemplate": "com.wm.adapter.sap.listener.RoutingListener",
                            "description": None,
                            "status": "enabled",
                            "lastError": None,
                            "listenerRuntimeState": "ACTIVE",
                            "state": "enabled"
                        }
                    }
                ]
            }
        ],
        "messaging": [
            "ListenMessageForPurchaseOrderProcess",
            "StellantisJMS"
        ]
    }
    
    # Test saving flow info
    webmethods_asset_puller.save_flow_info(mock_assets.get("flows", []))
    
    # Test saving listener info
    webmethods_asset_puller.save_listener_info(mock_assets.get("listener", []))
    
    # Test saving messaging info
    webmethods_asset_puller.save_messaging_info(mock_assets.get("messaging", []))
    
    print("Mock data tests completed. Check the github_repo directory for output files.")

if __name__ == "__main__":
    # Make sure the github_repo directories exist
    os.makedirs("./github_repo/workflows", exist_ok=True)
    os.makedirs("./github_repo/flows", exist_ok=True)
    os.makedirs("./github_repo/listeners", exist_ok=True)
    os.makedirs("./github_repo/messaging", exist_ok=True)
    
    test_with_mock_data()

# Made with Bob
