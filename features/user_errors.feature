Feature: Providing useful errors to a user when they run the tool incorrectly

  Scenario Outline: Trying to run an unknown command
    When I run the command:
      """
      biobox <cmd> short_read_assembler bioboxes/velvet --help
      """
    Then the stdout should be empty
    And the exit code should be 1
    And the stderr should equal:
      """
      Unknown command: "<cmd>".
      Run `biobox --help` for a list of available.

      """

    Examples:
      | cmd     |
      | dummy   |
      | unknown |


  Scenario Outline: Trying to use an unknown biobox type
    When I run the command:
      """
      biobox <command> unknown bioboxes/velvet
      """
    Then the stdout should be empty
    And the exit code should be 1
    And the stderr should equal:
      """
      Unknown biobox type: "unknown".
      Run `biobox --help` for a list of available.

      """

    Examples:
      | command |
      | login   |
      | run     |
      | verify  |

  @internet
  Scenario Outline: Trying to use an unknown biobox image
    Given I create the directory "output"
    When I run the command:
      """
      biobox <command> <type> bioboxes/unknown <args>
      """
    Then the stdout should be empty
    And the stderr should equal:
      """
      No Docker image available with the name: bioboxes/unknown
      Did you include the namespace too? E.g. bioboxes/velvet.

      """
    And the exit code should be 1

    Examples:
      | command | type                 | args                                              |
      | run     | short_read_assembler | --input=reads.fq.gz --output=$(realpath .)/output |
      | login   | short_read_assembler |                                                   |
      | verify  | short_read_assembler |                                                   |

  Scenario: Trying to mount a non-empty output directory
    Given I create the directory "output"
    And I copy the example data files:
      | source         | dest                  |
      | assembly.fasta | output/assembly.fasta |
    When I run the command:
      """
      biobox run short_read_assembler bioboxes/velvet --input=reads.fq.gz --output=output
      """
    Then the stdout should be empty
    And the exit code should be 1
    And the stderr should equal:
      """
      Specified output directory "output" is not empty.

      """
