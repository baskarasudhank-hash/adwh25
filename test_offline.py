"""
test_offline.py - Quick self-test of the local features.
No microphone and no API key needed.
Run:  python test_offline.py
"""

import commands


def check(question, expect_word=None, expect_handled=True):
    handled, reply, action = commands.try_command(question)
    ok = handled == expect_handled
    if ok and expect_word:
        ok = expect_word in reply.lower()
    mark = "PASS" if ok else "FAIL"
    print("[" + mark + "]  You say : " + question)
    print("        Reply   : " + (reply if reply else "(goes to Z.ai)"))
    print()
    return ok


def main():
    print("Running offline tests of Nova's local commands...\n")
    results = []

    results.append(check("hello", "how can i help"))
    results.append(check("what is the time", "the time is"))
    results.append(check("what is the date today", "today is"))
    results.append(check("who are you", "i am nova"))
    results.append(check("tell me a joke", None))
    results.append(check("thank you", "welcome"))
    results.append(check("open youtube", "opening youtube"))
    results.append(check("search for python tutorials", "searching google"))
    results.append(check("explain black holes", None, expect_handled=False))

    passed = sum(results)
    total = len(results)
    print("-" * 50)
    print("Result: " + str(passed) + " / " + str(total) + " tests passed")
    if passed == total:
        print("All local commands work correctly!")


if __name__ == "__main__":
    main()
