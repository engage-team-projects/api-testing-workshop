Feature: Get Friends API

  Scenario: Successfully get all friends
    Given the Friends API is running
    When I get all friends
    Then the response status code should be 200
    And the response should be a list of friends