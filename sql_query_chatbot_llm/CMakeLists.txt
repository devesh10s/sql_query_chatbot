cmake_minimum_required(VERSION 3.16)
project(vajra)

set(CMAKE_CXX_STANDARD 17)

add_subdirectory(${PROJECT_SOURCE_DIR}/common)
add_subdirectory(${PROJECT_SOURCE_DIR}/3rdparty/jwtpp)
add_subdirectory(${PROJECT_SOURCE_DIR}/3rdparty/SQLiteCpp)

add_executable(event_processor event_processor/main.cpp event_processor/EventProcessor.cpp event_processor/EventProcessor.h)
target_link_libraries(event_processor -lpthread)
target_link_libraries(event_processor vajraServerSdk)

add_executable(rule_engine rule_engine/main.cpp rule_engine/RuleEngine.cpp rule_engine/RuleEngine.h rule_engine/PluginLoader.cpp rule_engine/PluginLoader.h)
target_link_libraries(rule_engine -ldl)
target_link_libraries(rule_engine vajraServerSdk)
target_link_libraries(rule_engine -lpthread)

add_executable(rule_builder rule_builder/main.cpp rule_builder/rule_builder.cpp rule_builder/rule_builder.h)
target_link_libraries(rule_builder -ldl)
target_link_libraries(rule_builder vajraServerSdk)
target_link_libraries(rule_builder -lpthread)
target_link_libraries(rule_builder -lpqxx)


add_executable(cpe_string_maker cpe_string_maker/main.cpp cpe_string_maker/cpe.cpp cpe_string_maker/cpe.h)
target_link_libraries(cpe_string_maker -lcurl)
target_link_libraries(cpe_string_maker vajraServerSdk)
target_link_libraries(cpe_string_maker -lpthread)
target_link_libraries(cpe_string_maker sqlite3)
add_subdirectory(3rdparty/RapidFuzz)
target_link_libraries(cpe_string_maker rapidfuzz::rapidfuzz)

add_executable(nvd_data nvd_data/nvd_data.cpp)
target_link_libraries(nvd_data -lcurl)
target_link_libraries(nvd_data vajraServerSdk)
target_link_libraries(nvd_data -lpthread)
target_link_libraries(nvd_data sqlite3)

add_executable(va va/main.cpp va/cpe_to_cve.cpp va/cpe_to_cve.h)
target_link_libraries(va -lcurl)
target_link_libraries(va vajraServerSdk)
target_link_libraries(va -lpthread)
target_link_libraries(va sqlite3)

# Find the CURL package (CMake will find it if it's installed)
find_package(CURL REQUIRED)

# Add the executable for your project
add_executable(sql_chatbot sql_chatbot/chatbot.cpp)

# Link the libraries
target_link_libraries(sql_chatbot PRIVATE
    ${CURL_LIBRARIES}      # Link CURL
    vajraServerSdk         # Link your custom vajraServerSdk library
    pthread                # Link pthread for threading support
)

add_executable(vajra_api server/api_server.cpp server/WebServer.cpp server/api/nodes.cpp server/api/nodes.h server/api/events.cpp server/api/events.h server/api/config.cpp server/api/config.h server/api/stats.cpp server/api/stats.h server/RequestRouter.cpp server/RequestRouter.h server/http_common.cpp server/http_common.h server/api/scheduled_query.h server/api/scheduled_query.cpp server/api/dashboard.cpp server/api/dashboard.h server/api/python_rule.cpp server/api/python_rule.h server/api/rule_builder.cpp server/api/rule_builder.h server/api/settings.cpp server/api/settings.h)
target_link_libraries(vajra_api -lboost_log_setup)
target_link_libraries(vajra_api -lboost_log)
target_link_libraries(vajra_api -lboost_thread)
target_link_libraries(vajra_api -lboost_system)
target_link_libraries(vajra_api -lssl)
target_link_libraries(vajra_api -lcrypto)
target_link_libraries(vajra_api -lpthread)
target_link_libraries(vajra_api vajraServerSdk)
target_link_libraries(vajra_api jwtpp-static)

add_executable(vajra_server server/fleet_main.cpp server/WebServer.cpp server/request_handler.cpp server/request_handler.h server/RequestRouter.cpp server/RequestRouter.h server/http_common.cpp server/http_common.h)
target_link_libraries(vajra_server -lboost_log_setup)
target_link_libraries(vajra_server -lboost_log)
target_link_libraries(vajra_server -lboost_thread)
target_link_libraries(vajra_server -lboost_system)
target_link_libraries(vajra_server -lssl)
target_link_libraries(vajra_server -lcrypto)
target_link_libraries(vajra_server -lpthread)
target_link_libraries(vajra_server vajraServerSdk)

add_executable(userctl utilities/userctl.cpp)
target_link_libraries(userctl -lboost_program_options)
target_link_libraries(userctl vajraServerSdk)
target_link_libraries(userctl jwtpp-static)

add_executable(correlation_engine correlation/main.cpp)
target_link_libraries(correlation_engine -lboost_log_setup)
target_link_libraries(correlation_engine -lboost_log)
target_link_libraries(correlation_engine -lboost_thread)
target_link_libraries(correlation_engine -lboost_system)
target_link_libraries(correlation_engine -lpthread)
target_link_libraries(correlation_engine vajraServerSdk)

if (NOT DEFINED WITHOUT_REMEDIATION)
    add_executable(vajra_agent remediation/main.cpp remediation/FilesystemMonitor.cpp remediation/FilesystemMonitor.h
            remediation/RemediationService.cpp remediation/RemediationService.h remediation/ThreatSignatureService.cpp
            remediation/HTTPClient.cpp remediation/HTTPClient.h remediation/PluginLoader.cpp remediation/PluginLoader.h remediation/OsqueryConfig.cpp remediation/OsqueryConfig.h remediation/CommunicationService.cpp)
    target_link_libraries(vajra_agent -lcurl)
    target_link_libraries(vajra_agent SQLiteCpp)
    target_link_libraries(vajra_agent sqlite3)
    target_link_libraries(vajra_agent -lprocps)
    target_link_libraries(vajra_agent -lpthread)
    target_link_libraries(vajra_agent -ldl)
    target_link_libraries(vajra_agent -lssl)
    target_link_libraries(vajra_agent -lcrypto)
    target_link_libraries(vajra_agent vajraServerSdk)

    add_library(vajraAgentHook SHARED remediation/agent_hook/agent_hook.cpp)
    add_library(vajraRules SHARED remediation/blocking_rules/plugin_main.cpp remediation/blocking_rules/blocking_rules.cpp remediation/blocking_rules/blocking_rules.h)
endif()

add_library(eventRules SHARED event_rules/plugin_main.cpp
                               event_rules/detection_rules.cpp 
                               event_rules/detection_rules.h 
                               event_rules/win_detection_rules.cpp 
                               event_rules/win_detection_rules.h 
                               event_rules/gtfobins_rules.cpp 
                               event_rules/gtfobins_rules.h 
                               event_rules/collection_rules.cpp 
                               event_rules/collection_rules.h 
                               event_rules/command_control_rules.cpp 
                               event_rules/command_control_rules.h 
                               event_rules/credential_access_rules.cpp 
                               event_rules/credential_access_rules.h 
                               event_rules/exfiltration_rules.cpp 
                               event_rules/exfiltration_rules.h
                               event_rules/win_impact_rules.cpp
                               event_rules/win_impact_rules.h
                               event_rules/win_execution_rules.cpp
                               event_rules/win_execution_rules.h
                               event_rules/win_exfilteration_rules.cpp
                               event_rules/win_exfilteration_rules.h
                               event_rules/win_defence_evasion_rules.cpp
                               event_rules/win_defence_evasion_rules.h
                               event_rules/win_privilege_escalation_rules.cpp
                               event_rules/win_privilege_escalation_rules.h
                               event_rules/win_collection_rules.cpp
                               event_rules/win_collection_rules.h
                               event_rules/win_discovery_rules.cpp
                               event_rules/win_discovery_rules.h
                               event_rules/win_command_control_rules.cpp
                               event_rules/win_command_control_rules.h  
                               event_rules/win_credential_access_rules.cpp
                               event_rules/win_credential_access_rules.h  
                               event_rules/win_persistence_rules.cpp
                               event_rules/win_persistence_rules.h
                               event_rules/win_initial_access_rules.cpp
                               event_rules/win_initial_access_rules.h 
                               event_rules/win_lateral_movement.cpp 
                               event_rules/win_lateral_movement.h
                               event_rules/win_resource_development_rules.cpp
                               event_rules/win_resource_development_rules.h
                               event_rules/defence_evasion_rules.cpp
                               event_rules/defence_evasion_rules.h
                               event_rules/discovery_rules.cpp
                               event_rules/discovery_rules.h
                               event_rules/execution_rules.cpp
                               event_rules/execution_rules.h
                               event_rules/impact_rules.cpp
                               event_rules/impact_rules.h
                               event_rules/persistence_rules.cpp
                               event_rules/persistence_rules.h
                               event_rules/privilege_escalation_rules.cpp
                               event_rules/privilege_escalation_rules.h
                               )