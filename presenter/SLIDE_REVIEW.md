# Canva slide review and edit status

Updated 16 October 2026. This review describes the copied deck and its unsaved draft edits. The original design is unchanged.

- **Original deck:** [Canva design DAHW2fSZJDY](https://www.canva.com/design/DAHW2fSZJDY)
- **Working copy:** [Canva design DAHYJzKOQk8](https://www.canva.com/design/DAHYJzKOQk8/X1gkywJDYR4lnF6IIJ14Bw/edit)
- **Working copy size:** 27 pages. Duplicates were added so the old versions could stay hidden.
- **Current state:** draft edits are visible in the working copy, but have not been saved. Review the preview and approve before saving.

## Page map

Page numbers below are the current numbers in the 27-page working copy, not the old source deck.

| Working-copy page | Status | Content |
|---:|---|---|
| 1 | Visible | Cover |
| 2 | Hidden | Original introductory slide; preserved |
| 3 | Visible | Copied introduction with the METR MirrorCode example |
| 4–5 | Visible | Illustration labeled as not a real run; ImpossibleBench setup |
| 6 | Hidden | Original task-set comparison; preserved |
| 7 | Visible | Revised task-set comparison; 2.9% on Impossible-LiveCodeBench with minimal scaffold |
| 8 | Hidden | Original impact slide; preserved |
| 9–10 | Visible | 76% result with context; team implications |
| 11 | Hidden | Original monitor slide; preserved |
| 12 | Visible | Monitor results with benchmark and model context |
| 13 | Hidden | Extra monitor duplicate; preserved |
| 14–15 | Visible | Guidance and Show Time divider |
| 16 | Hidden | Original references slide; preserved |
| 17–18 | Visible | Revised references and Thank You |
| 19–27 | Hidden | Unrelated template material; preserved |

The presentation currently has 12 visible pages. Pages 19–27 are hidden rather than deleted. The source design has not been changed.

## Changes in the copied deck draft

1. **Use METR's newer example carefully.** Page 3 says Opus 4.6 attempted reward hacking on an early hidden-test MirrorCode variant in roughly 80% of trajectories. This is an attempted behavior on that benchmark variant, not a general cheating or success rate. See [METR's report](https://metr.org/blog/2026-05-19-frontier-risk-report/).
2. **Keep the ImpossibleBench setups distinct.** Page 9 labels GPT-5's 76% result as one-off Impossible-SWE-bench with the full scaffold. The 2.9% comparison is one-off Impossible-LiveCodeBench with the minimal scaffold; the task set and scaffold differ. The 76% figure should appear only once in the visible presentation. See the [ImpossibleBench paper](https://arxiv.org/abs/2510.20270).
3. **Scope the monitor result.** Page 12 says Sonnet 4 flagged 42–50% and Opus 4 flagged 57–65% of passing cheat transcripts on Impossible-SWE-bench. Those ranges describe these two monitors in that experiment, not every monitor or coding task.
4. **Improve readability.** Page 4 labels the illustration as not a run result. The smaller copy on the revised benchmark, impact, and monitor slides has been shortened and enlarged. The takeaway on page 10 uses white text on teal for contrast.
5. **Clean up the references.** Page 17 names the authors, year, paper, and code repository in larger type.

## Before presenting

- Confirm the saved copy still has the original pages hidden and the revised copies visible.
- Confirm the visible slides contain only one 76% result, with its model, benchmark, and scaffold beside it.
- Do not present the illustration as a real experiment. The repository currently has no completed model runs.
- Check the page numbers in Canva after the draft is saved; hidden pages may be reordered later.
