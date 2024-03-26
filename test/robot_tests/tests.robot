*** Settings ***
Library  SeleniumLibrary
Library  Process
Library  OperatingSystem
Library  DependencyLibrary

Variables    ../_test_variables.py

*** Test Cases ***
Test Shinylive - /get-string
    Wait Until Page Contains    test_wrapper_get_string... ...passed

Test Shinylive - /get-json
    Wait Until Page Contains    test_wrapper_get_json... ...passed

Test Shinylive - /get-not-found-parameter - FOUND
    Wait Until Page Contains    test_wrapper_get_parameter_found... ...passed

Test Shinylive - /get-not-found-parameter - NOT FOUND
    Wait Until Page Contains    test_wrapper_get_parameter_not_found... ...passed

Test Shinylive - /post-payload
    Wait Until Page Contains    test_wrapper_post_payload... ...passed

Test Shinylive - /get-text-download
    Wait Until Page Contains    test_wrapper_get_file_download... ...passed

Test Shinylive - /get-image-download
    Wait Until Page Contains    test_wrapper_get_image_download... ...passed

Test Shinylive - /get-streaming
    Wait Until Page Contains    test_wrapper_streaming_fake... ...passed
