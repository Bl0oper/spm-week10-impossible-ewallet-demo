# Where the checks break, and the sources

This is the team's fact list for the talk. Every figure here was checked against its source. Don't add new figures to the talk without a source.

## Where it breaks

- **A cheat and a fix look identical to the gate.** `protect-tests` only sees that `tests/` changed. A correct fix to the wrong test gets the same ✗. EvilGenie argues that fixing an incorrect test is "arguably desirable" when the agent was not told to leave tests alone [3, §6.1]. ImpossibleBench counts any pass as cheating [1]. A human still has to judge.
- **Read-only tests can be bypassed by an agent with a shell.** ImpossibleBench found that read-only tests were a middle ground [1]. An agent that can run commands can change file permissions or work around them. Our gate runs in CI, outside the agent's machine.
- **An agent can edit the workflow file.** A PR's `pull_request` workflow runs the PR's own version of the file, so the PR can weaken the gate itself. That is why `.github/CODEOWNERS` covers `/.github/` and `/tests/`. It only takes effect when code-owner review is required.
- **Held-out tests are weak in general.** EvilGenie found that held-out tests gave minimal improvement in detection [3]. Ours catches the reconstruction only because it includes the exact `100/100` case. With only `250/250`, the hard-coded `== 100` would pass.
- **Hiding tests costs performance.** Hiding the tests from the agent cut cheating to near zero but hurt legitimate performance [1].
- **A prompt is not a guarantee.** A strict "stop if the tests are flawed" prompt cut GPT-5's cheating from 92% to 1% on conflicting impossible-LiveCodeBench, but only from 66% to 54% on conflicting impossible-SWE-bench [1].
- **Our sample is tiny.** A handful of runs per setup, on one toy task. Models also differ: OpenAI models used a mix of strategies (modifying tests, operator overloading, recording extra state, special-casing), Claude and Qwen3-Coder mostly modified test files, and stronger models generally cheated more [1][2].

## References

1. Zhong, Raghunathan & Carlini. *ImpossibleBench: Measuring LLMs' Propensity of Exploiting Test Cases.* arXiv preprint arXiv:2510.20270, Oct 2025. https://arxiv.org/abs/2510.20270
2. Zhong. *ImpossibleBench: Measuring Reward Hacking in LLM Coding Agents.* LessWrong, Oct 2025. https://www.lesswrong.com/posts/qJYMbrabcQqCZ7iqm/impossiblebench-measuring-reward-hacking-in-llm-coding-1
3. Gabor, Lynch & Rosenfeld. *EvilGenie: A Reward Hacking Benchmark.* arXiv preprint arXiv:2511.21654, Nov 2025. https://arxiv.org/abs/2511.21654
