Feature: Allow a user to ssh into an image to test internally

  Scenario Outline: Logging into an image and listing file locations
    When I run the interactive command:
      """
      biobox login <type> <image>
      """
    And I type:
      """
      find /bbx
      """
    And I exit the shell
    Then the stdout should contain:
      """
      /bbx/output
      """
    And the stdout should contain:
      """
      /bbx/input/biobox.yaml
      """
    And the stdout should contain:
      """
      /bbx/input/<file>
      """

    Examples:
      | type                 | image           | file           |
      | short_read_assembler | bioboxes/velvet | reads.fq.gz    |
      | assembler_benchmark  | bioboxes/quast  | assembly.fasta |
