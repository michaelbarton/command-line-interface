import time, pexpect

PROCESS_EXIT = pexpect.EOF
LINE_ENDING  = '\r\n'

def type(process, input_):
    process.sendline(input_.encode())
    process.expect(LINE_ENDING)
    return process.before

@when(u'I run the interactive command')
def step_impl(context):
    process = pexpect.spawn(context.text)
    process.sendline("")
    status = process.expect([PROCESS_EXIT, LINE_ENDING])

    # In the case when the PROCESS_EXIT expression has matched, this means
    # the biobox CLI did not start
    if status == 0:
        assert False, "Behave CLI failed to start:\n{}".format(str(process))

    class Output(object):
        pass

    context.output = Output()
    context.output.stderr = ""
    context.output.stdout = ""
    context.process = process

@when(u'I type')
def step_impl(context):
    cmd = context.text.strip()
    context.output.stdout = type(context.process, cmd)

@when(u'I exit the shell')
def step_impl(context):
    context.process.sendline("exit")
