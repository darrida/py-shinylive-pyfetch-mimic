
*** Settings ***
Library  SeleniumLibrary
Library  Process
Library  OperatingSystem
Library  DependencyLibrary

Variables    _test_variables.py

Suite Setup    Start Webserver And Browser
Suite Teardown    Shutdown Webserver And Browser

*** Keywords ***
Start Webserver and Browser
    Log To Console  start
    Log To Console    ${PROJECT_ROOT_DIR}
    ${PROCESS_DEFAULT}    Start Process    python3    ${PROJECT_ROOT_DIR}/src_test_webserver/main.py
    Sleep    2
    Set suite variable    ${PROCESS_DEFAULT}
    Log To Console     ${PROCESS_DEFAULT}
    Open Browser  ${URL}  ${Browser}
    Wait Until Page Contains    Run tests    timeout=10
    Select Frame    xpath=//*[@id="root"]/div[2]/div[5]/iframe
    Wait Until Page Contains    Run tests
    Click Button    Run tests
    Unselect Frame

Shutdown Webserver and Browser
    Close All Browsers
    Terminate All Processes
    Log To Console    end

Stop the webserver
    Terminate All Processes
    Close All Browsers
    # Coverage Stop
    # ${RUN_PROCESS}    Run Process    coverage    html
    # ${RUN_PROCESS}    Run Process    coverage    xml
    Log To Console    end
