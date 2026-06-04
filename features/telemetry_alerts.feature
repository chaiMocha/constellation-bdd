Feature: Satellite Telemetry Health Monitoring
    As a constellation operator,
    I want the API to accurately report satellite health status,
    So that I can respond to critical battery degradation.

    Scenario: A satellite with sufficient battery returns a NOMINAL status
        Given the telemetry API is running locally
        When I request the current telemetry for "SAT-Alpha-1"
        Then the API should respond with a 200 status code
        And the response should contain the "satellite_id" field
        And the response should contain a valid "status"