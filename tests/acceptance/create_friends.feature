Feature: Add Friends API
  Scenario: Can successfully create a friend
    Given the Friends API is running
    When I create a friend with name "John Doe" and age 30
    Then the response status code should be 201
    And the response should include the friend's ID

    Scenario: Creating a friend with missing data gives bad request
      Given the Friends API is running
